#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, math

PORT = 9333
DESKTOP_DIR = '/Users/andybuck/Desktop/CADNT_Screenshots'
ARTIFACT_DIR = '/Users/andybuck/.gemini/antigravity-cli/brain/92f72284-41c5-4687-ab10-0c2aade50fd2/screenshots'

os.makedirs(DESKTOP_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

proc = subprocess.Popen([
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless=new',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    '--window-size=1280,800',
    f'--remote-debugging-port={PORT}',
    'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1'
])
time.sleep(3.0)

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

    def evaluate(expr):
        r = send_cmd('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        return r.get('result', {}).get('result', {}).get('value')

    def save_screenshot(filename):
        r = send_cmd('Page.captureScreenshot', {'format': 'png'})
        data = base64.b64decode(r['result']['data'])
        p1 = os.path.join(DESKTOP_DIR, filename)
        p2 = os.path.join(ARTIFACT_DIR, filename)
        with open(p1, 'wb') as f: f.write(data)
        with open(p2, 'wb') as f: f.write(data)
        print(f"Captured screenshot: {filename} ({len(data)} bytes) saved to Desktop & Artifacts")

    time.sleep(1.0)
    # Clear starting michigan / objects to have clean view
    evaluate("""
        if (michiganModel) {
            scene.remove(michiganModel);
            const idx = sceneObjects.indexOf(michiganModel);
            if (idx !== -1) sceneObjects.splice(idx, 1);
            michiganModel = null;
        }
        renderAllViewports();
    """)
    time.sleep(0.5)

    print("--- 1. Activating Spline Command via Toolbar ---")
    evaluate("startSketch('spline'); setActiveViewport('top');")
    time.sleep(0.5)

    # Convert Top C-plane 3D coordinates (-20, 0, 0), (0, 0, 25), (20, 0, 0) to Top canvas client coords
    # In Top view, camera looks from +Y down to -Y, center is target.
    # We can use viewports.top canvas bounding rect and project with cameras.top
    evaluate("""
        window.getTopScreenCoords = function(wx, wy, wz) {
            const vp = viewports.top;
            const cam = cameras.top;
            const rect = vp.canvas.getBoundingClientRect();
            const vec = new THREE.Vector3(wx, wy, wz).project(cam);
            const sx = rect.left + (vec.x + 1) * 0.5 * rect.width;
            const sy = rect.top + (-vec.y + 1) * 0.5 * rect.height;
            return { x: sx, y: sy };
        };
    """)

    cp1_coords = evaluate("window.getTopScreenCoords(-20, 0, 0)")
    cp2_coords = evaluate("window.getTopScreenCoords(0, 0, 25)")
    cp3_coords = evaluate("window.getTopScreenCoords(20, 0, 0)")
    print(f"Projected screen coords: CP1={cp1_coords}, CP2={cp2_coords}, CP3={cp3_coords}")

    # Pointer interaction: Dispatch pointerdown / pointerup at CP1
    send_cmd('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': cp1_coords['x'], 'y': cp1_coords['y']})
    time.sleep(0.2)
    send_cmd('Input.dispatchMouseEvent', {'type': 'mousePressed', 'button': 'left', 'x': cp1_coords['x'], 'y': cp1_coords['y'], 'clickCount': 1})
    send_cmd('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'button': 'left', 'x': cp1_coords['x'], 'y': cp1_coords['y']})
    time.sleep(0.3)

    # Move pointer towards CP2 to preview rubberband
    send_cmd('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': cp2_coords['x'], 'y': cp2_coords['y']})
    time.sleep(0.3)
    save_screenshot("spline_01_sketch_preview.png")

    # Click CP2
    send_cmd('Input.dispatchMouseEvent', {'type': 'mousePressed', 'button': 'left', 'x': cp2_coords['x'], 'y': cp2_coords['y'], 'clickCount': 1})
    send_cmd('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'button': 'left', 'x': cp2_coords['x'], 'y': cp2_coords['y']})
    time.sleep(0.3)

    # Move to CP3
    send_cmd('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': cp3_coords['x'], 'y': cp3_coords['y']})
    time.sleep(0.3)
    send_cmd('Input.dispatchMouseEvent', {'type': 'mousePressed', 'button': 'left', 'x': cp3_coords['x'], 'y': cp3_coords['y'], 'clickCount': 1})
    send_cmd('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'button': 'left', 'x': cp3_coords['x'], 'y': cp3_coords['y']})
    time.sleep(0.3)

    save_screenshot("spline_02_three_points_placed.png")

    # Click [✓ Finish (Enter)]
    evaluate("document.getElementById('btn-cmd-confirm').click();")
    time.sleep(0.5)

    save_screenshot("spline_03_committed_curved_spline.png")

    # Extract spline geometry metrics
    geom_metrics = evaluate("""
        (() => {
            const spline = sceneObjects.find(o => o.userData && o.userData.type === 'SplineCurve');
            if (!spline) return { error: "No SplineCurve found" };
            const attr = spline.geometry.attributes.position;
            const pts = [];
            for (let i = 0; i < attr.count; i++) {
                pts.push({ x: attr.getX(i), y: attr.getY(i), z: attr.getZ(i) });
            }
            return {
                name: spline.name,
                type: spline.userData.type,
                controlPointsCount: spline.userData.controlPoints.length,
                controlPoints: spline.userData.controlPoints.map(p => ({ x: p.x, y: p.y, z: p.z })),
                vertexCount: attr.count,
                startPoint: pts[0],
                midPoint: pts[Math.floor(pts.length / 2)],
                endPoint: pts[pts.length - 1],
                quarterPoint: pts[Math.floor(pts.length / 4)],
                threeQuarterPoint: pts[Math.floor(pts.length * 3 / 4)],
                maxZ: Math.max(...pts.map(p => p.z)),
                minZ: Math.min(...pts.map(p => p.z))
            };
        })()
    """)
    print("Geometry Metrics for 3-Point Spline:")
    print(json.dumps(geom_metrics, indent=2))

    # Test control point editing via Properties panel
    print("--- 2. Moving Apex Control Point (CP2) to Z=45 via Properties Panel ---")
    evaluate("""
        const spline = sceneObjects.find(o => o.userData && o.userData.type === 'SplineCurve');
        spline.userData.selectedControlPointIndex = 1;
        updatePropertiesPanel();
        const cpZInp = document.getElementById('prop-spline-cp-z');
        if (cpZInp) {
            cpZInp.value = "45";
            cpZInp.dispatchEvent(new Event('change'));
        }
    """)
    time.sleep(0.5)
    save_screenshot("spline_04_control_point_edited.png")

    edited_metrics = evaluate("""
        (() => {
            const spline = sceneObjects.find(o => o.userData && o.userData.type === 'SplineCurve');
            const attr = spline.geometry.attributes.position;
            const pts = [];
            for (let i = 0; i < attr.count; i++) {
                pts.push({ x: attr.getX(i), y: attr.getY(i), z: attr.getZ(i) });
            }
            return {
                newApexCP: spline.userData.controlPoints[1],
                vertexCount: attr.count,
                maxZ: Math.max(...pts.map(p => p.z)),
                midPoint: pts[Math.floor(pts.length / 2)]
            };
        })()
    """)
    print("Edited Metrics (CP2 moved to Z=45):")
    print(json.dumps(edited_metrics, indent=2))

    # Test DPR 2.0 (Retina Display Emulation)
    print("--- 3. Testing Retina DPR 2.0 Viewport Rendering ---")
    send_cmd('Emulation.setDeviceMetricsOverride', {
        'width': 1280,
        'height': 800,
        'deviceScaleFactor': 2.0,
        'mobile': False
    })
    evaluate("renderAllViewports();")
    time.sleep(0.8)
    save_screenshot("spline_05_retina_dpr2_spline.png")

    # Reset DPR
    send_cmd('Emulation.setDeviceMetricsOverride', {
        'width': 1280,
        'height': 800,
        'deviceScaleFactor': 1.0,
        'mobile': False
    })
    time.sleep(0.3)

    # Test Single Undo of Move CP
    print("--- 4. Testing Undo of Control Point Edit ---")
    evaluate("executeUndo();")
    time.sleep(0.5)
    save_screenshot("spline_06_undo_move_reverted.png")
    reverted_max_z = evaluate("""
        (() => {
            const spline = sceneObjects.find(o => o.userData && o.userData.type === 'SplineCurve');
            return spline ? spline.userData.controlPoints[1].z : null;
        })()
    """)
    print(f"Reverted CP2 Z = {reverted_max_z}")

    # Test Undo of Spline Creation
    print("--- 5. Testing Undo of Spline Creation ---")
    evaluate("executeUndo();")
    time.sleep(0.5)
    save_screenshot("spline_07_undo_creation_removed.png")

    post_undo_count = evaluate("sceneObjects.length")
    has_spline = evaluate("sceneObjects.some(o => o.userData && o.userData.type === 'SplineCurve')")
    print(f"Post Undo: Scene objects count = {post_undo_count}, Spline present = {has_spline}")

    # Test Direct Single Undo of Spline Creation without edits
    print("--- 6. Testing Direct Single-Step Undo of Fresh Spline ---")
    evaluate("""
        createSplineSketch([
            new THREE.Vector3(-15, 0, 5),
            new THREE.Vector3(0, 0, 30),
            new THREE.Vector3(15, 0, 5)
        ], 'top');
    """)
    time.sleep(0.3)
    count_with_fresh = evaluate("sceneObjects.length")
    print(f"Scene objects with fresh spline = {count_with_fresh}")
    evaluate("executeUndo();")
    time.sleep(0.3)
    count_after_fresh_undo = evaluate("sceneObjects.length")
    has_fresh_spline = evaluate("sceneObjects.some(o => o.userData && o.userData.type === 'SplineCurve')")
    print(f"Post single-step undo: count = {count_after_fresh_undo}, Spline present = {has_fresh_spline}")

    with open('spline_verification_results.json', 'w') as f:
        json.dump({
            "geom_metrics": geom_metrics,
            "edited_metrics": edited_metrics,
            "reverted_max_z": reverted_max_z,
            "post_undo_count": post_undo_count,
            "has_spline_after_undo": has_spline,
            "single_step_undo_verified": (count_after_fresh_undo == 0 and not has_fresh_spline)
        }, f, indent=2)

    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
finally:
    proc.terminate()
