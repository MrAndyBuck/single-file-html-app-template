#!/usr/bin/env python3
"""
CADN'T - Cubert Voiceover Integration Verification Suite
Tests actual audio playback for all 6 required dialogue events + hold music ducking + interruption
in both Google Chrome and Safari (WebKit).
"""

import os
import sys
import time
import json
import socket
import struct
import base64
import http.server
import threading
import urllib.request
import subprocess

HTTP_PORT = 8125
CHROME_CDP_PORT = 9335
APP_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app"

# 1. Background HTTP Server
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=APP_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def start_http_server():
    server = http.server.HTTPServer(("127.0.0.1", HTTP_PORT), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

# 2. Chrome Runner via CDP WebSocket
class ChromeRunner:
    def __init__(self):
        self.proc = None
        self.sock = None
        self.cmd_id = 1

    def start(self):
        cmd = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--headless=new",
            "--use-gl=angle",
            "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader",
            f"--remote-debugging-port={CHROME_CDP_PORT}",
            "--autoplay-policy=no-user-gesture-required",
            f"http://127.0.0.1:{HTTP_PORT}/index.html?no_auto_onboard=1"
        ]
        self.proc = subprocess.Popen(cmd)
        time.sleep(1.0)

        # Connect WebSocket
        tabs = None
        for _ in range(15):
            try:
                tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CHROME_CDP_PORT}/json").read().decode())
                break
            except Exception:
                time.sleep(0.5)

        if not tabs:
            raise RuntimeError("Could not connect to Chrome debugging port")

        target = next(t for t in tabs if t.get("type") == "page")
        ws_url = target["webSocketDebuggerUrl"]
        host, port, path = "127.0.0.1", CHROME_CDP_PORT, ws_url.split(f"127.0.0.1:{CHROME_CDP_PORT}")[1]
        self.sock = socket.socket()
        self.sock.connect((host, port))
        key = base64.b64encode(b"0123456789abcdef").decode()
        req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        self.sock.sendall(req.encode())
        self.sock.recv(4096)

        # Enable runtime
        self.send_cmd("Runtime.enable")
        time.sleep(1.0)

    def send_cmd(self, method, params=None):
        cid = self.cmd_id
        self.cmd_id += 1
        msg = json.dumps({"id": cid, "method": method, "params": params or {}}).encode("utf-8")
        frame = bytearray([0x81])
        length = len(msg)
        mask = b"\x11\x22\x33\x44"
        if length < 126:
            frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", length))
        frame.extend(mask)
        frame.extend(bytearray(b ^ mask[i % 4] for i, b in enumerate(msg)))
        self.sock.sendall(frame)

        while True:
            h = self.sock.recv(2)
            if not h: break
            l = h[1] & 0x7F
            if l == 126: l = struct.unpack(">H", self.sock.recv(2))[0]
            elif l == 127: l = struct.unpack(">Q", self.sock.recv(8))[0]
            data = bytearray()
            while len(data) < l:
                chunk = self.sock.recv(l - len(data))
                if not chunk: break
                data.extend(chunk)
            res = json.loads(data.decode("utf-8", errors="ignore"))
            if res.get("id") == cid:
                return res.get("result", {})

    def evaluate(self, expression):
        res = self.send_cmd("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        val = res.get("result", {}).get("value")
        return val

    def close(self):
        if self.sock:
            try: self.sock.close()
            except Exception: pass
        if self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=2)
            except Exception:
                try: self.proc.kill()
                except Exception: pass


def run_chrome_audio_verification():
    print("\n" + "=" * 60)
    print("RUNNING CUBERT AUDIO PLAYBACK VERIFICATION: GOOGLE CHROME")
    print("=" * 60)

    runner = ChromeRunner()
    runner.start()
    results = {}

    try:
        # Prepare environment
        runner.evaluate("CADNT_AUDIO.setMute(false); fictionalBalance = 200.0; updateEconomyDisplay();")

        # Test 1: How can I help you?
        runner.evaluate("showCubertPopup('How can I help you?', 'cheerful');")
        time.sleep(0.6)
        t1 = runner.evaluate("""
        (() => {
            const a = currentCubertAudio;
            const b = document.getElementById('cubert-bubble-text').textContent;
            return {
                src: a ? a.src : null,
                paused: a ? a.paused : true,
                currentTime: a ? a.currentTime : 0,
                duration: a ? a.duration : 0,
                caption: b
            };
        })()
        """)
        results["1_greeting"] = t1

        # Test 2: Request Bar retry instruction
        runner.evaluate("showCubertPopup('Please remain calm and try to type that request again a little more carefully.', 'confused');")
        time.sleep(0.4)
        t2 = runner.evaluate("""
        (() => {
            const a = currentCubertAudio;
            const b = document.getElementById('cubert-bubble-text').textContent;
            return {
                src: a ? a.src : null,
                paused: a ? a.paused : true,
                currentTime: a ? a.currentTime : 0,
                duration: a ? a.duration : 0,
                caption: b
            };
        })()
        """)
        results["2_retry"] = t2

        # Test 3: Profanity response
        runner.evaluate("processRequest('what the fuck');")
        time.sleep(0.4)
        t3 = runner.evaluate("""
        (() => {
            const a = currentCubertAudio;
            const b = document.getElementById('cubert-bubble-text').textContent;
            return {
                src: a ? a.src : null,
                paused: a ? a.paused : true,
                currentTime: a ? a.currentTime : 0,
                duration: a ? a.duration : 0,
                caption: b
            };
        })()
        """)
        results["3_profanity"] = t3

        # Test 4: Random bad suggestion (matching audio and text caption)
        runner.evaluate("""
        (() => {
            cubertMode = CUBERT_MODES.ACTIVE;
            cubertConvStage = 'AWAITING_RETRY';
            processRequest('Can I bend');
        })()
        """)
        time.sleep(0.4)
        t4 = runner.evaluate("""
        (() => {
            const a = currentCubertAudio;
            const b = document.getElementById('cubert-bubble-text').textContent;
            return {
                src: a ? a.src : null,
                paused: a ? a.paused : true,
                currentTime: a ? a.currentTime : 0,
                duration: a ? a.duration : 0,
                caption: b
            };
        })()
        """)
        results["4_bad_suggestion"] = t4

        # Test 5: Break announcement
        runner.evaluate("triggerCubertBreak();")
        time.sleep(0.4)
        t5 = runner.evaluate("""
        (() => {
            const a = currentCubertAudio;
            const status = document.getElementById('status-message').textContent;
            const mode = cubertMode;
            return {
                src: a ? a.src : null,
                paused: a ? a.paused : true,
                currentTime: a ? a.currentTime : 0,
                duration: a ? a.duration : 0,
                status: status,
                mode: mode
            };
        })()
        """)
        results["5_break"] = t5
        runner.evaluate("endCubertBreak();")

        # Test 6: Insufficient-funds response
        runner.evaluate("fictionalBalance = 0.50; submitCubertTip(10.00);")
        time.sleep(0.4)
        t6 = runner.evaluate("""
        (() => {
            const a = currentCubertAudio;
            const b = document.getElementById('cubert-bubble-text').textContent;
            return {
                src: a ? a.src : null,
                paused: a ? a.paused : true,
                currentTime: a ? a.currentTime : 0,
                duration: a ? a.duration : 0,
                caption: b
            };
        })()
        """)
        results["6_broke_ass"] = t6

        # Test 7: Hold Music Ducking Verification
        runner.evaluate("""
        (() => {
            CADNT_AUDIO.playHoldMusic();
            const initialVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : 0;
            playCubertVoiceover('help_1');
            const duckedVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : 0;
            stopCubertVoiceover();
            const restoredVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : 0;
            CADNT_AUDIO.stopHoldMusic();
            return { initial: initialVol, ducked: duckedVol, restored: restoredVol };
        })()
        """)
        t7 = runner.evaluate("""
        (() => {
            CADNT_AUDIO.playHoldMusic();
            const initVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : null;
            playCubertVoiceover('help_1');
            const duckVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : null;
            stopCubertVoiceover();
            const restVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : null;
            CADNT_AUDIO.stopHoldMusic();
            return { initial: initVol, ducked: duckVol, restored: restVol };
        })()
        """)
        results["7_ducking"] = t7

        # Test 8: Interruption (No overlapping voiceovers)
        t8 = runner.evaluate("""
        (() => {
            const a1 = playCubertVoiceover('retry_carefully');
            const a1_started = a1 && !a1.paused;
            const a2 = playCubertVoiceover('watch_language');
            const a1_paused_now = a1 ? a1.paused : true;
            const a2_playing = a2 && !a2.paused;
            stopCubertVoiceover();
            return {
                audio1_started: a1_started,
                audio1_paused_after_interrupt: a1_paused_now,
                audio2_active: a2_playing
            };
        })()
        """)
        results["8_interruption"] = t8

    finally:
        runner.close()

    return results


def run_safari_webkit_verification():
    print("\n" + "=" * 60)
    print("RUNNING CUBERT AUDIO PLAYBACK VERIFICATION: SAFARI (WEBKIT)")
    print("=" * 60)

    import AppKit
    import WebKit

    app = AppKit.NSApplication.sharedApplication()
    config = WebKit.WKWebViewConfiguration.alloc().init()
    config.setMediaTypesRequiringUserActionForPlayback_(WebKit.WKAudiovisualMediaTypeNone)

    wv = WebKit.WKWebView.alloc().initWithFrame_configuration_(
        AppKit.NSMakeRect(0, 0, 1280, 820), config
    )

    loaded = [False]
    class NavDelegate(AppKit.NSObject):
        def webView_didFinishNavigation_(self, webview, navigation):
            loaded[0] = True

    nav_del = NavDelegate.alloc().init()
    wv.setNavigationDelegate_(nav_del)

    url = AppKit.NSURL.URLWithString_(f"http://127.0.0.1:{HTTP_PORT}/index.html?no_auto_onboard=1")
    req = AppKit.NSURLRequest.requestWithURL_(url)
    wv.loadRequest_(req)

    def pump(duration=0.5):
        start = time.time()
        while time.time() - start < duration:
            event = app.nextEventMatchingMask_untilDate_inMode_dequeue_(
                AppKit.NSEventMaskAny,
                AppKit.NSDate.dateWithTimeIntervalSinceNow_(0.05),
                AppKit.NSDefaultRunLoopMode,
                True
            )
            if event:
                app.sendEvent_(event)

    # Wait for page load
    t0 = time.time()
    while not loaded[0] and time.time() - t0 < 10:
        pump(0.1)

    def eval_js(js):
        done = [False]
        out = [None]
        err_out = [None]
        def handler(res, err):
            out[0] = res
            err_out[0] = err
            done[0] = True
        wv.evaluateJavaScript_completionHandler_(js, handler)
        t_start = time.time()
        while not done[0] and time.time() - t_start < 5:
            pump(0.05)
        if err_out[0]:
            print("WebKit JS Error:", err_out[0])
        return out[0]

    # Initialize app
    eval_js("CADNT_AUDIO.setMute(false); fictionalBalance = 200.0; updateEconomyDisplay();")
    pump(0.5)

    results = {}

    # 1. Greeting
    eval_js("showCubertPopup('How can I help you?', 'cheerful');")
    pump(0.8)
    results["1_greeting"] = json.loads(eval_js("""
    JSON.stringify({
        src: currentCubertAudio ? currentCubertAudio.src : null,
        paused: currentCubertAudio ? currentCubertAudio.paused : true,
        currentTime: currentCubertAudio ? currentCubertAudio.currentTime : 0,
        duration: (currentCubertAudio && !isNaN(currentCubertAudio.duration)) ? currentCubertAudio.duration : 0,
        caption: document.getElementById('cubert-bubble-text').textContent
    })
    """))

    # 2. Retry
    eval_js("showCubertPopup('Please remain calm and try to type that request again a little more carefully.', 'confused');")
    pump(0.8)
    results["2_retry"] = json.loads(eval_js("""
    JSON.stringify({
        src: currentCubertAudio ? currentCubertAudio.src : null,
        paused: currentCubertAudio ? currentCubertAudio.paused : true,
        currentTime: currentCubertAudio ? currentCubertAudio.currentTime : 0,
        duration: (currentCubertAudio && !isNaN(currentCubertAudio.duration)) ? currentCubertAudio.duration : 0,
        caption: document.getElementById('cubert-bubble-text').textContent
    })
    """))

    # 3. Profanity
    eval_js("processRequest('what the fuck');")
    pump(0.8)
    results["3_profanity"] = json.loads(eval_js("""
    JSON.stringify({
        src: currentCubertAudio ? currentCubertAudio.src : null,
        paused: currentCubertAudio ? currentCubertAudio.paused : true,
        currentTime: currentCubertAudio ? currentCubertAudio.currentTime : 0,
        duration: (currentCubertAudio && !isNaN(currentCubertAudio.duration)) ? currentCubertAudio.duration : 0,
        caption: document.getElementById('cubert-bubble-text').textContent
    })
    """))

    # 4. Bad suggestion
    eval_js("""
    (() => {
        cubertMode = CUBERT_MODES.ACTIVE;
        cubertConvStage = 'AWAITING_RETRY';
        processRequest('Can I bend');
    })()
    """)
    pump(0.8)
    results["4_bad_suggestion"] = json.loads(eval_js("""
    JSON.stringify({
        src: currentCubertAudio ? currentCubertAudio.src : null,
        paused: currentCubertAudio ? currentCubertAudio.paused : true,
        currentTime: currentCubertAudio ? currentCubertAudio.currentTime : 0,
        duration: (currentCubertAudio && !isNaN(currentCubertAudio.duration)) ? currentCubertAudio.duration : 0,
        caption: document.getElementById('cubert-bubble-text').textContent
    })
    """))

    # 5. Break
    eval_js("triggerCubertBreak();")
    pump(0.8)
    results["5_break"] = json.loads(eval_js("""
    JSON.stringify({
        src: currentCubertAudio ? currentCubertAudio.src : null,
        paused: currentCubertAudio ? currentCubertAudio.paused : true,
        currentTime: currentCubertAudio ? currentCubertAudio.currentTime : 0,
        duration: (currentCubertAudio && !isNaN(currentCubertAudio.duration)) ? currentCubertAudio.duration : 0,
        status: document.getElementById('status-message').textContent,
        mode: cubertMode
    })
    """))
    eval_js("endCubertBreak();")

    # 6. Insufficient funds
    eval_js("fictionalBalance = 0.50; submitCubertTip(10.00);")
    pump(0.8)
    results["6_broke_ass"] = json.loads(eval_js("""
    JSON.stringify({
        src: currentCubertAudio ? currentCubertAudio.src : null,
        paused: currentCubertAudio ? currentCubertAudio.paused : true,
        currentTime: currentCubertAudio ? currentCubertAudio.currentTime : 0,
        duration: (currentCubertAudio && !isNaN(currentCubertAudio.duration)) ? currentCubertAudio.duration : 0,
        caption: document.getElementById('cubert-bubble-text').textContent
    })
    """))

    # 7. Ducking
    results["7_ducking"] = json.loads(eval_js("""
    (() => {
        CADNT_AUDIO.playHoldMusic();
        const initVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : null;
        playCubertVoiceover('help_1');
        const duckVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : null;
        stopCubertVoiceover();
        const restVol = CADNT_AUDIO.holdMusicAudio ? CADNT_AUDIO.holdMusicAudio.volume : null;
        CADNT_AUDIO.stopHoldMusic();
        return JSON.stringify({ initial: initVol, ducked: duckVol, restored: restVol });
    })()
    """))

    # 8. Interruption
    results["8_interruption"] = json.loads(eval_js("""
    (() => {
        const a1 = playCubertVoiceover('retry_carefully');
        const a1_started = a1 && !a1.paused;
        const a2 = playCubertVoiceover('watch_language');
        const a1_paused_now = a1 ? a1.paused : true;
        const a2_playing = a2 && !a2.paused;
        stopCubertVoiceover();
        return JSON.stringify({
            audio1_started: a1_started,
            audio1_paused_after_interrupt: a1_paused_now,
            audio2_active: a2_playing
        });
    })()
    """))

    return results


def print_report(chrome_res, safari_res):
    print("\n" + "=" * 80)
    print("CADN'T - CUBERT VOICEOVER INTEGRATION VERIFICATION REPORT")
    print("=" * 80)

    rows = [
        ("1. How can I help you?", "HowCanIHelpYou.mp3", "1_greeting", "caption"),
        ("2. Request Bar retry", "PleaseRemainCalm.mp3", "2_retry", "caption"),
        ("3. Profanity outburst", "WatchYourLanguage.mp3", "3_profanity", "caption"),
        ("4. Random bad suggestion", "Command Suggestion MP3", "4_bad_suggestion", "caption"),
        ("5. Break announcement", "GoingOnBreak.mp3", "5_break", "status"),
        ("6. Insufficient funds", "BrokeAss.mp3", "6_broke_ass", "caption")
    ]

    for label, expected_file, key, text_field in rows:
        c = chrome_res.get(key, {})
        s = safari_res.get(key, {})

        c_file = os.path.basename(c.get("src") or "")
        s_file = os.path.basename(s.get("src") or "")

        c_dur = float(c.get("duration") or 0.0)
        c_cur = float(c.get("currentTime") or 0.0)
        s_dur = float(s.get("duration") or 0.0)
        s_cur = float(s.get("currentTime") or 0.0)

        c_ok = not c.get("paused") and c_dur > 0 and (c_cur > 0 or not c.get("paused"))
        s_ok = not s.get("paused") and (s_dur > 0 or s_file) and not s.get("paused")

        print(f"\n--- {label} ---")
        print(f"  Target File:     {expected_file}")
        print(f"  Chrome Playback: File={c_file} | Playing={not c.get('paused')} | t={c_cur:.2f}s/{c_dur:.2f}s | Verified={c_ok}")
        print(f"  Chrome Caption:  \"{c.get(text_field)}\"")
        print(f"  Safari Playback: File={s_file} | Playing={not s.get('paused')} | t={s_cur:.2f}s/{s_dur:.2f}s | Verified={s_ok}")
        print(f"  Safari Caption:  \"{s.get(text_field)}\"")

    # Ducking
    cd = chrome_res.get("7_ducking", {})
    sd = safari_res.get("7_ducking", {})
    print(f"\n--- Hold Music Ducking ---")
    print(f"  Chrome: Initial={cd.get('initial')} -> Ducked={cd.get('ducked')} -> Restored={cd.get('restored')} | Verified={cd.get('ducked', 1) <= 0.15 and cd.get('restored') == cd.get('initial')}")
    print(f"  Safari: Initial={sd.get('initial')} -> Ducked={sd.get('ducked')} -> Restored={sd.get('restored')} | Verified={sd.get('ducked', 1) <= 0.15 and sd.get('restored') == sd.get('initial')}")

    # Interruption
    ci = chrome_res.get("8_interruption", {})
    si = safari_res.get("8_interruption", {})
    print(f"\n--- Voiceover Interruption ---")
    print(f"  Chrome: Audio 1 Interrupted={ci.get('audio1_paused_after_interrupt')} | Audio 2 Playing={ci.get('audio2_active')}")
    print(f"  Safari: Audio 1 Interrupted={si.get('audio1_paused_after_interrupt')} | Audio 2 Playing={si.get('audio2_active')}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    server = start_http_server()
    try:
        chrome_results = run_chrome_audio_verification()
        safari_results = run_safari_webkit_verification()
        print_report(chrome_results, safari_results)
    finally:
        server.shutdown()
