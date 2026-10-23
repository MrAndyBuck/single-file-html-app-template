#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os

PORT = 9335
DESKTOP_DIR = "/Users/andybuck/Desktop"
OCT22_DIR = "/Users/andybuck/Desktop/OCT_22"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(DESKTOP_DIR, exist_ok=True)
os.makedirs(OCT22_DIR, exist_ok=True)
os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)

VARIATIONS = [
    {
        "id": "var_01_cheerful_greeting",
        "name": "1. Cheerful Greeting",
        "expr": "cheerful",
        "text": "How can I help you?",
        "tip": False,
        "desc": "Default appearance and greeting when summoned manually, by Help, or after failures."
    },
    {
        "id": "var_02_thinking_uncertain",
        "name": "2. Thinking / Uncertain",
        "expr": "thinking",
        "text": "Hmm... I am not quite sure what you mean.",
        "tip": False,
        "desc": "Hand on chin looking upward during uncertain or processing moments."
    },
    {
        "id": "var_03_confused_retry",
        "name": "3. Confused / Calm Retry",
        "expr": "confused",
        "text": "Please remain calm and try to type that request again a little more carefully.",
        "tip": False,
        "desc": "Stage 2 retry request asking the user to remain calm and re-type."
    },
    {
        "id": "var_04_scolding_profanity",
        "name": "4. Scolding (Profanity Interrupt)",
        "expr": "scolding",
        "text": "Watch your fucking language.",
        "tip": False,
        "desc": "Triggered immediately when profanity is detected anywhere in user input."
    },
    {
        "id": "var_05_shrugging_bad_suggestion",
        "name": "5. Shrugging / Incompetent Bad Suggestion",
        "expr": "shrugging",
        "text": "I know what you need! Can I loft!",
        "tip": False,
        "desc": "Stage 3 bad suggestion recommending a random unrelated CAD command."
    },
    {
        "id": "var_06_helpful_tip_selector",
        "name": "6. Helpful / Tip Request",
        "expr": "helpful",
        "text": "Would you like to leave Cubert a tip for this stellar guidance?",
        "tip": True,
        "desc": "Finger-snap cash gesture presenting the $1, $5, $10, and tiny $0 tip selector."
    },
    {
        "id": "var_07_shrugging_broke_ass",
        "name": "7. Shrugging / Broke Ass",
        "expr": "shrugging",
        "text": "Broke ass.",
        "tip": False,
        "desc": "Delivered when the user attempts to tip more than their fictional account balance."
    },
    {
        "id": "var_08_burntout_break_standby",
        "name": "8. Burnt-Out Cubert (Office Chair)",
        "expr": "burntout",
        "text": "Hey man, I'm going to go on break. Back in 15.",
        "tip": False,
        "desc": "Exhausted with cigarette and 1000-yard stare. Docked in bottom-left during standby & break."
    }
]

def run():
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

        def save_bytes(filename, b):
            for d in [DESKTOP_DIR, OCT22_DIR, PROJECT_SCREENSHOTS]:
                with open(os.path.join(d, filename), 'wb') as f:
                    f.write(b)
            print(f"[SAVED] {filename} (to Desktop, OCT_22, screenshots/)")

        def capture_full(filename):
            res = send_cmd('Page.captureScreenshot', {'format': 'png'})
            data = res.get('result', {}).get('data')
            if data:
                save_bytes(filename, base64.b64decode(data))

        def capture_clip(filename, clip):
            res = send_cmd('Page.captureScreenshot', {'format': 'png', 'clip': clip})
            data = res.get('result', {}).get('data')
            if data:
                save_bytes(filename, base64.b64decode(data))

        time.sleep(1.0)
        # Dismiss any initial modal
        evaluate('''(() => {
            const ob = document.getElementById("modal-onboarding");
            if (ob && ob.open) ob.close();
            renderAllViewports();
        })()''')

        # Capture each variation
        for v in VARIATIONS:
            print(f"\nCapturing: {v['name']} ({v['expr']})...")
            evaluate(f'''(() => {{
                showCubertPopup({json.dumps(v['text'])}, {json.dumps(v['expr'])}, {json.dumps(v['tip'])});
            }})()''')
            time.sleep(0.35)

            # Full application capture
            full_name = f"cubert_variation_{v['id']}_full.png"
            capture_full(full_name)

            # Popup bounding box crop
            rect = evaluate('''(() => {
                const el = document.getElementById("cubert-popup");
                if (!el) return null;
                const r = el.getBoundingClientRect();
                return {
                    x: Math.max(0, Math.floor(r.left - 12)),
                    y: Math.max(0, Math.floor(r.top - 12)),
                    width: Math.ceil(r.width + 24),
                    height: Math.ceil(r.height + 24),
                    scale: 1.0
                };
            })()''')

            if rect:
                crop_name = f"cubert_variation_{v['id']}_closeup.png"
                capture_clip(crop_name, rect)

        # Navigate to gallery sheet
        print("\nNavigating to all-in-one gallery overview sheet...")
        send_cmd('Page.navigate', {'url': 'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/cubert_gallery.html'})
        time.sleep(1.2)
        capture_full("cubert_variations_all_in_one_gallery.png")

    finally:
        proc.terminate()

if __name__ == '__main__':
    run()
