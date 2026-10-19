#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/92f72284-41c5-4687-ab10-0c2aade50fd2/screenshots"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9298

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
            if not header or len(header) < 2:
                raise RuntimeError("Socket closed or incomplete header")
            b1, b2 = header[0], header[1]
            opcode = b1 & 0x0f
            masked = (b2 & 0x80) != 0
            payload_len = b2 & 0x7f
            if payload_len == 126:
                payload_len = struct.unpack(">H", s.recv(2))[0]
            elif payload_len == 127:
                payload_len = struct.unpack(">Q", s.recv(8))[0]
            if masked:
                mask = s.recv(4)
            raw = bytearray()
            while len(raw) < payload_len:
                chunk = s.recv(payload_len - len(raw))
                if not chunk: break
                raw.extend(chunk)
            if masked:
                raw = bytearray(b ^ mask[i % 4] for i, b in enumerate(raw))
            if opcode == 1:
                resp = json.loads(raw.decode("utf-8"))
                if resp.get("id") == target_id:
                    return resp

    def eval_expr(expr):
        cid = send_cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        res = recv_msg(cid)
        if "result" in res and "result" in res["result"]:
            val = res["result"]["result"].get("value")
            return val
        return None

    def take_screenshot(filename, clip=None):
        params = {"format": "png"}
        if clip:
            params["clip"] = clip
        cid = send_cmd("Page.captureScreenshot", params)
        res = recv_msg(cid)
        img_b64 = res["result"]["data"]
        path1 = os.path.join(SS_DIR, filename)
        path2 = os.path.join(ART_DIR, filename)
        with open(path1, "wb") as f:
            f.write(base64.b64decode(img_b64))
        with open(path2, "wb") as f:
            f.write(base64.b64decode(img_b64))
        print(f"Captured screenshot: {filename} ({len(img_b64)} bytes)")

    # 1. Check startup state
    time.sleep(1.0)
    app_info = eval_expr("""({
        title: document.title,
        version: window.APP_VERSION,
        objectsCount: typeof sceneObjects !== 'undefined' ? sceneObjects.length : 0,
        hasMichigan: typeof michiganModel !== 'undefined' && michiganModel !== null,
        themeBtn: document.getElementById('btn-theme-toggle') !== null,
        themeMenuItem: document.getElementById('mitem-view-theme') !== null,
        headerTitleW: document.querySelector('.win95-title-content') ? document.querySelector('.win95-title-content').getBoundingClientRect().width : 0
    })""")
    print("Initial App State:", json.dumps(app_info, indent=2))

    assert app_info["themeBtn"] is False, "Theme button was not removed!"
    assert app_info["themeMenuItem"] is False, "Theme menu item was not removed!"
    assert app_info["headerTitleW"] >= 380, f"Header title width {app_info['headerTitleW']} is less than 380px!"

    # 2. Check 10 placeholder tools
    tools_check = eval_expr("""(() => {
        const ids = ["tool-sweep", "tool-pipe", "tool-loft", "tool-shell", "tool-offset", "tool-mirror", "tool-array", "tool-trim", "tool-extend", "tool-project"];
        return ids.map(id => ({ id, exists: document.getElementById(id) !== null }));
    })()""")
    print("Placeholder tools check:", tools_check)
    assert all(t["exists"] for t in tools_check), "Not all 10 placeholder tools exist!"

    # 3. Click placeholder tool 'Sweep' to verify retro "Coming Soon" popup
    eval_expr("""(() => {
        const btn = document.getElementById('tool-sweep');
        if (btn) btn.click();
    })()""")
    time.sleep(0.5)

    modal_state = eval_expr("""(() => {
        const m = document.getElementById('modal-coming-soon');
        return {
            open: m ? (m.open || m.hasAttribute('open')) : false,
            title: document.getElementById('coming-soon-title') ? document.getElementById('coming-soon-title').textContent : '',
            msg: document.getElementById('coming-soon-msg') ? document.getElementById('coming-soon-msg').textContent : ''
        };
    })()""")
    print("Coming soon modal state:", modal_state)
    assert modal_state["open"] is True, "Coming Soon modal did not open!"
    take_screenshot("features_01_placeholder_coming_soon.png")

    # Close modal
    eval_expr("""(() => {
        const btn = document.getElementById('btn-close-coming-soon') || document.querySelector('#modal-coming-soon .btn-caption-close');
        if (btn) btn.click();
        const m = document.getElementById('modal-coming-soon');
        if (m && m.close) m.close();
    })()""")
    time.sleep(0.5)

    # 4. Asymmetrical Chamfer Verification (e.g. D1=2.0, D2=6.0)
    print("Testing Asymmetrical Chamfer...")
    eval_expr("""(() => {
        window.IS_TESTING = true;
        createBoxPrimitive();
        const box = sceneObjects[sceneObjects.length - 1];
        selectObject(box);
        processRequest("Can I chamfer 2 6");
        const scope = document.getElementById("fillet-param-scope");
        scope.value = "vertical";
        scope.onchange();
    })()""")
    time.sleep(0.5)

    chamfer_ui_state = eval_expr("""(() => {
        return {
            typeVal: document.getElementById("fillet-param-type").value,
            d1: document.getElementById("fillet-param-val").value,
            d2: document.getElementById("fillet-param-val2").value,
            cVal2Display: document.getElementById("fillet-container-val2").style.display,
            lbl1: document.getElementById("fillet-lbl-val1").textContent,
            lbl2: document.getElementById("fillet-lbl-val2").textContent,
            selectedCount: activeCommand ? activeCommand.selectedEdgeCount() : 0,
            prompt: document.getElementById("command-prompt").textContent
        };
    })()""")
    print("Asymmetrical Chamfer UI State:", chamfer_ui_state)
    assert chamfer_ui_state["typeVal"] == "asymmetric"
    assert chamfer_ui_state["d1"] == "2"
    assert chamfer_ui_state["d2"] == "6"
    assert chamfer_ui_state["selectedCount"] == 4

    # Apply chamfer
    eval_expr("""activeCommand.confirm()""")
    time.sleep(1.0) # artificial delay

    chamfer_solid_state = eval_expr("""(() => {
        const obj = selectedObjects[0];
        if (!obj) return null;
        const pos = obj.geometry.attributes.position;
        // Collect unique X and Z offsets on cut vertices
        const xs = new Set(), zs = new Set();
        for (let i = 0; i < pos.count; i++) {
            xs.add(Math.round(pos.getX(i) * 100) / 100);
            zs.add(Math.round(pos.getZ(i) * 100) / 100);
        }
        return {
            name: obj.name,
            type: obj.userData.type,
            filletParams: obj.userData.filletParams,
            vertCount: pos.count,
            uniqueX: Array.from(xs).sort((a,b)=>a-b),
            uniqueZ: Array.from(zs).sort((a,b)=>a-b)
        };
    })()""")
    print("Asymmetrical Chamfer Solid:", chamfer_solid_state)
    assert chamfer_solid_state["type"] == "AsymChamferedSolid"
    eval_expr("""if (requestLogBox) requestLogBox.style.display = 'none';""")
    time.sleep(0.3)
    take_screenshot("features_02_asymmetric_chamfer.png")

    # 5. Asymmetrical Fillet Verification (e.g. R1=2.0, R2=6.0)
    print("Testing Asymmetrical Fillet...")
    eval_expr("""(() => {
        createBoxPrimitive();
        const box = sceneObjects[sceneObjects.length - 1];
        selectObject(box);
        processRequest("Can I fillet 2 6");
        const scope = document.getElementById("fillet-param-scope");
        scope.value = "vertical";
        scope.onchange();
    })()""")
    time.sleep(0.5)

    fillet_ui_state = eval_expr("""(() => {
        return {
            typeVal: document.getElementById("fillet-param-type").value,
            r1: document.getElementById("fillet-param-val").value,
            r2: document.getElementById("fillet-param-val2").value,
            cVal2Display: document.getElementById("fillet-container-val2").style.display,
            lbl1: document.getElementById("fillet-lbl-val1").textContent,
            lbl2: document.getElementById("fillet-lbl-val2").textContent,
            selectedCount: activeCommand ? activeCommand.selectedEdgeCount() : 0,
            prompt: document.getElementById("command-prompt").textContent
        };
    })()""")
    print("Asymmetrical Fillet UI State:", fillet_ui_state)
    assert fillet_ui_state["typeVal"] == "asymmetric"
    assert fillet_ui_state["r1"] == "2"
    assert fillet_ui_state["r2"] == "6"
    assert fillet_ui_state["selectedCount"] == 4

    # Apply fillet
    eval_expr("""activeCommand.confirm()""")
    time.sleep(1.0) # artificial delay

    fillet_solid_state = eval_expr("""(() => {
        const obj = selectedObjects[0];
        if (!obj) return null;
        const pos = obj.geometry.attributes.position;
        return {
            name: obj.name,
            type: obj.userData.type,
            filletParams: obj.userData.filletParams,
            vertCount: pos.count
        };
    })()""")
    print("Asymmetrical Fillet Solid:", fillet_solid_state)
    assert fillet_solid_state["type"] == "AsymFilletedSolid"
    eval_expr("""if (requestLogBox) requestLogBox.style.display = 'none';""")
    time.sleep(0.3)
    take_screenshot("features_03_asymmetric_fillet.png")

    # Clean workspace overview before tests
    take_screenshot("features_04_full_ui_overview.png")

    # 6. Run all automated tests in the application suite
    print("Running in-app test suite...")
    test_results = eval_expr("""runAllTests()""")
    print("Test Suite Summary:", {
        "passed": test_results.get("passed"),
        "failed": test_results.get("failed"),
        "total": test_results.get("total")
    })
    failures = [d for d in test_results.get("details", []) if d.get("status") == "FAIL"]
    if failures:
        print("Failed tests:", json.dumps(failures, indent=2))
    assert test_results.get("failed", 0) == 0, f"{test_results.get('failed')} tests failed!"

    take_screenshot("features_05_test_results_passed.png")
    print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")

finally:
    proc.terminate()
    proc.wait()
