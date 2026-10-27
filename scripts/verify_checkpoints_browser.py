#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, sys

PORT = 9301
SCREENSHOT_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

chrome_proc = subprocess.Popen([
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless=new',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    '--window-size=1280,800',
    f'--remote-debugging-port={PORT}',
    'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1'
])

time.sleep(1.2)

try:
    tabs = None
    for _ in range(20):
        try:
            tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json').read().decode())
            break
        except Exception:
            time.sleep(0.4)
    if not tabs:
        raise Exception("Could not connect to Chrome debugging port")
    target = next(t for t in tabs if t.get('type') == 'page')
    ws_url = target['webSocketDebuggerUrl']
    host, port, path = '127.0.0.1', PORT, ws_url.split(f'127.0.0.1:{PORT}')[1]
    s = socket.socket()
    s.connect((host, port))
    key = base64.b64encode(b'0123456789abcdef').decode()
    req = f'GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
    s.sendall(req.encode())
    s.recv(4096)

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

    def evaluate(expr, await_promise=False):
        res = send_cmd('Runtime.evaluate', {
            'expression': expr,
            'awaitPromise': await_promise,
            'returnByValue': True
        })
        if 'exceptionDetails' in res.get('result', {}):
            raise Exception("JS Exception: " + json.dumps(res['result']['exceptionDetails']))
        return res.get('result', {}).get('result', {}).get('value')

    def capture_screenshot(filename):
        res = send_cmd('Page.captureScreenshot', {'format': 'png'})
        data = res['result']['data']
        path = os.path.join(SCREENSHOT_DIR, filename)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(data))
        print(f"Captured screenshot: {filename} ({len(data)} bytes)")

    # Wait for page readiness
    print("Waiting for CADN'T initialization...")
    for _ in range(20):
        time.sleep(0.5)
        ready = evaluate("typeof APP !== 'undefined' && typeof window.COMMAND_REGISTRY !== 'undefined'")
        if ready: break

    app_ver = evaluate("typeof APP !== 'undefined' ? APP.version : 'unknown'")
    print("CADN'T ready! App version:", app_ver)

    # =========================================================================
    # CHECKPOINT A: All 18 Advertisements Verification
    # =========================================================================
    print("\n--- CHECKPOINT A: VERIFYING ALL 18 ADVERTISEMENTS ---")
    ad_load_results = evaluate("window.testAllAdsLoading()", await_promise=True)
    print(f"testAllAdsLoading returned {len(ad_load_results)} items.")
    assert len(ad_load_results) == 18, f"Expected 18 ads, got {len(ad_load_results)}"
    assert all(r['loaded'] is True for r in ad_load_results), "Some ads failed to load!"
    assert all(r['width'] > 0 and r['height'] > 0 for r in ad_load_results), "Some ads have invalid dimensions!"
    print("All 18 ad images successfully loaded in browser with non-zero dimensions!")

    ad_cycle_results = evaluate("window.runAdCycleTest()", await_promise=False)
    print("runAdCycleTest result:", json.dumps(ad_cycle_results, indent=2))
    assert ad_cycle_results['success'] == True, "Ad cycle test failed!"
    assert ad_cycle_results['cycle1UniqueCount'] == 18, "Did not get 18 distinct ads in cycle!"
    assert ad_cycle_results['zeroRepeats'] == True, "Repeats detected in cycle!"
    assert ad_cycle_results['noBoundaryRepeat'] == True, "Boundary repeat detected between cycles!"
    assert ad_cycle_results['allNewFilesIncluded'] == True, "Not all 4 new ads included in cycle!"
    print("Ad cycle test verified: exactly 18 unique ads, zero repeats in cycle, no boundary repeat, all 4 new ads included!")

    inventory_md = evaluate("window.getAdAssetInventoryTable()", await_promise=False)
    print("\nAD ASSET INVENTORY TABLE:")
    print(inventory_md)
    with open("scratch/ad_asset_inventory.md", "w") as f:
        f.write(inventory_md)

    # Display Ad showing new asset MrCleanAppAd.png (index 11)
    evaluate("window.showAdPopup(11)")
    time.sleep(0.5)
    capture_screenshot("checkpoint_A_01_new_ad_mrclean.png")

    # Stack layered ad on top (index 4: AsbestosAppAd.webp)
    evaluate("window.pushAdLayer(4)")
    time.sleep(0.5)
    capture_screenshot("checkpoint_A_02_layered_stacked_ads.png")

    # Dismiss ads
    evaluate("const m = document.getElementById('modal-ad'); if (m && m.open) m.close(); const s = document.getElementById('ad-stack-container'); if (s) s.innerHTML = '';")

    # =========================================================================
    # CHECKPOINT B: Complete Help Command Reference Verification
    # =========================================================================
    print("\n--- CHECKPOINT B: VERIFYING COMPLETE HELP COMMAND REFERENCE ---")
    evaluate("window.openHelpWindow()")
    time.sleep(0.5)

    help_visible = evaluate("document.getElementById('modal-help').open === true")
    cubert_open = evaluate("cubertMode === CUBERT_MODES.ACTIVE && document.getElementById('cubert-popup').style.display === 'flex'")
    print(f"Help visible: {help_visible}, Cubert beside Help: {cubert_open}")
    assert help_visible, "Help modal not open!"
    assert cubert_open, "Cubert not summoned beside Help!"
    capture_screenshot("checkpoint_B_01_help_window_cubert_beside.png")

    # Search for antigravity in Help
    evaluate("""(() => {
    const input = document.getElementById('help-search');
    input.value = 'antigravity';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    })()""")
    time.sleep(0.4)
    antigravity_count = evaluate("document.querySelectorAll('#help-list .help-card').length")
    print(f"Help search 'antigravity' matches: {antigravity_count}")
    capture_screenshot("checkpoint_B_02_help_search_antigravity.png")

    # Search for chinese in Help
    evaluate("""(() => {
    const input = document.getElementById('help-search');
    input.value = 'chinese';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    })()""")
    time.sleep(0.4)
    chinese_count = evaluate("document.querySelectorAll('#help-list .help-card').length")
    print(f"Help search 'chinese' matches: {chinese_count}")
    capture_screenshot("checkpoint_B_03_help_search_chinese.png")

    # Close Help
    evaluate("window.closeHelpWindow(); if (typeof hideCubertPopup === 'function') hideCubertPopup();")
    time.sleep(0.3)
    help_closed = evaluate("document.getElementById('modal-help').open === false")
    print("Help closed successfully:", help_closed)
    assert help_closed, "Help modal failed to close!"

    # =========================================================================
    # CHECKPOINT C: Antigravity Is Not Recognized & Full Behavior Verification
    # =========================================================================
    print("\n--- CHECKPOINT C: VERIFYING ANTIGRAVITY COMMAND & BEHAVIOR ---")

    # Setup 3 separate primitives with distinct positions
    evaluate("""(() => {
    createBoxPrimitive();
    const b = sceneObjects[sceneObjects.length - 1];
    b.position.set(-25, 10, 0);

    createSpherePrimitive();
    const s = sceneObjects[sceneObjects.length - 1];
    s.position.set(0, 15, -20);
    s.userData.locked = true; // Locked to prevent escaping sphere drift and verify locked object participation

    createCylinderPrimitive();
    const c = sceneObjects[sceneObjects.length - 1];
    c.position.set(25, 10, 15);

    renderAllViewports();
    })()""")
    time.sleep(0.5)

    baseline_coords = evaluate("""
    sceneObjects.map(o => ({
      name: o.name,
      pos: { x: o.position.x, y: o.position.y, z: o.position.z },
      rot: { x: o.rotation.x, y: o.rotation.y, z: o.rotation.z }
    }))
    """)
    print("Baseline object count:", len(baseline_coords))
    capture_screenshot("checkpoint_C_01_primitives_baseline.png")

    # Setup MediaRecorder in page for composite 4-viewport recording
    evaluate("""
    window.__RECORDED_CHUNKS__ = [];
    window.__RECORDING_ERROR__ = null;
    try {
      const compCanvas = document.createElement('canvas');
      compCanvas.width = 800;
      compCanvas.height = 600;
      const ctx = compCanvas.getContext('2d');

      const topC = document.getElementById('canvas-top');
      const perspC = document.getElementById('canvas-perspective');
      const frontC = document.getElementById('canvas-front');
      const rightC = document.getElementById('canvas-right');

      function drawComposite() {
        try {
          ctx.drawImage(topC, 0, 0, 400, 300);
          ctx.drawImage(perspC, 400, 0, 400, 300);
          ctx.drawImage(frontC, 0, 300, 400, 300);
          ctx.drawImage(rightC, 400, 300, 400, 300);
        } catch (e) {}
      }

      const stream = compCanvas.captureStream(30);
      const mime = (typeof MediaRecorder !== 'undefined' && MediaRecorder.isTypeSupported('video/webm;codecs=vp8')) ? 'video/webm;codecs=vp8' : 'video/webm';
      if (typeof MediaRecorder !== 'undefined') {
        window.__MEDIA_RECORDER__ = new MediaRecorder(stream, { mimeType: mime });
        window.__MEDIA_RECORDER__.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) window.__RECORDED_CHUNKS__.push(e.data);
        };
        window.__MEDIA_RECORDER__.start(50);
      }

      window.__COMP_INTERVAL__ = setInterval(() => {
        drawComposite();
      }, 1000 / 30);
    } catch (err) {
      window.__RECORDING_ERROR__ = err.message;
    }
    """)

    # Fire antigravity command
    print("Executing 'can i antigravity'...")
    evaluate("processRequest('can i antigravity')")
    antigravity_active = evaluate("isAntigravityActive === true")
    print("isAntigravityActive:", antigravity_active)
    assert antigravity_active, "Antigravity failed to activate!"

    # Capture sequential frames of motion
    time.sleep(0.5)
    capture_screenshot("checkpoint_C_02_antigravity_floating_t0_5.png")

    time.sleep(0.5)
    capture_screenshot("checkpoint_C_02_antigravity_floating_t1_0.png")
    t1_y = evaluate("sceneObjects.map(o => o.position.y)")
    print("Positions Y at t=1.0s:", t1_y)

    time.sleep(0.5)
    capture_screenshot("checkpoint_C_02_antigravity_floating_t1_5.png")

    time.sleep(0.5)
    capture_screenshot("checkpoint_C_02_antigravity_floating_t2_0.png")

    time.sleep(1.0)
    capture_screenshot("checkpoint_C_03_antigravity_floating_t3_0.png")
    t3_y = evaluate("sceneObjects.map(o => o.position.y)")
    print("Positions Y at t=3.0s:", t3_y)

    time.sleep(1.0)
    capture_screenshot("checkpoint_C_03_antigravity_floating_t4_0.png")

    time.sleep(1.2)
    capture_screenshot("checkpoint_C_04_antigravity_flown_away_t5_0.png")
    t5_y = evaluate("sceneObjects.map(o => o.position.y)")
    print("Positions Y at t=5.0s:", t5_y)

    # Stop MediaRecorder and retrieve video
    evaluate("""
    if (window.__COMP_INTERVAL__) clearInterval(window.__COMP_INTERVAL__);
    if (window.__MEDIA_RECORDER__ && window.__MEDIA_RECORDER__.state !== 'inactive') {
      window.__MEDIA_RECORDER__.stop();
    }
    """)
    time.sleep(0.5)

    has_video = evaluate("window.__RECORDED_CHUNKS__ && window.__RECORDED_CHUNKS__.length > 0")
    print("Video chunks recorded:", has_video)
    if has_video:
        video_base64 = evaluate("""
        new Promise(resolve => {
          const blob = new Blob(window.__RECORDED_CHUNKS__, { type: 'video/webm' });
          const reader = new FileReader();
          reader.onloadend = () => {
            const b64 = reader.result.split(',')[1];
            resolve(b64);
          };
          reader.readAsDataURL(blob);
        })
        """, await_promise=True)
        video_path = os.path.join(SCREENSHOT_DIR, "antigravity_motion.webm")
        with open(video_path, "wb") as f:
            f.write(base64.b64decode(video_base64))
        print(f"Saved real browser motion recording: {video_path} ({os.path.getsize(video_path)} bytes)")

    # Restore gravity
    print("\nExecuting 'can i restore gravity'...")
    evaluate("processRequest('can i restore gravity')")
    time.sleep(0.5)
    capture_screenshot("checkpoint_C_05_gravity_restored.png")

    restored_coords = evaluate("""
    sceneObjects.map(o => ({
      name: o.name,
      pos: { x: o.position.x, y: o.position.y, z: o.position.z },
      rot: { x: o.rotation.x, y: o.rotation.y, z: o.rotation.z }
    }))
    """)

    # Verify exact coordinate restoration
    print("Comparing baseline vs restored coordinates:")
    max_diff = 0
    for orig, rest in zip(baseline_coords, restored_coords):
        dx = abs(orig['pos']['x'] - rest['pos']['x'])
        dy = abs(orig['pos']['y'] - rest['pos']['y'])
        dz = abs(orig['pos']['z'] - rest['pos']['z'])
        diff = max(dx, dy, dz)
        if diff > max_diff: max_diff = diff
        print(f"  {orig['name']}: orig ({orig['pos']['x']}, {orig['pos']['y']}, {orig['pos']['z']}) -> restored ({rest['pos']['x']}, {rest['pos']['y']}, {rest['pos']['z']}) | diff: {diff}")
    assert max_diff < 0.001, f"Coordinates not restored! Max diff: {max_diff}"
    print(f"Coordinates 100% verified restored! (Max diff: {max_diff})")

    # Test second alias: 'can i remove gravity'
    print("\nTesting second alias 'can i remove gravity'...")
    evaluate("processRequest('can i remove gravity')")
    assert evaluate("isAntigravityActive === true"), "Second alias failed to activate antigravity!"
    time.sleep(0.5)

    # Test undo
    print("Testing 'can i undo' to reverse antigravity...")
    evaluate("processRequest('can i undo')")
    assert evaluate("isAntigravityActive === false"), "Undo failed to stop antigravity!"
    capture_screenshot("checkpoint_C_06_antigravity_undone.png")

    undone_coords = evaluate("""
    sceneObjects.map(o => ({
      name: o.name,
      pos: { x: o.position.x, y: o.position.y, z: o.position.z }
    }))
    """)
    for orig, und in zip(baseline_coords, undone_coords):
        diff = max(abs(orig['pos']['x'] - und['pos']['x']), abs(orig['pos']['y'] - und['pos']['y']), abs(orig['pos']['z'] - und['pos']['z']))
        assert diff < 0.001, f"Undo did not restore coordinates! Diff: {diff}"
    print("Undo verified: all object coordinates restored!")

    # Test protection of native saved files and STL/OBJ export
    print("\nTesting geometry serialization & export protection during antigravity...")
    evaluate("processRequest('can i antigravity')")
    time.sleep(1.0)
    serialized = evaluate("serializeProjectState()")
    if isinstance(serialized, str):
        serialized = json.loads(serialized)
    evaluate("processRequest('can i restore gravity')")
    
    # Verify coordinates in serialized state match un-displaced baseline
    deserialized_boxes = [o for o in serialized.get('objects', []) if 'Box' in o.get('name', '')]
    if deserialized_boxes:
        box_pos = deserialized_boxes[0]['position']
        orig_box = [o for o in baseline_coords if 'Box' in o['name']][0]['pos']
        pos_diff = max(abs(box_pos[0] - orig_box['x']), abs(box_pos[1] - orig_box['y']), abs(box_pos[2] - orig_box['z']))
        print(f"Serialized baseline difference: {pos_diff}")
        assert pos_diff < 0.001, "Serialized state captured temporary displacement instead of true geometry!"
        print("Project serialization protection verified!")

    print("\nALL VERIFICATIONS PASSED WITH FLYING COLORS!")

finally:
    chrome_proc.terminate()
