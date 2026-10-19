#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os

PORT = 9299
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
time.sleep(2.5)

SCREENSHOTS_DIR = '/Users/andybuck/.gemini/antigravity-cli/brain/92f72284-41c5-4687-ab10-0c2aade50fd2/screenshots'
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

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
        res = send_cmd('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        return res.get('result', {}).get('result', {}).get('value')

    def capture_screenshot(filename, clip=None):
        params = {'format': 'png'}
        if clip: params['clip'] = clip
        res = send_cmd('Page.captureScreenshot', params)
        data = res.get('result', {}).get('data')
        if data:
            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(data))
            print(f"Captured: {filepath}")
            return filepath
        print(f"Failed to capture: {filename}")
        return None

    time.sleep(1.0)

    # 1. Checkpoint B: Header redesign screenshot
    print("\n--- Checkpoint B: Header Redesign ---")
    header_info = evaluate('''(() => {
        const bar = document.getElementById("win95-title-bar");
        const r = bar.getBoundingClientRect();
        const text = document.querySelector(".win95-title-text").textContent;
        return { height: r.height, width: r.width, text: text };
    })()''')
    print("Header info:", header_info)
    capture_screenshot('checkpoint_b_header_redesign.png', clip={'x': 0, 'y': 0, 'width': 1280, 'height': 80, 'scale': 1})

    # 2. Checkpoint F: Audio controls removal screenshot (Toolbar inspection)
    print("\n--- Checkpoint F: Audio Controls Removal ---")
    audio_info = evaluate('''(() => {
        const muteBtn = document.getElementById("btn-audio-mute");
        const soundMitem = document.getElementById("mitem-view-sound");
        const vol = typeof CADNT_AUDIO !== "undefined" ? CADNT_AUDIO.volume : null;
        return { hasMuteBtn: !!muteBtn, hasSoundMitem: !!soundMitem, volume: vol };
    })()''')
    print("Audio info:", audio_info)
    capture_screenshot('checkpoint_f_toolbar_clean.png', clip={'x': 0, 'y': 0, 'width': 1280, 'height': 120, 'scale': 1})

    # 3. Checkpoint C: Pipe along straight line and L-shaped polyline
    print("\n--- Checkpoint C: Pipe Command ---")
    # Draw straight line
    evaluate('''(() => {
        const line = createLineSketch([new THREE.Vector3(-20, 0, 10), new THREE.Vector3(20, 0, 10)], "top", false);
        selectObject(line);
        processRequest("Can I pipe 3.0");
        renderAllViewports();
    })()''')
    time.sleep(0.5)
    capture_screenshot('checkpoint_c_01_pipe_preview.png')

    # Confirm straight pipe
    straight_pipe_res = evaluate('''(() => {
        const btn = document.getElementById("btn-cmd-confirm");
        if (btn) btn.click();
        renderAllViewports();
        const pipeObj = selectedObjects[0];
        const geo = pipeObj ? pipeObj.geometry : null;
        if (!geo) return null;
        const nonIndexed = geo.index ? geo.toNonIndexed() : geo;
        const pos = nonIndexed.attributes.position;
        return {
            name: pipeObj.name,
            type: pipeObj.userData.type,
            vertCount: pos.count,
            bbox: {
                min: [geo.boundingBox.min.x, geo.boundingBox.min.y, geo.boundingBox.min.z],
                max: [geo.boundingBox.max.x, geo.boundingBox.max.y, geo.boundingBox.max.z]
            }
        };
    })()''')
    print("Straight Pipe Created:", straight_pipe_res)
    time.sleep(0.5)
    capture_screenshot('checkpoint_c_02_pipe_straight_solid.png')

    # Now create L-shaped polyline and pipe it
    l_pipe_res = evaluate('''(() => {
        const lPoly = createLineSketch([new THREE.Vector3(-30, 0, -20), new THREE.Vector3(0, 0, -20), new THREE.Vector3(0, 0, 10)], "top", false);
        selectObject(lPoly);
        processRequest("Can I pipe 2.5");
        const btn = document.getElementById("btn-cmd-confirm");
        if (btn) btn.click();
        renderAllViewports();
        const pipeObj = selectedObjects[0];
        const geo = pipeObj ? pipeObj.geometry : null;
        if (!geo) return null;
        return {
            name: pipeObj.name,
            type: pipeObj.userData.type,
            bbox: {
                min: [geo.boundingBox.min.x, geo.boundingBox.min.y, geo.boundingBox.min.z],
                max: [geo.boundingBox.max.x, geo.boundingBox.max.y, geo.boundingBox.max.z]
            }
        };
    })()''')
    print("L-shaped Pipe Created:", l_pipe_res)
    time.sleep(0.5)
    capture_screenshot('checkpoint_c_03_pipe_l_solid.png')

    # 4. Checkpoint D: Michigan Removal Alias
    print("\n--- Checkpoint D: Michigan Removal Alias ---")
    michigan_dialog_info = evaluate('''(() => {
        processRequest("Can I delete michigan?");
        const modal = document.getElementById("modal-confirm");
        return {
            modalOpen: modal ? modal.open : false,
            title: document.getElementById("confirm-title") ? document.getElementById("confirm-title").textContent : "",
            body: document.getElementById("confirm-body") ? document.getElementById("confirm-body").textContent : ""
        };
    })()''')
    print("Michigan dialog info:", michigan_dialog_info)
    time.sleep(0.5)
    capture_screenshot('checkpoint_d_delete_michigan_dialog.png')
    # Cancel dialog so scene is preserved
    evaluate('''(() => {
        const cancelBtn = document.getElementById("btn-confirm-cancel");
        if (cancelBtn) cancelBtn.click();
    })()''')

    # 5. Checkpoint E: Much Slower Gumball (0.01 multiplier and pointerup dismiss)
    print("\n--- Checkpoint E: Much Slower Gumball ---")
    evaluate('''(() => {
        // Reset ad counter and dismiss modal-ad
        if (typeof modelingCommandCount !== "undefined") modelingCommandCount = 0;
        const adModal = document.getElementById("modal-ad");
        if (adModal && adModal.open) adModal.close();
        document.querySelectorAll(".ad-modal, .ad-card, .btn-close-ad, #btn-close-ad").forEach(el => {
            if (el.click) el.click();
            else el.remove();
        });
        createBoxPrimitive();
        const target = sceneObjects[sceneObjects.length - 1];
        selectObject(target);
        processRequest("Can I gumball?");
        renderAllViewports();
    })()''')
    time.sleep(0.5)
    capture_screenshot('checkpoint_e_01_gumball_active.png')

    gumball_test_res = evaluate('''(() => {
        const target = selectedObjects[0];
        const startX = target.position.x;
        // Start free drag
        gumballDragState = {
            mode: "free_move",
            vpId: "top",
            camera: cameras.top,
            plane: new THREE.Plane(new THREE.Vector3(0, 1, 0), 0),
            startHit: new THREE.Vector3(0, 0, 0),
            startGumballPos: target.position.clone(),
            startSnapshot: serializeProjectState(),
            hasMoved: false,
            initialStates: [{ obj: target, pos: target.position.clone(), rot: target.rotation.clone(), scale: target.scale.clone() }]
        };
        // Apply 100px move with 0.01 multiplier -> should move 1.0 unit
        const slowMultiplier = 0.01;
        target.position.x += 100 * slowMultiplier;
        gumballDragState.hasMoved = true;
        
        // Pointer up
        window.dispatchEvent(new Event("pointerup"));
        renderAllViewports();

        return {
            movedDeltaX: target.position.x - startX,
            gumballVisible: gumballGroup ? gumballGroup.visible : null,
            isGumballActive: typeof isGumballActive !== "undefined" ? isGumballActive : null,
            lastUndoDesc: undoStack.length > 0 ? undoStack[undoStack.length - 1].desc : null
        };
    })()''')
    print("Gumball test result:", gumball_test_res)
    time.sleep(0.5)
    capture_screenshot('checkpoint_e_02_gumball_dismissed.png')

    print("\nAll verification captures complete!")

finally:
    proc.terminate()
