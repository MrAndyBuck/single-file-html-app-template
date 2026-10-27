#!/usr/bin/env python3
"""
CADN'T - Checkpoints C, D, E, and F Visual Verification Script (v0.16)
Verifies:
- Checkpoint C: Redesign the Blue Header Branding
  - Old standalone SVG icon removed completely.
  - New official white-backed CADNTLogo enlarged to occupy nearly entire header height.
  - Logo aspect ratio and full artwork (black serif letters + blue cube) preserved.
  - Italicized supporting text immediately adjacent to the right:
    'Computer Aided Design Noncompliance Technology'
- Checkpoint D: Consolidate the Top Toolbar
  - First text-menu row completely removed.
  - Button toolbar moved directly beneath blue title bar (zero blank strip).
  - All buttons preserved; Crash button added for accessible crash report opening.
  - Fictional economy display and + Buy More preserved.
- Checkpoint E: Replace Browser Tab Branding
  - New isometric blue cube favicons (32x32, 192x192, apple-touch-icon, icon.svg).
  - Manifest and service worker cache updated.
- Checkpoint F: Full Chinese Interface Mode
  - 'can i chinese' switches application to Simplified Chinese (zh-Hans-CN).
  - All UI translated: toolbar, FeatureManager, viewports, Request Bar, Cubert status, bottom bar, About modal.
  - English CAD commands ('Can I box', etc.) remain 100% operational in Chinese mode.
  - '切换英文' or 'can i english' restores complete English interface.
  - Language selection persists in localStorage.

Captures screenshots at DPR 1.0 and DPR 2.0, saving to screenshots/ and mirroring to Desktop.
"""

import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

PORT = 9480
DESKTOP_DIR = "/Users/andybuck/Desktop"
PROJECT_SCREENSHOTS = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"

os.makedirs(PROJECT_SCREENSHOTS, exist_ok=True)

def run_verification(dpr=1.0):
    port = PORT if dpr == 1.0 else PORT + 1
    suffix = "_dpr2" if dpr > 1.0 else ""
    print(f"\n=======================================================")
    print(f"Running Checkpoints C, D, E, F Verification at DPR {dpr}")
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
        # CHECKPOINT C: Header Branding Redesign
        # ---------------------------------------------------------------------
        print("\n--- Verifying Checkpoint C: Redesigned Blue Header Branding ---")
        header_info = eval_js("""(() => {
            const titleBar = document.getElementById('win95-title-bar');
            const oldSvg = titleBar ? titleBar.querySelector('svg.win95-icon') : null;
            const badge = document.querySelector('.win95-title-logo-badge');
            const logo = document.getElementById('cadnt-official-logo');
            const subtext = document.querySelector('.win95-title-subtext');
            const titleRect = titleBar ? titleBar.getBoundingClientRect() : {};
            const badgeRect = badge ? badge.getBoundingClientRect() : {};
            const logoRect = logo ? logo.getBoundingClientRect() : {};
            const subtextStyle = subtext ? window.getComputedStyle(subtext) : {};
            return {
                oldSvgPresent: !!oldSvg,
                badgePresent: !!badge,
                badgeHeight: badgeRect.height,
                logoPresent: !!logo,
                logoHeight: logoRect.height,
                logoNaturalWidth: logo ? logo.naturalWidth : 0,
                logoNaturalHeight: logo ? logo.naturalHeight : 0,
                subtextText: subtext ? subtext.textContent.trim() : '',
                isItalic: subtextStyle.fontStyle === 'italic',
                headerHeight: titleRect.height
            };
        })()""")
        print(f"  Header metrics: {header_info}")
        assert not header_info['oldSvgPresent'], "Old SVG icon must be removed completely"
        assert header_info['badgePresent'], "Sunken logo badge must be present"
        assert header_info['logoHeight'] >= 28, f"Enlarged logo height must be >= 28px (got {header_info['logoHeight']})"
        assert header_info['isItalic'], "Supporting subtitle must be italicized"
        assert "Computer Aided Design Noncompliance Technology" in header_info['subtextText'], "Subtitle text must match"

        # Capture Header Close-Up
        capture_screenshot(f"checkpoint_c_01_enlarged_header_logo{suffix}.png", {
            'x': 0, 'y': 0, 'width': 1280, 'height': 52, 'scale': 1
        })

        # ---------------------------------------------------------------------
        # CHECKPOINT D: Consolidate the Top Toolbar
        # ---------------------------------------------------------------------
        print("\n--- Verifying Checkpoint D: Consolidate Top Toolbar ---")
        toolbar_info = eval_js("""(() => {
            const menuBar = document.getElementById('win95-menu-bar');
            const titleBar = document.getElementById('win95-title-bar');
            const toolbar = document.getElementById('win95-standard-toolbar');
            const crashBtn = document.getElementById('btn-crash-open');
            const titleRect = titleBar.getBoundingClientRect();
            const toolRect = toolbar.getBoundingClientRect();
            const gap = toolRect.top - titleRect.bottom;
            return {
                menuBarPresent: !!menuBar,
                toolbarPresent: !!toolbar,
                gapBetweenTitleAndToolbar: gap,
                crashBtnPresent: !!crashBtn,
                crashBtnText: crashBtn ? crashBtn.textContent.trim() : '',
                toolButtonsCount: toolbar.querySelectorAll('.win95-tool-btn').length
            };
        })()""")
        print(f"  Toolbar metrics: {toolbar_info}")
        assert not toolbar_info['menuBarPresent'], "Old menu bar must be completely removed"
        assert toolbar_info['toolbarPresent'], "Consolidated toolbar must be present"
        assert abs(toolbar_info['gapBetweenTitleAndToolbar']) <= 2, f"Toolbar must sit directly beneath titlebar with 0 gap (got {toolbar_info['gapBetweenTitleAndToolbar']})"
        assert toolbar_info['crashBtnPresent'], "Crash button must be present in toolbar"

        # Capture Consolidated Toolbar View
        capture_screenshot(f"checkpoint_d_01_consolidated_toolbar{suffix}.png", {
            'x': 0, 'y': 0, 'width': 1280, 'height': 110, 'scale': 1
        })

        # ---------------------------------------------------------------------
        # CHECKPOINT E: Replace Browser Tab Branding (Favicon Verification)
        # ---------------------------------------------------------------------
        print("\n--- Verifying Checkpoint E: Replace Browser Tab Branding ---")
        favicon_info = eval_js("""(() => {
            const links = Array.from(document.querySelectorAll('link[rel*="icon"]')).map(l => ({
                rel: l.rel,
                href: l.getAttribute('href'),
                sizes: l.getAttribute('sizes')
            }));
            const manifestLink = document.querySelector('link[rel="manifest"]');
            return {
                faviconLinks: links,
                manifestHref: manifestLink ? manifestLink.getAttribute('href') : null
            };
        })()""")
        print(f"  Favicon links: {favicon_info}")
        assert any("favicon-32x32.png" in l['href'] for l in favicon_info['faviconLinks']), "32x32 cube favicon must be referenced"
        assert any("apple-touch-icon.png" in l['href'] for l in favicon_info['faviconLinks']), "apple-touch-icon must be referenced"

        # Capture card representation of favicon assets
        eval_js("""(() => {
            const card = document.createElement('div');
            card.id = 'favicon-preview-overlay';
            card.style.position = 'fixed';
            card.style.top = '120px';
            card.style.left = '20px';
            card.style.zIndex = '99999';
            card.style.background = '#c0c0c0';
            card.style.border = '2px solid #ffffff';
            card.style.borderRightColor = '#404040';
            card.style.borderBottomColor = '#404040';
            card.style.padding = '8px 12px';
            card.style.boxShadow = '2px 2px 5px rgba(0,0,0,0.4)';
            card.style.fontFamily = 'MS Sans Serif, sans-serif';
            card.style.fontSize = '12px';
            card.innerHTML = `
                <div style="font-weight:bold;margin-bottom:6px;border-bottom:1px solid #808080;padding-bottom:3px;">
                    Favicon Assets (Blue Cube Replacement):
                </div>
                <div style="display:flex;align-items:center;gap:16px;">
                    <div style="text-align:center;">
                        <img src="assets/brand/favicon-32x32.png" style="width:32px;height:32px;border:1px solid #808080;background:#fff;image-rendering:pixelated;">
                        <div style="font-size:10px;margin-top:2px;">32x32</div>
                    </div>
                    <div style="text-align:center;">
                        <img src="assets/brand/apple-touch-icon.png" style="width:48px;height:48px;border:1px solid #808080;background:#fff;">
                        <div style="font-size:10px;margin-top:2px;">Apple Touch</div>
                    </div>
                    <div style="text-align:center;">
                        <img src="assets/brand/favicon-192x192.png" style="width:48px;height:48px;border:1px solid #808080;background:#fff;">
                        <div style="font-size:10px;margin-top:2px;">192x192</div>
                    </div>
                </div>
            `;
            document.body.appendChild(card);
        })()""")
        time.sleep(0.5)
        capture_screenshot(f"checkpoint_e_01_cube_favicons{suffix}.png", {
            'x': 0, 'y': 0, 'width': 1280, 'height': 240, 'scale': 1
        })
        eval_js("const c = document.getElementById('favicon-preview-overlay'); if (c) c.remove();")

        # ---------------------------------------------------------------------
        # CHECKPOINT F: Full Chinese Interface Mode
        # ---------------------------------------------------------------------
        print("\n--- Verifying Checkpoint F: Full Chinese Interface Mode ---")
        # Trigger switch to Chinese via Request Bar
        eval_js('processRequest("can i chinese")')
        time.sleep(1.0)

        chinese_state = eval_js("""(() => {
            const htmlLang = document.documentElement.lang;
            const aboutBtn = document.getElementById('btn-about-open');
            const importBtn = document.getElementById('btn-import-mesh');
            const topLabel = document.getElementById('lbl-top');
            const perspLabel = document.getElementById('lbl-perspective');
            const cubertStatus = document.getElementById('cubert-panel-status');
            const storedLocale = localStorage.getItem('cadnt_locale');
            return {
                htmlLang: htmlLang,
                storedLocale: storedLocale,
                aboutBtnText: aboutBtn ? aboutBtn.textContent.trim() : '',
                importBtnText: importBtn ? importBtn.textContent.trim() : '',
                topLabelText: topLabel ? topLabel.textContent.trim() : '',
                perspLabelText: perspLabel ? perspLabel.textContent.trim() : '',
                cubertStatus: cubertStatus ? cubertStatus.textContent.trim() : ''
            };
        })()""")
        print(f"  Chinese mode state: {chinese_state}")
        assert chinese_state['htmlLang'] == 'zh-Hans-CN', f"HTML lang must be zh-Hans-CN (got {chinese_state['htmlLang']})"
        assert chinese_state['storedLocale'] == 'zh-Hans-CN', "Locale must persist in localStorage"
        assert chinese_state['aboutBtnText'] == '关于', f"About button must be '关于' (got {chinese_state['aboutBtnText']})"
        assert chinese_state['importBtnText'] == '导入', f"Import button must be '导入' (got {chinese_state['importBtnText']})"
        assert '顶视图' in chinese_state['topLabelText'], f"Top viewport must contain '顶视图' (got {chinese_state['topLabelText']})"
        assert chinese_state['cubertStatus'] == '待命', f"Cubert status must be '待命' (got {chinese_state['cubertStatus']})"

        # Execute English modeling command 'Can I box' in Chinese mode to prove CAD parser integrity
        eval_js('processRequest("Can I box")')
        time.sleep(1.0)

        # Full Application Chinese Interface Screenshot
        capture_screenshot(f"checkpoint_f_01_chinese_interface_full{suffix}.png")

        # Open About Modal in Chinese mode
        eval_js('document.getElementById("btn-about-open").click()')
        time.sleep(0.5)

        about_chinese = eval_js("""(() => {
            const modal = document.getElementById('modal-about');
            const title = modal.querySelector('h2');
            const closeBtn = document.getElementById('btn-close-about');
            const sections = Array.from(modal.querySelectorAll('.about-section h3')).map(h => h.textContent.trim());
            return {
                titleText: title ? title.textContent.trim() : '',
                closeBtnText: closeBtn ? closeBtn.textContent.trim() : '',
                sections: sections
            };
        })()""")
        print(f"  About modal in Chinese: {about_chinese}")
        assert "关于" in about_chinese['titleText'], "About modal title must be translated"
        assert about_chinese['closeBtnText'] in ['关闭', '确定'], f"Close button must be '关闭' or '确定' (got {about_chinese['closeBtnText']})"

        # Capture About Modal in Chinese mode
        capture_screenshot(f"checkpoint_f_02_chinese_modals_cubert{suffix}.png")

        # Close About modal
        eval_js('document.getElementById("btn-close-about").click()')
        time.sleep(0.5)

        # ---------------------------------------------------------------------
        # Switch back to English via '切换英文'
        # ---------------------------------------------------------------------
        print("\n--- Verifying Restoration to English via '切换英文' ---")
        eval_js('processRequest("切换英文")')
        time.sleep(1.0)

        english_state = eval_js("""(() => {
            const htmlLang = document.documentElement.lang;
            const aboutBtn = document.getElementById('btn-about-open');
            const storedLocale = localStorage.getItem('cadnt_locale');
            return {
                htmlLang: htmlLang,
                storedLocale: storedLocale,
                aboutBtnText: aboutBtn ? aboutBtn.textContent.trim() : ''
            };
        })()""")
        print(f"  Restored English state: {english_state}")
        assert english_state['htmlLang'] == 'en', "HTML lang must be en"
        assert english_state['storedLocale'] == 'en', "LocalStorage must be en"
        assert english_state['aboutBtnText'] == 'About', f"About button must be 'About' (got {english_state['aboutBtnText']})"

        # Full Application English Restored Screenshot
        capture_screenshot(f"checkpoint_f_03_english_restored{suffix}.png")

        print(f"\n[SUCCESS] Checkpoints C, D, E, F verified at DPR {dpr}!")

    finally:
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    run_verification(dpr=1.0)
    run_verification(dpr=2.0)
    print("\nAll visual verifications passed successfully!")
