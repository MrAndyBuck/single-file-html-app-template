#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os

PORT = 9311
TARGET_DIR = "/Users/andybuck/Documents/Antigravity/CADNT_Screenshots/Oct_22"
PROJECT_SCREENSHOTS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(TARGET_DIR, exist_ok=True)
os.makedirs(PROJECT_SCREENSHOTS_DIR, exist_ok=True)

proc = subprocess.Popen([
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless=new',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    '--window-size=1280,820',
    f'--remote-debugging-port={PORT}',
    'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1'
])

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
            raw_bytes = base64.b64decode(data)
            # Save to OCT_22 target dir
            tpath = os.path.join(TARGET_DIR, filename)
            with open(tpath, 'wb') as f:
                f.write(raw_bytes)
            # Also save to project screenshots dir for tracking
            ppath = os.path.join(PROJECT_SCREENSHOTS_DIR, filename)
            with open(ppath, 'wb') as f:
                f.write(raw_bytes)
            print(f"Captured: {tpath}")
            return tpath
        print(f"Failed to capture: {filename}")
        return None

    time.sleep(1.0)

    # Dismiss any active onboarding modal if visible
    evaluate('''(() => {
        const ob = document.getElementById("modal-onboarding");
        if (ob && ob.open) ob.close();
        renderAllViewports();
    })()''')
    time.sleep(0.5)

    print("\n--- 1. Capturing Permanent Cubert Panel (Idle State) ---")
    idle_info = evaluate('''(() => {
        const p = document.getElementById("cubert-panel");
        const img = document.getElementById("cubert-static-img");
        const status = document.getElementById("cubert-panel-status");
        let rect = null;
        if (p) {
            const r = p.getBoundingClientRect();
            rect = { x: r.x, y: r.y, width: r.width, height: r.height };
        }
        return {
            hasPanel: !!p,
            imgSrc: img ? img.getAttribute("src") : null,
            status: status ? status.textContent : null,
            panelRect: rect
        };
    })()''')
    print("Idle Cubert Panel Info:", idle_info)

    # 1. Full application showing permanent panel at bottom left
    capture_screenshot("oct22_01_cubert_panel_idle_full_app.png")

    # 2. Close-up of the permanent Cubert panel in left sidebar
    rect = idle_info.get("panelRect") or {"x": 4, "y": 550, "width": 240, "height": 165}
    capture_screenshot("oct22_02_cubert_panel_closeup.png", clip={
        'x': max(0, int(rect['x']) - 4),
        'y': max(0, int(rect['y']) - 4),
        'width': int(rect['width']) + 8,
        'height': int(rect['height']) + 8,
        'scale': 1
    })

    print("\n--- 2. Capturing Cubert Workspace Popup (Active State) ---")
    popup_info = evaluate('''(() => {
        showCubertPopup("How can I help you?", "help_1");
        const pop = document.getElementById("cubert-popup");
        const txt = document.getElementById("cubert-bubble-text");
        const cap = document.getElementById("cubert-caption-text");
        let rect = null;
        if (pop) {
            const r = pop.getBoundingClientRect();
            rect = { x: r.x, y: r.y, width: r.width, height: r.height };
        }
        return {
            hasPopup: !!pop,
            display: pop ? pop.style.display : null,
            text: txt ? txt.textContent : null,
            caption: cap ? cap.textContent : null,
            popRect: rect
        };
    })()''')
    print("Popup Info:", popup_info)
    time.sleep(0.5)

    # 3. Full application with active Cubert popup overlapping 3D viewports
    capture_screenshot("oct22_03_cubert_workspace_popup_active.png")

    # 4. Close-up of the active Cubert popup window
    popRect = popup_info.get("popRect") or {"x": 800, "y": 450, "width": 380, "height": 180}
    capture_screenshot("oct22_04_cubert_popup_closeup.png", clip={
        'x': max(0, int(popRect['x']) - 6),
        'y': max(0, int(popRect['y']) - 6),
        'width': int(popRect['width']) + 12,
        'height': int(popRect['height']) + 12,
        'scale': 1
    })

    print("\n--- All visual outputs successfully saved to OCT_22! ---")

finally:
    proc.terminate()
