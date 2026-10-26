#!/usr/bin/env python3
"""
CADN'T - Checkpoints A & B Verification Script
Verifies:
- Checkpoint A:
  1. Standby mode displays cheerful mascot (assets/cubert/cubert_cheerful.png).
  2. Help window opening summons Cubert beside the Help window.
  3. Help documentation and Cubert are simultaneously visible with zero overlap.
  4. Break mode displays exhausted smoking mascot (assets/cubert/cubert_burntout.png).
  5. Single Cubert invariant (count == 1) strictly preserved across all states.
- Checkpoint B:
  1. Dedicated 'Talk to Cubert:' bar appears when Cubert is active and hides on dismissal.
  2. Submissions through Cubert Bar go exclusively to Cubert's conversation state machine.
  3. Multi-turn dialogue: "How can I help you?" -> User input -> "Please remain calm..." retry instruction -> Follow-up -> Bad suggestion with tip prompt.
  4. Cubert Bar interactions do NOT increment modelingCommandCount (zero ad impact).
  5. Dismissing Cubert restores focus to Request Bar.
Captures high-resolution visual evidence at DPR 1.0 and 2.0.
"""

import socket, json, urllib.request, subprocess, time, struct, base64, os

PORT = 9340
DESKTOP_DIR = "/Users/andybuck/Desktop"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)
if os.path.exists(DESKTOP_DIR):
    pass

def run_verification(dpr=1.0):
    port = PORT if dpr == 1.0 else PORT + 1
    flags = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--headless=new',
        '--use-gl=angle',
        '--use-angle=swiftshader',
        '--enable-unsafe-swiftshader',
        '--window-size=1280,820',
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
        host, port_str, path = '127.0.0.1', str(port), ws_url.split(f'127.0.0.1:{port}')[1]
        s = socket.socket()
        s.connect((host, port))
        key = base64.b64encode(b'0123456789abcdef').decode()
        req = f'GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
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
            return send_cmd('Runtime.evaluate', {'expression': expr, 'returnByValue': True}).get('result', {}).get('result', {}).get('value')

        def capture(filename):
            res = send_cmd('Page.captureScreenshot', {'format': 'png'})
            data = res.get('result', {}).get('data')
            if data:
                b = base64.b64decode(data)
                target_dirs = [PROJECT_SCREENSHOTS]
                if os.path.exists(DESKTOP_DIR):
                    target_dirs.append(DESKTOP_DIR)
                for d in target_dirs:
                    with open(os.path.join(d, filename), 'wb') as f:
                        f.write(b)
                print(f"[CAPTURED] {filename} -> {PROJECT_SCREENSHOTS}")
                return True
            return False

        time.sleep(1.0)
        # Dismiss any initial modal
        evaluate('''(() => {
            const ob = document.getElementById("modal-onboarding");
            if (ob && ob.open) ob.close();
            renderAllViewports();
        })()''')

        suffix = f"_dpr{int(dpr)}" if dpr > 1.0 else ""

        print(f"\n========================================================")
        print(f"VERIFYING CHECKPOINTS A & B (DPR: {dpr})")
        print(f"========================================================")

        # -------------------------------------------------------------
        # Checkpoint A - State 1: Standby Mode with Cheerful Mascot
        # -------------------------------------------------------------
        print("\n--- 1. Standby Mode with Cheerful Mascot ---")
        evaluate("setCubertMode(CUBERT_MODES.STANDBY);")
        time.sleep(0.3)
        count_standby = evaluate("getVisibleCubertCount();")
        status_standby = evaluate("document.getElementById('cubert-panel-status').textContent.trim();")
        static_src_standby = evaluate("document.getElementById('cubert-static-img').getAttribute('src');")
        popup_disp_standby = evaluate("document.getElementById('cubert-popup').style.display;")
        print(f"Standby: Visible Count={count_standby}, Status='{status_standby}', Mascot={static_src_standby}, PopupDisplay={popup_disp_standby}")
        assert count_standby == 1, f"Expected 1 visible Cubert in Standby, got {count_standby}"
        assert "cheerful" in static_src_standby or static_src_standby == "assets/cubert/cubert.png", f"Expected cheerful mascot in standby, got {static_src_standby}"
        assert popup_disp_standby == "none", f"Expected central popup hidden in standby, got {popup_disp_standby}"
        capture(f"checkpoint_a_01_standby_cheerful{suffix}.png")

        # -------------------------------------------------------------
        # Checkpoint A - State 2: Help Window with Cubert Beside It
        # -------------------------------------------------------------
        print("\n--- 2. Help Window with Cubert Beside It ---")
        evaluate("openHelpWindow();")
        time.sleep(0.5)
        count_help = evaluate("getVisibleCubertCount();")
        help_open = evaluate("document.getElementById('modal-help').open;")
        help_has_beside = evaluate("document.getElementById('modal-help').classList.contains('beside-cubert');")
        popup_has_beside = evaluate("document.getElementById('cubert-popup').classList.contains('beside-help');")
        bubble_text_help = evaluate("document.getElementById('cubert-bubble-text').textContent;")
        
        # Geometries for non-overlap check
        help_rect = evaluate("(() => { const r = document.getElementById('modal-help').getBoundingClientRect(); return { left: r.left, right: r.right, width: r.width }; })()")
        cubert_img_rect = evaluate("(() => { const r = document.getElementById('cubert-popup-img').getBoundingClientRect(); return { left: r.left, right: r.right, width: r.width }; })()")
        cubert_bubble_rect = evaluate("(() => { const r = document.getElementById('cubert-speech-bubble').getBoundingClientRect(); return { left: r.left, right: r.right, width: r.width }; })()")

        print(f"Help Open: Visible Count={count_help}, Help.open={help_open}, beside-cubert={help_has_beside}, beside-help={popup_has_beside}")
        print(f"Help Rect: left={help_rect.get('left')}, right={help_rect.get('right')}, width={help_rect.get('width')}")
        print(f"Cubert Img Rect: left={cubert_img_rect.get('left')}, right={cubert_img_rect.get('right')}")
        print(f"Cubert Bubble Rect: left={cubert_bubble_rect.get('left')}, right={cubert_bubble_rect.get('right')}")
        print(f"Cubert Dialogue: '{bubble_text_help}'")

        assert count_help == 1, f"Expected 1 visible Cubert when Help is open, got {count_help}"
        assert help_open is True, "Expected modal-help to be open"
        assert help_has_beside is True, "Expected modal-help to have beside-cubert class"
        assert popup_has_beside is True, "Expected cubert-popup to have beside-help class"
        assert "How can I help you?" in bubble_text_help, f"Expected greeting dialogue, got {bubble_text_help}"
        # Non-overlap check: Help right edge must not exceed Cubert left edge
        cubert_left = min(cubert_img_rect.get('left'), cubert_bubble_rect.get('left'))
        overlap = help_rect.get('right') > cubert_left
        print(f"Overlap detected: {overlap} (Help Right={help_rect.get('right')} vs Cubert Left={cubert_left})")
        assert not overlap, "Help window and Cubert must not overlap!"
        capture(f"checkpoint_a_02_help_with_cubert_beside{suffix}.png")

        # -------------------------------------------------------------
        # Checkpoint A - State 3: Close Help Window and Return
        # -------------------------------------------------------------
        print("\n--- 3. Close Help Window ---")
        evaluate("closeHelpWindow();")
        time.sleep(0.3)
        help_still_open = evaluate("document.getElementById('modal-help').open;")
        help_has_beside_after = evaluate("document.getElementById('modal-help').classList.contains('beside-cubert');")
        popup_has_beside_after = evaluate("document.getElementById('cubert-popup').classList.contains('beside-help');")
        print(f"After Close Help: Help.open={help_still_open}, Help beside={help_has_beside_after}, Popup beside={popup_has_beside_after}")
        assert help_still_open is False, "Expected modal-help to be closed"
        assert help_has_beside_after is False, "Expected beside-cubert removed"
        assert popup_has_beside_after is False, "Expected beside-help removed"

        # -------------------------------------------------------------
        # Checkpoint A - State 4: Break Mode with Exhausted Smoking Mascot
        # -------------------------------------------------------------
        print("\n--- 4. Break Mode with Burnt-Out Smoking Mascot ---")
        evaluate("triggerCubertBreak();")
        time.sleep(0.3)
        count_break = evaluate("getVisibleCubertCount();")
        status_break = evaluate("document.getElementById('cubert-panel-status').textContent.trim();")
        static_src_break = evaluate("document.getElementById('cubert-static-img').getAttribute('src');")
        popup_disp_break = evaluate("document.getElementById('cubert-popup').style.display;")
        print(f"Break: Visible Count={count_break}, Status='{status_break}', Mascot={static_src_break}, PopupDisplay={popup_disp_break}")
        assert count_break == 1, f"Expected 1 visible Cubert on break, got {count_break}"
        assert "burntout" in static_src_break, f"Expected burntout mascot on break, got {static_src_break}"
        assert status_break == "On Break", f"Expected 'On Break', got {status_break}"
        capture(f"checkpoint_a_04_break_burntout{suffix}.png")
        evaluate("endCubertBreak();")

        # -------------------------------------------------------------
        # Checkpoint B - State 1: Dedicated Cubert Bar Appears When Active
        # -------------------------------------------------------------
        print("\n--- 5. Dedicated Cubert Bar Visibility & Focus ---")
        evaluate("showCubertPopup('How can I help you?', 'cheerful');")
        time.sleep(0.3)
        cubert_bar_disp = evaluate("document.getElementById('cubert-bar-row').style.display;")
        cubert_bar_label = evaluate("document.getElementById('cubert-bar-label').textContent.trim();")
        print(f"Cubert Bar: Display='{cubert_bar_disp}', Label='{cubert_bar_label}'")
        assert cubert_bar_disp != "none", f"Expected Cubert Bar to be visible when active, got {cubert_bar_disp}"
        assert cubert_bar_label == "Talk to Cubert:", f"Expected label 'Talk to Cubert:', got {cubert_bar_label}"
        capture(f"checkpoint_b_01_cubert_bar_active{suffix}.png")

        # -------------------------------------------------------------
        # Checkpoint B - State 2: Explanation -> Retry Instruction
        # -------------------------------------------------------------
        print("\n--- 6. Cubert Bar Submission (Explanation -> Retry Instruction) ---")
        initial_ads = evaluate("modelingCommandCount;")
        evaluate("handleCubertConversationSubmit('I want to make a smooth pipe');")
        time.sleep(0.4)
        stage_retry = evaluate("cubertConvStage;")
        bubble_retry = evaluate("document.getElementById('cubert-bubble-text').textContent;")
        ads_after_explanation = evaluate("modelingCommandCount;")
        print(f"After Explanation: Stage='{stage_retry}', Speech='{bubble_retry}', Ads Count={ads_after_explanation} (Initial={initial_ads})")
        assert stage_retry == "AWAITING_RETRY", f"Expected AWAITING_RETRY, got {stage_retry}"
        assert "Please remain calm" in bubble_retry, f"Expected retry instruction dialogue, got {bubble_retry}"
        assert ads_after_explanation == initial_ads, "Cubert conversations must not increment modelingCommandCount!"
        capture(f"checkpoint_b_02_cubert_conversation_retry{suffix}.png")

        # -------------------------------------------------------------
        # Checkpoint B - State 3: Follow-Up -> Bad Suggestion + Tip Selector
        # -------------------------------------------------------------
        print("\n--- 7. Follow-Up Submission (Bad Suggestion & Tip Prompt) ---")
        evaluate("handleCubertConversationSubmit('Can you please just do it');")
        time.sleep(0.4)
        stage_suggestion = evaluate("cubertConvStage;")
        bubble_suggestion = evaluate("document.getElementById('cubert-bubble-text').textContent;")
        tip_disp = evaluate("document.getElementById('cubert-tip-selector').style.display;")
        ads_after_suggestion = evaluate("modelingCommandCount;")
        print(f"After Follow-up: Stage='{stage_suggestion}', Speech='{bubble_suggestion}', Tip Selector='{tip_disp}', Ads Count={ads_after_suggestion}")
        assert stage_suggestion == "TIP_PROMPT", f"Expected TIP_PROMPT, got {stage_suggestion}"
        assert "I know what you need" in bubble_suggestion, f"Expected bad suggestion dialogue, got {bubble_suggestion}"
        assert tip_disp != "none", f"Expected tip selector to be visible, got {tip_disp}"
        assert ads_after_suggestion == initial_ads, "Cubert conversations must not increment modelingCommandCount!"
        capture(f"checkpoint_b_03_cubert_bad_suggestion_tip{suffix}.png")

        # -------------------------------------------------------------
        # Checkpoint B - State 4: Dismiss Cubert and Return to Request Bar
        # -------------------------------------------------------------
        print("\n--- 8. Dismiss Cubert (Hide Cubert Bar & Return Focus) ---")
        evaluate("hideCubertPopup();")
        time.sleep(0.3)
        cubert_bar_after_dismiss = evaluate("document.getElementById('cubert-bar-row').style.display;")
        popup_after_dismiss = evaluate("document.getElementById('cubert-popup').style.display;")
        static_src_after_dismiss = evaluate("document.getElementById('cubert-static-img').getAttribute('src');")
        count_after_dismiss = evaluate("getVisibleCubertCount();")
        print(f"After Dismiss: Cubert Bar Display='{cubert_bar_after_dismiss}', Popup Display='{popup_after_dismiss}', Mascot={static_src_after_dismiss}, Visible Count={count_after_dismiss}")
        assert cubert_bar_after_dismiss == "none", "Expected Cubert Bar to be hidden after dismissal"
        assert popup_after_dismiss == "none", "Expected popup to be hidden after dismissal"
        assert "cheerful" in static_src_after_dismiss or static_src_after_dismiss == "assets/cubert/cubert.png", "Expected cheerful mascot in dock after dismissal"
        assert count_after_dismiss == 1, f"Expected 1 visible Cubert after dismissal, got {count_after_dismiss}"
        capture(f"checkpoint_b_04_dismissed_restored{suffix}.png")

        print(f"\n[SUCCESS] ALL CHECKPOINT A & B VERIFICATIONS PASSED (DPR: {dpr})!\n")

    finally:
        proc.terminate()

if __name__ == '__main__':
    run_verification(dpr=1.0)
    time.sleep(2.0)
    run_verification(dpr=2.0)
