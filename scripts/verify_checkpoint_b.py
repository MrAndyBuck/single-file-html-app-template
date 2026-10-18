#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9270

proc = subprocess.Popen([
    CHROME_BIN,
    "--headless=new",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--window-size=1440,900",
    f"--remote-debugging-port={PORT}",
    "about:blank"
])
time.sleep(1.5)

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
        msg = {"id": cid, "method": method}
        if params: msg["params"] = params
        data = json.dumps(msg).encode("utf-8")
        frame = bytearray([0x81])
        length = len(data)
        mask_key = b"\x11\x22\x33\x44"
        if length < 126:
            frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", length))
        frame.extend(mask_key)
        frame.extend(bytearray(b ^ mask_key[i % 4] for i, b in enumerate(data)))
        s.sendall(frame)
        return cid

    def recv_msg(target_id):
        while True:
            header = s.recv(2)
            if not header: return None
            length = header[1] & 0x7f
            if length == 126:
                length = struct.unpack(">H", s.recv(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", s.recv(8))[0]
            payload = b""
            while len(payload) < length:
                payload += s.recv(length - len(payload))
            msg = json.loads(payload.decode("utf-8", errors="ignore"))
            if msg.get("id") == target_id:
                return msg

    def eval_js(js):
        cid = send_cmd("Runtime.evaluate", {"expression": js, "returnByValue": True})
        res = recv_msg(cid)
        if "result" in res and "result" in res["result"]:
            val = res["result"]["result"].get("value")
            if val is not None:
                return val
            if "description" in res["result"]["result"]:
                return res["result"]["result"]["description"]
        return str(res)

    def capture_screenshot(filename):
        cid = send_cmd("Page.captureScreenshot", {"format": "png"})
        res = recv_msg(cid)
        img_bytes = base64.b64decode(res["result"]["data"])
        p1 = os.path.join(SS_DIR, filename)
        p2 = os.path.join(ART_DIR, filename)
        with open(p1, "wb") as f: f.write(img_bytes)
        with open(p2, "wb") as f: f.write(img_bytes)
        print(f"Captured {filename} ({len(img_bytes)} bytes)")
        return p1

    # Load App without auto-onboarding modal
    cid = send_cmd("Page.navigate", {"url": "file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1"})
    recv_msg(cid)
    time.sleep(2.5)

    # Dismiss any modals and minimize debug HUD
    eval_js("""
    (() => {
        const m = document.getElementById("modal-onboarding");
        if (m && m.open) m.close();
        localStorage.setItem("cadnt_onboarded", "true");
        const hud = document.getElementById("debug-overlay");
        if (hud) hud.classList.add("minimized");
        while (sceneObjects.length > 0) {
            scene.remove(sceneObjects[0]);
            sceneObjects.shift();
        }
    })()
    """)
    time.sleep(0.5)

    # -------------------------------------------------------------
    # Scenario 1: Connected sketch lines in progress with endpoint snapping
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        setActiveViewport("top");
        startSketch("line");
        // Points P0, P1, P2, P3
        handleSketchClick(new THREE.Vector3(-15, 0, -10), "top");
        handleSketchClick(new THREE.Vector3(15, 0, -10), "top");
        handleSketchClick(new THREE.Vector3(15, 0, 10), "top");
        handleSketchClick(new THREE.Vector3(-15, 0, 10), "top");
        // Hover cursor near P0 to trigger snap and close indicator
        updateRubberband(new THREE.Vector3(-14.6, 0, -9.6), "top");
    })()
    """)
    time.sleep(0.6)
    ss1 = capture_screenshot("checkpoint_b_01_connected_sketch_closing.png")

    # -------------------------------------------------------------
    # Scenario 2: Close profile & Extrude into true 3D Solid
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        // Click on P0 to close profile
        handleSketchClick(new THREE.Vector3(-15, 0, -10), "top");
        // Select the new closed profile and extrude it
        const closedProf = sceneObjects[sceneObjects.length - 1];
        selectObject(closedProf);
        const extrudedSolid = extrudeSelectedProfile(16);
        selectObject(extrudedSolid);
        // Switch to Perspective active viewport to see 3D isometric view
        setActiveViewport("perspective");
    })()
    """)
    time.sleep(0.8)
    ss2 = capture_screenshot("checkpoint_b_02_sketch_extruded_solid.png")

    # -------------------------------------------------------------
    # Scenario 3: Rhino-Style Point-to-Point Move in action
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        const solid = selectedObjects[0];
        startModelingCommand("move");
        // Set base point at solid centroid (0, 8, 0)
        activeCommand.handlePointerDown(new THREE.Vector3(0, 0, 0), "top");
        // Preview pointermove to destination point (24, 0, 18)
        activeCommand.handlePointerMove(new THREE.Vector3(24, 0, 18), "top");
    })()
    """)
    time.sleep(0.8)
    ss3 = capture_screenshot("checkpoint_b_03_rhino_move_point_to_point.png")

    # Finalize move
    move_stats = eval_js("""
    (() => {
        const solid = selectedObjects[0];
        const origPos = solid.position.clone();
        activeCommand.confirm();
        const newPos = solid.position.clone();
        return JSON.stringify({
            orig: [origPos.x, origPos.y, origPos.z],
            new: [newPos.x, newPos.y, newPos.z],
            displacement: [newPos.x - origPos.x, newPos.y - origPos.y, newPos.z - origPos.z]
        });
    })()
    """)
    print("MOVE COMPLETED STATS:", move_stats)

    # Launch macOS Preview directly for instant review
    print("Opening verification screenshots in macOS Preview...")
    subprocess.run(["open", "-a", "Preview", ss1, ss2, ss3])

finally:
    proc.terminate()
