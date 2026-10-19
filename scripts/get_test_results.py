#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64

PORT = 9299
proc = subprocess.Popen([
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless=new',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    f'--remote-debugging-port={PORT}',
    'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?run_tests=1&no_auto_onboard=1'
])
time.sleep(3.0)
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

    time.sleep(3.0)
    res = send_cmd('Runtime.evaluate', {
        'expression': 'JSON.stringify(window.__TEST_RESULTS__ || {})',
        'returnByValue': True
    })
    results = json.loads(res['result']['result']['value'])
    with open('test_run_output.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("SAVED test_run_output.json with total:", results.get("total"), "failures:", len(results.get("failures", [])))
finally:
    proc.terminate()
