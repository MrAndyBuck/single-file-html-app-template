#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/92f72284-41c5-4687-ab10-0c2aade50fd2/screenshots"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9325

print(f"Launching Chrome on port {PORT}...")
proc = subprocess.Popen([
    CHROME_BIN,
    "--headless=new",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--window-size=1440,900",
    f"--remote-debugging-port={PORT}",
    "file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1"
])
time.sleep(2.5)

try:
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

    cmd_counter = 1
    def send_cmd(method, params=None):
        global cmd_counter
        cid = cmd_counter
        cmd_counter += 1
        msg = json.dumps({"id": cid, "method": method, "params": params or {}}).encode("utf-8")
        frame = bytearray([0x81])
        length = len(msg)
        mask = b"\x11\x22\x33\x44"
        if length < 126:
            frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", length))
        frame.extend(mask)
        frame.extend(bytearray(b ^ mask[i % 4] for i, b in enumerate(msg)))
        s.sendall(frame)

        while True:
            h = s.recv(2)
            if not h: break
            l = h[1] & 0x7F
            if l == 126: l = struct.unpack(">H", s.recv(2))[0]
            elif l == 127: l = struct.unpack(">Q", s.recv(8))[0]
            raw = bytearray()
            while len(raw) < l: raw.extend(s.recv(l - len(raw)))
            res = json.loads(raw.decode("utf-8"))
            if res.get("id") == cid:
                return res.get("result", {})

    def evaluate(expr):
        res = send_cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        if "exceptionDetails" in res:
            raise Exception(res["exceptionDetails"])
        return res.get("result", {}).get("value")

    def capture_screenshot(filename):
        evaluate("""
            (() => {
                document.querySelectorAll('.ad-overlay, .ad-card, dialog[open]').forEach(el => {
                    if (typeof el.close === 'function') el.close();
                    else el.remove();
                });
                const hud = document.getElementById('debug-overlay');
                if (hud) hud.classList.add('minimized');
                renderAllViewports();
            })()
        """)
        time.sleep(0.2)
        res = send_cmd("Page.captureScreenshot", {"format": "png"})
        raw = base64.b64decode(res["data"])
        p1 = os.path.join(SS_DIR, filename)
        p2 = os.path.join(ART_DIR, filename)
        with open(p1, "wb") as f:
            f.write(raw)
        with open(p2, "wb") as f:
            f.write(raw)
        print(f"Captured screenshot: {filename} ({len(raw)} bytes)")

    # 1. Run automated test suite
    print("\n--- 1. RUNNING IN-PAGE AUTOMATED TEST SUITE ---")
    evaluate("runAllTests()")
    test_res = evaluate("window.__TEST_RESULTS__")
    print(f"Unit Tests: {test_res['passed']} / {test_res['total']} PASSED, {test_res['failed']} FAILED")
    assert test_res['failed'] == 0, f"Automated tests failed! Details: {test_res['details']}"

    # Dismiss test overlay for clean screenshots
    evaluate("""
        const overlay = document.getElementById('test-results-log');
        if (overlay) overlay.style.display = 'none';
    """)

    # Helper functions to dispatch PointerEvents directly on active viewport canvas
    def pointer_down(vp_name, client_x, client_y):
        return evaluate(f"""
            (() => {{
                const vp = viewports['{vp_name}'];
                const pe = new PointerEvent('pointerdown', {{
                    bubbles: true,
                    cancelable: true,
                    clientX: {client_x},
                    clientY: {client_y},
                    button: 0,
                    buttons: 1
                }});
                vp.canvas.dispatchEvent(pe);
                return true;
            }})()
        """)

    def pointer_move(vp_name, client_x, client_y):
        return evaluate(f"""
            (() => {{
                const vp = viewports['{vp_name}'];
                const pe = new PointerEvent('pointermove', {{
                    bubbles: true,
                    cancelable: true,
                    clientX: {client_x},
                    clientY: {client_y},
                    button: 0,
                    buttons: 0
                }});
                vp.canvas.dispatchEvent(pe);
                return true;
            }})()
        """)

    # Get Top Viewport Canvas Bounding Rect
    top_bounds = evaluate("""
        (() => {
            const vp = viewports.top;
            const r = vp.canvas.getBoundingClientRect();
            return { left: r.left, top: r.top, width: r.width, height: r.height };
        })()
    """)
    print("Top Viewport Canvas Bounds:", top_bounds)

    cx = top_bounds["left"] + top_bounds["width"] * 0.5
    cy = top_bounds["top"] + top_bounds["height"] * 0.5

    # =========================================================================
    # TEST RECTANGLE WORKFLOW AT DPR 1.0
    # =========================================================================
    print("\n--- 2. TEST: RECTANGLE SKETCH AT DPR 1.0 ---")
    send_cmd("Emulation.setDeviceMetricsOverride", {
        "width": 1440,
        "height": 900,
        "deviceScaleFactor": 1.0,
        "mobile": False
    })

    initial_count = evaluate("sceneObjects.length")
    print(f"Scene objects before sketch: {initial_count}")

    # Activate Rectangle via toolbar icon
    evaluate("document.querySelector('[data-cmd=\"rect\"]').click();")
    assert evaluate("activeSketchMode") == "rect", "Active sketch mode must be 'rect'"

    # Corner 1 click
    c1_x, c1_y = cx - 75, cy - 50
    pointer_down("top", c1_x, c1_y)
    assert evaluate("sketchPoints.length") == 1, "Corner 1 sets exactly one anchor point"
    assert evaluate("sceneObjects.length") == initial_count, "No geometry committed on Corner 1"

    # Move pointer 25 times to simulate active mouse movement
    c2_x, c2_y = cx + 75, cy + 50
    preview_counts = []
    for step in range(1, 26):
        cur_x = c1_x + (c2_x - c1_x) * (step / 25.0)
        cur_y = c1_y + (c2_y - c1_y) * (step / 25.0)
        pointer_move("top", cur_x, cur_y)
        cnt = evaluate('scene.children.filter(c => c.name === "Sketch_Rubberband" || (c.userData && c.userData.isTransientPreview)).length')
        preview_counts.append(cnt)

    print(f"Preview counts during 25 pointer moves (min, max): ({min(preview_counts)}, {max(preview_counts)})")
    assert all(c == 1 for c in preview_counts), f"There must be EXACTLY ONE preview object at all times during movement! Found: {set(preview_counts)}"

    # Capture preview screenshot
    capture_screenshot("sketch_01_rect_preview.png")

    # Corner 2 click
    pointer_down("top", c2_x, c2_y)

    post_rect_count = evaluate("sceneObjects.length")
    print(f"Scene objects after Corner 2 click: {post_rect_count}")
    assert post_rect_count == initial_count + 1, f"Expected exactly 1 new object, got {post_rect_count - initial_count}"

    rect_info = evaluate("""
        (() => {
            const obj = sceneObjects[sceneObjects.length - 1];
            return {
                name: obj.name,
                type: obj.userData.type,
                closed: obj.userData.closed,
                numPoints: obj.userData.points.length,
                points: obj.userData.points.map(p => ({ x: p.x, y: p.y, z: p.z })),
                hasShape: !!obj.userData.shape,
                isLineLoop: obj.isLineLoop === true,
                activeMode: activeSketchMode,
                lingeringPreviews: scene.children.filter(c => c.name === "Sketch_Rubberband" || (c.userData && c.userData.isTransientPreview)).length
            };
        })()
    """)
    print("Committed Rectangle Info:", json.dumps(rect_info, indent=2))
    assert rect_info["type"] == "ClosedProfile", "Object must be ClosedProfile"
    assert rect_info["closed"] is True, "Object must be closed"
    assert rect_info["numPoints"] == 4, f"Rectangle must have exactly 4 corners, got {rect_info['numPoints']}"
    assert rect_info["hasShape"] is True, "Rectangle must carry 2D Shape for extrusion"
    assert rect_info["isLineLoop"] is True, "Rectangle must be rendered as THREE.LineLoop (4 boundary edges)"
    assert rect_info["activeMode"] is None, "Rectangle command must automatically exit after Corner 2!"
    assert rect_info["lingeringPreviews"] == 0, f"Expected 0 lingering preview objects, got {rect_info['lingeringPreviews']}"

    # Verify clicking elsewhere does NOT create additional rectangles
    pointer_down("top", cx + 110, cy + 110)
    assert evaluate("sceneObjects.length") == post_rect_count, "Clicking elsewhere must not create additional rectangles!"

    capture_screenshot("sketch_02_rect_committed.png")

    # Verify single Undo removes complete rectangle
    evaluate("executeUndo()")
    count_after_undo = evaluate("sceneObjects.length")
    print(f"Scene objects after Undo: {count_after_undo}")
    assert count_after_undo == initial_count, f"Single Undo must remove rectangle! Expected {initial_count}, got {count_after_undo}"

    # Verify Redo restores rectangle
    evaluate("executeRedo()")
    count_after_redo = evaluate("sceneObjects.length")
    print(f"Scene objects after Redo: {count_after_redo}")
    assert count_after_redo == post_rect_count, "Redo must restore rectangle"

    # Select profile and extrude it into 3D geometry
    evaluate("""
        (() => {
            const rect = sceneObjects[sceneObjects.length - 1];
            selectObject(rect);
            extrudeSelectedProfile(18);
        })()
    """)
    extrude_info = evaluate("""
        (() => {
            const solid = sceneObjects[sceneObjects.length - 1];
            return {
                name: solid.name,
                type: solid.userData.type,
                vertCount: solid.geometry.attributes.position.count
            };
        })()
    """)
    print("Extruded Solid Info:", extrude_info)
    assert extrude_info["type"] == "ExtrudedSolid", "Extrusion must produce ExtrudedSolid"
    assert extrude_info["vertCount"] > 0, "Extruded solid must contain geometry vertices"
    capture_screenshot("sketch_03_rect_extruded.png")

    # =========================================================================
    # TEST CIRCLE & LINE WORKFLOWS
    # =========================================================================
    print("\n--- 3. TEST: CIRCLE AND LINE WORKFLOWS ---")
    before_circ = evaluate("sceneObjects.length")

    # Activate Circle via request bar "Can I circle"
    evaluate("processRequest('Can I circle')")
    assert evaluate("activeSketchMode") == "circle"

    # Center click
    pointer_down("top", cx - 110, cy)
    assert evaluate("sketchPoints.length") == 1
    assert evaluate("sceneObjects.length") == before_circ

    # Move pointer 10 times to verify preview
    for step in range(1, 11):
        pointer_move("top", cx - 110 + step * 4, cy)
    circ_previews = evaluate('scene.children.filter(c => c.name === "Sketch_Rubberband").length')
    assert circ_previews == 1, "Circle preview must have exactly 1 object"

    # Radius click
    pointer_down("top", cx - 70, cy)
    assert evaluate("sceneObjects.length") == before_circ + 1, "Exactly one circle committed"
    assert evaluate("activeSketchMode") is None, "Circle command auto-exits"
    circ_obj = evaluate("sceneObjects[sceneObjects.length - 1].userData")
    assert circ_obj["type"] == "ClosedProfile" and circ_obj["closed"] is True

    # Test single 2-click Line
    before_line = evaluate("sceneObjects.length")
    evaluate("processRequest('Can I line')")
    assert evaluate("activeSketchMode") == "line"

    # P1 click
    pointer_down("top", cx + 50, cy - 35)
    assert evaluate("sketchPoints.length") == 1

    # Move pointer 10 times to verify preview
    for step in range(1, 11):
        pointer_move("top", cx + 50 + step * 6, cy - 35)
    line_previews = evaluate('scene.children.filter(c => c.name === "Sketch_Rubberband").length')
    assert line_previews == 1, "Line preview must have exactly 1 object"

    # P2 click
    pointer_down("top", cx + 110, cy - 35)
    assert evaluate("sceneObjects.length") == before_line + 1, "Exactly one line committed"
    assert evaluate("activeSketchMode") is None, "Line command auto-exits"
    line_obj = evaluate("sceneObjects[sceneObjects.length - 1].userData")
    assert line_obj["type"] == "SketchCurve" and len(line_obj["points"]) == 2

    capture_screenshot("sketch_04_circle_and_line.png")

    # =========================================================================
    # TEST RETINA (DPR 2.0)
    # =========================================================================
    print("\n--- 4. TEST: RETINA DPR 2.0 INTERACTION ---")
    send_cmd("Emulation.setDeviceMetricsOverride", {
        "width": 1440,
        "height": 900,
        "deviceScaleFactor": 2.0,
        "mobile": False
    })
    time.sleep(0.5)

    dpr = evaluate("window.devicePixelRatio")
    print(f"Verified window.devicePixelRatio: {dpr}")
    assert dpr == 2.0, f"Expected DPR 2.0, got {dpr}"

    dpr2_before = evaluate("sceneObjects.length")
    evaluate("startSketch('rect')")
    assert evaluate("activeSketchMode") == "rect"

    # Corner 1
    pointer_down("top", cx - 40, cy + 25)
    assert evaluate("sketchPoints.length") == 1

    # Move cursor
    for step in range(1, 15):
        pointer_move("top", cx - 40 + step * 6, cy + 25 + step * 4)

    dpr2_previews = evaluate('scene.children.filter(c => c.name === "Sketch_Rubberband").length')
    assert dpr2_previews == 1, f"Expected 1 preview at DPR 2.0, got {dpr2_previews}"

    # Corner 2
    pointer_down("top", cx + 50, cy + 85)
    assert evaluate("sceneObjects.length") == dpr2_before + 1, "DPR 2.0 creates exactly 1 rectangle"
    assert evaluate("activeSketchMode") is None, "DPR 2.0 auto-exits"
    dpr2_rect = evaluate("sceneObjects[sceneObjects.length - 1].userData")
    assert dpr2_rect["type"] == "ClosedProfile" and len(dpr2_rect["points"]) == 4

    capture_screenshot("sketch_05_retina_dpr2_rect.png")

    print("\n=======================================================")
    print("ALL CHECKPOINT A VERIFICATION CRITERIA SUCCESSFULLY PASSED!")
    print("=======================================================")

finally:
    try: s.close()
    except: pass
    proc.terminate()
    proc.wait()
