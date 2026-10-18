#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9295

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

    def capture_screenshot(filename, clip=None):
        params = {"format": "png"}
        if clip:
            params["clip"] = clip
        cid = send_cmd("Page.captureScreenshot", params)
        res = recv_msg(cid)
        img_bytes = base64.b64decode(res["result"]["data"])
        p1 = os.path.join(SS_DIR, filename)
        p2 = os.path.join(ART_DIR, filename)
        with open(p1, "wb") as f: f.write(img_bytes)
        with open(p2, "wb") as f: f.write(img_bytes)
        print(f"Captured {filename} ({len(img_bytes)} bytes)")
        return p1

    # Run automated test suite
    print("Running automated unit test suite (window.runAllTests())...")
    eval_js("window.runAllTests()")
    for _ in range(40):
        time.sleep(0.3)
        done = eval_js("window.__TESTS_DONE__ === true")
        if done is True or done == "true":
            break

    test_res_str = eval_js("JSON.stringify(window.__TEST_RESULTS__ || {})")
    test_res = json.loads(test_res_str) if test_res_str else {}
    print(f"AUTOMATED UNIT TEST SUITE: {test_res.get('passed', 0)}/{test_res.get('total', 0)} PASSED, {test_res.get('failed', 0)} FAILED.")

    # Reset workspace
    eval_js("""
    (() => {
        const m = document.getElementById("modal-onboarding");
        if (m && m.open) m.close();
        localStorage.setItem("cadnt_onboarded", "true");
        const hud = document.getElementById("debug-overlay");
        if (hud) hud.style.display = "none";
        const testLog = document.getElementById("test-results-log");
        if (testLog) testLog.remove();
        requestLogBox.innerHTML = "";
    })()
    """)
    time.sleep(0.5)

    captured_files = []

    # =========================================================================
    # SCENARIO 1: Insufficient Funds Modal ("haha broke bitch" + Finger.jpg)
    # =========================================================================
    print("\n--- SCENARIO 1: Insufficient Funds Modal ---")
    eval_js("""
    (() => {
        creditBalance = 5.00;
        updateEconomyDisplay();
        showInsufficientFundsModal("fillet", 49.00, 5.00);
    })()
    """)
    time.sleep(0.6)
    s1_file = capture_screenshot("ua_01_insufficient_funds_haha_broke_bitch.png")
    captured_files.append(s1_file)

    s1_data = eval_js("""
    (() => {
        const modal = document.getElementById("modal-insufficient-funds");
        const msg = document.getElementById("insufficient-funds-msg");
        const img = document.getElementById("insufficient-funds-img");
        return {
            open: modal && modal.open,
            message: msg ? msg.textContent.trim() : null,
            imageSrc: img ? img.getAttribute("src") : null,
            credits: creditBalance
        };
    })()
    """)
    print("Scenario 1 Data:", json.dumps(s1_data, indent=2))
    eval_js('document.getElementById("modal-insufficient-funds").close()')
    eval_js('creditBalance = 249.00; updateEconomyDisplay();')
    time.sleep(0.4)

    # =========================================================================
    # SCENARIO 2: Features Toolbar Full-Height Compact Grid Screenshot
    # =========================================================================
    print("\n--- SCENARIO 2: Compact Feature Toolbar ---")
    dock_rect = eval_js("""
    (() => {
        const dock = document.getElementById("right-modeling-dock");
        const rect = dock.getBoundingClientRect();
        return { x: rect.left, y: rect.top, width: rect.width, height: rect.height, scale: 1 };
    })()
    """)
    print("Features dock dimensions:", dock_rect)
    s2_file = capture_screenshot("ua_02_features_panel_compact_full_height.png", clip=dock_rect)
    captured_files.append(s2_file)

    # =========================================================================
    # SCENARIO 3: Ad Shuffle Bag & Diagnostic HUD View
    # =========================================================================
    print("\n--- SCENARIO 3: Ad Shuffle Bag Non-Replacement & Debug View ---")
    eval_js("""
    (() => {
        const hud = document.getElementById("debug-overlay");
        if (hud) {
            hud.style.display = "block";
            hud.classList.remove("minimized");
        }
        initializeOrRefillAdBag();
        // Trigger 2 ad draws
        getNextShuffleBagAdIndex();
        getNextShuffleBagAdIndex();
        updateAdDebugView();
    })()
    """)
    time.sleep(0.5)
    s3_file = capture_screenshot("ua_03_ad_shuffle_bag_debug_view.png")
    captured_files.append(s3_file)
    s3_data = eval_js("""
    (() => {
        return {
            remaining: document.getElementById("dbg-ads-remaining").textContent,
            shownCount: document.getElementById("dbg-ads-shown-count").textContent,
            history: document.getElementById("dbg-ads-history").textContent,
            pending: document.getElementById("dbg-ads-pending").textContent
        };
    })()
    """)
    print("Scenario 3 Data:", json.dumps(s3_data, indent=2))
    eval_js('document.getElementById("debug-overlay").style.display = "none"')

    # =========================================================================
    # SCENARIO 4: Single-Edge Fillet (Close-up Before, Selection/Preview, After)
    # =========================================================================
    print("\n--- SCENARIO 4: Single-Edge Fillet Close-Up & Geometric Validation ---")
    eval_js("""
    (() => {
        while (sceneObjects.length > 0) {
            scene.remove(sceneObjects[0]);
            sceneObjects.shift();
        }
        createBoxPrimitive();
        const box = sceneObjects[0];
        box.name = "Fillet_Test_Box";
        box.position.set(0, 10, 0);
        box.geometry = new THREE.BoxGeometry(20, 20, 20);
        box.updateMatrix();
        box.updateMatrixWorld(true);
        selectObject(box);

        // Position perspective camera for a dramatic close-up of the front-top-right corner (+10, +20, +10)
        cameras.perspective.position.set(22, 28, 26);
        cameras.perspective.lookAt(new THREE.Vector3(10, 20, 10));
        cameras.perspective.zoom = 1.8;
        cameras.perspective.updateProjectionMatrix();
        setActiveViewport("perspective");
        renderAllViewports();
    })()
    """)
    time.sleep(0.5)
    s4a_file = capture_screenshot("ua_04_fillet_01_before_sharp_edge_closeup.png")
    captured_files.append(s4a_file)

    # Start Fillet and select EXACTLY ONE edge (Edge #0: vertical edge at +10, +10)
    eval_js("""
    (() => {
        startModelingCommand("fillet", { val: 3.5 });
        activeCommand.toggleEdge(0);
        renderAllViewports();
    })()
    """)
    time.sleep(0.5)
    s4b_file = capture_screenshot("ua_04_fillet_02_single_edge_selected_preview.png")
    captured_files.append(s4b_file)

    # Confirm Fillet and capture completed rounded geometry
    eval_js("""
    (() => {
        window.IS_TESTING = true;
        activeCommand.confirm();
        window.IS_TESTING = false;
        renderAllViewports();
    })()
    """)
    time.sleep(0.8)
    s4c_file = capture_screenshot("ua_04_fillet_03_completed_rounded_solid_closeup.png")
    captured_files.append(s4c_file)

    fillet_geom_data = eval_js("""
    (() => {
        const box = sceneObjects[sceneObjects.length - 1];
        const pos = box.geometry.attributes.position.array;
        const norm = box.geometry.attributes.normal.array;
        
        // Find arc profile vertices in local coordinates
        const arcPts = [];
        for (let i = 0; i < pos.length; i += 3) {
            const x = pos[i], y = pos[i+1], z = pos[i+2];
            if (x > 6.4 && z > 6.4) {
                arcPts.push({ x: Number(x.toFixed(2)), z: Number(z.toFixed(2)) });
            }
        }
        const uniqueArc = [...new Set(arcPts.map(p => `${p.x},${p.z}`))].sort();

        // Check if cut corner (10, 10) exists
        const hasSharpCorner = uniqueArc.includes("10,10");
        
        // Check unaffected corner (-10, 10, -10)
        let unaffectedIntact = false;
        for (let i = 0; i < pos.length; i += 3) {
            if (Math.abs(pos[i] - (-10)) < 0.01 && Math.abs(pos[i+1] - 10) < 0.01 && Math.abs(pos[i+2] - (-10)) < 0.01) {
                unaffectedIntact = true;
                break;
            }
        }
        
        return {
            name: box.name,
            type: box.userData.type,
            vertexCount: pos.length / 3,
            triangleCount: pos.length / 9,
            hasSharpCorner,
            unaffectedIntact,
            arcProfileSample: uniqueArc
        };
    })()
    """)
    print("Fillet Geometric Validation:", json.dumps(fillet_geom_data, indent=2))

    # =========================================================================
    # SCENARIO 5: Single-Edge Chamfer (Close-up Before, Selection/Preview, After)
    # =========================================================================
    print("\n--- SCENARIO 5: Single-Edge Chamfer Close-Up & Geometric Validation ---")
    eval_js("""
    (() => {
        while (sceneObjects.length > 0) {
            scene.remove(sceneObjects[0]);
            sceneObjects.shift();
        }
        createBoxPrimitive();
        const box = sceneObjects[0];
        box.name = "Chamfer_Test_Box";
        box.position.set(0, 10, 0);
        box.geometry = new THREE.BoxGeometry(20, 20, 20);
        box.updateMatrix();
        box.updateMatrixWorld(true);
        selectObject(box);

        cameras.perspective.position.set(22, 28, 26);
        cameras.perspective.lookAt(new THREE.Vector3(10, 20, 10));
        cameras.perspective.zoom = 1.8;
        cameras.perspective.updateProjectionMatrix();
        setActiveViewport("perspective");
        renderAllViewports();
    })()
    """)
    time.sleep(0.5)
    s5a_file = capture_screenshot("ua_05_chamfer_01_before_sharp_edge_closeup.png")
    captured_files.append(s5a_file)

    # Start Chamfer and select EXACTLY ONE edge (Edge #0: vertical edge at +10, +10)
    eval_js("""
    (() => {
        startModelingCommand("chamfer", { val: 4.0 });
        activeCommand.toggleEdge(0);
        renderAllViewports();
    })()
    """)
    time.sleep(0.5)
    s5b_file = capture_screenshot("ua_05_chamfer_02_single_edge_selected_preview.png")
    captured_files.append(s5b_file)

    # Confirm Chamfer and capture completed beveled geometry
    eval_js("""
    (() => {
        window.IS_TESTING = true;
        activeCommand.confirm();
        window.IS_TESTING = false;
        renderAllViewports();
    })()
    """)
    time.sleep(0.8)
    s5c_file = capture_screenshot("ua_05_chamfer_03_completed_beveled_solid_closeup.png")
    captured_files.append(s5c_file)

    chamfer_geom_data = eval_js("""
    (() => {
        const box = sceneObjects[sceneObjects.length - 1];
        const pos = box.geometry.attributes.position.array;
        
        const bevelPts = [];
        for (let i = 0; i < pos.length; i += 3) {
            const x = pos[i], y = pos[i+1], z = pos[i+2];
            if (x > 5.9 && z > 5.9) {
                bevelPts.push({ x: Number(x.toFixed(2)), z: Number(z.toFixed(2)) });
            }
        }
        const uniqueBevel = [...new Set(bevelPts.map(p => `${p.x},${p.z}`))].sort();
        const hasSharpCorner = uniqueBevel.includes("10,10");
        
        let unaffectedIntact = false;
        for (let i = 0; i < pos.length; i += 3) {
            if (Math.abs(pos[i] - (-10)) < 0.01 && Math.abs(pos[i+1] - 10) < 0.01 && Math.abs(pos[i+2] - (-10)) < 0.01) {
                unaffectedIntact = true;
                break;
            }
        }
        
        return {
            name: box.name,
            type: box.userData.type,
            vertexCount: pos.length / 3,
            triangleCount: pos.length / 9,
            hasSharpCorner,
            unaffectedIntact,
            bevelProfileSample: uniqueBevel
        };
    })()
    """)
    print("Chamfer Geometric Validation:", json.dumps(chamfer_geom_data, indent=2))

    # Open all generated screenshots in macOS Preview
    print("\nOpening all user acceptance screenshots in macOS Preview...")
    subprocess.run(["open", "-a", "Preview"] + captured_files)
    print("All screenshots launched in Preview.")

finally:
    proc.terminate()
    print("Verification script finished cleanly.")
