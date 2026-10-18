#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9272

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

    # Step 1: Run complete automated test suite
    print("Navigating to index.html with ?run_tests=1...")
    cid = send_cmd("Page.navigate", {"url": "file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?run_tests=1&no_auto_onboard=1"})
    recv_msg(cid)
    time.sleep(3.0)

    test_results = eval_js("""
    (() => {
        return JSON.stringify(window.__TEST_RESULTS__ || {});
    })()
    """)
    print("AUTOMATED TEST RESULTS:", test_results)

    # Step 2: Setup clean workspace for Checkpoint C visual verification
    eval_js("""
    (() => {
        const m = document.getElementById("modal-onboarding");
        if (m && m.open) m.close();
        localStorage.setItem("cadnt_onboarded", "true");
        const hud = document.getElementById("debug-overlay");
        if (hud) hud.style.display = "none";
        const testLog = document.getElementById("test-results-log");
        if (testLog) testLog.remove();
        while (sceneObjects.length > 0) {
            scene.remove(sceneObjects[0]);
            sceneObjects.shift();
        }
        selectedObjects = [];
        clearSelection();
        requestLogBox.innerHTML = "";
    })()
    """)
    time.sleep(0.5)

    # -------------------------------------------------------------
    # Scenario 1: Object selected, Gumball hidden by default
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        createBoxPrimitive();
        const box = sceneObjects[sceneObjects.length - 1];
        box.position.set(0, 8, 0);
        box.updateMatrixWorld(true);
        selectObject(box);
        status("Box_1 selected. Gumball hidden by default. Enter 'Can I gumball?' to activate.");
        addLog("Box_1 selected. Gumball hidden by default.", "log-info");
        document.getElementById("request-input").value = "";
    })()
    """)
    time.sleep(0.8)
    ss1 = capture_screenshot("checkpoint_c_01_gumball_hidden_by_default.png")

    state1 = eval_js("""
    (() => {
        return JSON.stringify({
            selected: selectedObjects.length,
            isGumballActive: isGumballActive,
            gumballVisible: gumballGroup ? gumballGroup.visible : false
        });
    })()
    """)
    print("SCENARIO 1 STATE:", state1)

    # -------------------------------------------------------------
    # Scenario 2: 'Can I gumball?' entered, Gumball appears on selection
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        document.getElementById("request-input").value = "Can I gumball?";
        processRequest("Can I gumball?");
    })()
    """)
    time.sleep(0.8)
    ss2 = capture_screenshot("checkpoint_c_02_gumball_activated_on_selection.png")

    state2 = eval_js("""
    (() => {
        return JSON.stringify({
            selected: selectedObjects.length,
            isGumballActive: isGumballActive,
            gumballVisible: gumballGroup ? gumballGroup.visible : false,
            gumballPos: gumballGroup ? [gumballGroup.position.x, gumballGroup.position.y, gumballGroup.position.z] : null
        });
    })()
    """)
    print("SCENARIO 2 STATE:", state2)

    # -------------------------------------------------------------
    # Scenario 3: Completed Free Move via Shift + M + Drag, Gumball dismissed immediately
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        const box = selectedObjects[0];
        const initialPos = box.position.clone();
        // Simulate start of free move drag with Shift+M
        gumballDragState = {
            mode: "free_move",
            vpId: "top",
            camera: cameras.top,
            plane: new THREE.Plane(new THREE.Vector3(0, 1, 0), 0),
            startHit: new THREE.Vector3(0, 0, 0),
            startGumballPos: box.position.clone(),
            startSnapshot: serializeProjectState(),
            hasMoved: true,
            initialStates: [{ obj: box, pos: box.position.clone(), rot: box.rotation.clone(), scale: box.scale.clone() }]
        };
        // Free move displacement
        box.position.x += 24;
        box.position.z += 18;
        box.updateMatrixWorld(true);
        // Release mouse/trackpad -> pointerup event
        window.dispatchEvent(new Event("pointerup"));
        document.getElementById("request-input").value = "";
    })()
    """)
    time.sleep(0.8)
    ss3 = capture_screenshot("checkpoint_c_03_free_move_gumball_dismissed.png")

    state3 = eval_js("""
    (() => {
        return JSON.stringify({
            selected: selectedObjects.length,
            isGumballActive: isGumballActive,
            gumballVisible: gumballGroup ? gumballGroup.visible : false,
            gumballDragState: gumballDragState !== null,
            undoStackDepth: undoStack.length,
            lastUndoDesc: undoStack.length > 0 ? undoStack[undoStack.length - 1].desc : null
        });
    })()
    """)
    print("SCENARIO 3 STATE:", state3)

    # Launch macOS Preview directly for instant review
    print("Opening verification screenshots in macOS Preview...")
    subprocess.run(["open", "-a", "Preview", ss1, ss2, ss3])

finally:
    proc.terminate()
