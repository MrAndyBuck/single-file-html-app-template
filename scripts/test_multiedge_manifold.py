#!/usr/bin/env python3
import math

def build_box_manifold_cut(width, height, depth, mode, param, edge_ids, segs=16):
    """
    Constructs an exact 2-manifold triangle mesh for a box centered at (0,0,0)
    with edge_ids filleted or chamfered by param.
    Supports single edge (any 0..11) or multiple edges in the same orientation.
    """
    w2 = width / 2.0
    h2 = height / 2.0
    d2 = depth / 2.0

    configs = {
        0: (1, -h2, h2, 0, -w2, w2, 2, -d2, d2, +1, +1),
        1: (1, -h2, h2, 0, -w2, w2, 2, -d2, d2, -1, +1),
        2: (1, -h2, h2, 0, -w2, w2, 2, -d2, d2, -1, -1),
        3: (1, -h2, h2, 0, -w2, w2, 2, -d2, d2, +1, -1),

        4: (0, -w2, w2, 1, -h2, h2, 2, -d2, d2, +1, +1),
        5: (0, -w2, w2, 1, -h2, h2, 2, -d2, d2, +1, -1),
        6: (0, -w2, w2, 1, -h2, h2, 2, -d2, d2, -1, +1),
        7: (0, -w2, w2, 1, -h2, h2, 2, -d2, d2, -1, -1),

        8: (2, -d2, d2, 0, -w2, w2, 1, -h2, h2, +1, +1),
        9: (2, -d2, d2, 0, -w2, w2, 1, -h2, h2, -1, +1),
        10: (2, -d2, d2, 0, -w2, w2, 1, -h2, h2, -1, -1),
        11: (2, -d2, d2, 0, -w2, w2, 1, -h2, h2, +1, -1),
    }

    if not edge_ids:
        edge_ids = [0]

    first_cfg = configs[edge_ids[0]]
    sweep_axis, s_min, s_max, u_axis, u_min, u_max, v_axis, v_min, v_max = first_cfg[:9]

    # Check if all edges share the same sweep_axis
    for eid in edge_ids:
        if configs[eid][0] != sweep_axis:
            return None # Mixed orientations fallback to CSG

    active_corners = set()
    for eid in edge_ids:
        su, sv = configs[eid][9], configs[eid][10]
        active_corners.add((su, sv))

    is_right_handed = ((u_axis + 1) % 3 == v_axis)

    corners = [
        (-1, -1, u_min, v_min),
        (+1, -1, u_max, v_min),
        (+1, +1, u_max, v_max),
        (-1, +1, u_min, v_max)
    ]

    poly = []
    for (cu, cv, u_val, v_val) in corners:
        if (cu, cv) in active_corners:
            if cu == +1 and cv == +1:
                p_in = (u_max, v_max - param)
                p_out = (u_max - param, v_max)
                center = (u_max - param, v_max - param)
                theta_start, theta_end = 0.0, math.pi / 2.0
            elif cu == -1 and cv == +1:
                p_in = (u_min + param, v_max)
                p_out = (u_min, v_max - param)
                center = (u_min + param, v_max - param)
                theta_start, theta_end = math.pi / 2.0, math.pi
            elif cu == -1 and cv == -1:
                p_in = (u_min, v_min + param)
                p_out = (u_min + param, v_min)
                center = (u_min + param, v_min + param)
                theta_start, theta_end = math.pi, 3.0 * math.pi / 2.0
            elif cu == +1 and cv == -1:
                p_in = (u_max - param, v_min)
                p_out = (u_max, v_min + param)
                center = (u_max - param, v_min + param)
                theta_start, theta_end = 3.0 * math.pi / 2.0, 2.0 * math.pi

            if mode == "chamfer":
                poly.append(p_in)
                poly.append(p_out)
            else: # fillet
                for i in range(segs + 1):
                    t = theta_start + (theta_end - theta_start) * (i / segs)
                    u = center[0] + param * math.cos(t)
                    v = center[1] + param * math.sin(t)
                    poly.append((u, v))
        else:
            poly.append((u_val, v_val))

    N = len(poly)
    if not is_right_handed:
        poly.reverse()

    def make_vec3(u, v, s):
        xyz = [0.0, 0.0, 0.0]
        xyz[u_axis] = u
        xyz[v_axis] = v
        xyz[sweep_axis] = s
        return tuple(xyz)

    verts = []
    # Bottom cap (s_min)
    for (u, v) in poly:
        verts.append(make_vec3(u, v, s_min))
    # Top cap (s_max)
    for (u, v) in poly:
        verts.append(make_vec3(u, v, s_max))

    tris = []
    # Bottom cap (CW)
    for i in range(1, N - 1):
        tris.append((0, i + 1, i))
    # Top cap (CCW)
    for i in range(1, N - 1):
        tris.append((N, N + i, N + i + 1))
    # Sides
    for i in range(N):
        next_i = (i + 1) % N
        b1, b2 = i, next_i
        t1, t2 = N + i, N + next_i
        tris.append((b1, b2, t2))
        tris.append((b1, t2, t1))

    return verts, tris

def analyze_topology(verts, tris):
    edge_count = {}
    for (i0, i1, i2) in tris:
        edges = [
            tuple(sorted([i0, i1])),
            tuple(sorted([i1, i2])),
            tuple(sorted([i2, i0]))
        ]
        for e in edges:
            edge_count[e] = edge_count.get(e, 0) + 1

    open_edges = [e for e, c in edge_count.items() if c == 1]
    non_manifold_edges = [e for e, c in edge_count.items() if c > 2]
    manifold_edges = [e for e, c in edge_count.items() if c == 2]

    V = len(verts)
    E = len(edge_count)
    F = len(tris)
    chi = V - E + F

    return {
        "V": V, "E": E, "F": F,
        "Chi": chi,
        "openEdges": len(open_edges),
        "nonManifoldEdges": len(non_manifold_edges),
        "isWatertight": len(open_edges) == 0,
        "isManifold": len(open_edges) == 0 and len(non_manifold_edges) == 0
    }

print("Testing multi-edge fillet and chamfer:")
# 2 vertical edges [0, 1]
v2_c, t2_c = build_box_manifold_cut(20, 20, 20, "chamfer", 2.0, [0, 1])
print("Chamfer [0, 1]:", analyze_topology(v2_c, t2_c))

v2_f, t2_f = build_box_manifold_cut(20, 20, 20, "fillet", 2.0, [0, 1], segs=16)
print("Fillet [0, 1]:", analyze_topology(v2_f, t2_f))

# 4 vertical edges [0, 1, 2, 3]
v4_c, t4_c = build_box_manifold_cut(20, 20, 20, "chamfer", 2.0, [0, 1, 2, 3])
print("Chamfer [0, 1, 2, 3]:", analyze_topology(v4_c, t4_c))

v4_f, t4_f = build_box_manifold_cut(20, 20, 20, "fillet", 2.0, [0, 1, 2, 3], segs=16)
print("Fillet [0, 1, 2, 3]:", analyze_topology(v4_f, t4_f))
