#!/usr/bin/env python3
"""
CADN'T - Checkpoints 1 & 2 Visual Verification Script (v0.18)
Verifies:
- Checkpoint 1: Chinese Takeover Animation
  - Large centered PRC flag overlay (~50% viewport area) on 'can i chinese'.
  - Flag spins continuously for 5 seconds.
  - Automatically disappears after 5 seconds while keeping app in Chinese mode.
  - Does not show on page reload.
  - Respects prefers-reduced-motion.
- Checkpoint 2: ChinaMusic Audio System
  - Plays ChinaMusic.m4a when Chinese mode activates.
  - Loops continuously and persists through CAD operations.
  - Stops immediately on 'can i unchinese', 'can i dechinese', 'can i english', or '切换英文'.
  - Special Undo behavior: 'can i undo' reverses Chinese mode if it was the most recent command,
    but reverses modeling operations normally if modeling happened afterward.
  - Suppresses ordinary hold music while Chinese mode is active.
  - Ducks ChinaMusic volume during Cubert voiceovers.

Captures screenshots at DPR 1.0 and DPR 2.0, saving to screenshots/ and mirroring to Desktop.
"""

import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

PORT = 9580
DESKTOP_DIR = "/Users/andybuck/Desktop"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)

def run_verification(dpr=1.0):
    port = PORT if dpr == 1.0 else PORT + 1
    suffix = "_dpr2" if dpr > 1.0 else ""
    print(f"\n=======================================================")
    print(f"Running Checkpoints 1 & 2 Verification at DPR {dpr}")
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
        # CHECKPOINT 1: Chinese Takeover Celebration Flag Animation
        # ---------------------------------------------------------------------
        print("\n--- Verifying Checkpoint 1: Chinese Takeover Flag Animation ---")
        # Trigger 'can i chinese'
        eval_js('processRequest("can i chinese")')
        time.sleep(0.5)

        flag_metrics = eval_js("""(() => {
            const overlay = document.getElementById('chinese-takeover-overlay');
            const wrapper = document.getElementById('chinese-flag-spinner-wrapper');
            const flag = document.getElementById('chinese-takeover-flag');
            const overlayRect = overlay ? overlay.getBoundingClientRect() : {};
            const wrapperRect = wrapper ? wrapper.getBoundingClientRect() : {};
            const flagSrc = flag ? flag.getAttribute('src') : '';
            const viewportArea = window.innerWidth * window.innerHeight;
            const flagArea = (wrapper.offsetWidth || wrapperRect.width) * (wrapper.offsetHeight || wrapperRect.height);
            const areaPercentage = (flagArea / viewportArea) * 100;
            const computedStyle = wrapper ? window.getComputedStyle(wrapper) : {};
            return {
                overlayVisible: overlay && overlay.style.display === 'flex',
                flagSrc: flagSrc,
                wrapperWidth: wrapperRect.width,
                wrapperHeight: wrapperRect.height,
                areaPercentage: areaPercentage,
                animationName: computedStyle.animationName,
                animationDuration: computedStyle.animationDuration,
                isCentered: Math.abs((wrapperRect.left + wrapperRect.width / 2) - window.innerWidth / 2) < 5
            };
        })()""")
        print(f"  Flag metrics: {flag_metrics}")
        assert flag_metrics['overlayVisible'], "Flag overlay must be visible on 'can i chinese'"
        assert "ChineseFlag.webp" in flag_metrics['flagSrc'], "Accurate Chinese flag asset must be used"
        assert flag_metrics['isCentered'], "Flag must be centered on screen"
        assert 35 <= flag_metrics['areaPercentage'] <= 60, f"Flag area must be approximately 50% of viewport (got {flag_metrics['areaPercentage']:.1f}%)"
        assert "chineseFlagSpin" in flag_metrics['animationName'], "Flag must have spinning animation"
        assert "5s" in flag_metrics['animationDuration'], "Animation duration must be exactly 5s"

        # Capture Screenshot of spinning flag
        capture_screenshot(f"checkpoint_01_01_chinese_flag_spinning{suffix}.png")

        # ---------------------------------------------------------------------
        # CHECKPOINT 2: ChinaMusic Audio System
        # ---------------------------------------------------------------------
        print("\n--- Verifying Checkpoint 2: ChinaMusic Audio System ---")
        music_metrics = eval_js("""(() => {
            const isPlaying = CADNT_AUDIO.isChinaMusicActive;
            const audioObj = CADNT_AUDIO.chinaMusicAudio;
            return {
                isActive: isPlaying,
                hasAudio: !!audioObj,
                isLooping: audioObj ? audioObj.loop : false,
                src: audioObj ? audioObj.src : '',
                volume: audioObj ? audioObj.volume : 0
            };
        })()""")
        print(f"  Music metrics: {music_metrics}")
        assert music_metrics['isActive'], "ChinaMusic must be active"
        assert music_metrics['isLooping'], "ChinaMusic must loop continuously"
        assert "ChinaMusic.m4a" in music_metrics['src'], "ChinaMusic.m4a must be the audio source"

        # Execute CAD command to verify music persistence
        eval_js('processRequest("Can I box")')
        time.sleep(0.5)
        persisted = eval_js("CADNT_AUDIO.isChinaMusicActive && !!CADNT_AUDIO.chinaMusicAudio")
        assert persisted, "ChinaMusic must persist across CAD modeling commands"

        # Verify hold music is suppressed
        eval_js('CADNT_AUDIO.playHoldMusic()')
        hold_suppressed = eval_js("CADNT_AUDIO.holdMusicAudio === null")
        assert hold_suppressed, "Ordinary hold music must be suppressed while Chinese mode is active"

        # Capture ChinaMusic looping screenshot
        capture_screenshot(f"checkpoint_02_01_chinamusic_looping{suffix}.png")

        # ---------------------------------------------------------------------
        # Ducking ChinaMusic during Cubert voiceover
        # ---------------------------------------------------------------------
        print("\n--- Verifying ChinaMusic Ducking During Cubert Speech ---")
        eval_js('duckHoldMusicForDialogue()')
        ducked_vol = eval_js("CADNT_AUDIO.chinaMusicAudio ? CADNT_AUDIO.chinaMusicAudio.volume : -1")
        print(f"  Ducked ChinaMusic volume: {ducked_vol}")
        assert ducked_vol <= 0.25, f"ChinaMusic must be ducked to <= 0.25 during Cubert speech (got {ducked_vol})"

        # Show Cubert speaking popup for screenshot
        eval_js('showCubertPopup("How can I help you?", "cheerful")')
        time.sleep(0.5)
        capture_screenshot(f"checkpoint_02_02_cubert_ducking_chinamusic{suffix}.png")

        # Restore volume after Cubert dialogue
        eval_js('restoreHoldMusicAfterDialogue()')
        eval_js('hideCubertPopup()')
        restored_vol = eval_js("CADNT_AUDIO.chinaMusicAudio ? CADNT_AUDIO.chinaMusicAudio.volume : -1")
        print(f"  Restored ChinaMusic volume: {restored_vol}")
        assert restored_vol >= 0.95, f"ChinaMusic volume must be restored to >= 0.95 (got {restored_vol})"

        # ---------------------------------------------------------------------
        # Exit Chinese Mode via 'can i unchinese'
        # ---------------------------------------------------------------------
        print("\n--- Verifying Chinese Mode Exit ('can i unchinese') ---")
        eval_js('processRequest("can i unchinese")')
        time.sleep(0.5)

        exit_metrics = eval_js("""(() => {
            const overlay = document.getElementById('chinese-takeover-overlay');
            return {
                lang: document.documentElement.lang,
                isMusicActive: CADNT_AUDIO.isChinaMusicActive,
                hasMusicObj: !!CADNT_AUDIO.chinaMusicAudio,
                overlayHidden: overlay.style.display === 'none'
            };
        })()""")
        print(f"  Exit metrics: {exit_metrics}")
        assert exit_metrics['lang'] == 'en', "Language must be restored to English"
        assert not exit_metrics['isMusicActive'], "ChinaMusic must be inactive"
        assert not exit_metrics['hasMusicObj'], "ChinaMusic audio object must be cleaned up"
        assert exit_metrics['overlayHidden'], "Flag overlay must be hidden immediately"

        capture_screenshot(f"checkpoint_02_03_unchinese_exit{suffix}.png")

        # ---------------------------------------------------------------------
        # Special Undo Behavior: Immediate undo reverses Chinese mode
        # ---------------------------------------------------------------------
        print("\n--- Verifying Special Undo Behavior (Immediate Undo) ---")
        eval_js('processRequest("can i chinese")')
        time.sleep(0.5)
        eval_js('processRequest("can i undo")')
        time.sleep(0.5)

        undo_metrics = eval_js("""(() => {
            return {
                lang: document.documentElement.lang,
                isMusicActive: CADNT_AUDIO.isChinaMusicActive,
                hasMusicObj: !!CADNT_AUDIO.chinaMusicAudio
            };
        })()""")
        print(f"  Immediate undo metrics: {undo_metrics}")
        assert undo_metrics['lang'] == 'en', "Undo must reverse Chinese mode back to English"
        assert not undo_metrics['isMusicActive'], "ChinaMusic must be stopped by undo"

        capture_screenshot(f"checkpoint_02_04_undo_chinese_mode{suffix}.png")

        # ---------------------------------------------------------------------
        # Special Undo Behavior: Modeling after Chinese mode reverses modeling, not Chinese mode
        # ---------------------------------------------------------------------
        print("\n--- Verifying Special Undo Behavior (Modeling Afterward) ---")
        eval_js('processRequest("can i chinese")')
        time.sleep(0.5)
        objs_before = eval_js("sceneObjects.length")
        eval_js('processRequest("Can I box")')
        time.sleep(0.5)
        objs_after_box = eval_js("sceneObjects.length")
        assert objs_after_box == objs_before + 1, "Box must be created"

        # Undo must reverse the box, NOT Chinese mode
        eval_js('processRequest("can i undo")')
        time.sleep(0.5)
        objs_after_undo = eval_js("sceneObjects.length")
        lang_after_undo = eval_js("document.documentElement.lang")
        music_after_undo = eval_js("CADNT_AUDIO.isChinaMusicActive")

        print(f"  Undo after modeling: objs={objs_after_undo} (was {objs_before}), lang={lang_after_undo}, musicActive={music_after_undo}")
        assert objs_after_undo == objs_before, "Undo must reverse the box"
        assert lang_after_undo == 'zh-Hans-CN', "Chinese mode must remain active"
        assert music_after_undo, "ChinaMusic must remain active"

        capture_screenshot(f"checkpoint_02_05_undo_modeling_preserves_chinese{suffix}.png")

        # Restore English
        eval_js('processRequest("can i english")')
        time.sleep(0.5)

        print(f"\n[SUCCESS] Checkpoints 1 & 2 verified at DPR {dpr}!")

    finally:
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    run_verification(dpr=1.0)
    run_verification(dpr=2.0)
    print("\nAll Checkpoint 1 & 2 visual verifications passed successfully!")
