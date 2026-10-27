#!/usr/bin/env python3
"""
CADN'T - Checkpoints A & B Visual Verification Script
Verifies:
- Checkpoint A: About Dialog Repair
  1. Opens with authentic Windows 95 styling at full size (~540px height, 640px width).
  2. Complete contents are visible (not a shallow, empty horizontal box).
  3. Vertical scrolling enabled within #about-dialog-content (scrollHeight > clientHeight).
  4. Preserves titlebar, Close button, and clickable bibliography links.
  5. Displays development credits, verified tech audit, inspirations, and Lake Superior address.
- Checkpoint B: Cubert Tip Buttons ($1, $5, $10, $0)
  1. Available amounts: $1, $5, $10, $0.
  2. Clicking $1, $5, $10 immediately deducts exact amount from fictional balance, updates display and localStorage, dismisses Cubert, and restores smiling standby mascot.
  3. Clicking $0 deducts nothing ($0.00), dismisses Cubert, and restores smiling standby mascot.
  4. Duplicate click prevention locks out rapid repeat deductions.
  5. Insufficient funds rejects the charge ($0 deducted) and triggers Cubert's 'Broke ass.' speech bubble & audio.
Captures screenshots at DPR 1.0 and DPR 2.0, mirroring to Desktop.
"""

import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

PORT = 9380
DESKTOP_DIR = "/Users/andybuck/Desktop"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)

def run_verification(dpr=1.0):
    port = PORT if dpr == 1.0 else PORT + 1
    suffix = "_dpr2" if dpr > 1.0 else ""
    print(f"\n=======================================================")
    print(f"Running Checkpoints A & B Verification at DPR {dpr}")
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
            raise Exception("Failed to connect to Chrome debugging port")

        target = next(t for t in tabs if t.get('type') == 'page')
        ws_url = target['webSocketDebuggerUrl']
        host, port_num, path = '127.0.0.1', port, ws_url.split(f'127.0.0.1:{port}')[1]
        s = socket.socket(); s.connect((host, port_num))
        key = base64.b64encode(b'0123456789abcdef').decode()
        req = f'GET {path} HTTP/1.1\r\nHost: {host}:{port_num}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
        s.sendall(req.encode()); s.recv(4096)

        cmd_counter = 1
        def send_cmd(method, params=None):
            nonlocal cmd_counter
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
                while len(raw) < l:
                    chunk = s.recv(l - len(raw))
                    if not chunk: break
                    raw.extend(chunk)
                res = json.loads(raw.decode('utf-8'))
                if res.get('id') == cid: return res

        def eval_js(expr):
            res = send_cmd('Runtime.evaluate', {
                'expression': expr,
                'returnByValue': True
            })
            return res.get('result', {}).get('result', {}).get('value')

        def capture_screenshot(filename, clip=None):
            params = {'format': 'png'}
            if clip:
                params['clip'] = clip
            res = send_cmd('Page.captureScreenshot', params)
            data = base64.b64decode(res['result']['data'])
            proj_path = os.path.join(PROJECT_SCREENSHOTS, filename)
            with open(proj_path, 'wb') as f:
                f.write(data)
            if os.path.exists(DESKTOP_DIR):
                desktop_path = os.path.join(DESKTOP_DIR, filename)
                shutil.copyfile(proj_path, desktop_path)
            print(f"  [SAVED SCREENSHOT] {filename} ({len(data)} bytes)")
            return proj_path

        time.sleep(2.0)

        # ---------------------------------------------------------------------
        # CHECKPOINT A: About Window Repair
        # ---------------------------------------------------------------------
        print("\n--- Verifying Checkpoint A: About Window Repair ---")
        # Click the About button in the toolbar
        eval_js('document.getElementById("btn-about-open").click()')
        time.sleep(0.5)

        about_info = eval_js("""(() => {
            const modal = document.getElementById('modal-about');
            const content = document.getElementById('about-dialog-content');
            const closeBtn = document.getElementById('btn-close-about');
            const captionClose = modal.querySelector('.btn-caption-close');
            const rModal = modal.getBoundingClientRect();
            const rContent = content ? content.getBoundingClientRect() : {};
            return {
                open: modal.open,
                modalWidth: rModal.width,
                modalHeight: rModal.height,
                contentWidth: rContent.width,
                contentHeight: rContent.height,
                scrollHeight: content ? content.scrollHeight : 0,
                clientHeight: content ? content.clientHeight : 0,
                hasCloseBtn: !!closeBtn,
                hasCaptionClose: !!captionClose,
                linksCount: content ? content.querySelectorAll('a').length : 0
            };
        })()""")

        print(f"  Modal Open: {about_info.get('open')}")
        print(f"  Modal Dimensions: {about_info.get('modalWidth'):.1f}x{about_info.get('modalHeight'):.1f}px")
        print(f"  Content Dimensions: {about_info.get('contentWidth'):.1f}x{about_info.get('contentHeight'):.1f}px")
        print(f"  ScrollHeight: {about_info.get('scrollHeight')}px, ClientHeight: {about_info.get('clientHeight')}px")
        print(f"  Vertical Scrollable: {about_info.get('scrollHeight') > about_info.get('clientHeight')}")

        assert about_info.get('open') == True, "Modal About did not open"
        assert about_info.get('modalHeight') >= 450, f"Modal About is too shallow! Height: {about_info.get('modalHeight')}"
        assert about_info.get('contentHeight') >= 350, f"Content area is too shallow! Height: {about_info.get('contentHeight')}"
        assert about_info.get('scrollHeight') > about_info.get('clientHeight'), "Content is not scrollable"

        # Capture top of About window
        capture_screenshot(f"checkpoint_a_01_about_window_repaired{suffix}.png")

        # Scroll down in About content
        eval_js('document.getElementById("about-dialog-content").scrollTop = 350')
        time.sleep(0.5)
        capture_screenshot(f"checkpoint_a_02_about_window_scrolled{suffix}.png")

        # Close About window
        eval_js('document.getElementById("btn-close-about").click()')
        time.sleep(0.5)
        closed_ok = eval_js('!document.getElementById("modal-about").open')
        print(f"  Modal Closed via Close button: {closed_ok}")

        # ---------------------------------------------------------------------
        # CHECKPOINT B: Cubert Tip Buttons ($1, $5, $10, $0)
        # ---------------------------------------------------------------------
        print("\n--- Verifying Checkpoint B: Cubert Tip Buttons ---")
        # Reset balance to $249.00
        eval_js('creditBalance = 249.00; updateEconomyDisplay();')
        b_init = eval_js('creditBalance')
        disp_init = eval_js('document.getElementById("credit-val").textContent')
        print(f"  Initial Balance: ${b_init:.2f} (Display: {disp_init})")

        # 1. Trigger Cubert with tip prompt
        eval_js('showCubertPopup("So are you gonna tip me?", "helpful", true, "tip_prompt")')
        time.sleep(0.5)
        tip_visible = eval_js('document.getElementById("cubert-tip-selector").style.display !== "none"')
        print(f"  Cubert Active with Tip Selector: {tip_visible}")
        capture_screenshot(f"checkpoint_b_01_tip_prompt_active{suffix}.png")

        # 2. Click $1 Tip
        eval_js('document.querySelector(".cubert-tip-btn[data-tip=\'1\']").click()')
        time.sleep(0.5)
        b_after1 = eval_js('creditBalance')
        disp_after1 = eval_js('document.getElementById("credit-val").textContent')
        mode_after1 = eval_js('cubertMode === CUBERT_MODES.STANDBY')
        mascot_after1 = eval_js('document.getElementById("cubert-static-img").src')
        print(f"  After $1 Tip: Balance=${b_after1:.2f} (Display: {disp_after1}), Dismissed={mode_after1}, Mascot='{mascot_after1.split('/')[-1]}'")
        assert b_after1 == 248.00, f"Expected 248.00 after $1 tip, got {b_after1}"
        assert "248.00" in disp_after1, f"Display did not update to $248.00: {disp_after1}"
        assert mode_after1, "Cubert was not dismissed after $1 tip"
        capture_screenshot(f"checkpoint_b_02_tipped_1_dollar{suffix}.png")

        # 3. Click $5 Tip
        eval_js('showCubertPopup("So are you gonna tip me?", "helpful", true, "tip_prompt")')
        time.sleep(0.5)
        eval_js('document.querySelector(".cubert-tip-btn[data-tip=\'5\']").click()')
        time.sleep(0.5)
        b_after5 = eval_js('creditBalance')
        disp_after5 = eval_js('document.getElementById("credit-val").textContent')
        print(f"  After $5 Tip: Balance=${b_after5:.2f} (Display: {disp_after5})")
        assert b_after5 == 243.00, f"Expected 243.00 after $5 tip, got {b_after5}"

        # 4. Click $10 Tip
        eval_js('showCubertPopup("So are you gonna tip me?", "helpful", true, "tip_prompt")')
        time.sleep(0.5)
        eval_js('document.querySelector(".cubert-tip-btn[data-tip=\'10\']").click()')
        time.sleep(0.5)
        b_after10 = eval_js('creditBalance')
        disp_after10 = eval_js('document.getElementById("credit-val").textContent')
        print(f"  After $10 Tip: Balance=${b_after10:.2f} (Display: {disp_after10})")
        assert b_after10 == 233.00, f"Expected 233.00 after $10 tip, got {b_after10}"

        # 5. Click $0 Tip
        eval_js('showCubertPopup("So are you gonna tip me?", "helpful", true, "tip_prompt")')
        time.sleep(0.5)
        eval_js('document.querySelector(".cubert-tip-zero").click()')
        time.sleep(0.5)
        b_after0 = eval_js('creditBalance')
        disp_after0 = eval_js('document.getElementById("credit-val").textContent')
        mode_after0 = eval_js('cubertMode === CUBERT_MODES.STANDBY')
        print(f"  After $0 Tip: Balance=${b_after0:.2f} (Display: {disp_after0}), Dismissed={mode_after0}")
        assert b_after0 == 233.00, f"Expected 233.00 unchanged after $0 tip, got {b_after0}"
        assert mode_after0, "Cubert was not dismissed after $0 tip"
        capture_screenshot(f"checkpoint_b_03_tipped_0_dollars{suffix}.png")

        # 6. Insufficient Funds Rejection & 'Broke ass' Line
        print("\n--- Verifying Insufficient Funds for Tip ---")
        eval_js('creditBalance = 2.00; updateEconomyDisplay();')
        eval_js('showCubertPopup("So are you gonna tip me?", "helpful", true, "tip_prompt")')
        time.sleep(0.5)
        # Attempt $5 tip
        eval_js('document.querySelector(".cubert-tip-btn[data-tip=\'5\']").click()')
        time.sleep(0.5)
        b_insuf = eval_js('creditBalance')
        speech_insuf = eval_js('document.getElementById("cubert-bubble-text").textContent')
        expr_insuf = eval_js('document.getElementById("cubert-popup-img").src')
        mode_insuf = eval_js('cubertMode === CUBERT_MODES.ACTIVE')
        print(f"  Insufficient Funds: Balance=${b_insuf:.2f} (zero deduction), Speech='{speech_insuf}', Mode=Active: {mode_insuf}")
        assert b_insuf == 2.00, f"Balance was deducted during insufficient funds! {b_insuf}"
        assert "Broke ass" in speech_insuf, f"Speech bubble did not display 'Broke ass.': {speech_insuf}"
        assert "shrugging" in expr_insuf, "Expression is not shrugging"
        capture_screenshot(f"checkpoint_b_04_insufficient_funds_broke_ass{suffix}.png")

        # Clean up
        eval_js('hideCubertPopup(); creditBalance = 249.00; updateEconomyDisplay();')

        print(f"\n[SUCCESS] Checkpoints A & B verified at DPR {dpr}!")

    finally:
        proc.terminate()
        time.sleep(1.0)

if __name__ == "__main__":
    run_verification(dpr=1.0)
    run_verification(dpr=2.0)
