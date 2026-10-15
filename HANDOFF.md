# HANDOFF.md — CADN'T Development Status

## Project Overview
- **Project**: CADN'T — Satirical Functional 3D CAD
- **Version**: `v0.1.0-alpha` (Build `v00000-009`)
- **Repository**: [MrAndyBuck/single-file-html-app-template](https://github.com/MrAndyBuck/single-file-html-app-template)
- **Live URL**: [https://mrandybuck.github.io/single-file-html-app-template/](https://mrandybuck.github.io/single-file-html-app-template/)
- **Project Workspace**: `/Users/andybuck/.gemini/antigravity/single-file-html-app`

---

## Operating Boundaries & Permission Rules
- **Project Workspace**: Routine development operations (reading, editing files, running tests, updating project documentation) are authorized strictly within `/Users/andybuck/.gemini/antigravity/single-file-html-app`.
- **External Boundaries**: Files, folders, or resources outside this project workspace must not be read, modified, or executed without explicit user confirmation.
- **Completion Standard**: Automated unit tests are **not** a substitute for real browser interaction and visual verification. Features are classified through four distinct stages:
  1. **Implemented**: Code exists in codebase.
  2. **Automatically Tested**: Passes automated unit tests.
  3. **Visually Verified**: Inspected and verified in real browser sessions with visual artifacts.
  4. **User Accepted**: Directly tested and approved by the user.
- **Deployment Control**: Code is committed to branch `dev`. Code is pushed to `main` and GitHub Pages strictly upon explicit user approval.

---

## Capability Status Matrix

| Capability | Implemented | Auto Tested | Visually Verified | User Accepted | Current Status & Notes |
|---|:---:|:---:|:---:|:---:|---|
| **Clean 4-Canvas Viewport Architecture** | **YES** | **YES** | **YES** | **YES** | 4 distinct `<canvas>` elements on CSS Grid (`#vp-top`, `#vp-perspective`, `#vp-front`, `#vp-right`), each with independent `THREE.WebGLRenderer` and camera sharing the scene. User accepted. |
| **Simple Cube Framing Demonstration** | **YES** | **YES** | **YES** | **YES** | $20 \times 20 \times 20$ blue box with white edges resting at $(0, 10, 0)$, cleanly framed in Top (plan), Perspective (3D), Front (elevation), and Right (side) views. User accepted. |
| **WASD Camera Orbit (Perspective Only)** | **YES** | **YES** | **YES** | **YES** | W/S (vertical elevation), A/D (horizontal azimuth). Only Perspective camera moves; Top, Front, and Right orthographic views remain fixed. User accepted. |
| **Viewport Pan & Zoom** | **YES** | **YES** | **YES** | **YES** | Arrow keys pan active camera; Shift+Arrows zoom active camera. Independent targets and zoom factors for Top, Front, Right, and Perspective. User accepted. |
| **Trackpad Wheel Restriction** | **YES** | **YES** | **YES** | **YES** | Mouse/trackpad wheel zoom strictly cancelled on all 4 viewport canvases with user toast advisory. User accepted. |
| **Service Worker & Cache Freshness** | **YES** | **YES** | **YES** | **YES** | Network-First for HTML/navigation, unconditional `skipWaiting()` and `clients.claim()`, `#chip` click hard-purges SW registrations and cache storage. |
| **Interactive Command Bar (`#command-bar`)** | **YES** | **YES** | **YES** | *Awaiting Manual Test* | Clear command badge, dynamic instructions, parameter inputs, `[✓ Confirm (Enter)]`, `[✕ Cancel (Esc)]`. |
| **Boolean Union (CSG)** | **YES** | **YES** | **YES** | *Awaiting Manual Test* | Interactive multi-solid selection; computes CSG union, produces unified solid mesh with edge wires. |
| **Boolean Difference (CSG)** | **YES** | **YES** | **YES** | *Awaiting Manual Test* | 2-stage Base vs. Tool selection; computes CSG subtraction, updates all 4 views. |
| **Join (Curves & Meshes)** | **YES** | **YES** | **YES** | *Awaiting Manual Test* | Chains curve segments into `ClosedProfile` (extrudable) or polyline; merges mesh geometries. Distinct from CSG Union. |
| **Profile Extrusion into 3D** | **YES** | **YES** | **YES** | *Awaiting Manual Test* | Extrudes closed 2D profiles into 3D solid meshes (`THREE.ExtrudeGeometry`) with depth input. |
| **Object Transformations (Move/Rot/Scale)**| **YES** | **YES** | **YES** | *Awaiting Manual Test* | Interactive parameter inputs for dx/dy/dz, axis/deg, scale factor, with Enter/Escape support. |
| **Real Advertisement Assets & Cadence** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | 9 local ad images loaded from `assets/ads/`. Centered modal triggers after every 10 modeling commands; counter resets only on trigger. Clicking ad rotates image; tiny 10px close button dismisses ad and restores workspace. |
| **Automatic Ad Asset Registration** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | `scripts/generate_asset_manifest.py` scans `assets/ads/` (PNG, JPG, JPEG, WebP) during build/commit via `.git/hooks/pre-commit`, updates `assets/manifest.json`, `sw.js` cache, and `index.html`. |
| **Hold Music Integration** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | Real local audio asset `assets/audio/New Recording 12.m4a` played on long operations (Save, Import, Sweep, Union, Fillet). No loop (`loop = false`), stops on completion/cancel, respects mute toggle, default ~50% volume. |
| **Asset Manifest & SW Offline Caching** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | `assets/manifest.json` maps all real assets; cached in Service Worker (`sw.js`) for offline functionality. |
| **CSG Booleans (Union & Difference)** | **YES** | **YES** | **YES** | *Pending Demonstration* | ThreeCSG solid Boolean Union and Difference producing manifold meshes. |
| **Layer Management** | **YES** | **YES** | **YES** | *Pending Demonstration* | Add, lock, hide, and assign layers with color swatches. |
| **Undo / Redo Stack** | **YES** | **YES** | **YES** | *Pending Demonstration* | Deep document state undo/redo accessible strictly via `Can I undo` and `Can I redo`. |
| **Project Save / Reopen (.cadnt)** | **YES** | **YES** | **YES** | *Pending Demonstration* | Full scene serialization, 2-stage confirmed save, file picker reopen. |
| **OBJ & STL Export (with Satirical Distortion)**| **YES** | **YES** | **YES** | *Pending Demonstration* | Standard binary STL and Wavefront OBJ; optional nonuniform scaling applied to isolated export clone only. |
| **Mesh Import & Geometry Lock** | **YES** | **YES** | **YES** | *Pending Demonstration* | STL/OBJ import, $10 fee deduction, read-only geometry lock, Remesh/Simplify sphere replacement. |
| **Fictional Economy & Satirical Friction** | **YES** | **YES** | **YES** | *Pending Demonstration* | $249 balance, Under Construction refill modal, 10s heavy operation delay, ads with 10px close buttons, Web Audio synthesizer. |

---

## 1. Deployment & Safari Cache Diagnosis (Why Safari Displayed v00000-004)

### Investigation Findings
1. **GitHub Pages Deployment Verified**:
   - Remote repository commit history confirms commit `5031e77` was pushed to `origin/main` and successfully built by GitHub Pages actions.
2. **The Root Cause: Service Worker Cache-First Lock**:
   - `sw.js` was configured with a strict Cache-First strategy:
     ```javascript
     caches.match(e.request, { ignoreSearch: true })
     ```
   - In install handler: `if (!self.registration.active) self.skipWaiting();`
   - Because `self.registration.active` was already `true` (from the initial visit in build `v00000-004`), `self.skipWaiting()` was **never** called. The new worker stayed in `waiting` state, and the old service worker continued serving `v00000-004` directly from Cache Storage.
   - Furthermore, `{ ignoreSearch: true }` caused cache-busting query strings like `?v=v00000-005` or `?t=123` to return the cached `v00000-004` file.
   - GitHub Pages headers additionally send `cache-control: max-age=600`.

### The Solution Implemented in `sw.js` (Build `v00000-006`)
1. **Unconditional `skipWaiting()`**: The service worker activates immediately on install without waiting for clients to close:
   ```javascript
   self.addEventListener("install", (e) => {
     self.skipWaiting();
     ...
   });
   ```
2. **Immediate Cache Eviction & Claim**: Old caches are deleted on activate and `self.clients.claim()` takes immediate control.
3. **Network-First for HTML/Navigation**:
   - All navigation and HTML document requests are fetched from the network first. If online, the browser always receives fresh code. Cache is used strictly as an offline fallback.
4. **Preserve Query Parameters**: Removed `{ ignoreSearch: true }` so query parameters bypass stale cached entries.
5. **Interactive Cache Purge**: Clicking `#chip` in the bottom bar triggers:
   ```javascript
   navigator.serviceWorker.getRegistrations().then(regs => regs.forEach(r => r.unregister()));
   caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))));
   window.location.href = window.location.pathname + "?t=" + Date.now();
   ```

---

## 2. The 4-Canvas Viewport Architecture

Rather than continuing incremental patches to single-canvas WebGL scissor math (which suffered from Three.js `_pixelRatio` double-multiplication and Retina display coordinate inversion), the viewport system was cleanly refactored into a **4-Canvas Architecture**:

### Architectural Components
1. **HTML & CSS Grid**:
   - `#stage-container` configured as a CSS Grid: `display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 2px;`
   - Four distinct viewport panes:
     - `#vp-top` containing `#canvas-top`
     - `#vp-perspective` containing `#canvas-perspective`
     - `#vp-front` containing `#canvas-front`
     - `#vp-right` containing `#canvas-right`
2. **Independent Renderers & Cameras**:
   - Four separate `THREE.WebGLRenderer` instances, one bound to each canvas.
   - Each canvas naturally sizes its internal buffer: `renderer.setSize(w, h, false)`.
   - Zero scissor testing, zero WebGL scissor math, zero Y-inversion coordinate bugs, and zero depth buffer collision between viewports.
3. **Direct Raycasting & Interaction**:
   - Each canvas receives pointer events directly. NDC is simply:
     $$\text{ndcX} = \frac{e.clientX - \text{rect.left}}{\text{rect.width}} \times 2 - 1$$
     $$\text{ndcY} = -\left(\frac{e.clientY - \text{rect.top}}{\text{rect.height}} \times 2 - 1\right)$$
   - Zero quadrant offset math or clipping boundaries required.
4. **Simple Test Cube Demonstration**:
   - $20 \times 20 \times 20$ blue box with white edges centered at $(0, 10, 0)$ resting on the ground plane $Y=0$.
   - Framed across Top, Perspective, Front, and Right views.
   - WASD keys orbit **only** the Perspective camera; Top, Front, and Right orthographic views remain stationary.
   - The starting Michigan model code is preserved in `createMichiganModel()` and ready to be re-enabled once the user approves the 4-canvas foundation.

---

## 3. Visual Verification Artifacts

All screenshots captured in headless Chrome under macOS Retina High-DPI (`--force-device-scale-factor=2`, window size $1280 \times 820$):

### A. Simple Cube Verification (Base Architecture Acceptance)
1. **Simple Cube Framed in 4 Views (With Diagnostic HUD)**:
   [dpr2_4canvas_simple_cube.png](file:///Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/dpr2_4canvas_simple_cube.png)
   - Shows Top-Left (Top view plan of cube), Top-Right (Perspective 3D view of cube), Bottom-Left (Front elevation view of cube), and Bottom-Right (Right side view of cube).
   - HUD displays active viewport `PERSPECTIVE`, active canvas `CANVAS#canvas-perspective`, `DPR: 2.0 [4-Canvas Architecture]`, and build `v00000-006-DIAG`.
2. **Simple Cube Framed in 4 Views (Unobscured / Minimized HUD)**:
   [dpr2_4canvas_simple_cube_minhud.png](file:///Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/dpr2_4canvas_simple_cube_minhud.png)
   - Unobscured view of all four quadrants clearly showing the Right viewport (bottom-right) rendering the side profile of the cube.
3. **WASD Post-Orbit State (Perspective Only)**:
   [dpr2_4canvas_cube_orbited.png](file:///Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/dpr2_4canvas_cube_orbited.png)
   - Shows Perspective camera orbited via `KeyW` and `KeyD` (Azimuth: 65°, Elevation: 3°).
   - Crucial verification: Top, Front, and Right viewports remain completely fixed and unrotated while Perspective orbited in 3D.

### B. Michigan Starting Model Verification (Re-Enabled in 4-Canvas Architecture)
1. **Michigan Model Framed Across All 4 Views (Unobscured / Minimized HUD)**:
   [dpr2_4canvas_michigan_minhud.png](file:///Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/dpr2_4canvas_michigan_minhud.png)
   - Top-Left: Plan view of Upper and Lower peninsulas centered on ground grid.
   - Top-Right: 3D perspective isometric view with shaded faces and wire edges.
   - Bottom-Left: Front elevation view resting on ground grid at $Y=0$.
   - Bottom-Right: Right side elevation view resting on ground grid at $Y=0$.
2. **Michigan Model Post-WASD Orbit**:
   [dpr2_4canvas_michigan_orbited.png](file:///Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/dpr2_4canvas_michigan_orbited.png)
   - Perspective camera orbited via `KeyD` (Azimuth: 63°, Elevation: 37°).
   - Top, Front, and Right views remain completely stationary.

---

## 4. Advertisement Assets & Hold Music Integration (Build `v00000-009-DEV`)

### A. Asset Locations & Preservation
- **Ad Images**: Located in `assets/ads/` (synced from `/Users/andybuck/Documents/Antigravity/assets/Ads`) with exact filenames, extensions, and cases preserved:
  - `AmwayAppAd.jpeg` *(New)*
  - `AppAds.jpeg`
  - `CnBAppAd.png`
  - `EnronAppAd.jpg`
  - `MomsAppAd.jpg` *(New)*
  - `PalantirAppAd.jpeg`
  - `TheranosAppAd.jpeg`
  - `TourismAppAd.jpeg`
  - `ViagraAppAd.webp` *(New)*
- **Hold Music**: Located in `assets/audio/` with exact filename preserved:
  - `New Recording 12.m4a`
- **Asset Manifest**: Automatically generated `assets/manifest.json` mapping all 9 real ad images and audio tracks.
- **Service Worker Offline Cache**: Automatically updated `FILES` in `sw.js` with all 9 ad images and audio file.

### B. Automatic Advertisement Asset Registration (`scripts/generate_asset_manifest.py`)
1. **Design & Automation**:
   - Python CLI script [`scripts/generate_asset_manifest.py`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/scripts/generate_asset_manifest.py) scans `assets/ads/` for supported image types (`.png`, `.jpg`, `.jpeg`, `.webp`) and `assets/audio/` for supported audio formats.
   - Automatically writes `assets/manifest.json`.
   - Automatically synchronizes `const FILES` in `sw.js` for offline PWA caching.
   - Automatically synchronizes `const ASSET_MANIFEST` in `index.html`.
   - Inlined dynamic loader `loadAssetManifest()` in `index.html` fetches `./assets/manifest.json` on startup as a runtime fallback.
   - **Git Pre-Commit Hook**: Installed `.git/hooks/pre-commit` to automatically run `scripts/generate_asset_manifest.py` and stage manifest files whenever images are added and committed.

### C. Advertisement Modal & Cadence
1. **Cadence Rules**:
   - `recordModelingCommand()` increments `modelingCommandCount` solely on actual geometry modifications.
   - Non-modeling commands and ad interactions do NOT advance the counter.
   - Triggers exactly on every 10th modeling command (`count % 10 === 0`), resets `modelingCommandCount` to 0. Startup never triggers an ad.
2. **Modal Interaction & Visual Design**:
   - Centered `<dialog id="modal-ad">` with red satire neon border.
   - Image proportions preserved without stretching or cropping (`object-fit: contain`, `max-width: 90vw`, `max-height: 80vh`).
   - Tiny close button (`#btn-close-ad`, 10px $\times$ 10px) immediately visible in upper-right corner.
   - Clicking directly on the advertisement image rotates to another randomly selected advertisement from the manifest (`rotateAd()`).
   - Ad image clicks do not open external links and do not count as modeling commands.
   - Dismissing the ad restores the previous CAD workspace operation immediately.

### D. Hold Music Playback Rules
1. **Long Loading Operations**:
   - Hooked into `triggerArtificialDelay()` for: Save, STL/OBJ Import, Sweep, Boolean Union, and Fillet.
2. **Playback Engine (`CADNT_AUDIO`)**:
   - Plays `assets/audio/New Recording 12.m4a` at loading start.
   - Does NOT loop (`audio.loop = false`).
   - Stopping or canceling loading (`#btn-cancel-loading` or completion) immediately pauses, rewinds, and clears audio.
   - Overlapping tracks strictly prevented; respects Sound / Mute toggle; default volume ~50%.

### E. Visual Verification Artifacts

All screenshots captured in real browser sessions under macOS Retina High-DPI (`DPR: 2.0`, $1280 \times 820$ window) and saved to `/Users/andybuck/Desktop/CADNT_Screenshots/`:

1. **Step 1 — 9 Commands Executed (No Ad Popup)**:
   [ad_cadence_9_commands.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/ad_cadence_9_commands.png)
2. **Step 2 — 10th Command Executed (Ad Modal Triggered)**:
   [ad_tenth_command_modal.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/ad_tenth_command_modal.png)
3. **Step 3 — Ad Image Click Rotation**:
   [ad_rotated_image.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/ad_rotated_image.png)
4. **Step 4 — Tiny Close Button Click**:
   [ad_closed_restored.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/ad_closed_restored.png)
5. **Step 5 — Second 10 Commands (20th Command Overall)**:
   [ad_twentieth_command_modal.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/ad_twentieth_command_modal.png)
6. **Step 6 — Hold Music Playback During Loading**:
   [hold_music_loading_modal.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/hold_music_loading_modal.png)
7. **Step 7 — Sound / Mute Toggle Silencing**:
   [hold_music_muted.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/hold_music_muted.png)
8. **Step 8 — Exiting / Canceling Loading Operation**:
   [hold_music_canceled_stopped.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/hold_music_canceled_stopped.png)
9. **Step 9 — Newly Registered Ad Display (Amway)**:
   [ad_rotation_amwayappad.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/ad_rotation_amwayappad.png)
   - Confirms `AmwayAppAd.jpeg` displays with native aspect ratio, centered modal, and tiny 10px close button.
10. **Step 10 — Newly Registered Ad Display (Moms)**:
    [ad_rotation_momsappad.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/ad_rotation_momsappad.png)
    - Confirms `MomsAppAd.jpg` displays cleanly in rotation without distortion.
11. **Step 11 — Newly Registered Ad Display (Viagra WebP)**:
    [ad_rotation_viagraappad.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/ad_rotation_viagraappad.png)
    - Confirms WebP format `ViagraAppAd.webp` displays in full fidelity.

---

## 5. Current Git & Deployment Status
- **Current Branch**: `main`
- **Modified & Added Files**:
  - `scripts/generate_asset_manifest.py` (Automatic scanning & registration CLI tool)
  - `.git/hooks/pre-commit` (Automated pre-commit manifest synchronization hook)
  - `assets/ads/*` (All 9 advertisement images, including 3 new additions)
  - `assets/manifest.json` (Automatically regenerated 9-ad manifest)
  - `sw.js` (Offline cache updated with all 9 ads and audio track, version `v00000-009`)
  - `index.html` (Manifest synced with 9 ads, `loadAssetManifest()` added, version `v00000-009`)
  - `HANDOFF.md` (Updated status and verification records)
- **Automated Tests**: 48/48 PASSING (0 FAILED)
- **Visual Verification**: All newly added ads verified in real browser rotation with screenshots.
- **Git Status**: Deployed to `main` and pushed to GitHub Pages as `v00000-009`.
