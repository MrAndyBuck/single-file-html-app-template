#!/usr/bin/env python3
import math
from test_manifold_edge_cut import build_box_edge_cut, analyze_topology

def compute_mesh_volume(verts, tris):
    vol = 0.0
    for (i0, i1, i2) in tris:
        v0 = verts[i0]
        v1 = verts[i1]
        v2 = verts[i2]
        # v0 . (v1 x v2)
        cross_x = v1[1] * v2[2] - v1[2] * v2[1]
        cross_y = v1[2] * v2[0] - v1[0] * v2[2]
        cross_z = v1[0] * v2[1] - v1[1] * v2[0]
        vol += (v0[0] * cross_x + v0[1] * cross_y + v0[2] * cross_z)
    return vol / 6.0

print("--- TESTING VOLUME AND OUTWARD NORMAL CONSISTENCY ---")
v_box = 20 * 20 * 20 # 8000

for edge_id in range(12):
    v_c, t_c = build_box_edge_cut(20, 20, 20, "chamfer", 2.0, edge_id)
    vol_c = compute_mesh_volume(v_c, t_c)
    expected_c = 8000.0 - (0.5 * 2.0 * 2.0 * 20.0) # 7960.0
    
    v_f, t_f = build_box_edge_cut(20, 20, 20, "fillet", 2.0, edge_id, segs=32)
    vol_f = compute_mesh_volume(v_f, t_f)
    expected_f = 8000.0 - ((4.0 - math.pi) * 20.0) # 7982.831853...
    
    print(f"Edge {edge_id:02d}: Chamfer Vol={vol_c:.3f} (exp: {expected_c:.3f}, diff={vol_c - expected_c:.4f}) | Fillet Vol={vol_f:.3f} (exp: {expected_f:.3f}, diff={vol_f - expected_f:.4f})")
