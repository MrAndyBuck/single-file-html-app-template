#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os

PORT = 9325
DESKTOP_DIR = "/Users/andybuck/Desktop"
OCT22_DIR = "/Users/andybuck/Desktop/OCT_22"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(DESKTOP_DIR, exist_ok=True)
os.makedirs(OCT22_DIR, exist_ok=True)
os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)

def run_capture(dpr=1.0):
    flags = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--headless=new',
        '--use-gl=angle',
        '--use-angle=swiftshader',
        '--enable-unsafe-swiftshader',
        '--window-size=1280,820',
        f'--remote-debugging-port={PORT}',
        'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1'
    ]
    if dpr > 1.0:
        flags.append(f'--force-device-scale-factor={dpr}')

    proc = subprocess.Popen(flags)
    time.sleep(2.5)

    try:
        tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json').read().decode())
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
                # Desktop
                with open(os.path.join(DESKTOP_DIR, filename), 'wb') as f:
                    f.write(b)
                # OCT_22
                with open(os.path.join(OCT22_DIR, filename), 'wb') as f:
                    f.write(b)
                # Project Screenshots
                with open(os.path.join(PROJECT_SCREENSHOTS, filename), 'wb') as f:
                    f.write(b)
                print(f"Captured: {filename} (saved to Desktop, OCT_22, and screenshots/)")
                return True
            return False

        time.sleep(1.0)
        # Dismiss onboarding if any
        evaluate('''(() => {
            const ob = document.getElementById("modal-onboarding");
            if (ob && ob.open) ob.close();
            renderAllViewports();
        })()''')

        if dpr == 1.0:
            # 1. Default Cubert in permanent panel (Idle state)
            print("\n1. Default Cubert in permanent panel...")
            evaluate("hideCubertPopup();")
            time.sleep(0.3)
            capture("clippy_01_default_panel_idle.png")

            # 2. Cheerful Cubert greeting centrally
            print("\n2. Cheerful Cubert greeting...")
            evaluate('showCubertPopup("How can I help you?", "cheerful");')
            time.sleep(0.4)
            capture("clippy_02_cheerful_greeting.png")

            # 3. Thinking Cubert
            print("\n3. Thinking Cubert...")
            evaluate('showCubertPopup("Hmm... I am not quite sure what you mean.", "thinking");')
            time.sleep(0.4)
            capture("clippy_03_thinking_uncertain.png")

            # 4. Scolding Cubert (Profanity)
            print("\n4. Scolding Cubert...")
            evaluate('showCubertPopup("Watch your fucking language.", "scolding");')
            time.sleep(0.4)
            capture("clippy_04_scolding_profanity.png")

            # 5. Shrugging Cubert (Bad suggestion)
            print("\n5. Shrugging Cubert...")
            evaluate('showCubertPopup("I know what you need! Can I polygon 5!", "shrugging");')
            time.sleep(0.4)
            capture("clippy_05_shrugging_bad_suggestion.png")

            # 6. Helpful Cubert requesting tip
            print("\n6. Helpful Cubert requesting tip...")
            evaluate('showCubertPopup("Would you like to leave Cubert a tip for this stellar guidance?", "helpful", true);')
            time.sleep(0.4)
            capture("clippy_06_tipping_selector.png")

            # 7. Burnt-out Cubert in permanent panel on break
            print("\n7. Burnt-out Cubert on break...")
            evaluate('triggerCubertBreak();')
            time.sleep(0.4)
            capture("clippy_07_break_burntout_panel.png")

        else:
            # DPR 2.0 Retina capture
            print("\n8. Retina DPR 2.0 full app capture...")
            evaluate('showCubertPopup("How can I help you?", "cheerful");')
            time.sleep(0.5)
            capture("clippy_08_retina_dpr2_full_app.png")

    finally:
        proc.terminate()

print("--- Running DPR 1.0 Captures ---")
run_capture(1.0)

print("\n--- Running DPR 2.0 Retina Capture ---")
run_capture(2.0)

print("\nALL CLIPPYS CAPTURED SUCCESSFULLY TO DESKTOP AND OCT_22!")
