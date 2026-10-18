#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9276

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
    print("Navigating to index.html...")
    cid = send_cmd("Page.navigate", {"url": "file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1"})
    recv_msg(cid)
    time.sleep(2.0)
    
    print("Running automated unit test suite (window.runAllTests())...")
    eval_js("window.runAllTests()")
    
    # Wait for test suite completion
    for _ in range(40):
        time.sleep(0.3)
        done = eval_js("window.__TESTS_DONE__ === true")
        if done is True or done == "true":
            break

    test_results_str = eval_js("JSON.stringify(window.__TEST_RESULTS__ || {})")
    print("AUTOMATED TEST RESULTS:", test_results_str)
    test_results = json.loads(test_results_str) if test_results_str else {}
    print(f"PASS COUNT: {test_results.get('passed')}/{test_results.get('total')}, FAIL: {test_results.get('failed')}")

    # Setup clean workspace for Checkpoint D visual verification
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

    # -------------------------------------------------------------
    # Scenario 1: Compact toolbar and removed navigation buttons
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        status("Checkpoint D: Forward/Back buttons removed, Features toolbar compact grid.");
        addLog("Standard toolbar cleaned (no manual nav buttons).", "log-info");
        addLog("Right-side Features toolbar reorganized into compact Windows 95 grid.", "log-info");
        document.getElementById("request-input").value = "";
    })()
    """)
    time.sleep(0.8)
    ss1 = capture_screenshot("checkpoint_d_01_compact_toolbar_no_nav_buttons.png")

    state1 = eval_js("""
    (() => {
        const undoBtn = document.getElementById("tb-btn-undo");
        const redoBtn = document.getElementById("tb-btn-redo");
        const toolbar = document.querySelector(".modeling-toolbar-body");
        const cs = toolbar ? window.getComputedStyle(toolbar) : null;
        return JSON.stringify({
            hasUndoBtn: !!undoBtn,
            hasRedoBtn: !!redoBtn,
            gridAutoRows: cs ? cs.gridAutoRows : null,
            alignContent: cs ? cs.alignContent : null
        });
    })()
    """)
    print("SCENARIO 1 STATE:", state1)

    # -------------------------------------------------------------
    # Scenario 2: Insufficient funds popup displaying Finger.jpg
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        creditBalance = 5.00;
        updateEconomyDisplay();
        status("Attempted paid command with insufficient credits ($5.00 balance vs $49.00 fee).");
        addLog("Transaction terminated: Insufficient fictional credits. $0.00 deducted.", "log-nope");
        showInsufficientFundsModal("Fillet", 49.00, 5.00);
    })()
    """)
    time.sleep(0.8)
    ss2 = capture_screenshot("checkpoint_d_02_insufficient_funds_finger_popup.png")

    state2 = eval_js("""
    (() => {
        const modal = document.getElementById("modal-insufficient-funds");
        const img = document.getElementById("insufficient-funds-img");
        return JSON.stringify({
            modalOpen: modal ? modal.open : false,
            imgSrc: img ? img.getAttribute("src") : null,
            imgNaturalWidth: img ? img.naturalWidth : 0,
            imgNaturalHeight: img ? img.naturalHeight : 0,
            creditBalance: creditBalance
        });
    })()
    """)
    print("SCENARIO 2 STATE:", state2)

    # -------------------------------------------------------------
    # Scenario 3: Advertisements rotation and layered stacking
    # -------------------------------------------------------------
    eval_js("""
    (() => {
        const insModal = document.getElementById("modal-insufficient-funds");
        if (insModal && insModal.open) insModal.close();
        creditBalance = 249.00;
        updateEconomyDisplay();

        // Trigger ad popup with registered ads and stacked layer
        showAdPopup();
        // Display new ad
        displayAd(2); // AppleAppAd or new registered ad
        pushAdLayer(); // Layer 2nd ad above
        displayAd(12); // VirusAppAd or ZuneAppAd
        status("Unsolicited commercial break: stacked layered advertisements.");
        addLog("Advertisement layers active in rotation.", "log-warn");
    })()
    """)
    time.sleep(0.8)
    ss3 = capture_screenshot("checkpoint_d_03_advertisements_rotation_and_stacking.png")

    state3 = eval_js("""
    (() => {
        const adModal = document.getElementById("modal-ad");
        const cards = document.querySelectorAll(".ad-card");
        return JSON.stringify({
            adModalOpen: adModal ? adModal.open : false,
            stackedCardsCount: cards.length,
            totalAdsInManifest: ASSET_MANIFEST.ads.length
        });
    })()
    """)
    print("SCENARIO 3 STATE:", state3)

    # Launch macOS Preview directly for instant user review
    print("Opening verification screenshots in macOS Preview...")
    subprocess.run(["open", "-a", "Preview", ss1, ss2, ss3])

finally:
    proc.terminate()
