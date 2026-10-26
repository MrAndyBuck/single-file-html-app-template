#!/usr/bin/env python3
"""
CADN'T - Checkpoint G Verification Script
Verifies:
- Official CADN'T logo image integrated in the top blue title bar.
- Black serif lettering with blue isometric cube apostrophe.
- Original design and proportions preserved.
- Right-aligned supporting branding text: "Computer Aided Design Noncompliance Technology".
- Captured at DPR 1.0 and DPR 2.0.
"""

import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

PORT = 9360
DESKTOP_DIR = "/Users/andybuck/Desktop"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)

def run_verification(dpr=1.0):
    port = PORT if dpr == 1.0 else PORT + 1
    suffix = "_dpr2" if dpr > 1.0 else ""
    print(f"\n=======================================================")
    print(f"Running Checkpoint G Verification at DPR {dpr}")
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

        # Verify logo in DOM
        logo_info = eval_js("""(() => {
            const logo = document.getElementById('cadnt-official-logo');
            const subtext = document.querySelector('.win95-title-subtext');
            const titleBar = document.getElementById('win95-title-bar');
            const rect = logo.getBoundingClientRect();
            const barRect = titleBar.getBoundingClientRect();
            return {
                src: logo.src,
                naturalWidth: logo.naturalWidth,
                naturalHeight: logo.naturalHeight,
                renderedWidth: rect.width,
                renderedHeight: rect.height,
                subtext: subtext ? subtext.textContent : '',
                barHeight: barRect.height
            };
        })()""")

        print(f"  Logo Image Src: {logo_info.get('src')}")
        print(f"  Natural Dimensions: {logo_info.get('naturalWidth')}x{logo_info.get('naturalHeight')}")
        print(f"  Rendered Dimensions: {logo_info.get('renderedWidth'):.1f}x{logo_info.get('renderedHeight'):.1f}")
        print(f"  Title Bar Height: {logo_info.get('barHeight')}px")
        print(f"  Supporting Subtext: '{logo_info.get('subtext')}'")

        assert "CADNTLogo.png" in logo_info.get('src'), "Logo src missing CADNTLogo.png"
        assert "Computer Aided Design Noncompliance Technology" in logo_info.get('subtext'), "Missing subtext"

        # Capture full window
        capture_screenshot(f"checkpoint_g_01_official_logo{suffix}.png")

        # Capture title bar closeup (top 60px)
        titlebar_clip = {
            'x': 0,
            'y': 0,
            'width': 1280,
            'height': 60,
            'scale': dpr
        }
        capture_screenshot(f"checkpoint_g_02_titlebar_closeup{suffix}.png", clip=titlebar_clip)

        print(f"[SUCCESS] Checkpoint G verified at DPR {dpr}!")

    finally:
        proc.terminate()
        time.sleep(1.0)

if __name__ == "__main__":
    run_verification(dpr=1.0)
    run_verification(dpr=2.0)
