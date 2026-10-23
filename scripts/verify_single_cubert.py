#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os

PORT = 9330
DESKTOP_DIR = "/Users/andybuck/Desktop"
OCT22_DIR = "/Users/andybuck/Desktop/OCT_22"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(DESKTOP_DIR, exist_ok=True)
os.makedirs(OCT22_DIR, exist_ok=True)
os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)

def run_verification():
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

    proc = subprocess.Popen(flags)
    time.sleep(1.0)

    try:
        tabs = None
        for _ in range(15):
            try:
                tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json').read().decode())
                break
            except Exception:
                time.sleep(0.5)

        if not tabs:
            raise Exception("Failed to connect to Chrome debugging port")

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
                for d in [DESKTOP_DIR, OCT22_DIR, PROJECT_SCREENSHOTS]:
                    with open(os.path.join(d, filename), 'wb') as f:
                        f.write(b)
                print(f"[CAPTURED] {filename} (saved to Desktop, OCT_22, and screenshots/)")
                return True
            return False

        time.sleep(1.0)
        # Dismiss any initial modal
        evaluate('''(() => {
            const ob = document.getElementById("modal-onboarding");
            if (ob && ob.open) ob.close();
            renderAllViewports();
        })()''')

        # -------------------------------------------------------------
        # State 1: Standby Mode
        # Only burnt-out smoking Cubert in bottom-left panel. Center is empty.
        # -------------------------------------------------------------
        print("\n--- Testing State 1: Standby Mode ---")
        evaluate("setCubertMode(CUBERT_MODES.STANDBY);")
        time.sleep(0.4)
        count1 = evaluate("getVisibleCubertCount();")
        status1 = evaluate("document.getElementById('cubert-panel-status').textContent.trim();")
        staticSrc1 = evaluate("document.getElementById('cubert-static-img').getAttribute('src');")
        popupDisp1 = evaluate("document.getElementById('cubert-popup').style.display;")
        print(f"Standby State: visible Cuberts = {count1}, status = '{status1}', static src = '{staticSrc1}', popup display = '{popupDisp1}'")
        assert count1 == 1, f"Expected 1 visible Cubert in Standby, got {count1}"
        assert popupDisp1 == "none", f"Expected popup hidden in Standby, got {popupDisp1}"
        capture("single_cubert_01_standby.png")

        # -------------------------------------------------------------
        # State 2: Active / Helping Mode
        # Only expressive Cubert centrally over CAD workspace. Bottom-left is hidden.
        # -------------------------------------------------------------
        print("\n--- Testing State 2: Active / Helping Mode ---")
        evaluate('showCubertPopup("How can I help you?", "cheerful");')
        time.sleep(0.5)
        count2 = evaluate("getVisibleCubertCount();")
        status2 = evaluate("document.getElementById('cubert-panel-status').textContent.trim();")
        staticDisp2 = evaluate("document.getElementById('cubert-static-img').style.display;")
        popupDisp2 = evaluate("document.getElementById('cubert-popup').style.display;")
        print(f"Active State: visible Cuberts = {count2}, status = '{status2}', static display = '{staticDisp2}', popup display = '{popupDisp2}'")
        assert count2 == 1, f"Expected 1 visible Cubert in Active, got {count2}"
        assert staticDisp2 == "none", f"Expected bottom-left Cubert hidden in Active, got {staticDisp2}"
        assert popupDisp2 != "none", f"Expected popup visible in Active, got {popupDisp2}"
        capture("single_cubert_02_active.png")

        # -------------------------------------------------------------
        # State 3: Dismissed / Return to Standby Mode
        # Central Cubert disappears, burnt-out Cubert in bottom-left is restored.
        # -------------------------------------------------------------
        print("\n--- Testing State 3: Dismissed / Return to Standby ---")
        evaluate("document.getElementById('btn-cubert-close').click();")
        time.sleep(0.4)
        count3 = evaluate("getVisibleCubertCount();")
        status3 = evaluate("document.getElementById('cubert-panel-status').textContent.trim();")
        staticDisp3 = evaluate("document.getElementById('cubert-static-img').style.display;")
        popupDisp3 = evaluate("document.getElementById('cubert-popup').style.display;")
        print(f"Dismissed State: visible Cuberts = {count3}, status = '{status3}', static display = '{staticDisp3}', popup display = '{popupDisp3}'")
        assert count3 == 1, f"Expected 1 visible Cubert when Dismissed, got {count3}"
        assert popupDisp3 == "none", f"Expected popup hidden when Dismissed, got {popupDisp3}"
        assert staticDisp3 != "none", f"Expected bottom-left restored when Dismissed, got {staticDisp3}"
        capture("single_cubert_03_dismissed.png")

        # -------------------------------------------------------------
        # State 4: Break Mode
        # Burnt-out Cubert in bottom-left on break, unavailable for 60s.
        # -------------------------------------------------------------
        print("\n--- Testing State 4: Break Mode ---")
        evaluate("triggerCubertBreak();")
        time.sleep(0.4)
        count4 = evaluate("getVisibleCubertCount();")
        status4 = evaluate("document.getElementById('cubert-panel-status').textContent.trim();")
        staticDisp4 = evaluate("document.getElementById('cubert-static-img').style.display;")
        popupDisp4 = evaluate("document.getElementById('cubert-popup').style.display;")
        print(f"Break State: visible Cuberts = {count4}, status = '{status4}', static display = '{staticDisp4}', popup display = '{popupDisp4}'")
        assert count4 == 1, f"Expected 1 visible Cubert during Break, got {count4}"
        assert popupDisp4 == "none", f"Expected popup hidden during Break, got {popupDisp4}"
        assert staticDisp4 != "none", f"Expected bottom-left visible during Break, got {staticDisp4}"
        assert status4 == "On Break", f"Expected status 'On Break', got {status4}"
        capture("single_cubert_04_break.png")

        print("\n[SUCCESS] ALL 4 STATES VERIFIED WITH EXACTLY 1 VISIBLE CUBERT EACH!")

    finally:
        proc.terminate()

if __name__ == '__main__':
    run_verification()
