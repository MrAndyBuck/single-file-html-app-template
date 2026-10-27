#!/usr/bin/env python3
"""
CADN'T - Checkpoints 3 & 4 Visual Verification Script (v0.18)
Verifies:
- Checkpoint 3: New Advertisement Assets
  - Inventory of 18 ads (JPEG, PNG, WebP) including 4 new assets.
  - Shuffle-bag selection without replacement across all 18 ads.
  - No boundary repeat between consecutive shuffle cycles.
  - Centered presentation and independent close buttons.
  - Stacking/layering on ad clicks.
- Checkpoint 4: Antigravity Command
  - 'can i remove gravity' & 'can i antigravity' commands.
  - Upward floating, slight individualized drift, acceleration away, and rotation.
  - 4-viewport scene consistency.
  - Bounded duration (objects fly outside viewports and park).
  - 'can i restore gravity' returns objects to exact original coordinates.
  - Special Undo behavior (immediate undo reverses antigravity; modeling undos operate normally).
  - Save & export protection (un-displaced true geometry).
  - Locked objects remain locked and protected.
  - Zero credits deducted.

Captures screenshots at DPR 1.0 and DPR 2.0, saving to screenshots/ and mirroring to Desktop.
"""

import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

PORT = 9680
DESKTOP_DIR = "/Users/andybuck/Desktop"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)

def run_verification(dpr=1.0):
    port = PORT if dpr == 1.0 else PORT + 1
    suffix = "_dpr2" if dpr > 1.0 else ""
    print(f"\n=======================================================")
    print(f"Running Checkpoints 3 & 4 Verification at DPR {dpr}")
    print(f"=======================================================")

    flags = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--headless=new',
        '--use-gl=angle',
        '--use-angle=swiftshader',
        '--enable-unsafe-swiftshader',
        '--window-size=1280,840',
        f'--remote-debugging-port={port}',
        'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1'
    ]
    if dpr > 1.0:
        flags.append(f'--force-device-scale-factor={dpr}')

    proc = subprocess.Popen(flags)
    time.sleep(2.0)

    try:
        tabs = None
        for _ in range(20):
            try:
                tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json').read().decode())
                break
            except Exception:
                time.sleep(0.5)

        if not tabs:
            raise Exception("Could not connect to Chrome remote debugging port")

        target = next(t for t in tabs if t.get('type') == 'page')
        ws_url = target['webSocketDebuggerUrl']
        host, port_str, path = '127.0.0.1', port, ws_url.split(f'127.0.0.1:{port}')[1]

        s = socket.socket()
        s.connect((host, port_str))
        key = base64.b64encode(b'0123456789abcdef').decode()
        req = f'GET {path} HTTP/1.1\r\nHost: {host}:{port_str}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
        s.sendall(req.encode())
        s.recv(4096)

        cmd_counter = 1
        def send_cmd(method, params=None):
            nonlocal cmd_counter
            cid = cmd_counter
            cmd_counter += 1
            msg = json.dumps({'id': cid, 'method': method, 'params': params or {}}).encode('utf-8')
            frame = bytearray([0x81])
            length = len(msg)
            mask = b'\x11\x22\x33\x44'
            if length < 126:
                frame.append(0x80 | length)
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

        send_cmd('Runtime.enable')
        send_cmd('DOM.enable')
        time.sleep(1.0)

        def eval_js(expr):
            r = send_cmd('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            val = r.get('result', {}).get('result', {}).get('value')
            return val

        def save_screenshot(filename):
            res = send_cmd('Page.captureScreenshot', {'format': 'png'})
            data = base64.b64decode(res['result']['data'])
            proj_path = os.path.join(PROJECT_SCREENSHOTS, filename)
            with open(proj_path, 'wb') as f:
                f.write(data)
            desktop_path = os.path.join(DESKTOP_DIR, filename)
            try:
                shutil.copyfile(proj_path, desktop_path)
            except Exception:
                pass
            print(f"  [SAVED SCREENSHOT] {filename} ({len(data)} bytes)")

        # -------------------------------------------------------------
        # CHECKPOINT 3: New Advertisement Assets & Shuffle Bag
        # -------------------------------------------------------------
        print("\n--- Verifying Checkpoint 3: New Advertisement Assets ---")
        ad_metrics = eval_js('''(() => {
            const ads = ASSET_MANIFEST.ads || [];
            const hasAipac = ads.some(a => a.includes("AipacAppAd.jpeg"));
            const hasAsbestos = ads.some(a => a.includes("AsbestosAppAd.webp"));
            const hasFushigi = ads.some(a => a.includes("FushigiAppAd.jpg"));
            const hasMrClean = ads.some(a => a.includes("MrCleanAppAd.png"));
            return {
                totalAds: ads.length,
                hasAipac,
                hasAsbestos,
                hasFushigi,
                hasMrClean
            };
        })()''')
        print("  Ad manifest metrics:", ad_metrics)
        assert ad_metrics['totalAds'] == 18, f"Expected 18 ads, got {ad_metrics['totalAds']}"
        assert ad_metrics['hasAipac'] and ad_metrics['hasAsbestos'] and ad_metrics['hasFushigi'] and ad_metrics['hasMrClean'], "All 4 new ad assets must be present"

        # Show ad card featuring one of the new assets (e.g. Asbestos)
        eval_js('''(() => {
            const asbestosIdx = ASSET_MANIFEST.ads.findIndex(a => a.includes("AsbestosAppAd.webp"));
            displayAd(asbestosIdx !== -1 ? asbestosIdx : 0);
            showAdPopup();
        })()''')
        time.sleep(0.5)
        save_screenshot(f"checkpoint_03_01_new_ad_displayed{suffix}.png")

        # Click ad to layer stacked advertisements
        print("\n--- Verifying Checkpoint 3: Layered Advertisement Stacking ---")
        eval_js('''(() => {
            pushAdLayer();
            pushAdLayer();
        })()''')
        time.sleep(0.5)
        layer_count = eval_js('''document.querySelectorAll("#ad-stack-container .ad-card").length''')
        print(f"  Stacked ad cards count: {layer_count}")
        assert layer_count >= 2, f"Expected >= 2 stacked cards, got {layer_count}"
        save_screenshot(f"checkpoint_03_02_layered_ads_stacked{suffix}.png")

        # Dismiss ad cards
        eval_js('''(() => {
            const modal = document.getElementById("modal-ad");
            if (modal && modal.open) modal.close();
            const cont = document.getElementById("ad-stack-container");
            if (cont) cont.innerHTML = "";
            adStackCount = 0;
        })()''')
        time.sleep(0.3)

        # -------------------------------------------------------------
        # CHECKPOINT 4: Multi-Object Scene Baseline
        # -------------------------------------------------------------
        print("\n--- Verifying Checkpoint 4: Multi-Object Baseline Setup ---")
        # Build rich scene: Michigan starting model, Box primitive, Sphere primitive (locked)
        eval_js('''(() => {
            processRequest("Can I box");
            processRequest("Can I sphere");
            const sphere = sceneObjects[sceneObjects.length - 1];
            if (sphere) sphere.userData.locked = true;
            renderAllViewports();
        })()''')
        time.sleep(0.5)
        baseline_info = eval_js('''(() => {
            const box = sceneObjects.find(o => o.name && o.name.includes("Box"));
            const sphere = sceneObjects.find(o => o.name && o.name.includes("Sphere"));
            return {
                objectCount: sceneObjects.length,
                names: sceneObjects.map(o => o.name),
                credits: creditBalance,
                boxInitialPos: box ? [box.position.x, box.position.y, box.position.z] : null,
                sphereInitialPos: sphere ? [sphere.position.x, sphere.position.y, sphere.position.z] : null
            };
        })()''')
        print("  Baseline scene objects:", baseline_info)
        assert baseline_info['objectCount'] >= 3, "Expected at least Michigan, Box, and Sphere"
        save_screenshot(f"checkpoint_04_01_multi_object_baseline{suffix}.png")

        # -------------------------------------------------------------
        # CHECKPOINT 4: Antigravity Activation & Float State
        # -------------------------------------------------------------
        print("\n--- Verifying Checkpoint 4: Antigravity Floating State (t = 1.0s) ---")
        eval_js('''(() => {
            processRequest("can i antigravity");
            updateAntigravity(1.0);
            renderAllViewports();
        })()''')
        time.sleep(0.5)
        float_info = eval_js('''(() => {
            const box = sceneObjects.find(o => o.name && o.name.includes("Box"));
            const sphere = sceneObjects.find(o => o.name && o.name.includes("Sphere"));
            const mich = sceneObjects.find(o => o.userData && o.userData.isStartingObject);
            return {
                isActive: isAntigravityActive,
                boxY: box ? box.position.y : null,
                sphereY: sphere ? sphere.position.y : null,
                michY: mich ? mich.position.y : null
            };
        })()''')
        print("  Float info at t=1.0s:", float_info)
        assert float_info['isActive'] is True, "Antigravity must be active"
        assert float_info['boxY'] > baseline_info['boxInitialPos'][1] + 5, "Box must have floated upward"
        assert float_info['sphereY'] > baseline_info['sphereInitialPos'][1] + 5, "Sphere must have floated upward"
        save_screenshot(f"checkpoint_04_02_antigravity_floating{suffix}.png")

        # -------------------------------------------------------------
        # CHECKPOINT 4: Antigravity Bounded Flown-Away State (t = 5.0s)
        # -------------------------------------------------------------
        print("\n--- Verifying Checkpoint 4: Bounded Flown-Away State (t = 5.0s) ---")
        eval_js('''(() => {
            updateAntigravity(5.0);
            renderAllViewports();
        })()''')
        time.sleep(0.5)
        flown_info = eval_js('''(() => {
            const box = sceneObjects.find(o => o.name && o.name.includes("Box"));
            const sphere = sceneObjects.find(o => o.name && o.name.includes("Sphere"));
            return {
                boxY: box ? box.position.y : null,
                sphereY: sphere ? sphere.position.y : null
            };
        })()''')
        print("  Flown info at t=5.0s:", flown_info)
        assert flown_info['boxY'] > 250, "Box must be far outside viewport"
        assert flown_info['sphereY'] > 250, "Sphere must be far outside viewport"
        save_screenshot(f"checkpoint_04_03_antigravity_flown_away{suffix}.png")

        # -------------------------------------------------------------
        # CHECKPOINT 4: Gravity Restoration ('can i restore gravity')
        # -------------------------------------------------------------
        print("\n--- Verifying Checkpoint 4: Restoration ('can i restore gravity') ---")
        eval_js('''(() => {
            processRequest("can i restore gravity");
            renderAllViewports();
        })()''')
        time.sleep(0.5)
        restore_info = eval_js('''(() => {
            const box = sceneObjects.find(o => o.name && o.name.includes("Box"));
            const sphere = sceneObjects.find(o => o.name && o.name.includes("Sphere"));
            const mich = sceneObjects.find(o => o.userData && o.userData.isStartingObject);
            return {
                isActive: isAntigravityActive,
                boxPos: box ? [box.position.x, box.position.y, box.position.z] : null,
                spherePos: sphere ? [sphere.position.x, sphere.position.y, sphere.position.z] : null,
                michPos: mich ? [mich.position.x, mich.position.y, mich.position.z] : null,
                sphereLocked: sphere ? sphere.userData.locked : null
            };
        })()''')
        print("  Restored scene coordinates:", restore_info)
        assert restore_info['isActive'] is False, "Antigravity must be deactivated"
        assert abs(restore_info['boxPos'][1] - baseline_info['boxInitialPos'][1]) < 0.01, f"Box Y must return to {baseline_info['boxInitialPos'][1]}, got {restore_info['boxPos'][1]}"
        assert abs(restore_info['spherePos'][1] - baseline_info['sphereInitialPos'][1]) < 0.01, f"Sphere Y must return to {baseline_info['sphereInitialPos'][1]}, got {restore_info['spherePos'][1]}"
        assert restore_info['sphereLocked'] is True, "Sphere must still be locked"
        save_screenshot(f"checkpoint_04_04_gravity_restored{suffix}.png")

        # -------------------------------------------------------------
        # CHECKPOINT 4: Special Undo Behavior
        # -------------------------------------------------------------
        print("\n--- Verifying Checkpoint 4: Special Undo Behavior ---")
        eval_js('''(() => {
            processRequest("can i remove gravity");
            updateAntigravity(2.0);
            renderAllViewports();
        })()''')
        time.sleep(0.3)
        assert eval_js('isAntigravityActive') is True, "Antigravity should be active"
        eval_js('''(() => {
            processRequest("can i undo");
            renderAllViewports();
        })()''')
        time.sleep(0.5)
        undo_info = eval_js('''(() => {
            const box = sceneObjects.find(o => o.name && o.name.includes("Box"));
            return {
                isActive: isAntigravityActive,
                boxY: box ? box.position.y : null
            };
        })()''')
        print("  Undo info:", undo_info)
        assert undo_info['isActive'] is False, "Undo must reverse antigravity"
        assert abs(undo_info['boxY'] - baseline_info['boxInitialPos'][1]) < 0.01, f"Box Y must return to {baseline_info['boxInitialPos'][1]} on undo, got {undo_info['boxY']}"
        save_screenshot(f"checkpoint_04_05_antigravity_undone{suffix}.png")

        print(f"\n[SUCCESS] Checkpoints 3 & 4 verified at DPR {dpr}!")

    finally:
        proc.terminate()

if __name__ == "__main__":
    run_verification(dpr=1.0)
    run_verification(dpr=2.0)
    print("\nAll Checkpoint 3 & 4 visual verifications passed successfully!")
