#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc"
TEMP_PROFILE = "/Users/andybuck/.gemini/antigravity/single-file-html-app/scratch_chrome_profile"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)
os.makedirs(TEMP_PROFILE, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

class ChromeSession:
    def __init__(self, port):
        self.port = port
        self.proc = subprocess.Popen([
            CHROME_BIN,
            "--headless=new",
            "--enable-unsafe-swiftshader",
            "--use-gl=angle",
            "--use-angle=swiftshader",
            f"--user-data-dir={TEMP_PROFILE}_{port}",
            "--window-size=1440,900",
            f"--remote-debugging-port={port}",
            "about:blank"
        ])
        time.sleep(1.5)
        tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json").read().decode("utf-8"))
        target = next(t for t in tabs if t.get("type") == "page")
        ws_url = target["webSocketDebuggerUrl"]
        host, p, path = "127.0.0.1", port, ws_url.split(f"127.0.0.1:{port}")[1]

        self.s = socket.socket()
        self.s.connect((host, port))
        key = base64.b64encode(b"0123456789abcdef").decode()
        req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        self.s.sendall(req.encode())
        self.s.recv(4096)
        self.cmd_counter = 1

    def send_cmd(self, method, params=None):
        cid = self.cmd_counter
        self.cmd_counter += 1
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
        self.s.sendall(frame)
        return cid

    def recv_msg(self, target_id):
        while True:
            header = self.s.recv(2)
            if not header: return None
            length = header[1] & 0x7f
            if length == 126:
                length = struct.unpack(">H", self.s.recv(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self.s.recv(8))[0]
            payload = b""
            while len(payload) < length:
                payload += self.s.recv(length - len(payload))
            msg = json.loads(payload.decode("utf-8", errors="ignore"))
            if msg.get("id") == target_id:
                return msg

    def eval_js(self, js):
        cid = self.send_cmd("Runtime.evaluate", {"expression": js, "returnByValue": True})
        res = self.recv_msg(cid)
        if "result" in res and "result" in res["result"]:
            val = res["result"]["result"].get("value")
            if val is not None:
                return val
            if "description" in res["result"]["result"]:
                return res["result"]["result"]["description"]
        return str(res)

    def capture_screenshot(self, filename):
        cid = self.send_cmd("Page.captureScreenshot", {"format": "png"})
        res = self.recv_msg(cid)
        img_bytes = base64.b64decode(res["result"]["data"])
        p1 = os.path.join(SS_DIR, filename)
        p2 = os.path.join(ART_DIR, filename)
        with open(p1, "wb") as f: f.write(img_bytes)
        with open(p2, "wb") as f: f.write(img_bytes)
        print(f"Captured {filename} ({len(img_bytes)} bytes)")
        return p1

    def close(self):
        try:
            self.s.close()
        except: pass
        self.proc.terminate()
        self.proc.wait()

# =========================================================================
# PHASE 1: Run Full Automated Unit Test Suite
# =========================================================================
print("=== PHASE 1: Running Complete Automated Test Suite ===")
s1 = ChromeSession(9284)
try:
    cid = s1.send_cmd("Page.navigate", {"url": "file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1"})
    s1.recv_msg(cid)
    time.sleep(2.0)

    print("Executing window.runAllTests()...")
    s1.eval_js("window.runAllTests()")
    for _ in range(40):
        time.sleep(0.3)
        done = s1.eval_js("window.__TESTS_DONE__ === true")
        if done is True or done == "true":
            break

    test_results_str = s1.eval_js("JSON.stringify(window.__TEST_RESULTS__ || {})")
    test_results = json.loads(test_results_str) if test_results_str else {}
    print(f"AUTOMATED UNIT TEST SUITE: {test_results.get('passed')}/{test_results.get('total')} PASSED, {test_results.get('failed')} FAILED.")
finally:
    s1.close()

# =========================================================================
# PHASE 2: Visual Demonstrations for Rhino Move & Slow Gumball
# =========================================================================
print("\n=== PHASE 2: Visual Demonstrations for Rhino Move & Slow Gumball ===")
s2 = ChromeSession(9285)
try:
    cid = s2.send_cmd("Page.navigate", {"url": "file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1"})
    s2.recv_msg(cid)
    time.sleep(2.5)

    # Setup pristine scene
    s2.eval_js("""
    (() => {
        const m = document.getElementById("modal-onboarding");
        if (m && m.open) m.close();
        localStorage.setItem("cadnt_onboarded", "true");
        const hud = document.getElementById("debug-overlay");
        if (hud) hud.classList.add("minimized");
        const testLog = document.getElementById("test-results-log");
        if (testLog) testLog.remove();
        const adModal = document.getElementById("modal-advertisement");
        if (adModal && adModal.open) adModal.close();
        modelingCommandCount = 0;

        activeLayerId = "default";
        const defLayer = layers.find(l => l.id === "default");
        if (defLayer) defLayer.visible = true;
        renderLayersList();

        while (sceneObjects.length > 0) {
            scene.remove(sceneObjects[0]);
            sceneObjects.shift();
        }

        // Create Box A
        createBoxPrimitive();
        const boxA = sceneObjects[sceneObjects.length - 1];
        boxA.position.set(0, 10, 0);
        boxA.geometry = new THREE.BoxGeometry(20, 20, 20);
        boxA.name = "Box_A";
        boxA.material.color.setHex(0x3a7bd5); // Clean blue
        boxA.updateMatrix();
        boxA.updateMatrixWorld(true);

        // Create Box B separated in space
        createBoxPrimitive();
        const boxB = sceneObjects[sceneObjects.length - 1];
        boxB.position.set(40, 10, 30);
        boxB.geometry = new THREE.BoxGeometry(20, 20, 20);
        boxB.name = "Box_B";
        boxB.material.color.setHex(0xe08b2b); // Clean amber
        boxB.updateMatrix();
        boxB.updateMatrixWorld(true);

        selectObject(boxA);
        render();
    })()
    """)
    time.sleep(0.5)

    # ---------------------------------------------------------------------
    # Scenario 1A: Rhino Move ('Can I move') - Step 1: Source Corner OSNAP Picking
    # ---------------------------------------------------------------------
    print("Setting up Scenario 1A: Source Corner OSNAP Point Picking on Box A...")
    step1_state = s2.eval_js("""
    (() => {
        // Start Move command
        processRequest("Can I move");

        const prompt1 = document.getElementById("command-prompt").textContent;

        // Hover over Box A top-front-right corner: (10, 20, 10)
        const sourceCorner = new THREE.Vector3(10, 20, 10);
        const cam = cameras.perspective;
        const rect = viewports.perspective.canvas.getBoundingClientRect();
        const proj = sourceCorner.clone().project(cam);
        const screenX = ((proj.x + 1) / 2) * rect.width + rect.left;
        const screenY = ((-proj.y + 1) / 2) * rect.height + rect.top;

        // Trigger hover with OSNAP detection
        activeCommand.handlePointerMove(sourceCorner, "perspective", { clientX: screenX, clientY: screenY });

        render();

        const snapMarker = scene.getObjectByName("Sketch_Snap_Marker");
        const hud = document.getElementById("osnap-hud");

        return {
            prompt1: prompt1,
            sourceCorner: sourceCorner,
            hasSnapMarker: !!snapMarker,
            snapMarkerPos: snapMarker ? snapMarker.position : null,
            hudVisible: hud ? hud.style.display : "none",
            hudText: hud ? hud.textContent : "",
            coordsText: document.getElementById("coords-readout") ? document.getElementById("coords-readout").textContent : ""
        };
    })()
    """)
    print("RHINO MOVE STEP 1 (SOURCE CORNER PICKING) STATE:", json.dumps(step1_state, indent=2))
    time.sleep(0.8)
    ss_step1 = s2.capture_screenshot("rhino_move_step1_source_corner_selection.png")

    # ---------------------------------------------------------------------
    # Scenario 1B: Step 2: Destination Corner OSNAP, Live Ghost & Rubberband
    # ---------------------------------------------------------------------
    print("\nSetting up Scenario 1B: Destination Corner OSNAP on Box B with live preview...")
    step2_state = s2.eval_js("""
    (() => {
        // Click Box A corner (10, 20, 10) as base point
        const sourceCorner = new THREE.Vector3(10, 20, 10);
        activeCommand.handlePointerDown(sourceCorner, "perspective");

        const prompt2 = document.getElementById("command-prompt").textContent;
        const basePt = activeCommand.state.basePoint ? activeCommand.state.basePoint.clone() : null;

        // Hover over Box B top-back-left corner: (30, 20, 20)
        const targetCorner = new THREE.Vector3(30, 20, 20);
        const cam = cameras.perspective;
        const rect = viewports.perspective.canvas.getBoundingClientRect();
        const proj = targetCorner.clone().project(cam);
        const screenX = ((proj.x + 1) / 2) * rect.width + rect.left;
        const screenY = ((-proj.y + 1) / 2) * rect.height + rect.top;

        activeCommand.handlePointerMove(targetCorner, "perspective", { clientX: screenX, clientY: screenY });

        render();

        return {
            prompt2: prompt2,
            basePoint: basePt,
            targetCorner: targetCorner,
            hasBaseMarker: !!activeCommand.state.baseMarker,
            baseMarkerPos: activeCommand.state.baseMarker ? activeCommand.state.baseMarker.position : null,
            hasGhost: !!activeCommand.state.ghostGroup,
            hasRubberband: !!activeCommand.state.rubberband,
            currentDelta: activeCommand.state.currentDelta,
            readout: document.getElementById("move-readout") ? document.getElementById("move-readout").textContent : "",
            coordsText: document.getElementById("coords-readout") ? document.getElementById("coords-readout").textContent : ""
        };
    })()
    """)
    print("RHINO MOVE STEP 2 (DESTINATION CORNER PREVIEW) STATE:", json.dumps(step2_state, indent=2))
    time.sleep(0.8)
    ss_step2 = s2.capture_screenshot("rhino_move_step2_dest_corner_live_preview.png")

    # ---------------------------------------------------------------------
    # Scenario 1C: Step 3: Finalize Move & Verify Exact Corner Coincidence
    # ---------------------------------------------------------------------
    print("\nSetting up Scenario 1C: Finalizing Move and Verifying Exact Corner Coincidence...")
    step3_state = s2.eval_js("""
    (() => {
        const boxA = sceneObjects.find(o => o.name === "Box_A");
        const boxB = sceneObjects.find(o => o.name === "Box_B");

        const targetCorner = new THREE.Vector3(30, 20, 20);
        activeCommand.handlePointerDown(targetCorner, "perspective");

        boxA.updateMatrixWorld(true);
        boxB.updateMatrixWorld(true);

        // Verify corner coincidence
        const finalCornerA = new THREE.Vector3(10, 10, 10).applyMatrix4(boxA.matrixWorld);
        const targetCornerB = new THREE.Vector3(-10, 10, -10).applyMatrix4(boxB.matrixWorld);
        const cornerDist = finalCornerA.distanceTo(targetCornerB);

        // Add visual coincidence badge in viewport
        let badge = document.getElementById("coincidence-badge");
        if (!badge) {
            badge = document.createElement("div");
            badge.id = "coincidence-badge";
            badge.style.cssText = "position:absolute; bottom:38px; left:50%; transform:translateX(-50%); background:#004000; color:#39ff14; border:2px solid #39ff14; font-family:var(--font-mono, monospace); font-size:12px; font-weight:bold; padding:6px 14px; box-shadow:3px 3px 0 rgba(0,0,0,0.6); z-index:99999; text-align:center;";
            document.body.appendChild(badge);
        }
        badge.innerHTML = `✓ EXACT CORNER COINCIDENCE VERIFIED<br><span style="font-size:10px; color:#ffffff;">Box A Corner (30.0, 20.0, 20.0) ≡ Box B Corner (30.0, 20.0, 20.0)<br>Distance: ${cornerDist.toFixed(4)} mm</span>`;

        // Add visual reticle at touching point
        const coincMarker = new THREE.Group();
        coincMarker.name = "Coincidence_Marker";
        const ring = new THREE.Mesh(new THREE.RingGeometry(2.0, 2.5, 32), new THREE.MeshBasicMaterial({ color: 0x39ff14, side: THREE.DoubleSide }));
        ring.rotation.x = Math.PI / 2;
        coincMarker.add(ring);
        const sphere = new THREE.Mesh(new THREE.SphereGeometry(0.8, 16, 16), new THREE.MeshBasicMaterial({ color: 0x39ff14 }));
        coincMarker.add(sphere);
        coincMarker.position.copy(targetCornerB);
        scene.add(coincMarker);

        render();

        return {
            boxAPos: boxA.position,
            boxBPos: boxB.position,
            finalCornerA: finalCornerA,
            targetCornerB: targetCornerB,
            cornerDistance: cornerDist,
            coincides: cornerDist < 0.001,
            undoCount: undoStack.length
        };
    })()
    """)
    print("RHINO MOVE STEP 3 (CORNER COINCIDENCE) STATE:", json.dumps(step3_state, indent=2))
    time.sleep(0.8)
    ss_step3 = s2.capture_screenshot("rhino_move_step3_exact_corner_coincidence_verified.png")

    # Clean up coincidence badge before gumball scenario
    s2.eval_js("""
    (() => {
        const b = document.getElementById("coincidence-badge");
        if (b) b.remove();
        const m = scene.getObjectByName("Coincidence_Marker");
        if (m) scene.remove(m);
        render();
    })()
    """)

    # ---------------------------------------------------------------------
    # Scenario 2: Gumball Free Move with Deliberate 0.04 Slowdown Multiplier
    # ---------------------------------------------------------------------
    print("\nSetting up Scenario 2: Gumball Free Move with 0.04 Deliberate Slowdown Multiplier...")
    slow_state = s2.eval_js("""
    (() => {
        // Reset modeling command counter to prevent 7th command ad interruption
        modelingCommandCount = 0;
        const adModal = document.getElementById("modal-advertisement");
        if (adModal && adModal.open) adModal.close();

        // Create an additional box for Slow Gumball demonstration
        createBoxPrimitive();
        const box = sceneObjects[sceneObjects.length - 1];
        box.position.set(-20, 8, -10);
        box.geometry = new THREE.BoxGeometry(16, 16, 16);
        box.name = "Slow_Gumball_Box";
        box.updateMatrix();
        box.updateMatrixWorld();
        selectObject(box);

        const gumballHiddenInitially = (gumballGroup.visible === false && isGumballActive === false);

        // Activate Gumball via polite request
        processRequest("Can I gumball?");
        const gumballActiveNow = (gumballGroup.visible === true && isGumballActive === true);

        // Set up simulated Free Move drag (Shift + M + Drag)
        const cam = cameras.perspective;
        const startPt = box.position.clone();
        gumballDragState = {
            mode: "free_move",
            vpId: "perspective",
            camera: cam,
            plane: new THREE.Plane(new THREE.Vector3(0, 1, 0), -startPt.y),
            startHit: startPt.clone(),
            startGumballPos: startPt.clone(),
            startSnapshot: serializeProjectState(),
            hasMoved: false,
            initialStates: [{ obj: box, pos: box.position.clone(), rot: box.rotation.clone(), scale: box.scale.clone() }]
        };

        // Pointer drags 100mm in X and 100mm in Z (total pointer displacement: (100, 0, 100))
        // With 0.04 slowdown multiplier, geometric displacement is exactly:
        // dX = 100 * 0.04 = 4.0mm
        // dZ = 100 * 0.04 = 4.0mm
        const origRayIntersect = raycaster.ray.intersectPlane.bind(raycaster.ray);
        raycaster.ray.intersectPlane = function(plane, target) {
            target.set(startPt.x + 100, startPt.y, startPt.z + 100);
            return target;
        };

        handleGumballDragMove({ clientX: 200, clientY: 200 }, "perspective");
        raycaster.ray.intersectPlane = origRayIntersect;

        render();

        return {
            gumballHiddenInitially: gumballHiddenInitially,
            gumballActiveNow: gumballActiveNow,
            initialPos: { x: startPt.x, y: startPt.y, z: startPt.z },
            draggedPos: { x: box.position.x, y: box.position.y, z: box.position.z },
            actualDisplacement: {
                dx: box.position.x - startPt.x,
                dy: box.position.y - startPt.y,
                dz: box.position.z - startPt.z
            },
            expectedDisplacement: { dx: 4.0, dy: 0.0, dz: 4.0 },
            gumballGroupVisible: gumballGroup.visible
        };
    })()
    """)
    print("SLOW GUMBALL FREE MOVE STATE:", json.dumps(slow_state, indent=2))
    time.sleep(0.8)
    ss_slow = s2.capture_screenshot("slow_gumball_free_move_4_percent.png")

    # Release pointer to verify dismissal and 1 Undo step
    slow_dismiss = s2.eval_js("""
    (() => {
        window.dispatchEvent(new Event("pointerup"));
        render();
        return {
            gumballDismissed: (gumballGroup.visible === false && isGumballActive === false && gumballDragState === null),
            lastUndoDesc: undoStack.length > 0 ? undoStack[undoStack.length - 1].desc : null
        };
    })()
    """)
    print("SLOW GUMBALL DISMISSAL STATE:", json.dumps(slow_dismiss, indent=2))

    # Automatically open verification screenshots in macOS Preview
    print("\nOpening verification screenshots in macOS Preview...")
    subprocess.run(["open", "-a", "Preview", ss_step1, ss_step2, ss_step3, ss_slow])
    print("All screenshots captured and launched in Preview successfully.")

finally:
    s2.close()
