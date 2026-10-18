#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9255

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
    resp = s.recv(4096).decode()

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
    })()
    """)

    # Setup base box
    eval_js("""
    (() => {
        while (sceneObjects.length > 0) {
            scene.remove(sceneObjects[0]);
            sceneObjects.shift();
        }
        createBoxPrimitive();
        const box = sceneObjects[0];
        box.position.set(0, 10, 0);
        box.geometry = new THREE.BoxGeometry(20, 20, 20);
        box.name = "Test_Box";
        box.updateMatrix();
        box.updateMatrixWorld();
        selectObject(box);
        render();
    })()
    """)
    time.sleep(0.5)

    # 1. Start Fillet, toggle Edge 0 and Edge 3
    eval_js("""
    (() => {
        startModelingCommand("fillet", { val: 3.0 });
        activeCommand.toggleEdge(0);
        activeCommand.toggleEdge(3);
        render();
    })()
    """)
    time.sleep(0.5)
    ss1 = capture_screenshot("checkpoint_a_01_fillet_edge_selection_preview.png")

    # 2. Confirm Fillet
    eval_js("""
    (() => {
        window.IS_TESTING = true;
        activeCommand.confirm();
        window.IS_TESTING = false;
        render();
    })()
    """)
    time.sleep(0.8)
    ss2 = capture_screenshot("checkpoint_a_02_fillet_completed_solid.png")

    # 3. Add second box and Chamfer vertical edges
    eval_js("""
    (() => {
        createBoxPrimitive();
        const box2 = sceneObjects[sceneObjects.length - 1];
        box2.position.set(32, 10, 0);
        box2.geometry = new THREE.BoxGeometry(20, 20, 20);
        box2.name = "Chamfer_Target";
        box2.updateMatrix();
        box2.updateMatrixWorld();
        selectObject(box2);

        startModelingCommand("chamfer", { val: 3.5 });
        const scopeSel = document.getElementById("fillet-param-scope");
        scopeSel.value = "vertical";
        scopeSel.onchange();

        window.IS_TESTING = true;
        activeCommand.confirm();
        window.IS_TESTING = false;
        render();
    })()
    """)
    time.sleep(0.8)
    ss3 = capture_screenshot("checkpoint_a_03_chamfer_selected_edges.png")

    # Inspect geometries
    stats = eval_js("""
    (() => {
        const filleted = sceneObjects.find(o => o.userData.type === "FilletedSolid");
        const chamfered = sceneObjects.find(o => o.userData.type === "ChamferedSolid");

        filleted.geometry.computeBoundingBox();
        chamfered.geometry.computeBoundingBox();

        // Check corner coordinates for Filleted
        const fPos = filleted.geometry.attributes.position;
        let maxRadiusPoint = 0;
        for (let i = 0; i < fPos.count; i++) {
            const x = fPos.getX(i), z = fPos.getZ(i);
            if (x > 7.0 && z > 7.0) {
                // In fillet corner (center is at 7, 7, radius 3)
                const distToCenter = Math.sqrt((x - 7.0)**2 + (z - 7.0)**2);
                if (Math.abs(distToCenter - 3.0) < 0.1) maxRadiusPoint++;
            }
        }

        // Check corner coordinates for Chamfered (bevel cut from 10-3.5=6.5 to 10)
        const cPos = chamfered.geometry.attributes.position;
        let bevelVerts = 0;
        for (let i = 0; i < cPos.count; i++) {
            const x = cPos.getX(i), z = cPos.getZ(i);
            // On bevel face x + z = 16.5
            if (Math.abs((x + z) - 16.5) < 0.1 && x >= 6.4 && z >= 6.4) {
                bevelVerts++;
            }
        }

        return JSON.stringify({
            filleted: {
                name: filleted.name,
                vertCount: fPos.count,
                boxMin: [filleted.geometry.boundingBox.min.x, filleted.geometry.boundingBox.min.y, filleted.geometry.boundingBox.min.z],
                boxMax: [filleted.geometry.boundingBox.max.x, filleted.geometry.boundingBox.max.y, filleted.geometry.boundingBox.max.z],
                arcVertMatches: maxRadiusPoint
            },
            chamfered: {
                name: chamfered.name,
                vertCount: cPos.count,
                boxMin: [chamfered.geometry.boundingBox.min.x, chamfered.geometry.boundingBox.min.y, chamfered.geometry.boundingBox.min.z],
                boxMax: [chamfered.geometry.boundingBox.max.x, chamfered.geometry.boundingBox.max.y, chamfered.geometry.boundingBox.max.z],
                bevelVertMatches: bevelVerts
            }
        });
    })()
    """)
    print("VERIFICATION STATS:", stats)

    # Test Undo
    undo_res = eval_js("""
    (() => {
        const countBefore = sceneObjects.length;
        processRequest("Can I undo");
        const countAfter = sceneObjects.length;
        return JSON.stringify({ countBefore, countAfter });
    })()
    """)
    print("UNDO TEST:", undo_res)

    # Launch macOS Preview directly
    print("Opening verification screenshots in macOS Preview...")
    subprocess.run(["open", "-a", "Preview", ss1, ss2, ss3])

finally:
    proc.terminate()
