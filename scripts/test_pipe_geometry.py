#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64

PORT = 9299
proc = subprocess.Popen([
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless=new',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    f'--remote-debugging-port={PORT}',
    'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html'
])
time.sleep(2.0)
try:
    tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json').read().decode())
    target = next(t for t in tabs if t.get('type') == 'page')
    ws_url = target['webSocketDebuggerUrl']
    host, port, path = '127.0.0.1', PORT, ws_url.split(f'127.0.0.1:{PORT}')[1]
    s = socket.socket(); s.connect((host, port))
    key = base64.b64encode(b'0123456789abcdef').decode()
    req = f'GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
    s.sendall(req.encode()); s.recv(4096)

    cmd_counter = 1
    def send_cmd(method, params=None):
        global cmd_counter
        cid = cmd_counter
        cmd_counter += 1
        msg = json.dumps({'id': cid, 'method': method, 'params': params or {}}).encode('utf-8')
        frame = bytearray([0x81])
        length = len(msg)
        mask = b'\x11\x22\x33\x44'
        if length < 126: frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack('>H', length))
        frame.extend(mask)
        frame.extend(bytearray(b ^ mask[i % 4] for i, b in enumerate(msg)))
        s.sendall(frame)
        while True:
            h = s.recv(2)
            if not h: break
            l = h[1] & 0x7F
            if l == 126: l = struct.unpack('>H', s.recv(2))[0]
            elif l == 127: l = struct.unpack('>Q', s.recv(8))[0]
            raw = bytearray()
            while len(raw) < l: raw.extend(s.recv(l - len(raw)))
            res = json.loads(raw.decode('utf-8'))
            if res.get('id') == cid: return res

    res = send_cmd('Runtime.evaluate', {
        'expression': '''(() => {
            function verifyMeshManifold(geo) {
              const nonIndexed = geo.index ? geo.toNonIndexed() : geo;
              const pos = nonIndexed.attributes.position;
              const eps = 1e-4;
              const uVerts = [];
              const vmap = [];
              for (let i = 0; i < pos.count; i++) {
                const vx = pos.getX(i), vy = pos.getY(i), vz = pos.getZ(i);
                let f = -1;
                for (let j = 0; j < uVerts.length; j++) {
                  if (Math.abs(uVerts[j].x - vx) < eps && Math.abs(uVerts[j].y - vy) < eps && Math.abs(uVerts[j].z - vz) < eps) {
                    f = j; break;
                  }
                }
                if (f === -1) {
                  f = uVerts.length;
                  uVerts.push({ x: vx, y: vy, z: vz });
                }
                vmap.push(f);
              }
              const edgeMap = new Map();
              for (let i = 0; i < pos.count; i += 3) {
                const v0 = vmap[i], v1 = vmap[i+1], v2 = vmap[i+2];
                const e1 = v0 < v1 ? (v0 + "_" + v1) : (v1 + "_" + v0);
                const e2 = v1 < v2 ? (v1 + "_" + v2) : (v2 + "_" + v1);
                const e3 = v2 < v0 ? (v2 + "_" + v0) : (v0 + "_" + v2);
                edgeMap.set(e1, (edgeMap.get(e1) || 0) + 1);
                edgeMap.set(e2, (edgeMap.get(e2) || 0) + 1);
                edgeMap.set(e3, (edgeMap.get(e3) || 0) + 1);
              }
              let open = 0, nonM = 0;
              for (const [k, count] of edgeMap.entries()) {
                if (count === 1) open++;
                else if (count > 2) nonM++;
              }
              const chi = uVerts.length - edgeMap.size + (pos.count / 3);
              return { isWatertight: open === 0, isManifold: open === 0 && nonM === 0, open, nonM, chi, uVerts: uVerts.length, faces: pos.count / 3 };
            }

            function buildCappedPipeGeometry(points, radius, tubSeg = 16, radSeg = 12) {
                let curve;
                if (points.length === 2) {
                    curve = new THREE.LineCurve3(points[0], points[1]);
                } else {
                    const cp = new THREE.CurvePath();
                    for (let i = 0; i < points.length - 1; i++) {
                        cp.add(new THREE.LineCurve3(points[i], points[i+1]));
                    }
                    curve = cp;
                }
                const tube = new THREE.TubeGeometry(curve, tubSeg, radius, radSeg, false);
                const posAttr = tube.attributes.position;
                const normAttr = tube.attributes.normal;
                const uvAttr = tube.attributes.uv;
                const origIndices = Array.from(tube.index.array);

                const positions = Array.from(posAttr.array);
                const normals = Array.from(normAttr.array);
                const uvs = Array.from(uvAttr.array);
                const indices = [...origIndices];

                const pStart = curve.getPoint(0);
                const pEnd = curve.getPoint(1);
                const tanStart = curve.getTangent(0).normalize().negate();
                const tanEnd = curve.getTangent(1).normalize();

                // Start cap center
                const startCenterIdx = positions.length / 3;
                positions.push(pStart.x, pStart.y, pStart.z);
                normals.push(tanStart.x, tanStart.y, tanStart.z);
                uvs.push(0.5, 0.5);

                for (let j = 0; j < radSeg; j++) {
                    const v0 = j;
                    const v1 = j + 1;
                    indices.push(startCenterIdx, v1, v0);
                }

                // End cap center
                const endCenterIdx = positions.length / 3;
                positions.push(pEnd.x, pEnd.y, pEnd.z);
                normals.push(tanEnd.x, tanEnd.y, tanEnd.z);
                uvs.push(0.5, 0.5);

                const lastRingOffset = tubSeg * (radSeg + 1);
                for (let j = 0; j < radSeg; j++) {
                    const v0 = lastRingOffset + j;
                    const v1 = lastRingOffset + j + 1;
                    indices.push(endCenterIdx, v0, v1);
                }

                const geo = new THREE.BufferGeometry();
                geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
                geo.setAttribute('normal', new THREE.Float32BufferAttribute(normals, 3));
                geo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
                geo.setIndex(indices);
                geo.computeVertexNormals();
                geo.computeBoundingBox();
                geo.computeBoundingSphere();
                return geo;
            }

            const pStraight = [new THREE.Vector3(0, 0, 0), new THREE.Vector3(30, 0, 0)];
            const geoStraight = buildCappedPipeGeometry(pStraight, 3.0, 16, 12);
            const topoStraight = verifyMeshManifold(geoStraight);

            const pL = [new THREE.Vector3(0, 0, 0), new THREE.Vector3(25, 0, 0), new THREE.Vector3(25, 0, 20)];
            const geoL = buildCappedPipeGeometry(pL, 2.5, 32, 12);
            const topoL = verifyMeshManifold(geoL);

            return { straight: topoStraight, L: topoL };
        })()''',
        'returnByValue': True
    })
    print('RAW RES:', json.dumps(res, indent=2))
finally:
    proc.terminate()
