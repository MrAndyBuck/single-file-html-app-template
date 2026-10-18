#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9300

proc = subprocess.Popen([
    CHROME_BIN,
    "--headless=new",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--window-size=1440,900",
    f"--remote-debugging-port={PORT}",
    "file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1"
])
time.sleep(2.0)

tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json").read().decode("utf-8"))
target = next(t for t in tabs if t.get("type") == "page")
ws_url = target["webSocketDebuggerUrl"]
host, port, path = "127.0.0.1", PORT, ws_url.split(f"127.0.0.1:{PORT}")[1]

s = socket.socket()
s.connect((host, port))
key = base64.b64encode(b"0123456789abcdef").decode()
req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
s.sendall(req.encode())
s.recv(4096)

cid = 1
def eval_js(js):
    global cid
    cid += 1
    msg = {"id": cid, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
    data = json.dumps(msg).encode("utf-8")
    frame = bytearray([0x81])
    length = len(data)
    mask = b"\x11\x22\x33\x44"
    if length < 126: frame.append(0x80 | length)
    elif length < 65536:
        frame.append(0x80 | 126)
        frame.extend(struct.pack(">H", length))
    frame.extend(mask)
    frame.extend(bytearray(b ^ mask[i % 4] for i, b in enumerate(data)))
    s.sendall(frame)
    while True:
        h = s.recv(2)
        l = h[1] & 0x7f
        if l == 126: l = struct.unpack(">H", s.recv(2))[0]
        elif l == 127: l = struct.unpack(">Q", s.recv(8))[0]
        p = b""
        while len(p) < l: p += s.recv(l - len(p))
        m = json.loads(p.decode("utf-8", errors="ignore"))
        if m.get("id") == cid:
            return m.get("result", {}).get("result", {}).get("value")

js_code = """
(() => {
  const geo = new THREE.BoxGeometry(20, 20, 20);
  const mat = new THREE.MeshStandardMaterial({ color: 0xcccccc });
  const box = new THREE.Mesh(geo, mat);

  function analyzeMesh(geometry) {
    geometry.computeBoundingBox();
    const bbox = geometry.boundingBox;
    const pos = geometry.attributes.position;
    const eps = 1e-4;

    const uniqueVerts = [];
    const vmap = [];
    for (let i = 0; i < pos.count; i++) {
      const vx = pos.getX(i), vy = pos.getY(i), vz = pos.getZ(i);
      let found = -1;
      for (let j = 0; j < uniqueVerts.length; j++) {
        const u = uniqueVerts[j];
        if (Math.abs(u.x - vx) < eps && Math.abs(u.y - vy) < eps && Math.abs(u.z - vz) < eps) {
          found = j; break;
        }
      }
      if (found === -1) {
        found = uniqueVerts.length;
        uniqueVerts.push({ x: vx, y: vy, z: vz });
      }
      vmap.push(found);
    }

    const edgeMap = new Map();
    for (let i = 0; i < pos.count; i += 3) {
      const v0 = vmap[i], v1 = vmap[i+1], v2 = vmap[i+2];
      const e1 = v0 < v1 ? `${v0}_${v1}` : `${v1}_${v0}`;
      const e2 = v1 < v2 ? `${v1}_${v2}` : `${v2}_${v1}`;
      const e3 = v2 < v0 ? `${v2}_${v0}` : `${v0}_${v2}`;
      edgeMap.set(e1, (edgeMap.get(e1) || 0) + 1);
      edgeMap.set(e2, (edgeMap.get(e2) || 0) + 1);
      edgeMap.set(e3, (edgeMap.get(e3) || 0) + 1);
    }

    let manifoldEdges = 0, openEdges = 0, nonManifoldEdges = 0;
    for (const [k, count] of edgeMap.entries()) {
      if (count === 2) manifoldEdges++;
      else if (count === 1) openEdges++;
      else nonManifoldEdges++;
    }

    const V = uniqueVerts.length;
    const E = edgeMap.size;
    const F = pos.count / 3;
    const chi = V - E + F;

    return {
      triangles: F,
      uniqueVertices: V,
      totalEdges: E,
      manifoldEdges,
      openEdges,
      nonManifoldEdges,
      eulerCharacteristic: chi,
      isWatertight: openEdges === 0,
      isManifold: openEdges === 0 && nonManifoldEdges === 0,
      bbox: {
        min: { x: bbox.min.x, y: bbox.min.y, z: bbox.min.z },
        max: { x: bbox.max.x, y: bbox.max.y, z: bbox.max.z }
      }
    };
  }

  const chamfer1 = analyzeMesh(computeEdgeCutGeometry(box, "chamfer", 2.0, [0]));
  const fillet1 = analyzeMesh(computeEdgeCutGeometry(box, "fillet", 2.0, [0]));

  return { chamfer: chamfer1, fillet: fillet1 };
})()
"""

res = eval_js(js_code)
print("Updated In-Browser Analysis Result:")
print(json.dumps(res, indent=2))
proc.kill()
