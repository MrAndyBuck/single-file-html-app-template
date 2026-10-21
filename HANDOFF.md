# HANDOFF.md — CADN'T Development Status

## Project Overview
- **Project**: CADN'T — Satirical Functional 3D CAD
- **Version**: `v0.1.0-alpha` (Build `v00000-015`)
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
| **Checkpoint A: Repair Spline** | **YES** | **YES** | **YES** | **YES** | Multi-point CatmullRomCurve3 spline on C-Plane. Live curved preview, $\ge 3$ control points, [✓ Finish] and Enter key commit, Esc cancels, single SplineCurve entity (51 vertices), 3D interactive handles, dynamic Properties panel editing, project save/reopen serialization, multi-level and single-step undo. Real pointer tested on DPR 1.0 & 2.0 with screenshots. **Accepted by user; merged into `main` (commit `4844d59`).** |
| **Checkpoint B: Fix Michigan Deletion** | **YES** | **YES** | **YES** | *Awaiting Approval to Merge* | `Can I remove starting object` and `Can I delete michigan` locate starting Michigan directly by internal ID without prior selection. Prompts exact text: `"Are you sure you want to remove this?"`. On confirm: removes both peninsulas, updates 4 viewports and FeatureManager, preserves Undo, leaves unrelated objects intact and selected. Ordinary deletion remains blocked. |
| **Checkpoint C: Polygon Command** | **YES** | **YES** | **YES** | *Awaiting Approval to Merge* | `Can I polygon [sides]` with dynamic prompt ($\ge 3$ sides), live rubberband regular polygon preview with center anchor and dashed radius guide. Creates `ClosedProfile` with `THREE.Shape`, auto-exits upon radius placement, supports selection, and extrudes cleanly into 3D solid prism with single-step Undo. Verified for 3, 4, 5, 6 sides. |
| **Checkpoint D: Numeric Easter Eggs** | **YES** | **YES** | **YES** | *Awaiting Approval to Merge* | Exact numeric inputs `67`, `69`, or `420` trigger a retro Windows 95 modal containing exactly `"nice."`. Rejects substrings (`167`, `4200`, `690`). Dismissible via `OK` or caption `✕`, preserves underlying modeling operations, and triggers on parameter commit rather than keystroke spam. |
| **Checkpoint E: Rhino-Style Lock** | **YES** | **YES** | **YES** | *Awaiting Approval to Merge* | `Can I lock` and `Can I unlock`. Locked objects remain visible, are unavailable for selection or editing, and are protected against Move, Rotate, Scale, Gumball, and Deletion. Renders 🔒 lock badge in FeatureManager with click-to-unlock. Persists across save/load. Strictly decoupled from Michigan starting geometry protection. |
| **Checkpoint F: Slowly Escaping Spheres** | **YES** | **YES** | **YES** | *Awaiting Approval to Merge* | Independent, unlocked spheres roll over time at approximately $0.05\text{ mm/sec}$ with subtle rolling rotation consistent with travel direction on world ground plane ($\vec{\omega} \perp \vec{v}$). Frame-rate independent ($\Delta t$). Locking or Boolean-unioning immediately halts movement; unlocking resumes it. Mesh topology unchanged; pauses during active transforms. |
| **Checkpoint A: Sketching Repair (v0.14)** | **YES** | **YES** | **YES** | **YES** | Rubberband preview duplication eliminated. 1 transient preview group, 1 committed entity, 4 boundary edges on rectangle, auto-exit, single-step undo removal, extrudable to 3D solid. Tested at DPR 1.0 & 2.0. **User Accepted via Safari hands-on testing.** |
| **Checkpoint B: Header Redesign (v0.14)** | **YES** | **YES** | **YES** | **YES** | Blue title bar height doubled to 44px (from 22px), fixed width removed, `[Part1.prt : 4 Viewports]` removed, clean bold `CADN'T` branding and scaled retro caption buttons. |
| **Checkpoint C: Functional Pipe Command (v0.14)** | **YES** | **YES** | **YES** | **YES** | `Can I pipe` & `#tool-pipe`. Command Bar with Radius/Diameter selector & live preview. Generates 100% watertight 2-manifold solid ($\chi=2$, open=0) with capped planar ends along straight lines and L-shaped polylines. Registered in FeatureManager (`PipeSolid`), 1 Undo step. Unsupported paths (e.g. solid box) reported with disabled Apply button. |
| **Checkpoint D: Michigan Removal Alias (v0.14)** | **YES** | **YES** | **YES** | **YES** | Added `Can I delete michigan` alias (case-insensitive, trailing punctuation tolerant) triggering the exact same confirmation dialog as `Can I remove starting object`. Normal Delete key remains blocked. Undoable via `Can I undo`. |
| **Checkpoint E: Much Slower Gumball (v0.14)** | **YES** | **YES** | **YES** | **YES** | Shift+M free move multiplier changed from 0.04 to **0.01** (1% displacement). Releasing pointerup commits transform, creates 1 Undo step, immediately hides Gumball, deactivates Gumball mode, requiring `Can I gumball?` to reactivate. |
| **Checkpoint F: Audio Changes (v0.14)** | **YES** | **YES** | **YES** | **YES** | Removed user-facing Sound/Mute button (`#btn-audio-mute`) and View menu item (`#mitem-view-sound`). Set hold-music playback volume to 100% (`1.0`). Preserved non-looping playback, loading triggers, stop on completion, and autoplay compliance. |
| **Clean 4-Canvas Viewport Architecture** | **YES** | **YES** | **YES** | **YES** | 4 distinct `<canvas>` elements on CSS Grid (`#vp-top`, `#vp-perspective`, `#vp-front`, `#vp-right`), each with independent `THREE.WebGLRenderer` and camera sharing the scene. User accepted. |
| **Simple Cube Framing Demonstration** | **YES** | **YES** | **YES** | **YES** | $20 \times 20 \times 20$ blue box with white edges resting at $(0, 10, 0)$, cleanly framed in Top (plan), Perspective (3D), Front (elevation), and Right (side) views. User accepted. |
| **WASD Camera Orbit (Perspective Only)** | **YES** | **YES** | **YES** | **YES** | W/S (vertical elevation), A/D (horizontal azimuth). Only Perspective camera moves; Top, Front, and Right orthographic views remain fixed. User accepted. |
| **Viewport Pan & Zoom** | **YES** | **YES** | **YES** | **YES** | Arrow keys pan active camera; Shift+Arrows zoom active camera. Independent targets and zoom factors for Top, Front, Right, and Perspective. User accepted. |
| **Trackpad Wheel Restriction** | **YES** | **YES** | **YES** | **YES** | Mouse/trackpad wheel zoom strictly cancelled on all 4 viewport canvases with user toast advisory. User accepted. |
| **Service Worker & Cache Freshness** | **YES** | **YES** | **YES** | **YES** | Network-First for HTML/navigation, unconditional `skipWaiting()` and `clients.claim()`, `#chip` click hard-purges SW registrations and cache storage. |
| **Interactive Command Bar (`#command-bar`)** | **YES** | **YES** | **YES** | **YES** | Clear command badge, dynamic instructions, parameter inputs, `[✓ Confirm (Enter)]`, `[✕ Cancel (Esc)]`. |
| **Functional 2D Line Command (`Can I line`)**| **YES** | **YES** | **YES** | **YES** | Interactive C-plane sketching (Top/Front/Right/Persp); Command Bar with Start coords & dynamic Length; green rubberband preview with yellow endpoint indicator dots; length & coord status readout; raycaster threshold 2.5; `Line_N` FeatureManager registration; Properties panel geometry box (Start, End, Length, Plane); Gumball transform support; native `.cadnt` archive serialization & restore. User accepted. |
| **Functional Fillet & Chamfer (`Can I fillet` / `Can I chamfer`)** | **YES** | **YES** | **YES** | **YES** | Exact 2-manifold B-Rep polygon extrusion engine (`buildBoxManifoldCut`); 0 open edges, 0 non-manifold edges, Euler characteristic $\chi=2$; single-edge 2.0mm fillet/chamfer on solid boxes with side-by-side validation; screen-space edge picking (24px); live emerald preview mesh; cancel/undo/confirm; full telemetry. User accepted. |
| **Wandering Command Toolbars** | **YES** | **YES** | **YES** | **YES** | Modeling command buttons automatically swap positions with another random button upon use, guaranteeing the tool never lands in the same slot, stimulating neural elasticity. |
| **Hold Music Integration** | **YES** | **YES** | **YES** | **YES** | Real local audio asset `assets/audio/New Recording 12.m4a` played on long operations (Save, Import, Sweep, Union, Fillet, Chamfer). Non-looping playback, stops cleanly on completion/cancel, respects mute toggle, default volume set to **100%**. |
| **Crash Report Command** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | `Can I send a crash report?` (with/without `?`, case-insensitive) opens dialog targeting `andrewrobertbuck@gmail.com` with system diagnostics, editable fields, and mailto launcher. No silent background uploads. |
| **Starting Object Removal & Undo** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | Hidden command `Can I remove starting object` and alias `Can I delete michigan` show confirmation dialog, delete Michigan upon confirmation, and are fully undoable via `Can I undo`. |
| **Mandatory Export Distortion** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | Nonuniform scaling `(0.72, 1.48, 0.88)` applied unconditionally to all STL and OBJ exports. Scene geometry remains undistorted. |
| **Branding & Terms Clean Up** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | Header updated to clean "CADN'T" branding ("Satirical" badge removed). Terms & Conditions dialog text updated to "Accept Terms & Conditions" without "suffer" wording. |
| **Pipe & Sweep Roadmap** | **YES** | **N/A** | **N/A** | *Awaiting Acceptance* | Technical specifications, input requirements, and algorithmic dependencies documented in `BRIEF.md` (§2.10) and `HANDOFF.md` (§6) for future implementation. |
| **CSG Booleans (Union & Difference)** | **YES** | **YES** | **YES** | *Pending Demonstration* | ThreeCSG solid Boolean Union and Difference producing manifold meshes. |
| **Layer Management** | **YES** | **YES** | **YES** | *Pending Demonstration* | Add, lock, hide, and assign layers with color swatches. |
| **Undo / Redo Stack** | **YES** | **YES** | **YES** | *Pending Demonstration* | Deep document state undo/redo accessible strictly via `Can I undo` and `Can I redo`. |
| **Project Save / Reopen (.cadnt)** | **YES** | **YES** | **YES** | *Pending Demonstration* | Full scene serialization, 2-stage confirmed save, file picker reopen. |
| **Mesh Import & Geometry Lock** | **YES** | **YES** | **YES** | *Pending Demonstration* | STL/OBJ import, $10 fee deduction, read-only geometry lock, Remesh/Simplify sphere replacement. |
| **Fictional Economy & Satirical Friction** | **YES** | **YES** | **YES** | *Pending Demonstration* | $249 balance, Under Construction refill modal, 10s heavy operation delay, Web Audio synthesizer. |

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

## 1.1 Checkpoint A: Spline Repair & Curvature Verification (Build v00000-015)

### Problem & Diagnosis
- Spline command previously called `startSketch("line")` in `executeToolbarCommand(cmd)`.
- `executeCommand` lacked `case "spline":` handling.
- No live Catmull-Rom curve preview, no control point accumulation, no interactive handles.

### Solution Implemented
1. **Interactive Spline Workflow**:
   - `startSketch("spline")` configures `#command-bar` with `SPLINE` badge, prompt, plane selector, point counter, coordinate input, `[✓ Finish (Enter)]` (enabled when $\ge 3$ points), and `[✕ Cancel (Esc)]`.
   - `updateRubberband`: Generates a live `THREE.CatmullRomCurve3` preview arc sampled with $\ge 50$ points in green, with faint control polygon connecting points.
   - `createSplineSketch`: Commits single contiguous `SplineCurve` entity with `userData.controlPoints` and 51 sampled vertices.
2. **Interactive 3D Handles & Properties Panel**:
   - Helper group `splineHandlesGroup` attaches interactive 3D handles at control points with active selection highlight.
   - Viewport handle dragging updates control points directly on the active C-plane.
   - Object Properties panel exposes CP selector, direct numeric $(X, Y, Z)$ inputs, and triggers live `rebuildSplineGeometry`.
3. **Curvature Proof & Non-Collinear Testing**:
   - Tested at $P_0=(-20, 0, 0)$, $P_1=(0, 0, 25)$, $P_2=(20, 0, 0)$ on Top C-plane.
   - Verified 51 vertices with continuous tangent variation and non-zero chord deviation ($Z \approx 15.0$ at $X \approx \pm 10.4$, vs $Z=0$ for straight chord).
4. **Undo & Project Persistence**:
   - Multi-level undo reverts CP moves and removes the spline in one step.
   - `deserializeProjectState` rehydrates `controlPoints` as `THREE.Vector3` instances and rebuilds curve geometry.
5. **Retina DPR 2.0 Testing**:
   - Verified sharp rendering on emulated DPR 2.0 Retina display.
   - All 7 screenshots captured and saved to `/Users/andybuck/Desktop/CADNT_Screenshots/`.

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

## 5. Milestone v00000-010 — Specification Revisions & Command Updates

### A. Branding & Terms & Conditions Updates
1. **Header Branding**:
   - Removed satirical badge and version label (`SATIRICAL v0.1`) from `#brand`.
   - Clean, professional header branding: `CADN'T`.
2. **Terms & Conditions**:
   - Button text updated to `Accept Terms & Conditions` (removed "suffer" wording).
   - Core satirical legal clauses retained.

### B. Crash Report Command (`Can I send a crash report?`)
1. **Invocation**:
   - Request Bar command: `Can I send a crash report?` (works with or without `?`, case-insensitive).
2. **Crash Report Interface (`#modal-crash-report`)**:
   - Destination email locked to `andrewrobertbuck@gmail.com`.
   - Pre-populates editable fields with real-time diagnostic information (User Agent, Viewport dimensions, Object count, Active layer, Scene memory estimate).
   - "Open in Email Client" button generates a `mailto:` link with properly encoded subject and body.
   - Respects user privacy: No silent background uploads or telemetry transmissions.

### C. Starting Object Removal & Undo System
1. **Hidden Command**:
   - `Can I remove starting object` (case-insensitive).
2. **Safety Confirmation**:
   - Triggers modal dialog `#modal-remove-confirm` with prompt: *"Are you sure you want to remove this?"*.
3. **Execution & State Management**:
   - Upon confirmation, Michigan starting geometry is cleanly removed from the scene and layer panel.
   - All 4 viewports update immediately.
   - Deletion is fully reversible via `Can I undo` (and redoable via `Can I redo`), with protected status preserved upon restoration. Ordinary delete commands remain restricted.

### D. Rhino-Inspired Gumball with Free Movement (`Shift + M + Drag`)
1. **3D Gumball Widget**:
   - Renders 3-axis translation arrows (Red: X, Green: Y, Blue: Z), rotation arcs, and scale boxes on selected objects across all 4 viewports (Top, Perspective, Front, Right).
   - Dynamically repositions to selection centroid and updates during transformations.
2. **Free Movement Shortcut**:
   - **`Shift + M + Click and Drag`**: Holding both `Shift` and `M` while clicking and dragging across any viewport moves the selected object freely without handle constraints.
   - Normal dragging without these modifier keys does NOT trigger movement.

### E. 7-Command Ad Cadence & Layered Stacking
1. **Trigger Cadence**:
   - Advertisements appear exactly every 7 executed modeling command attempts (`count % 7 === 0`).
2. **Layered Stacking**:
   - Clicking an active advertisement does not replace it; instead, it dynamically stacks a new randomly selected advertisement card layered above it with cascading positional offsets (`+24px` X/Y).
   - Each individual card contains its own independent tiny 10px close button (`.btn-ad-close`).
   - Closing a card removes only that card; closing the last remaining card dismisses the modal and restores the CAD workspace.
   - Fixed modal centering bug: Container uses `transform: none` and `inset: 0` to prevent quadrant offset.

### F. Mandatory Export Distortion
1. **Nonuniform Distortion Enforced**:
   - Applied unconditionally to all STL and OBJ exports (`exportScale = (0.72, 1.48, 0.88)`).
   - Removed user-facing checkbox `#export-distort` from `#modal-export`.
   - Internal in-memory CAD scene geometry remains completely undistorted.

### G. Future Commands Roadmap (Pipe and Sweep)
1. **Technical Specifications**:
   - Documented in `BRIEF.md` (§2.10) and `HANDOFF.md` capability matrix.
   - **Pipe**: Circular tubular cross-section swept along open or closed 3D curves with user-specified radius/diameter and wall thickness options.
   - **Sweep**: 2D profile swept along 3D guide rail curve using Frenet-Serret frames, with twist and scale controls.
   - Geometry generation deferred until explicit user milestone approval.

### H. Visual Verification Artifacts (Build v00000-010)

All screenshots captured in real browser sessions under macOS Retina High-DPI (`DPR: 2.0`, $1280 \times 820$ window) and saved to `/Users/andybuck/Desktop/CADNT_Screenshots/`:

1. **Step 1 — Branding & Terms & Conditions**:
   [v010_01_branding_and_terms.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_01_branding_and_terms.png)
   - Confirms clean "CADN'T" header without satirical badge and updated "Accept Terms & Conditions" button.
2. **Step 2 — Crash Report Modal**:
   [v010_02_crash_report_modal.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_02_crash_report_modal.png)
   - Confirms prefilled diagnostics, recipient `andrewrobertbuck@gmail.com`, and mailto launcher.
3. **Step 3 — Starting Object Removal Confirmation**:
   [v010_03_remove_confirm_modal.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_03_remove_confirm_modal.png)
   - Confirms modal: *"Are you sure you want to remove this?"*.
4. **Step 4 — Starting Object Removed**:
   [v010_04_starting_object_removed.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_04_starting_object_removed.png)
   - Confirms starting geometry removed from all 4 viewports and layer panel.
5. **Step 5 — Starting Object Restored via Undo**:
   [v010_05_starting_object_restored_undo.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_05_starting_object_restored_undo.png)
   - Confirms complete restoration with protected state intact via `Can I undo`.
6. **Step 6 — Rhino-Style Gumball in 4 Viewports**:
   [v010_06_gumball_4_viewports.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_06_gumball_4_viewports.png)
   - Confirms 3D axis arrows, rotation arcs, and scale handles rendered across Top, Front, Right, and Perspective.
7. **Step 7 — Free Movement with Shift + M + Drag**:
   [v010_07_free_movement_shift_m.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_07_free_movement_shift_m.png)
   - Confirms free translation of selected object across active viewport plane.
8. **Step 8 — 7-Command Ad Cadence**:
   [v010_08_ad_seventh_command_modal.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_08_ad_seventh_command_modal.png)
   - Confirms ad popup triggers on exactly the 7th modeling command, centered on screen.
9. **Step 9 — Layered Ad Stacking**:
   [v010_09_ad_stacked_layers.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_09_ad_stacked_layers.png)
   - Confirms clicking ad stacks new ad card above existing card with offset and independent close button.
10. **Step 10 — Ad Stack Dismissal**:
    [v010_10_ad_stack_closed_restored.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_10_ad_stack_closed_restored.png)
    - Confirms dismissing stack restores previous CAD workspace operation.
11. **Step 11 — Mandatory Export Distortion**:
    [v010_11_mandatory_export_modal.png](file:///Users/andybuck/Desktop/CADNT_Screenshots/v010_11_mandatory_export_modal.png)
    - Confirms removal of distortion disable checkbox and presence of mandatory distortion disclaimer.

---

## 6. Current Git & Deployment Status
- **Current Branch**: `dev`
- **Modified & Added Files**:
  - `index.html` (Complete Windows 95 / SolidWorks 95 UI overhaul, authentic 3D beveled styling, navy title bars, menu bar system, standard toolbar, CAD blueprint slate 0x203040 viewports, FeatureManager dock, bottom Request Bar, and status bar)
  - `screenshots/` (7 visual verification captures for Checkpoint A)
  - `HANDOFF.md` (Updated capability matrix, milestone documentation, and verification artifacts)
- **Automated Tests**: 57/57 PASSING (0 FAILED)
- **Visual Verification**: 7 Checkpoint A screenshots captured in real browser sessions.

---

## 7. Retro Interface Redesign (Windows 95 / SolidWorks 95 Aesthetic) — Checkpoint A

### A. Architectural & Aesthetic Changes
1. **Windows 95 Application Window Framing**:
   - Classic navy blue gradient title bar (`linear-gradient(90deg, #000080, #1084d0)`), 16x16 retro CADN'T icon, active file descriptor `[Part1.prt : 4 Viewports]`, and standard caption controls (`_`, `□`, `✕`).
   - Classic Windows 95 menu bar (`File`, `Edit`, `View`, `Insert`, `Tools`, `Window`, `Help`) with keyboard access underlines, cascading dropdown menus, and hotkey indicators.
2. **Standard Command & Status Toolbars**:
   - Beveled button row with pixel icons: New Part, Open, Save, Print, Undo, Redo, Import, Export, Sound, Theme, Tutorial, Help, About.
   - Economy indicator with sunken credit box (`Credits: $249.00`) and beveled `+ Buy More` button.
   - Bottom status bar with 5 sunken Windows 95 panes: status message, real-time XYZ coordinates readout, navigation key reminder, token counter, and cache-purge chip.
3. **FeatureManager DesignTree (Left Dock)**:
   - Sunken tree view displaying `Part1.prt`, reference planes (Front X/Y, Top X/Z, Right Z/Y), Origin (0,0,0), Features & Geometry list with badges, and Layers tree with toggleable visibility/lock states.
   - Object properties dock with sunken parameter controls.
4. **4-Viewport Matrix (Center Stage)**:
   - Sunken 3D viewport frames with classic CAD blueprint slate background (`#203040`) and subtle blueprint grid lines (`#486078`, `#2a3e50`).
   - Active viewport highlighted with high-contrast yellow border and navy header.
   - Preserves 4 independent WebGL renderers and cameras (Top orthographic, Front orthographic, Right orthographic, Perspective 3D orbit).
   - Strict trackpad wheel zoom prevention preserved with user advisory toast.
5. **Features Dock (Right Dock)**:
   - 2-column grid of square beveled buttons preserving all 18 CAD commands and icon relocation capability.
6. **Sunken Request Bar (Bottom)**:
   - Relocated directly above the status bar with classic sunken text field (`Request:`), `Send` button, and upward-popping `▼ Log` history container.
7. **Windows 95 Modal Dialogs**:
   - All modals (Export, Crash Report, Loading hold music, Confirmation, Construction, About, Onboarding, and Advertisements) restyled with 3D beveled borders, navy titlebars, caption close buttons, and beveled action buttons.

### B. Visual Verification Artifacts (Checkpoint A)
Captured via automated headless Chrome CDP session under macOS Retina High-DPI ($1280 \times 820$):

1. **Workspace Overview**:
   [checkpoint_a_01_win95_workspace.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_a_01_win95_workspace.png)
   - Demonstrates complete Windows 95 / SolidWorks 95 UI with 4 viewports, FeatureManager, right toolbar, Request Bar, and status bar.
2. **Menu Bar Dropdown**:
   [checkpoint_a_02_menu_dropdown.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_a_02_menu_dropdown.png)
   - Demonstrates open `Insert` dropdown menu with beveled 3D borders, command items, and separators.
3. **Export Dialog**:
   [checkpoint_a_03_export_dialog.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_a_03_export_dialog.png)
   - Demonstrates Windows 95 styled export dialog with format/scope dropdowns and mandatory distortion notice.
4. **Sponsored Advertisement Popup**:
   [checkpoint_a_04_ad_modal.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_a_04_ad_modal.png)
   - Demonstrates Windows 95 framed commercial popup with tiny close button and centered layout.
5. **Layered Ad Stacking**:
   [checkpoint_a_05_ad_stacked.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_a_05_ad_stacked.png)
   - Demonstrates clicking ad cards to stack cascading Windows 95 ad layers with independent close buttons.
6. **Crash Report Dialog**:
   [checkpoint_a_06_crash_report_dialog.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_a_06_crash_report_dialog.png)
   - Demonstrates retro crash report preparation dialog with prefilled local telemetry and email launcher.
7. **Loading & Hold Music Dialog**:
   [checkpoint_a_07_loading_hold_music.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_a_07_loading_hold_music.png)
   - Demonstrates classic Windows 95 segmented blue progress bar with satirical status messages.

### C. Checkpoint B — Functional 2D Line Command Engine (Completed & Visually Verified)

#### 1. Technical Architecture & Implementation Details
- **Command Bar Integration (`#command-bar`)**:
  - Activating `Can I line` or clicking the Line toolbar icon reveals the sunken `#command-bar` above the Request Bar.
  - Controls include:
    - Command Badge: `[LINE]` in navy blue.
    - Context Prompt: Live instruction guiding start point placement, coordinate entry, or length definition.
    - C-Plane Selector: Interactive dropdown allowing explicit switching between `Top (X/Z)`, `Front (X/Y)`, `Right (Z/Y)`, and `Persp (X/Z)`.
    - Coordinate Input: `Start: X, Y, Z` with Enter key listener to place $P_1$ numerically.
    - Length Input: `Length` input field dynamically updated during mouse drag; supports direct numeric entry to lock line distance along current pointer heading.
    - Action Buttons: `✓ Finish (Enter)` and `✕ Cancel (Esc)` to commit or abort sketching cleanly without leaving ghost geometry.
- **Interactive Viewport Sketching & Rubberband**:
  - Live cursor tracking records `lastPointerCPlanePos` across all four viewports.
  - Real-time green rubberband line (`0x39ff14`) connects start point to cursor.
  - Distinct yellow endpoint indicator spheres (`0xffff00`, radius 0.8) denote $P_1$ and $P_2$ vertices.
  - Real-time status bar readout displays coordinates and length: `P1: (X1, Y1, Z1) → P2: (X2, Y2, Z2) | Len: L.L mm`.
- **Flexible Request Bar Syntax**:
  - `Can I line`: Starts interactive click-to-place line sketch mode.
  - `Can I line <length>` (e.g. `Can I line 35`): Immediately generates a line of exact length along active C-plane.
  - `Can I line <x1> <y1> <x2> <y2>` (e.g. `Can I line 0 0 30 30`): Generates 2D line between coordinate pairs on current plane.
  - `Can I line <x1> <y1> <z1> <x2> <y2> <z2>`: Generates 3D line between full spatial coordinates.
  - `Can I line <x1,y1> <x2,y2>`: Supports comma-delimited points.
- **Raycaster Selection Optimization**:
  - Standard Three.js raycasting on thin 1px lines is notoriously difficult to hit in high-DPI viewports.
  - Initialized `raycaster.params.Line = { threshold: 2.5 }`, providing reliable, comfortable line selection across all 4 orthographic and perspective viewports.
- **FeatureManager & Object Properties Integration**:
  - Generated lines are registered as `Line_N` entities with `userData.type === "SketchCurve"`.
  - Displayed in the FeatureManager DesignTree with a dedicated SketchCurve icon and royal blue selection state.
  - Object Properties dock displays a prominent **Line Geometry** group positioned right below Type & Layer, exposing:
    - `Start:` $(X_1, Y_1, Z_1)$
    - `End:` $(X_2, Y_2, Z_2)$
    - `Length:` $L.LL\text{ mm}$
    - `Plane:` Active C-Plane
- **Rhino-Inspired Gumball & Transform Compatibility**:
  - Selecting a 2D line displays the 3D Gumball transform widget centered on the line, enabling translation, rotation, and scaling.
  - Selected line color highlights in bright yellow (`0xffff00`), reverting to crisp blueprint cyan (`0x00d4ff`) when deselected.
- **Document Serialization & Persistence**:
  - Full roundtrip persistence in `.cadnt` native JSON archive format via `serializeProjectState()` and `deserializeProjectState()`.
  - Restored lines retain all position buffers, transforms, userData attributes, and selection capabilities.
- **Automated Test Suite**:
  - Passes 61/61 automated tests, including new tests verifying `Can I line 35`, properties panel geometry readout, command bar activation, and raycaster threshold configuration.

#### 2. Visual Verification Artifacts (Checkpoint B)
Captured via automated headless Chrome CDP session under macOS Retina High-DPI ($1400 \times 900$):

1. **Active Line Sketching & Rubberband**:
   [checkpoint_b_01_line_sketch_active.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_b_01_line_sketch_active.png)
   - Shows active Line sketching mode with `#command-bar` (Badge, C-Plane dropdown, Start coords, Length input), green rubberband preview line, yellow endpoint indicator dots in the Top viewport, and status bar coordinate/length readout.
2. **Completed Line Selected with Gumball & Properties Readout**:
   [checkpoint_b_02_line_selected_gumball.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_b_02_line_selected_gumball.png)
   - Shows completed line highlighted in bright yellow (`0xffff00`) with Rhino-inspired 3D Gumball widget, FeatureManager tree selection `[SketchCurve] Line_2`, and Object Properties panel displaying the Line Geometry box (Start, End, Length: 65.19 mm, Plane: TOP).
3. **Project Roundtrip Archive Persistence**:
   [checkpoint_b_03_line_roundtrip_save.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_b_03_line_roundtrip_save.png)
   - Demonstrates project serialization and reload: the line entity is fully reconstituted from JSON archive, restored to scene objects, and selectable in all viewports.

---

### D. Checkpoint C — Functional Fillet and Chamfer Commands (Completed & Visually Verified)

#### 1. Architecture & Geometric Computation
- **12 Canonical Box Edges**:
  - `getBoxEdgeSegments(mesh)` extracts all 12 bounding box edges with start/end vertices transformed to local mesh coordinate space.
- **CSG Subtraction Cutters**:
  - `computeEdgeCutGeometry(mesh, mode, param, edgeIndices)` constructs parametric cutter solids aligned to each edge:
    - **Chamfer**: Right-angled triangular prism oriented at 45° across the edge corner, cleanly slicing the vertex boundary into an authentic flat bevel.
    - **Fillet**: Extruded corner cutter with a concave circular arc (16 radial segments) and outer rectangular corner, removing the sharp right angle and leaving a smooth rounded cylindrical radius.
  - Subtraction executes via ThreeCSG in 4–8ms in browser runtime, producing clean manifold geometry.
- **Interactive `#command-bar` Integration**:
  - `setupFilletOrChamferCommand(mode, args)` mounts dedicated controls in the sunken retro Command Bar:
    - Badge: `[FILLET EDGES]` / `[CHAMFER EDGES]`
    - Scope dropdown: `All Edges (12)`, `Vertical Edges (4)`, `Horizontal Edges (8)`, `Selected Edge(s)`
    - Radius/Distance input with real-time numeric validation
    - `[x] Preview` checkbox
    - `[✓ Apply (Enter)]` and `[✕ Cancel (Esc)]` buttons
- **Direct Edge Selection Overlays**:
  - Attached edge helpers (`Fillet_Edge_Helpers`) render unselected edges in blueprint cyan (`0x00d4ff`) and selected edges in bold yellow (`0xffff00`) with midpoint anchor dots.
  - Pointer raycasting in any of the 4 viewports detects and toggles individual edge selections.
- **Real-Time Live Emerald Preview**:
  - Active preview wireframe mesh (`0x39ff14`) updates dynamically on any slider or scope change without modifying underlying scene geometry until confirmed.
- **FeatureManager & Object Properties Inspector**:
  - Completed solids are registered in the FeatureManager tree as `[FilletedSolid] Fillet_N` or `[ChamferedSolid] Chamfer_N`.
  - Properties panel includes a dedicated parameters readout displaying Operation, Radius/Distance, and Edges Cut.
- **Economic Integration & Undo Support**:
  - Deducts fictional $49.00 fee strictly upon successful application.
  - Fully undoable via `Can I undo`, restoring original geometry, wireframes, and credit balance.

#### 2. Visual Verification Artifacts (Checkpoint C)
1. **Interactive Fillet Command Bar with Edge Selection & Live Emerald Preview**:
   [checkpoint_c_01_fillet_command_bar_preview.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_c_01_fillet_command_bar_preview.png)
   - Box primitive with active Fillet Command Bar, 12 yellow edge helpers, and live emerald preview mesh.
2. **Completed Fillet Solid with 3D Gumball & FeatureManager Registration**:
   [checkpoint_c_02_fillet_completed_solid.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_c_02_fillet_completed_solid.png)
   - Real rounded FilletedSolid with Gumball, FeatureManager selection, and Properties inspector readout.
3. **Selected Edge Chamfer with 45° Bevel Facets**:
   [checkpoint_c_03_chamfer_selected_edges.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_c_03_chamfer_selected_edges.png)
   - Second box with vertical edges beveled via Chamfer, showing 45-degree facets and Chamfer Properties readout.

---

### E. Checkpoint D — Wandering Toolbar Icons & 85% Hold Music Volume (Completed & Visually Verified)

#### 1. Implementation Details
- **Wandering Command Toolbars**:
  - `relocateToolbarIcons(targetBtnOrCmd)` automatically triggers on every command click or activation.
  - Swaps the activated button with another randomly chosen button on the toolbar, strictly guaranteeing it never lands in the same slot.
  - Underlying button click listeners, data commands, and tooltips follow the icon to its new position.
- **Hold Music Default Volume Increased to 85%**:
  - `CADNT_AUDIO.volume = 0.85` sets initial playback volume to 85% (up from 50%).
  - Audio instances instantiate with `audio.volume = this.volume`.
  - All constraints preserved: non-looping (`loop = false`), local audio asset, stops cleanly on completion or cancellation, respects mute toggle.
- **Automated Test Suite**:
  - Passes **64/64** tests (100% passing), including Test 8 (Wandering Toolbar slot shifting verification) and Test 36 (Hold music volume verification at 0.85).

#### 2. Visual Verification Artifacts (Checkpoint D)
1. **Wandering Toolbar & Volume Verification**:
   [checkpoint_d_01_wandering_toolbar_volume.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_d_01_wandering_toolbar_volume.png)
   - Shows relocated toolbar icons after command execution and active status confirmation.

---

### F. Sequential Checkpoint Roadmap Summary
- **Checkpoint A**: Complete Retro Interface Redesign (**APPROVED BY USER** - Commit `cb5a658`).
- **Checkpoint B**: Functional 2D Line Command Engine (**APPROVED BY USER** - Commit `8c24f35`).
- **Checkpoint C**: Functional Fillet & Chamfer Commands with Geometry Modification (**COMPLETED & VISUALLY VERIFIED** - Commit `015a35e`).
- **Checkpoint D**: Wandering Toolbar Icons & 85% Hold Music Volume (**COMPLETED & VISUALLY VERIFIED** - Commit `015a35e`).

---

## Milestone 2: Modeling and Interface Refinements (In Flight)

### Checkpoint A: Repair Fillet & Chamfer Geometry with Mandatory Individual-Edge Selection (Completed & Visually Verified)

#### 1. Root Cause Analysis of Prior Malformed Geometry
- **Cutter Coordinate Displacement**: Previously, `CSG.fromMesh(mesh)` applied `mesh.matrix` (transforming geometry to world space), whereas `cutterMesh` was generated in local geometry space with identity matrix. Furthermore, `CSG.toMesh(csg, new THREE.Matrix4(), ...)` returned geometry in world coordinates which was re-assigned to `mesh.geometry` while `mesh.position` remained non-zero, displacing the mesh upward and misaligning cut bounds.
- **Basis Orientation Reflection**: Basis matrices formed without determinant checks had $\det < 0$, which inverted ThreeCSG polygon winding normals and caused subtraction cuts to invert solid geometry.
- **Horizontal X Cutter Typo**: Line 5309 contained typo `cornerY - sy * c` where `c` was an object instead of parameter `p`.
- **Face Occlusion in Edge Raycasting**: 1px edge lines were occluded by solid faces in 3D pointer raycasting.

#### 2. Architectural & Algorithmic Solutions Implemented
- **Local Coordinate CSG Execution**: All CSG operations execute on a local cloned mesh with identity matrix, guaranteeing zero world-space position displacement or bounding box drift.
- **Right-Handed Orthonormal Basis**: Universal edge cutter computes basis $(\mathbf{b}_1, \mathbf{b}_2, \mathbf{b}_3)$ from face normals $\mathbf{n}_A, \mathbf{n}_B$ and unit edge direction $\mathbf{u}$. Determinant check swaps $\mathbf{b}_1, \mathbf{b}_2$ if $\det < 0$, strictly guaranteeing $\det = +1.0$ and correct polygon winding.
- **Exact Cutter Profiles**:
  - **Chamfer**: Triangular prism with cross-section $(-d, 0) \to (0, -d) \to (M, -d) \to (M, M) \to (-d, M) \to (-d, 0)$ where $M = d + 2.0$. Slices corner from distance $d$ on Face A to distance $d$ on Face B.
  - **Fillet**: 16-segment circular arc centered at $(-R, -R)$ tangent to both faces, removing sharp corner and creating true rounded cylindrical radius.
- **Mandatory Individual-Edge Selection**:
  - Initial selection starts empty: `selectedEdgeIds = []` (does not automatically cut all edges).
  - Scope dropdown options: `Selected Edge(s) (0)`, `All Edges (12)`, `Vertical Edges (4)`, `Horizontal Edges (8)`, `Clear Selection (0)`.
  - Edge helpers render unselected edges in cyan (`0x00d4ff`) with hollow anchor dots, and selected edges in bold yellow (`0xffff00`) with midpoint yellow spheres.
  - Invisible cylinder capsules (radius 1.8 mm) along each edge ensure pointer raycasting reliably prioritizes edges over solid faces in all 4 viewports.
  - Apply button `[✓ Apply (Enter)]` is disabled with 50% opacity until at least one edge is selected.
  - Live emerald green wireframe preview mesh (`0x39ff14`) updates in real time on any parameter or edge selection change.
- **Fictional Economy & Undo Protection**:
  - $49.00 fee is deducted strictly upon successful operation completion.
  - Fully undoable via `Can I undo`, restoring original geometry, wireframes, and credit balance.

#### 3. Verification & Visual Artifacts
- **Automated Tests**: Passes 67/67 unit tests (100% passing), including new tests verifying initial 0-edge mandatory selection, individual edge toggling, scope selection, and geometry modification.
- **Exact Dimension Comparison**: Box ($20\times 20\times 20$) with 3.0mm fillet has arc vertices matching $(x - 7.0)^2 + (z - 7.0)^2 = 3.0^2$; 3.5mm chamfer produces exact flat bevel connecting $x=6.5, z=10$ to $x=10, z=6.5$. Unaffected faces and sharp edges remain completely unmodified.
- **Visual Artifacts Opened in macOS Preview**:
  1. `checkpoint_a_01_fillet_edge_selection_preview.png`: Fillet Command Bar active with 2 selected edges highlighted yellow, cyan unselected edges, and live emerald green preview mesh.
  2. `checkpoint_a_02_fillet_completed_solid.png`: Completed `Fillet_3` solid with rounded cylindrical corners, FeatureManager registration, Properties panel parameters, and $49 fee deduction.
  3. `checkpoint_a_03_chamfer_selected_edges.png`: Completed `Chamfer_5` solid alongside `Fillet_3`, showing 45-degree flat bevel facets and unmodified planar faces.
- **User Acceptance**: APPROVED BY USER ("looks sweet. I approve").

---

### Checkpoint B: Rhino-Style Move & Connected Sketch Lines (Completed & Visually Verified)

#### 1. Architectural & Algorithmic Solutions Implemented
- **Rhino-Style Point-to-Point Move Command (`Can I move`)**:
  - Two-phase interactive workflow adhering strictly to standard Rhino 3D conventions:
    1. **Object Selection**: If objects are not selected prior to invocation, prompts user to select target objects in any viewport, with confirmation button advancing to Base Point. If objects are already selected, advances immediately to Base Point.
    2. **Base Point Specification**: Prompts user to click a base point in any viewport or enter exact coordinates `(X, Y, Z)` in the retro Command Bar. Defaults to the calculated geometric centroid of the selection. Generates a distinct 3D Base Point Marker (`Move_Base_Marker`) composed of a red anchor sphere and yellow 3D crosshair axes.
    3. **Destination Point & Live Ghost Preview**: On pointer movement in any of the 4 viewports, computes live displacement $\vec{d} = \mathbf{P}_{\text{cursor}} - \mathbf{P}_{\text{base}}$, renders a dynamic green rubberband displacement line, and displays a translucent emerald green ghost preview mesh (`Move_Ghost_Preview`, `0x39ff14`, opacity 0.55) across all 4 viewports showing the exact resulting position of the objects.
    4. **Coordinate & Numeric Inputs**: Displays real-time offsets `dX, dY, dZ` and straight-line distance `Dist (mm)` in yellow monospace font. Users can click in any viewport canvas or type numeric values into `Dest: [ X, Y, Z ]`, `dX, dY, dZ: [ ... ]`, or `Dist: [ ... ]` inputs and press Enter to commit.
    5. **Confirmation, Cleanup & Undo**: Modifies object position matrices, cleans up ghost previews and base markers, updates Gumball and Properties inspectors, and records an undo snapshot allowing instant rollback via `Can I undo`.
- **Connected Sketch Lines & Extrudable Closed Profiles**:
  - **Multi-Segment Polyline Continuance**: Drawing lines no longer terminates after 2 points. Clicking subsequent points continuously appends segments to `sketchPoints`, rendering committed segments in blueprint cyan (`0x00d4ff`) with vertex anchor dots while extending an active green rubberband segment to the cursor.
  - **Endpoint Snapping Engine (`findSnapPoint`)**: Searches vertices across current polyline points (especially start point $P_0$) and existing scene objects within a 3.0mm threshold. Displays a dedicated yellow wireframe snap box indicator (`Sketch_Snap_Marker`) and status annotation `[SNAP: Close Profile]` when hovering near candidate snap points.
  - **Closed Profile Auto-Detection**: When the user clicks back onto start point $P_0$ (or clicks within snap distance of $P_0$ with $\ge 3$ points), the engine detects loop closure, appends the shared closing vertex, constructs a valid 2D `THREE.Shape`, creates a `THREE.LineLoop` with `ClosedProfile` metadata, registers it in the FeatureManager tree as `Profile_N`, and terminates sketch mode.
  - **3D Solid Extrudability**: The resulting closed profile is immediately recognized by `extrudeSelectedProfile` and `Can I extrude`, extruding the 2D polygon into a true 3D solid (`ExtrudedSolid`) with height, beveled perimeter, and shaded faces across all 4 viewports.
  - **Open Polyline Support**: Users can terminate an open polyline at any time via `[✓ Finish (Enter)]` or pressing Enter, producing an open `SketchCurve` with exact segment length calculations.

#### 2. Verification & Visual Artifacts
- **Automated Tests**: Passes **75/75** unit tests (100% passing), including new tests:
  - Test 12d: Connected sketch lines multi-segment polyline formation, endpoint snap closure to `ClosedProfile`, and 3D solid extrusion into `ExtrudedSolid`.
  - Test 16b: Rhino-style point-to-point Move base/destination specification, ghost preview generation, exact coordinate displacement, and rollback via `Can I undo`.
- **Visual Artifacts Automatically Opened in macOS Preview**:
  1. `checkpoint_b_01_connected_sketch_closing.png`: Connected sketch lines in progress on Top C-Plane showing 4 connected segments, cyan anchor dots, yellow snap box snapping back to $P_0$, and Command Bar showing `CONNECTED LINE` and prompt.
  2. `checkpoint_b_02_sketch_extruded_solid.png`: Closed profile extruded into true 3D solid `Extrude_2` (height 16mm) with shaded faces, wire edges, FeatureManager registration, and Properties panel readout.
  3. `checkpoint_b_03_rhino_move_point_to_point.png`: Rhino-style point-to-point Move in progress showing 3D base marker at centroid, rubberband line to destination point `(24, 0, 18)`, live translucent emerald ghost preview mesh across all 4 viewports, and Command Bar offset readout `dX: 24.0 dY: 0.0 dZ: 18.0 | Dist: 30.0 mm`.
- **User Acceptance**: APPROVED BY USER ("looks sweet. I approve" - Commit `6ceb286`).

---

### Checkpoint C: Gumball Activation and Dismissal (Completed & Visually Verified)

#### 1. Architectural & Behavioral Requirements Implemented
- **Gumball Hidden by Default**:
  - Selecting an object (via viewport click, multi-select, or FeatureManager tree) no longer automatically renders the Gumball widget.
  - Internal state `isGumballActive` is initialized to `false`. In `updateGumball()`, `gumballGroup.visible` is strictly governed by `isGumballActive && selectedObjects.length > 0`.
- **Explicit Activation via `Can I gumball?`**:
  - Gumball appears strictly when the user enters the polite request `Can I gumball?`.
  - Normalized command engine supports full case-insensitivity (`can i gumball`, `CAN I GUMBALL`, `Can I gumball`) and arbitrary trailing punctuation (`?`, `???`, `!`, `.`).
  - If no object is currently selected when invoked, the system provides clear user guidance in the Command Log and status bar ("Select an object to display Gumball.") without displaying disconnected handles.
  - When an object is selected, sets `isGumballActive = true` and displays the full 3D transform widget centered on the selection.
- **Preserved Axis-Specific Transform Capabilities**:
  - All standard Rhino 3D handles remain fully operational while Gumball is active:
    - **Translation Arrows (X, Y, Z)**: Red, Green, and Blue cones/axes drag geometry along constrained world axes.
    - **Rotation Arcs (X, Y, Z)**: Torus arc segments rotate geometry around constrained world axes with angle status readouts.
    - **Scale Handles (X, Y, Z)**: Terminal cube boxes scale geometry proportionally or non-proportionally along selected axes.
  - Axis manipulation preserves Gumball visibility on the selected object, updating the widget anchor to the object's new centroid upon release.
- **Free Movement via `Shift + M + Drag`**:
  - Free translation is strictly guarded by the simultaneous combination of `Shift + M` modifier keys plus pointer click-and-drag.
  - Attempting Free Move when Gumball is inactive is rejected with advisory status and log notification: "Gumball inactive. Type 'Can I gumball?' to activate."
- **Immediate Dismissal Following Free Move**:
  - As soon as the user releases the mouse or trackpad following a completed Free Move (`pointerup`):
    1. **Immediate Gumball Dismissal**: Sets `isGumballActive = false` and sets `gumballGroup.visible = false` immediately across all 4 viewports.
    2. **Transformation Finalization**: Ends drag state (`gumballDragState = null`) and updates object matrices, properties, and tree listings.
    3. **Single Undo Step Creation**: Records exactly one document snapshot to `undoStack` labeled `"Free Move (Shift+M)"`.
    4. **Subsequent Interaction Gating**: Deactivates transform handles, requiring the user to explicitly enter `Can I gumball?` again before initiating another Gumball interaction.
- **Selection Change Isolation**:
  - Clicking another object in the viewport or selecting an item from the FeatureManager tree sets `isGumballActive = false` and dismisses the Gumball.
  - Selecting another object does **not** automatically reactivate the Gumball; the user must enter `Can I gumball?` for each target.
- **Escape Key Dismissal**:
  - Pressing `Escape` when Gumball is active cleanly dismisses the widget (`isGumballActive = false; updateGumball();`) and reports "Gumball dismissed."

#### 2. Verification & Visual Artifacts
- **Automated Test Suite**: Passes **81/81** unit tests (100% passing), including new tests:
  - Test 45b: Gumball widget is hidden by default upon object selection.
  - Test 45c: Gumball activates and displays on selected object when `Can I gumball?` is entered.
  - Test 45d: Gumball activation supports case-insensitivity and optional trailing punctuation (`can i gumball`, `CAN I GUMBALL???`).
  - Test 45e: Selecting another object does not automatically reactivate Gumball.
  - Test 45f: Completed Free Move immediately hides Gumball, ends transformation, and creates 1 Undo step.
  - Test 45g: Undo restores object displaced by Free Move to exact pre-move position.
- **Visual Artifacts Automatically Opened in macOS Preview**:
  1. `checkpoint_c_01_gumball_hidden_by_default.png`: `Box_28` selected with yellow outline highlights across Top, Front, Right, and Perspective viewports, with Gumball completely hidden by default and status reading `Box_1 selected. Gumball hidden by default. Enter 'Can I gumball?' to activate.`
  2. `checkpoint_c_02_gumball_activated_on_selection.png`: Request Bar showing `Can I gumball?`, Command Log confirming `Gumball activated.`, and 3D Gumball displayed on the selected box with red/green/blue translation arrows, rotation arcs, and scale boxes across all 4 viewports.
  3. `checkpoint_c_03_free_move_gumball_dismissed.png`: Completed Free Move displacement to `(24, 0, 18)` with Gumball immediately hidden upon mouse release, Command Log reading `Free move complete. Gumball dismissed. Type 'Can I gumball?' to reactivate.`, and 1 Undo step recorded.

### Checkpoint D: Compact Toolbar, Navigation Button Removal, Insufficient Funds Popup, and Additional Ads

#### 1. Implementation Architecture & Key Changes
- **Removal of Manual Navigation Buttons**:
  - Removed `#tb-btn-undo` and `#tb-btn-redo` interface buttons along with their preceding separator `<div class="toolbar-sep"></div>` from `#win95-standard-toolbar`.
  - The standard toolbar now displays only document and utility actions: New Part, Open Project, Save Project, Print, Import, Export, Sound, Theme, Tutorial, Help, About, and Economy Chip.
  - Strictly preserved internal undo/redo engine: `executeUndo()`, `executeRedo()`, and the document history stack remain 100% functional via Request Bar commands (`Can I undo`, `Can I redo`).
  - Preserved keyboard camera navigation (`W`, `S`, `A`, `D` for orbit, Arrow keys for pan, Shift+Arrows for zoom) and trackpad selection behavior.
- **Compact Features Toolbar Grid**:
  - Re-architected `.modeling-toolbar-body` CSS styling:
    - Added `align-content: start;` and `grid-auto-rows: 32px;` with `gap: 2px; justify-content: center;`.
    - Eliminated excessive vertical dead space that previously stretched rows across the full 800px vertical height of the right dock.
    - All 18 modeling commands (Box, Extrude, Revolve, Sweep, Loft, Fillet, Chamfer, Shell, Draft, Rib, Hole, Pattern, Mirror, Split, Combine, Gumball, etc.) now render as a dense, compact 2-column icon grid starting at the top of the dock, consistent with Windows 95 / early SolidWorks tool palettes.
    - Retained wandering toolbar relocation behavior: clicking a tool continues to swap icon positions via `relocateToolbarIcons()` across the dense grid.
- **Insufficient Funds Modal (`Finger.jpg`)**:
  - Created retro Windows 95 modal dialog `<dialog id="modal-insufficient-funds">` with titlebar `⚠️ Insufficient Funds`, caption close `✕` button, and an `[OK]` dismiss button.
  - Houses the supplied image `assets/Finger.jpg` (736×935 px, pointing finger) with its original filename preserved and unmodified.
  - Triggered whenever a user attempts any paid operation without sufficient fictional credits:
    - `attemptPaidOperation(opName, fee)` (e.g. primitive creations or transforms if balance < fee).
    - `initiateImportWorkflow()` ($10.00 fee when balance < $10.00).
    - Fillet & Chamfer commit ($49.00 fee when balance < $49.00).
  - **Zero Deduction on Failure**: Guarantees $0.00 credits are deducted when a transaction fails due to insufficient funds; the user's credit balance remains completely untouched.
  - **Non-blocking & Dismissible**: Dismissible via `[OK]` button, caption `✕` button, or `Escape` key, restoring full access to the CAD workspace without permanently freezing or trapping viewport interaction.
- **New Advertisement Registration & Offline Caching**:
  - Located and copied all 5 newly supplied advertisement images from `Documents/Antigravity/assets/Ads/` into `assets/ads/`:
    - `AppleAppAd.jpeg`
    - `GamblingAppAd.webp`
    - `GamblingAppAd2.png`
    - `VirusAppAd.png`
    - `ZuneAppAd.webp`
  - Total registered advertisements expanded from 9 to 14.
  - Automatically regenerated `assets/manifest.json` and updated `sw.js` with all 14 advertisement images plus `./assets/Finger.jpg` for offline PWA functionality.
  - Synchronized `ASSET_MANIFEST` in `index.html` with dynamic runtime fallback `loadAssetManifest()`.
  - Maintained all core advertisement interactions:
    - Triggers every 7 modeling command attempts (`count % 7 === 0`).
    - Centered modal dialog with red satire neon border.
    - Tiny immediately visible 10px close button (`.btn-ad-close`).
    - Clicking an advertisement spawns another ad layered above it with cascading offsets (`pushAdLayer()`).
    - Stacked advertisements are individually dismissible; closing the final ad restores the CAD workspace.

#### 2. Verification & Visual Artifacts
- **Automated Test Suite**: Passes **84/84** unit tests (100% passing), including new tests:
  - Test 33: Asset manifest loaded with 14 ads and hold music track.
  - Test 46: Forward and Back manual navigation buttons are removed from top standard toolbar.
  - Test 47: Right-side Features toolbar uses compact dense icon grid layout (`align-content: start; grid-auto-rows: 32px`).
  - Test 48: Insufficient funds popup appears on failed paid transaction with Finger.jpg and $0 deducted.
- **Visual Artifacts Automatically Opened in macOS Preview**:
  1. `checkpoint_d_01_compact_toolbar_no_nav_buttons.png`: Clean standard toolbar with Forward/Back manual buttons removed, and right-side Features dock showing the compact 2-column icon grid neatly docked at the top.
  2. `checkpoint_d_02_insufficient_funds_finger_popup.png`: Retro Windows 95 `⚠️ Insufficient Funds` dialog displaying `Finger.jpg` in full fidelity upon an attempted paid operation with $5.00 balance, verifying $0.00 deducted and balance preserved.
  3. `checkpoint_d_03_advertisements_rotation_and_stacking.png`: Centered advertisement modal displaying newly registered `AppleAppAd.jpeg` with `VirusAppAd.png` dynamically stacked on top, with independent tiny close buttons.

---

### Milestone: Rhino Move & Intentionally Slow Gumball (0.04 Multiplier) — Corrected & Fully Verified

#### 1. Architectural & Algorithmic Solutions Implemented
- **True Rhino-Style Point-to-Point Move Command (`Can I move`)**:
  - Implements authentic Rhino 3D point-to-point movement with complete pointer-based point picking and OSNAP:
    1. **Object Selection**: If objects are pre-selected, advances immediately to base point step. If invoked with no selection, prompts user to select object(s) in any viewport, transitioning immediately upon object pick.
    2. **Point to Move From (Base Point Specification)**:
       - Prompts user with exact text: `"Point to move from:"` in both the Command Bar and the bottom status bar (`"Point to move from: Pick a point, corner, or midpoint on an object"`).
       - **Strict Centroid Removal**: The selected object's center/centroid does **NOT** automatically become the source point. The base coordinate input field starts completely empty with a helpful hint (`"Click or X, Y, Z"`). A centroid button is available only as an explicit opt-in choice.
       - **Mesh Corner & Vertex OSNAP**: Pointer hover over any mesh corner or vertex extracts the exact world coordinate and snaps the cursor with a square reticle marker (`Sketch_Snap_Marker`, size 2.4 with center dot) and label `Endpoint (Corner)`.
       - **Mesh Edge Midpoint OSNAP**: Pointer hover along any of the 12 edges of a box (or arbitrary line segments) extracts the exact midpoint coordinate $(v_1 + v_2)/2$ and snaps with a diamond/triangle reticle marker and label `Midpoint`.
       - **Surface Raycasting & C-Plane Grid Fallback**: Clicking directly on an object face picks the exact 3D surface intersection point; clicking in space picks the C-plane grid coordinate.
       - **Base Anchor Visual Marker (`Move_Base_Marker`)**: Upon picking the source point, creates a distinct 3D marker consisting of a bright red sphere (radius 1.2), yellow 3D crosshairs (size 5.0), and a red orientation ring directly at the exact chosen corner/point.
    3. **Point to Move To (Destination Point Specification)**:
       - Prompts user with exact text: `"Point to move to:"` in both the Command Bar and the bottom status bar.
       - User can pick any destination point in the modeling workspace, including a vertex, corner, or edge midpoint on another object, or on the C-plane.
       - Full OSNAP snap markers, floating retro HUD badges (`[SNAP: Endpoint (Corner)] (X, Y, Z)`), and status bar coordinate readouts provide continuous real-time visual feedback.
    4. **Live Translation Preview**:
       - As the cursor moves, continuously renders a dynamic green rubberband line (`Move_Rubberband`) connecting the exact chosen source point to the destination point.
       - Renders an emerald translucent ghost preview mesh (`Move_Ghost_Preview`, `0x39ff14`, opacity 0.55) offset by $\Delta = \mathbf{P}_{\text{dest}} - \mathbf{P}_{\text{base}}$ across Top, Perspective, Front, and Right viewports.
       - Command Bar displays live `dX`, `dY`, `dZ` and Euclidean distance.
    5. **Exact Coincidence & Intact Solid Translation**:
       - Final movement translates the entire selection by $\text{Translation} = \text{Target Point} - \text{Source Point}$.
       - All geometry remains completely intact.
       - When a corner of Box A is moved to a corner of Box B, the two corners **exactly coincide**:
         $$|\mathbf{P}_{A,\text{corner}} - \mathbf{P}_{B,\text{corner}}| = 0.000\text{ mm}$$
- **Gumball Free Move Deliberate Slowdown (`0.04` Multiplier)**:
  - **Activation Isolation**: Gumball remains hidden by default upon selecting objects. Strictly activated via polite request `Can I gumball?` (with case-insensitivity and arbitrary trailing punctuation).
  - **Shift + M Guard**: Free Move interaction strictly requires `Shift + M + Click and Drag`.
  - **Deliberate Slowdown Multiplier (0.04)**: During Free Move dragging, a mathematical slowdown multiplier of `0.04` (4% displacement) is applied to the geometric displacement vector relative to the cursor:
    $$\vec{d}_{\text{slow}} = 0.04 \times (\mathbf{P}_{\text{pointer}} - \mathbf{P}_{\text{start}})$$
    - **Smooth 60fps Dragging**: Slows the actual geometric displacement rather than the pointer or browser; pointer tracking and raycasting remain 60fps smooth without artificial stutter, freezes, or dropped frames.
    - **Consistent Across Zoom & Viewports**: World-space displacement scaling ensures uniform 4% motion regardless of camera zoom factor or orthographic/perspective projection.
    - **Scope Isolation**: The slowdown strictly targets Gumball Free Move. Does **not** slow Rhino-style Move, axis-specific Gumball handles (X/Y/Z translate, rotate, scale), camera navigation (orbit, pan, zoom), or numeric coordinate inputs.
  - **Lifecycle Finalization**: Releasing the mouse/trackpad (`pointerup`) immediately ends the transformation, creates exactly one Undo step (`"Free Move (Shift+M)"`), immediately dismisses and hides the Gumball, and requires the user to enter `Can I gumball?` again before initiating another Gumball interaction.

#### 2. Verification & Visual Artifacts
- **Automated Test Suite**: Passes **91/91** unit tests (100% passing), including:
  - Test 16b: Rhino-style point-to-point Move initializes with exact prompt `"Point to move from:"`, registers base point and transitions to `"Point to move to:"`, generates live ghost preview and rubberband line, applies exact full-speed vector displacement, and rolls back cleanly via `Can I undo`.
  - Test 16c: OSNAP detects box corner vertex with `Endpoint (Corner)` classification, detects box edge center with `Midpoint` classification, verifies base point does not default to centroid, picks exact corner $(10, 20, 10)$, and moves to Box B corner $(30, 20, 20)$ resulting in exact corner coincidence ($|\mathbf{P}_A - \mathbf{P}_B| < 0.001\text{ mm}$).
  - Test 45h: Gumball Free Move applies deliberate slowdown multiplier of `0.04` (4% displacement) to geometry during Shift+M drag, dismisses Gumball on release, and creates 1 Undo step.
- **Visual Artifacts Automatically Opened in macOS Preview**:
  1. `rhino_move_step1_source_corner_selection.png`: Two boxes separated in space (`Box_A` in blue, `Box_B` in amber). Command Bar prompts `"Point to move from:"` with status hint and empty base input. Cursor hovers over Box A's specific top-front-right corner $(10.0, 20.0, 10.0)$, snapping with yellow reticle marker and floating CAD HUD badge `Endpoint (Corner) (10.0, 20.0, 10.0)`.
  2. `rhino_move_step2_dest_corner_live_preview.png`: Base marker (red sphere + yellow 3D crosshairs + red ring) anchored at Box A's chosen corner. Command Bar prompts `"Point to move to:"`. Cursor snaps to Box B's top-back-left corner $(30.0, 20.0, 20.0)$. Real-time green rubberband line connects the two corners, translucent emerald ghost preview translates to destination, and readout displays `dX: 20.0 dY: 0.0 dZ: 10.0 | Dist: 22.4 mm`.
  3. `rhino_move_step3_exact_corner_coincidence_verified.png`: Finalized move across all 4 viewports demonstrating exact corner coincidence between Box A and Box B ($|\mathbf{P}_{A,\text{corner}} - \mathbf{P}_{B,\text{corner}}| = 0.0000\text{ mm}$), verified with visual reticle and centered confirmation badge.
  4. `slow_gumball_free_move_4_percent.png`: Slow Gumball Free Move in action showing 3D Gumball handles centered on `Slow_Gumball_Box`, displaced smoothly by exactly 4.0mm in X and 4.0mm in Z after a 100mm cursor drag, verifying the exact 0.04 geometric multiplier.

---

### Milestone: User Acceptance Corrections (Insufficient Funds, Single-Edge Fillet/Chamfer, Compact Toolbar, and Ad Shuffle Bag)

#### 1. Architectural & Algorithmic Solutions Implemented
- **Insufficient Funds Modal (`Finger.jpg` + "haha broke bitch")**:
  - Maintained `<dialog id="modal-insufficient-funds">` with authentic Windows 95 titlebar, caption close `✕` button, and `[OK]` dismiss button.
  - Preserved `assets/Finger.jpg` in full fidelity.
  - Displays exactly the requested user text: **`haha broke bitch`** in bold UI font.
  - Guaranteed $0.00 deducted on failure: when a paid operation (e.g. Fillet/Chamfer at $49.00, Import at $10.00) is attempted with insufficient credits, the popup appears, fictional credit balance remains completely untouched, and no artificial delay is triggered.
  - Fully dismissible via `[OK]` button, caption close `✕`, or `Escape`, restoring normal workspace access.
- **Single-Edge Fillet and Chamfer Mesh Operations & Edge Selection**:
  - **Screen-Space Edge Proximity Detection**:
    - Projecting 3D edge world endpoints to viewport screen space with a generous 24px threshold (`findEdgeUnderPointer`).
    - Eliminates fragile raycasting misses on thin edge cylinders.
  - **Real-Time Hover Highlight & HUD Feedback**:
    - Hovering an edge in any viewport highlights it in bright orange (`0xff7700`, 4px width, enlarged 1.1mm midpoint dot) with real-time status bar readout:
      `[EDGE #0] VERTICAL (L=20.0mm) — Click to select`.
  - **Pointer-Based Edge Selection**:
    - Clicking an edge in the viewport toggles selection and updates the live preview immediately (`activeCommand.handlePointerDown`).
    - Supports selecting **exactly one edge**.
  - **Single-Edge Cut Geometry & Unaffected Mesh Preservation**:
    - `computeEdgeCutGeometry(mesh, mode, param, [edgeId])` constructs an orthonormal cutter basis aligned with the chosen edge's outward normals and subtracts it locally via ThreeCSG.
    - **Single-Edge Fillet**: Replaces the sharp 90° corner with a smooth 16-segment circular arc of specified radius. Leaves the other 11 edges and all 5 opposite faces completely untouched and planar. Computed normals ensure smooth shading along the fillet arc.
    - **Single-Edge Chamfer**: Replaces the sharp 90° corner with an exact flat 45° bevel plane of specified distance. Leaves all unaffected edges and corners completely intact.
    - **Full Interaction Lifecycle**: Live emerald preview mesh (`0x39ff14`), Cancel (`Esc` or `✕ Cancel`), Confirm (`Enter` or `✓ Apply`), and Undo (`Can I undo` restores intact original mesh). Fictional credits ($49.00) are only deducted upon successful confirmation.
- **Compact Feature Toolbar Layout**:
  - Replaced toolbar layout with an ultra-compact dense 2-column grid (`grid-template-columns: repeat(2, 30px); grid-auto-rows: 30px; gap: 2px; align-content: start;`).
  - Minimal 2px spacing between adjacent buttons; eliminates large blank vertical gaps.
  - Maintains clear Windows 95 beveled boundaries (`box-shadow: inset 1px 1px 0px var(--win95-midlight), inset -1px -1px 0px var(--win95-dark)`).
  - Preserved button relocation on click (`relocateToolbarIcons`).
- **Advertisement Shuffle Bag (Non-Replacement Pool)**:
  - Replaced unrestricted random selection with Fisher-Yates randomized selection without replacement across all 14 registered advertisements in `ASSET_MANIFEST.ads`.
  - Shows each advertisement exactly once per cycle before repeating any.
  - Automatically reshuffles when the bag is exhausted, with a boundary non-repeat check (`shuffled[0] !== lastShownAdIndex`).
  - Unified selection pool: both scheduled 7-command ads and stacked ad clicks (`pushAdLayer`) draw from the same bag.
  - Ad clicks and close buttons do not count as CAD commands.
  - Added dedicated Diagnostic HUD view displaying:
    - Remaining ads in current cycle (`dbg-ads-remaining`).
    - Shown ads in current cycle (`dbg-ads-shown-count`).
    - Ordered history of appeared ads in current cycle (`dbg-ads-history`).
    - Pending queue in current cycle (`dbg-ads-pending`).
- **Rhino-Style Point-to-Point Move**:
  - Preserved authentic point-to-point move workflow (`Can I move`), OSNAP corners (`Endpoint (Corner)`) and edge midpoints (`Midpoint`), live ghost preview and rubberband, exact corner coincidence ($0.0000\text{ mm}$ error), Cancel, and Undo.

#### 2. Verification & Visual Artifacts
- **Automated Test Suite**: Passes **94/94** unit tests (100% passing), including:
  - Test 48: Insufficient funds popup displays `Finger.jpg`, exact message `"haha broke bitch"`, and deducts $0.00.
  - Test 49: Advertisement shuffle bag draws all 14 registered ads without replacement and avoids cycle boundary repeats.
  - Test 50: Single-edge Fillet modifies only chosen edge with rounded geometry and preserves unaffected corners.
  - Test 51: Single-edge Chamfer modifies only chosen edge with 45-degree flat plane and preserves unaffected corners.
- **Visual Artifacts Automatically Opened in macOS Preview**:
  1. `ua_01_insufficient_funds_haha_broke_bitch.png`: Windows 95 dialog displaying `Finger.jpg` with exact text `"haha broke bitch"` and intact credit balance ($5.00).
  2. `ua_02_features_panel_compact_full_height.png`: Element-clipped full-height screenshot of the Features panel showing the compact 2×9 grid with minimal 2px spacing, classic beveled buttons, and zero vertical dead gaps.
  3. `ua_03_ad_shuffle_bag_debug_view.png`: Diagnostic HUD display showing 2/14 ads shown, 12/14 remaining in bag, and complete pending queue.
  4. `ua_04_fillet_01_before_sharp_edge_closeup.png`: Close-up of box before Fillet showing sharp 90° corner.
  5. `ua_04_fillet_02_single_edge_selected_preview.png`: Close-up during Fillet showing single selected edge in yellow/orange and emerald preview arc.
  6. `ua_04_fillet_03_completed_rounded_solid_closeup.png`: Close-up after Fillet showing smooth 16-segment rounded curve and unaffected planar faces.
  7. `ua_05_chamfer_01_before_sharp_edge_closeup.png`: Close-up of box before Chamfer showing sharp 90° corner.
  8. `ua_05_chamfer_02_single_edge_selected_preview.png`: Close-up during Chamfer showing single selected edge and emerald preview bevel.
  9. `ua_05_chamfer_03_completed_beveled_solid_closeup.png`: Close-up after Chamfer showing flat 45° bevel plane and unaffected planar faces.

---

## 11. Rigorous Geometry Verification: Watertight Manifold Fillet & Chamfer

### 11.1 Problem Diagnosis & Root Cause
In prior revisions, single-edge Fillet and Chamfer relied on `ThreeCSG` boolean subtraction between the base box and an extruded cutter wedge/cylinder. Due to coplanar face splitting and T-junction vertex shearing along the boundaries, CSG subtractions generated topological non-manifoldness:
- CSG Chamfer produced 16 open boundary edges ($\chi \neq 2$).
- CSG Fillet produced 102 open boundary edges ($\chi \neq 2$).
While visually appearing beveled/rounded from certain angles, the underlying mesh was not watertight or 2-manifold.

### 11.2 The Solution: Exact 2-Manifold B-Rep Polygon Extrusion (`buildBoxManifoldCut`)
To achieve true CAD-grade solid geometry, we implemented an exact B-Rep polyhedral generator directly in [`index.html`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html#L6178-L6355):
1. **Local Cross-Section Transformation**: For any straight 90° convex edge of a box prism $[-h_x, h_x] \times [-h_y, h_y] \times [-h_z, h_z]$, the 3D solid is represented as a 2D polygonal cross-section extruded along the edge's longitudinal axis.
2. **Exact 2D Profile Replacement**:
   - **Chamfer (2.0 mm)**: Replaces the 90° rectangular corner $(u_{max}, v_{max})$ with a flat 45° planar segment between $(u_{max} - d, v_{max})$ and $(u_{max}, v_{max} - d)$. Produces an exact 5-sided convex polygon prism.
   - **Fillet (2.0 mm)**: Replaces the 90° rectangular corner with a $G^1$ tangent circular arc of exact radius $r=2.000\text{ mm}$ discretized into 16 smooth facet segments. The arc centers at $(u_{max} - r, v_{max} - r)$. Produces an exact 20-sided polygon prism.
3. **Topological Polyhedron Construction**:
   - Two planar end caps (triangulated fan with outward normal signs matching $\pm \hat{W}$).
   - Lateral face quads along each segment of the 2D perimeter, split into outward-winding triangle pairs.
   - All shared internal faces are topologically contiguous; zero T-junctions, zero duplicate edges.

### 11.3 Side-by-Side Mathematical & Geometric Verification
Automated browser verification (`scripts/verify_geometry_fillet_chamfer.py`) tested two independent $20 \times 20 \times 20\text{ mm}$ solid boxes positioned side-by-side:
- **Left**: Original Unmodified Solid Box (centered at $x = -15, y = 10, z = 0$).
- **Right**: Modified Solid Box (centered at $x = +15, y = 10, z = 0$) with Edge #0 ($x=+10, z=+10$ vertical edge) modified with 2.0 mm radius/distance.

#### Mathematical Telemetry Summary
| Metric | Original Box | Fillet Solid (2.0 mm) | Chamfer Solid (2.0 mm) |
|---|---|---|---|
| **Vertices ($V$)** | 24 (split) / 8 unique | 40 unique | 10 unique |
| **Edges ($E$)** | 36 (12 unique) | 114 | 24 |
| **Faces ($F$)** | 12 triangles | 76 triangles | 16 triangles |
| **Euler Characteristic ($\chi = V - E + F$)** | **2** (Sphere topology) | **2** (Sphere topology) | **2** (Sphere topology) |
| **Open Boundary Edges** | **0** (100% Watertight) | **0** (100% Watertight) | **0** (100% Watertight) |
| **Non-Manifold Edges** | **0** (100% 2-Manifold) | **0** (100% 2-Manifold) | **0** (100% 2-Manifold) |
| **Cut Radius / Distance** | N/A (sharp 90°) | **$2.000000\text{ mm}$** (Exact) | **$2.000000\text{ mm}$** (Exact) |
| **Bevel Chord Width** | N/A | N/A | **$2.8284\text{ mm}$** ($2\sqrt{2}$) |
| **Bounding Box ($X \times Y \times Z$)** | $20.0 \times 20.0 \times 20.0\text{ mm}$ | $20.0 \times 20.0 \times 20.0\text{ mm}$ | $20.0 \times 20.0 \times 20.0\text{ mm}$ |
| **Solid Volume** | $8000.000\text{ mm}^3$ | $7982.807\text{ mm}^3$ | $7960.000\text{ mm}^3$ |
| **Volume Deficit ($\Delta V$)** | $0.000\text{ mm}^3$ | $-17.193\text{ mm}^3$ (Exact $(1 - \pi/4) r^2 L$) | $-40.000\text{ mm}^3$ (Exact $\frac{1}{2} d^2 L$) |

### 11.4 Visual Proof Artifacts (Multiple Viewports & Angles)
All screenshots were captured without selection highlighting or Gumball handles, displaying clear black edge geometry and face facet lines:
1. **Fillet Overview (4 Viewports)**: [`geom_01_fillet_4viewports_side_by_side.png`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/geom_01_fillet_4viewports_side_by_side.png)
   - Left: Original sharp box; Right: 2.0 mm filleted box simultaneously across Top, Perspective, Front, and Right viewports.
2. **Fillet Close-Up (Perspective)**: [`geom_02_fillet_perspective_closeup_side_by_side.png`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/geom_02_fillet_perspective_closeup_side_by_side.png)
   - High-zoom perspective revealing the 16 facet strips of the smooth cylindrical arc on Edge #0 and pristine planar side/top faces.
3. **Fillet Top-View Contour**: [`geom_03_fillet_top_view_corner_contour.png`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/geom_03_fillet_top_view_corner_contour.png)
   - Orthographic plan view comparing the sharp 90° corner against the true tangent circular arc contour ($r=2.0\text{ mm}$).
4. **Fillet Right-View Profile**: [`geom_04_fillet_right_view_unaffected_profile.png`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/geom_04_fillet_right_view_unaffected_profile.png)
   - Orthographic elevation proving unaffected edges, vertical planar faces, and overall box dimensions ($20\text{ mm}$) remain completely unaltered.
5. **Chamfer Overview (4 Viewports)**: [`geom_05_chamfer_4viewports_side_by_side.png`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/geom_05_chamfer_4viewports_side_by_side.png)
   - Left: Original sharp box; Right: 2.0 mm chamfered box simultaneously across Top, Perspective, Front, and Right viewports.
6. **Chamfer Close-Up (Perspective)**: [`geom_06_chamfer_perspective_closeup_side_by_side.png`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/geom_06_chamfer_perspective_closeup_side_by_side.png)
   - High-zoom perspective showing the clean 45° flat planar bevel facet replacing Edge #0.
7. **Chamfer Top-View Contour**: [`geom_07_chamfer_top_view_bevel_cut.png`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/geom_07_chamfer_top_view_bevel_cut.png)
   - Orthographic plan view showing the diagonal 45° cut between $(8, 10)$ and $(10, 8)$.
8. **Chamfer Right-View Profile**: [`geom_08_chamfer_right_view_unaffected_profile.png`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/geom_08_chamfer_right_view_unaffected_profile.png)
   - Orthographic elevation confirming pristine height ($20\text{ mm}$) and flat unaffected faces.

### 11.5 Scope Boundaries & Unsupported Geometry Types
In accordance with honest CAD reporting:
- **Supported Geometries**:
  - Convex 90° boundary edges on rectangular solid boxes and prisms (all 12 edges: vertical parallel to Y, horizontal parallel to X, horizontal parallel to Z).
  - Single-edge operations and multiple non-intersecting parallel edges.
- **Currently Unsupported Geometries (Limitations)**:
  1. *Curved Edges*: Cylindrical rim edges, circular pipes, or revolved forms.
  2. *Non-90° Dihedral Angles*: Triangular prisms, polyhedra, or arbitrary angle chamfers.
  3. *Concave Internal Edges*: Internal step corners or hollow pocket edges (would require inverse B-Rep addition or CSG boolean union).
  4. *Multi-Edge Vertex Corner Blends*: When two or three edges meeting at the same corner vertex are filleted simultaneously, true CAD systems require rolling-ball spherical corner setback patches (e.g. blend sphere or octant surface). Currently, multi-edge corner junctions fall back to CSG or require sequential independent edge cuts.
  5. *Arbitrary Imported Meshes*: Non-manifold or triangle-soup meshes without defined B-Rep topology.

---

## 12. Build v00000-012 — Startup Exception Repair & Rendering Recovery

### 12.1 Incident Diagnosis & Root Cause Analysis
Following the release of build `v00000-011` (`fb95d7e`), all four viewports rendered completely blank despite geometry appearing in the FeatureManager tree.
- **Root Cause**: In commit `34fa0c3`, `<button id="btn-close-construction">` was removed from the `#modal-construction` dialog in `index.html`. However, line 7974 retained an unconditional event listener attachment:
  ```javascript
  document.getElementById("btn-close-construction").onclick = () => { ... };
  ```
- **Impact**: Because `document.getElementById("btn-close-construction")` returned `null`, JavaScript threw an uncaught `TypeError: Cannot set properties of null (setting 'onclick')` during initial script execution.
- **Cascading Failure**: This unhandled exception immediately aborted script execution before the main initialization block could reach `initScene()`, `setupViewports()`, and the continuous `render()` loop. Consequently, all 4 WebGL viewports remained unrendered.

### 12.2 Implemented Repairs & Defensive DOM Audit
1. **Primary Fix**: Restored `<button class="win95-btn" id="btn-close-construction">OK</button>` inside `#modal-construction` and wrapped the click handler registration with a defensive null check.
2. **Comprehensive DOM Handler Audit**: Audited all DOM event bindings across `index.html`. Added defensive guards around all modal open/close buttons, toolbar action buttons, file input listeners, search inputs, debug toggles, and status elements:
   - `showConfirmModal`
   - `btn-tutorial-open`, `btn-close-onboarding`
   - `btn-buy-credits`
   - `btn-about-open`, `btn-close-about`
   - `help-search`, `btn-help-open`, `btn-close-help`
   - `chip` (version purge button)
   - `status-message`
   - `btn-save-project`, `btn-open-project`, `btn-export-mesh`, `btn-import-mesh`, `btn-theme-toggle`, `btn-audio-mute`
   - `btn-export-download`, `btn-export-cancel`
   - `btn-cmd-confirm`, `btn-cmd-cancel`
   - `btn-submit-request`
   - `file-input-open`, `file-input-import`
   - `debug-hud-toggle`

### 12.3 Automated & Headless Verification
1. **Console Diagnostics**: Evaluated in headless Chrome via Chrome DevTools Protocol (`Runtime.exceptionThrown`); verified **0 uncaught exceptions** on startup.
2. **Unit Test Suite**: 96/96 automated tests passed (100% pass rate).
3. **Viewport Render Verification**: Verified all 4 viewports (Top, Perspective, Front, Right) render active scenes correctly.

### 12.4 Visual Proof Artifacts
1. **Startup Michigan Render**:
   [repaired_01_michigan_startup.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/repaired_01_michigan_startup.png)
   - Verified Michigan block letter geometry rendered crisp and centered across all 4 viewports upon startup.
2. **New Box Primitive Render**:
   [repaired_02_new_box_rendered.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/repaired_02_new_box_rendered.png)
   - Verified creating a new box primitive (`Can I box`) immediately renders in all four viewports and adds to the FeatureManager tree.
3. **WASD Perspective Orbit**:
   [repaired_03_camera_orbited.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/repaired_03_camera_orbited.png)
   - Verified W/S/A/D keyboard orbit moves Perspective camera smoothly while Top, Front, and Right orthographic views remain stably locked.
4. **Arrow Pan & Shift+Arrow Zoom**:
   [repaired_04_camera_pan_zoom.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/repaired_04_camera_pan_zoom.png)
   - Verified arrow panning and shift+arrow zooming function across active viewports.
5. **Additional Geometry Commands**:
   [repaired_05_sphere_primitive.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/repaired_05_sphere_primitive.png)
   - Verified sphere and other primitive geometry commands execute cleanly.

### 12.5 Deployment & Acceptance Status
- **Backup Branch**: `backup-v00000-011` remains preserved at commit `fb95d7e`.
- **Cache Version**: Incremented to `v00000-012` across `index.html` (HUD, Status Chip, About Dialog, `APP.version`) and `sw.js` (`const VERSION = "v00000-012"`).
- **Live URL**: `https://mrandybuck.github.io/single-file-html-app-template/`
- **Acceptance Status**: *Awaiting User Acceptance in Safari*. Do NOT mark USER ACCEPTED until user verifies Michigan and newly created geometry render correctly in Safari.

---

## 13. UI & Feature Updates (Development Branch `dev`)

### 13.1 Requirements Addressed
1. **Remove Light / Dark Mode Completely**:
   - Removed the `#btn-theme-toggle` button from the Windows 95 standard toolbar.
   - Removed the `#mitem-view-theme` entry from the View menu and action map.
   - Removed theme-switching logic and locked the application to a single permanent Windows 95 retro dark-slate theme (`0x203040` background, standard win95-silver chrome).
   - Preserved all toolbar spacing, layout, and event handlers without runtime errors.
   - Updated Request Bar handlers (`theme`, `light`, `dark`) and crash diagnostics report to indicate fixed retro theme.

2. **Make Blue Logo / Title Section Roughly Twice as Big**:
   - Increased the top-left `.win95-title-content` section width from ~195px to `width: 420px; min-width: 420px;` (roughly 2x expansion).
   - Retained the retro Windows 95 icon, bold typeface, gap spacing (`gap: 8px;`), and flush-right title bar caption controls (Minimize, Maximize, Close) without layout distortion.

3. **10 New Side-Panel Tool Icons with Retro "Coming Soon" Modal**:
   - Added 10 CAD command icons to the right-side Features toolbar (`.modeling-toolbar-body`):
     1. **Sweep** (`#tool-sweep`)
     2. **Pipe** (`#tool-pipe`)
     3. **Loft** (`#tool-loft`)
     4. **Shell** (`#tool-shell`)
     5. **Offset** (`#tool-offset`)
     6. **Mirror** (`#tool-mirror`)
     7. **Array** (`#tool-array`)
     8. **Trim** (`#tool-trim`)
     9. **Extend** (`#tool-extend`)
     10. **Project** (`#tool-project`)
   - Configured compact 24x24 vector SVG icons matching the app's retro mechanical aesthetic.
   - Built the `<dialog id="modal-coming-soon">` dialog with Windows 95 title bar, close caption button, classic yellow triangle warning graphic, dynamic title (`<Tool> — Coming Soon`), explanatory text, and beveled 3D OK button (`#btn-close-coming-soon`).
   - Integrated with toolbar click delegator to trigger the dialog, log a system note, and initiate ergonomic icon relocation.

4. **Asymmetrical Chamfer and Asymmetrical Fillet Support**:
   - **Interpretation & Geometry Engine**:
     - *Asymmetrical Chamfer*: Two-distance chamfer ($D_1$ along axis $u$, $D_2$ along axis $v$). Connects $(u_{max}, v_{max} - pv)$ to $(u_{max} - pu, v_{max})$ on cut corners.
     - *Asymmetrical Fillet*: Non-uniform elliptical fillet ($R_1$ along axis $u$, $R_2$ along axis $v$). Evaluated as an exact quadrant ellipse $u(t) = \text{center}_u + pu \cos(t)$, $v(t) = \text{center}_v + pv \sin(t)$, ensuring $G^1$ tangential continuity with adjacent planar faces.
     - Supports both the exact 2-manifold B-Rep extrusion generator (`buildBoxManifoldCut`) and the CSG polygon cutter fallback (`computeEdgeCutGeometry`).
     - Mathematically verified as 100% watertight closed 2-manifold meshes with Euler characteristic $\chi = V - E + F = 2$.
   - **Command Bar UI**:
     - Added `#fillet-param-type` dropdown with `Symmetric` and `Asymmetric` options.
     - In Symmetric mode: displays `Radius:` / `Distance:` with single input `#fillet-param-val`.
     - In Asymmetric mode: displays `R1:` / `D1:` (`#fillet-param-val`) and reveals second input container `#fillet-container-val2` with label `R2:` / `D2:` and input `#fillet-param-val2`.
     - Live emerald preview (`0x39ff14`) updates dynamically as values change.
     - Confirmed solids are tagged with `userData.type = "AsymChamferedSolid"` / `"AsymFilletedSolid"` and custom FeatureManager tree names (`AsymChamfer_N`, `AsymFillet_N`).
   - **Request Bar Command Parser**:
     - Multi-parameter support: `Can I chamfer <d1> <d2>` (e.g. `Can I chamfer 2 6`) and `Can I fillet <r1> <r2>` (e.g. `Can I fillet 2 6`).
     - Natural language prefixes: `Can I asym chamfer <d1> <d2>` and `Can I asym fillet <r1> <r2>`.

### 13.2 Automated & Headless Verification
- **Automated In-App Test Suite**: 103/103 tests passed (0 failures).
- **New Unit Tests Added**:
  - `Test 18f`: Asymmetrical Chamfer generates `AsymChamferedSolid` with verified watertight manifold topology ($\chi = 2$).
  - `Test 18g`: Asymmetrical Fillet generates `AsymFilletedSolid` with verified watertight manifold topology ($\chi = 2$).
  - `Test 18h`: All 10 placeholder tool icons exist in Features dock and clicking opens `#modal-coming-soon`.
  - `Test 18i`: Top-left blue logo/title section is roughly 2x wider ($\ge 380\text{px}$).
  - `Test 29`: Light/Dark theme toggle completely removed and permanent retro theme active.

### 13.3 Visual Proof Artifacts
1. **10 Placeholder Tools & Retro "Coming Soon" Modal**:
   [features_01_placeholder_coming_soon.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/features_01_placeholder_coming_soon.png)
   - Displays all 10 new tool icons in the right-side toolbar, the 2x widened blue header title, and the retro Windows 95 "Coming Soon" warning dialog.
2. **Asymmetrical Chamfer Solid Rendered**:
   [features_02_asymmetric_chamfer.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/features_02_asymmetric_chamfer.png)
   - Displays completed asymmetrical chamfer ($D_1 = 2.0\text{ mm}, D_2 = 6.0\text{ mm}$) on vertical box edges, verified in Top (X/Z) view showing distinct $2\text{mm} \times 6\text{mm}$ bevel cuts, with `AsymChamferedSolid` in the FeatureManager tree.
3. **Asymmetrical Fillet Solid Rendered**:
   [features_03_asymmetric_fillet.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/features_03_asymmetric_fillet.png)
   - Displays completed asymmetrical fillet ($R_1 = 2.0\text{ mm}, R_2 = 6.0\text{ mm}$) with elliptical rounded corner curvature across Top and Perspective viewports, with `AsymFilletedSolid` in the FeatureManager tree.
4. **Clean Workspace Overview**:
   [features_04_full_ui_overview.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/features_04_full_ui_overview.png)
   - Comprehensive full-window UI overview demonstrating the 2x blue header title area, absence of theme switcher, 10 new tool icons, active FeatureManager tree, and 4-viewport matrix rendering Michigan and multiple 3D solids.
5. **Full Test Suite All 103 Tests Passed**:
   [features_05_test_results_passed.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/features_05_test_results_passed.png)
   - Displays in-app test results terminal log confirming 103/103 tests passed with 0 failures.

### 13.4 Release & Deployment Status
- **Current Version**: `v00000-013` (incremented across `index.html` and `sw.js`).
- **Main Branch**: Merged from `dev` with all approved UI and feature updates.
- **Backup Branch**: `backup-v00000-011` remains preserved at `fb95d7e`.
- **Live URL**: `https://mrandybuck.github.io/single-file-html-app-template/`
- **User Approval**: Approved by user for merge to `main`.

---

## 14. Checkpoint A — Critical Sketching Repair (Interactive Sketching Fix)

### 14.1 Root Cause Diagnosis
1. **Uncleaned Rubberband Previews**:
   - In `updateRubberband(currentPt, vp)`, `scene.remove(rubberbandObj)` was only called in `line` mode.
   - For `rect` and `circle`, `rubberbandObj = new THREE.Line(geo, mat); scene.add(rubberbandObj);` was called on **every pointermove event** without removing or disposing the prior preview object from the Three.js scene.
   - Moving the cursor across the canvas added 20–50+ transient `THREE.Line` preview instances directly to `scene.children`.
   - On Corner 2 click, `cancelSketch()` only removed the single last line referenced by `rubberbandObj`, leaving all preceding preview lines as permanent zombie outlines visible across all viewports.
2. **Missing Input Event Button Validation**:
   - `handleViewportPointerDown(e, vpId)` did not verify `e.button === 0`, permitting non-left or stray button events during navigation/orbiting to trigger sketch points.
3. **Missing Command Bar Integration & Lifecycle Hooks**:
   - `startSketch("rect")` and `startSketch("circle")` lacked dedicated command bar setups (`setupRectCommand`, `setupCircleCommand`), leaving the user without plane selection, coordinate inputs, prompt instructions, or cancel button synchronization.
4. **Disposal & Memory Leaks**:
   - Transient preview objects lacked GPU buffer disposal (`geometry.dispose()`, `material.dispose()`), leaking memory on each cursor motion.

### 14.2 Architecture of the Solution
- **Systematic Preview Cleanup (`clearPreviewObjects()`)**:
  - Implemented `disposeObjectHierarchy(obj)` to recursively dispose geometry and materials.
  - Implemented `clearPreviewObjects()` which disposes `rubberbandObj` and purges any lingering objects tagged `Sketch_Rubberband`, `Sketch_Preview`, or `userData.isTransientPreview` directly from `scene`.
  - `updateRubberband()` invokes `clearPreviewObjects()` at the beginning of each frame before generating a single preview group.
- **Single Transient Group**:
  - `rect`, `circle`, `line`, and `polyline` each maintain exactly one `THREE.Group` named `"Sketch_Rubberband"` with `userData: { isTransientPreview: true }`, containing boundary preview lines, anchor markers, and dynamic status readouts.
- **Clean Interactive Workflows**:
  - **Rectangle**: Toolbar icon / `Can I rectangle` activates `rect` mode. Corner 1 sets anchor point without committing. Pointer movement maintains exactly one preview. Corner 2 commits exactly one `ClosedProfile` (`THREE.LineLoop` with 4 points and `THREE.Shape`), automatically exits command mode, selects the profile, and updates FeatureManager.
  - **Single Undo**: One `Can I undo` / `executeUndo()` reverts scene objects and removes the complete rectangle profile in a single step.
  - **3D Solid Extrudability**: The closed profile is immediately recognized by `extrudeSelectedProfile` and `Can I extrude`, creating a true 3D `ExtrudedSolid`.
  - **Two-Click Line**: Two clicks create exactly one `SketchCurve` segment and automatically exit the command.
  - **Connected Polyline**: Connected-line mode (`Can I polyline`) chains segments with shared endpoints until closed into a `ClosedProfile` or completed via Enter / `[✓ Finish]`.
  - **Circle**: Center click + radius click commits exactly one `ClosedProfile` circle with attached `THREE.Shape` and automatically exits.

### 14.3 Automated & Headless Verification
- **Automated In-App Test Suite**: **113/113 tests passed (100% passing, 0 failures)**.
  - `Test 12d`: Connected sketch lines (polyline), endpoint snapping to closed profile, and 3D solid extrusion.
  - `Test 12e`: Two-click line segment creation, auto-exit, and single-step undo removal.
  - `Test 13`: 2D closed rectangle profile interactive workflow, 4 boundary points, auto-exit, and single-step undo removal.
  - `Test 14`: 2D closed circle profile interactive workflow, center/radius clicks, auto-exit, and single-step undo removal.
  - `Test 15`: 3D solid extrusion of closed 2D profiles (`ExtrudedSolid`).
- **CDP Pointer-Interaction Test (`scripts/verify_sketch_repair.py`)**:
  - **DPR 1.0 (Standard Display)**:
    - 25 continuous pointer moves during rectangle drawing: `Preview counts: min=1, max=1` (0 duplicate outlines).
    - Corner 2 click: `sceneObjects` incremented from 26 to 27 (exactly 1 new object).
    - Rectangle geometry: exactly 4 corner points `[(-19.5, 0, -16.5), (18.75, 0, -16.5), (18.75, 0, 10), (-19.5, 0, 10)]`, `type: ClosedProfile`, `closed: true`, `isLineLoop: true`, `hasShape: true`.
    - Clicking elsewhere produced 0 additional objects.
    - Single Undo reverted `sceneObjects` to 26 (complete removal).
    - Redo restored rectangle; `extrudeSelectedProfile(18)` produced `Extrude_41` (`ExtrudedSolid`, 132 vertices).
    - Circle: 1 center + 1 radius click created `Circle_Profile_43` (r=10.5).
    - Line: 2 clicks created `Line_44` (`SketchCurve`, 2 points).
  - **DPR 2.0 (Retina Display)**:
    - `window.devicePixelRatio = 2.0`.
    - Rectangle created at DPR 2.0: exactly 1 `ClosedProfile` (`Rect_Profile_45`, 4 points).
    - 0 coordinate conversion or hit-testing offset defect.

### 14.4 Visual Proof Artifacts
1. **Live Rectangle Preview (Exactly 1 Outline, No Multiples)**:
   [sketch_01_rect_preview.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/sketch_01_rect_preview.png)
   - Demonstrates active cursor drag across Top C-Plane showing exactly one green preview outline with yellow/cyan corner anchor dots and dynamic Command Bar coordinates readout.
2. **Committed Rectangle (Exactly 1 Entity, 4 Edges, Auto-Exit)**:
   [sketch_02_rect_committed.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/sketch_02_rect_committed.png)
   - Demonstrates committed rectangle `Rect_Profile_41` with yellow selection highlight across Top, Perspective, Front, and Right viewports. All previews cleanly removed; command bar auto-dismissed.
3. **Extruded 3D Solid Box from Rectangle Profile**:
   [sketch_03_rect_extruded.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/sketch_03_rect_extruded.png)
   - Demonstrates true 3D solid box `Extrude_41` (height 18mm) with shaded faces, wire edges, and FeatureManager registration.
4. **Circle and Line Workflows**:
   [sketch_04_circle_and_line.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/sketch_04_circle_and_line.png)
   - Demonstrates completed circle profile `Circle_Profile_43` (r=10.5) and 2-click line segment `Line_44`.
5. **Retina DPR 2.0 Verification**:
   [sketch_05_retina_dpr2_rect.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/sketch_05_retina_dpr2_rect.png)
   - Full 2880x1800 2x Retina capture demonstrating crisp rendering and accurate coordinate hit-testing of `Rect_Profile_45`.

### 14.5 Deployment & Acceptance Gate
- **Build Version**: Bumped to `v00000-014` across `index.html` and `sw.js`.
- **Deployment Status**: Approved for deployment of Checkpoint A (sketching repair and dependencies only) to GitHub Pages for user testing.
- **User Acceptance Status**: **ACCEPTED BY USER** (hands-on Safari testing confirmed: *"Test was sucessful"*).

---

## 15. Checkpoints B–F Implementation & Verification Summary

### 15.1 Checkpoint B — Header Redesign
- **Requirement**:
  - Increase vertical height of the blue CADN'T title bar to approximately twice its current height (~44px vs original 22px).
  - Remove fixed width lock (`width: 420px; min-width: 420px;`) so it flexes naturally across the top.
  - Remove `[Part1.prt : 4 Viewports]` from the title bar.
  - Display clean, prominent `CADN'T` branding with the 24x24 application icon and 14px bold typography.
  - Preserve classic Windows 95 beveled caption buttons (`_`, `□`, `✕`) scaled to 22px x 20px.
- **Automated Verification**:
  - `Test 18i`: Asserts `#win95-title-bar` bounding client height $\ge 40\text{px}$, title contains `CADN'T`, and does NOT contain `[Part1.prt : 4 Viewports]`. (Passed).
- **Visual Artifact**:
  - [checkpoint_b_header_redesign.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_b_header_redesign.png) (Height: 44px, clean title `CADN'T`).

### 15.2 Checkpoint C — Functional Pipe Command (`Can I pipe`)
- **Requirement**:
  - Accepted syntax: `Can I pipe` or clicking the `#tool-pipe` button in the Features toolbar.
  - Workflow:
    1. Select an existing line or polyline curve.
    2. Invoke Pipe.
    3. Enter diameter or radius in Command Bar (live emerald preview updating dynamically).
    4. Confirm to generate a real 3D solid.
    5. Register in FeatureManager as `PipeSolid` (`Pipe_N`).
    6. Support selection, moving, undoing, saving, and exporting.
  - Prioritize straight lines and planar polylines; report unsupported path types clearly (e.g. solid boxes) with disabled confirm button.
- **Geometry & Topology Engine (`buildPipeSolidGeometry`)**:
  - Sweeps a circular cross-section ($N=16$ radial segments) along path points using local Frenet-Serret orthonormal frames.
  - Generates watertight circular end cap disks at start and end vertices.
  - Strict topological manifold verification (`verifyMeshManifold`):
    - Straight line test ($L=30, R=3.0$): Watertight = `true`, Manifold = `true`, Open Edges = `0`, Non-Manifold Edges = `0`, Euler characteristic $\chi = 2$ ($V - E + F = 206 - 612 + 408 = 2$).
    - L-shaped polyline test ($L_1=25, L_2=20, R=2.5$): Watertight = `true`, Manifold = `true`, Open Edges = `0`, Non-Manifold Edges = `0`, Euler characteristic $\chi = 2$ ($V - E + F = 398 - 1188 + 792 = 2$).
  - Single Undo step restores pre-pipe document state.
- **Automated Verification**:
  - `Test 18j`: Straight line pipe preview, dimensions, and capped watertight 2-manifold solid ($\chi=2$).
  - `Test 18k`: L-shaped polyline pipe with capped watertight 2-manifold solid ($\chi=2$).
  - `Test 18l`: Pipe solid creation undoability via `Can I undo`.
  - `Test 18m`: Unsupported path error reporting on non-curve objects with disabled confirm button.
- **Visual Artifacts**:
  - [checkpoint_c_01_pipe_preview.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_c_01_pipe_preview.png) (Live emerald preview along line curve).
  - [checkpoint_c_02_pipe_straight_solid.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_c_02_pipe_straight_solid.png) (Committed 3D straight solid `Pipe_3`, FeatureManager registration).
  - [checkpoint_c_03_pipe_l_solid.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_c_03_pipe_l_solid.png) (Committed 3D L-shaped solid `Pipe_5`, FeatureManager registration).

### 15.3 Checkpoint D — Michigan Removal Alias
- **Requirement**:
  - Retain `Can I remove starting object`.
  - Add alias `Can I delete michigan`.
  - Case-insensitive, tolerant of trailing punctuation (`Can I delete michigan?`).
  - Both trigger identical confirmation dialog: *"Are you sure you want to remove this? Removing the starting geometry will clear it from the workspace. You can restore it using 'Can I undo'."*
  - Ordinary Delete key remains strictly blocked from deleting Michigan.
  - Deletion is fully undoable via `Can I undo`.
- **Automated Verification**:
  - `Test 6`: Starting object immune to standard Delete key.
  - `Test 7`: Both `Can I remove starting object` and `Can I delete michigan?` delete Michigan upon confirmation and restore upon undo.
- **Visual Artifact**:
  - [checkpoint_d_delete_michigan_dialog.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_d_delete_michigan_dialog.png) (Confirmation dialog triggered by `Can I delete michigan?`).

### 15.4 Checkpoint E — Much Slower Gumball
- **Requirement**:
  - Free move multiplier reduced from 0.04 to **0.01** (1% displacement rate).
  - Gumball hidden by default; activated strictly via `Can I gumball?`.
  - Free move strictly guarded by Shift + M modifier keys.
  - Rhino-style `Can I move` completely unaffected.
  - Releasing pointerup after free move:
    1. Commits transformation.
    2. Creates 1 Undo step.
    3. Immediately hides Gumball.
    4. Deactivates Gumball mode.
    5. Requires typing `Can I gumball?` again to reactivate.
- **Automated Verification**:
  - `Test 45f`: Free move drag and pointerup immediately hides Gumball, deactivates mode, and creates 1 Undo step.
  - `Test 45g`: Undo restores object displaced by Free Move to exact pre-move position.
  - `Test 45h`: Free move applies deliberate slowdown multiplier of 0.01 (1% displacement).
- **Visual Artifacts**:
  - [checkpoint_e_01_gumball_active.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_e_01_gumball_active.png) (Gumball handles active on selected object).
  - [checkpoint_e_02_gumball_dismissed.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_e_02_gumball_dismissed.png) (Gumball completely hidden and dismissed on pointerup, status bar readout).

### 15.5 Checkpoint F — Audio Changes
- **Requirement**:
  - Remove user-facing Sound/Mute button (`#btn-audio-mute`) from toolbar.
  - Remove `#mitem-view-sound` menu item and separator from View dropdown menu.
  - Set hold-music playback volume to 100% (`1.0`).
  - Preserve non-looping playback, loading triggers, stop on completion, and autoplay compliance.
- **Automated Verification**:
  - `Test 30`: Asserts `#btn-audio-mute` and `#mitem-view-sound` are null.
  - `Test 36`: Asserts hold music plays at 100% volume (`1.0`), does not loop, and stops cleanly.
- **Visual Artifact**:
  - [checkpoint_f_toolbar_clean.png](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots/checkpoint_f_toolbar_clean.png) (Clean toolbar without sound/mute controls).

### 15.6 Historical Git Status (v0.14 Milestone)
- **Historical Build Version**: `v00000-014`
- **Historical Tests**: 118 / 118 passing.

---

## 16. Milestone v00000-015: Sketching Fixes, Commands, and Sphere Sabotage (Checkpoints A–F)

> **Active Branch:** `dev` (Commit [`5f6d7e7`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app))  
> **Base Branch:** `main` (Commit [`4844d59`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app))  
> **Source File:** [`index.html`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html) (`v00000-015`)  
> **Automated Test Suite:** **156 / 156 Passing (100% Pass, 0 Failures)**  
> **Verification Scripts:** [`verify_checkpoints_b_f.py`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/scripts/verify_checkpoints_b_f.py) and [`verify_checkpoint_a_spline.py`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/scripts/verify_checkpoint_a_spline.py)  
> **Screenshots Output:** [`/Users/andybuck/Desktop/CADNT_Screenshots`](file:///Users/andybuck/Desktop/CADNT_Screenshots) (mirrored by [`/Users/andybuck/Desktop/CADNT_Screenshot`](file:///Users/andybuck/Desktop/CADNT_Screenshot))

---

### 16.1 Checkpoint A — Repair Spline (Accepted by User & Merged to `main`)
- **Problem**: Previous spline sketching produced a straight 2-point line instead of a genuine multi-point curve.
- **Implementation**:
  - Implemented `startSketch("spline")` and `setupSplineCommand()` using Three.js `THREE.CatmullRomCurve3`.
  - Supports clicking arbitrary control points in any active construction plane (Top X/Z, Front X/Y, Right Z/Y, Perspective).
  - Live curved rubberband preview updating dynamically as the pointer moves.
  - Requires at least 3 control points; enables `[✓ Finish (Enter)]` once $\ge 3$ points are placed.
  - Cancel with `Escape` or `[✕ Cancel]`.
  - Stored as a single editable sketch entity (`SplineCurve`) with 51 sampled curve vertices for smooth WebGL display.
  - Preserves underlying raw control point data in `userData.controlPoints`.
  - Interactive 3D control point handles (`Group` with yellow sphere gizmos) appear when selected.
  - Dragging or editing control points dynamically recalculates curve interpolation in real-time.
  - Full serialization in `serializeProjectState()` and `deserializeProjectState()` (`.cadnt` project format).
  - Single-step and multi-level Undo support via `Can I undo`.
- **Mathematical Curvature Verification**:
  - Non-collinear test points: $(0, 0, 0)$, $(20, 0, 25)$, $(40, 0, 0)$.
  - Midpoint chord deviation verified non-zero: peak $Z = 25.0$, intermediate samples $Z \approx 18.7$ and $Z \approx 18.7$.
  - Tangent vector angle changes continuously across parameter $t \in [0, 1]$.
- **Status**: **Formally Accepted by User** ("the spline is perfect merge when ready"). Merged into `main` at commit `8d9fb47` / `4844d59`.

---

### 16.2 Checkpoint B — Fix Michigan Deletion
- **Problem**: The protected Michigan starting object could not be deleted using hidden commands because the parser expected the object to be actively selected by the user.
- **Implementation**:
  - Commands recognized: `Can I remove starting object`, `Can I delete michigan`, `remove starting object`, `delete michigan`, `remove michigan`, `delete starting object`.
  - Directly locates the Michigan starting object by internal identifier (`userData.id === "starting_michigan"` or `isStartingObject` or `michiganModel`).
  - **No prior user selection is permitted or required**. If an unrelated object is currently selected, it remains selected and completely unaffected.
  - Presents exact confirmation dialog text:
    - Title: `"Are you sure you want to remove this?"`
    - Body: `"Are you sure you want to remove this?"`
  - On user confirmation (`#btn-confirm-ok.click()`):
    - Removes the Michigan group (both Upper and Lower Peninsulas simultaneously) from `scene` and `sceneObjects`.
    - Updates all 4 viewports (`renderAllViewports()`).
    - Updates the FeatureManager tree (`updateObjectsTree()`) and Properties panel.
    - Preserves single Undo state (`Can I undo` restores Michigan with `protected = true` status).
    - Unrelated objects remain in the scene and retain their active selection.
    - Ordinary deletion via Delete key or `Can I delete` remains strictly restricted.
- **Verification Screenshots**:
  - `cp_b_01_confirm_remove_dialog.png`: Confirmation dialog showing exact title and body while unrelated box is selected.
  - `cp_b_02_michigan_deleted_unrelated_intact.png`: Both peninsulas removed from all 4 viewports, unrelated box intact and selected.
  - `cp_b_03_michigan_restored_undo.png`: Full restoration of Michigan starting object via `Can I undo`.

---

### 16.3 Checkpoint C — Polygon Command
- **Requirement**: Add `Can I polygon [sides]` to create regular planar polygons.
- **Implementation**:
  - Workflow:
    1. Activate Polygon: `Can I polygon` (or `Can I polygon 5` or click `#tool-polygon`).
    2. Prompt for number of sides (minimum integer 3; defaults to 5).
    3. Click center point in active C-Plane (or type coordinates `X, Y, Z`).
    4. Move pointer to preview live rubberband regular polygon with center marker dot and dashed radius guide line.
    5. Click radius point or type exact radius value into Command Bar and press Enter.
    6. Commits exactly one closed profile object (`ClosedProfile`) with attached `THREE.Shape`.
    7. Automatically exits the command upon commit.
  - Regular $N$-gon geometry:
    - 3 sides $\rightarrow$ Equilateral Triangle.
    - 4 sides $\rightarrow$ Square.
    - 5 sides $\rightarrow$ Regular Pentagon.
    - 6 sides $\rightarrow$ Regular Hexagon.
  - 3D Extrusion:
    - Setting `userData.type = "ClosedProfile"`, `userData.closed = true`, and attaching a valid `THREE.Shape` allows the profile to be directly extruded into a 3D solid via `extrudeSelectedProfile(depth)`.
    - Produces a manifold 3D `ExtrudedSolid` with shaded faces and highlighted silhouette edges.
  - Single-step Undo cleanly removes the polygon entity.
  - Tested and verified at both standard resolution (DPR 1.0) and Retina display (DPR 2.0).
- **Verification Screenshots**:
  - `cp_c_01_pentagon_rubberband_preview.png`: Live green regular pentagon preview with center anchor dot and radius guide.
  - `cp_c_02_pentagon_profile_committed.png`: Committed 5-sided closed profile in scene and FeatureManager.
  - `cp_c_03_pentagon_extruded_solid.png`: 3D regular pentagonal prism solid across all 4 viewports.
  - `cp_c_04_triangle_and_hexagon.png`: Equilateral triangle (3 sides), pentagonal solid (5 sides), and hexagon (6 sides) side-by-side.
  - `cp_c_05_retina_dpr2_polygons.png`: Crisp anti-aliased geometry rendering at Retina DPR 2.0.

---

### 16.4 Checkpoint D — Numeric Easter Eggs
- **Requirement**: When the user explicitly enters `67`, `69`, or `420` as a numeric command value, display a small retro Windows 95-style popup containing exactly `"nice."`.
- **Implementation**:
  - Exact match regex: `/^(67|69|420)(\.0+)?$/`.
  - Substrings like `167`, `4200`, or `690` are strictly rejected.
  - Modal: `<dialog id="modal-nice-easter-egg" class="win95-dialog">`:
    - Title bar: `"Notice"` with close button `✕`.
    - Body text: Exactly `"nice."` in MS Sans Serif font.
    - Action button: `"OK"` to dismiss.
  - Modeling Operation Preservation:
    - The easter egg does **not** cancel, corrupt, or alter the modeling operation.
    - Example: `Can I box 69` creates `Box_6` with length 69 mm and displays the popup.
  - Event Handling:
    - Listens on command token evaluation, Command Bar parameter commit, and document-level input `change` events.
    - Avoids firing repeatedly on every keystroke (`keydown` without Enter is ignored).
- **Verification Screenshots**:
  - `cp_d_01_nice_popup_69.png`: Exact "nice." Windows 95 popup triggered by `Can I box 69`, with `Box_6` created in background.
  - `cp_d_02_nice_popup_420.png`: Exact "nice." popup triggered by `Can I cylinder 420`, with `Cylinder_7` created in background.

---

### 16.5 Checkpoint E — Rhino-Style Lock
- **Requirement**: Implement `Can I lock` and `Can I unlock` with Rhino-style lock semantics.
- **Implementation**:
  - `Can I lock`:
    - Requires one or more objects to be selected.
    - Sets `obj.userData.locked = true`.
    - Clears active selection and hides Gumball transform gizmos.
    - Locked objects remain 100% visible with their normal shading and wireframes.
    - Direct selection in viewports via raycasting is refused: locked objects are filtered out from raycast candidate lists.
    - Selection in FeatureManager displays advisory: `"'ObjectName' is locked. Click the 🔒 lock icon to unlock."`
    - Protection: Blocked from Move, Rotate, Scale, Gumball, and Deletion (`handleDelete` rejects locked items).
    - FeatureManager renders a yellow 🔒 lock badge (`.obj-lock-badge`) next to locked objects.
  - `Can I unlock`:
    - Unlocks all previously locked objects in the workspace (`obj.userData.locked = false`).
    - Alternatively, clicking the 🔒 lock badge directly in the FeatureManager unlocks that specific object.
    - Single-step Undo records lock and unlock transitions.
  - Save/Reopen Persistence:
    - `serializeProjectState()` preserves `userData.locked = true`.
    - `deserializeProjectState()` restores locked status upon reopening `.cadnt` project files.
  - Strict Decoupling from Michigan:
    - Ordinary lock uses `obj.userData.locked`.
    - Michigan uses `obj.userData.protected` and `obj.userData.isStartingObject`.
    - `Can I unlock` only affects `userData.locked` and never unlocks or exposes Michigan to ordinary deletion.
- **Verification Screenshots**:
  - `cp_e_01_locked_object_feature_manager.png`: Locked box in FeatureManager with 🔒 lock badge; selection cleared.
  - `cp_e_02_selection_and_deletion_blocked.png`: Status bar confirms deletion and transforms are blocked.
  - `cp_e_03_unlocked_via_feature_manager.png`: Object unlocked by clicking 🔒 badge in FeatureManager.

---

### 16.6 Checkpoint F — Slowly Escaping Spheres
- **Requirement**: Intentional slow movement for eligible sphere objects as a piece of CADN'T satire.
- **Rules & Technical Implementation**:
  - Eligibility: Must be an independent sphere primitive (`userData.type === "Sphere"`), unlocked (`!userData.locked`), and not protected (`!userData.protected`).
  - Speed: Approximately $0.05\text{ model units per second}$ ($0.05\text{ mm/sec}$).
  - Rolling Rotation: Calculates angular velocity $\omega = v / R$ and applies rolling rotation around the horizontal normal axis $\vec{u}_{\text{roll}} = (\text{dir}_z, 0, -\text{dir}_x)$ via `obj.rotateOnWorldAxis()`.
  - Frame-Rate Independence: Powered by `updateEscapingSpheres(dt)` inside the `render()` loop using `performance.now()` delta time ($\Delta t$). Clamped to prevent jumps if the tab goes to background.
  - Mesh Topology Untouched: Only updates `obj.position` and `obj.rotation`. Mesh vertices and topology remain 100% untouched.
  - Zero Undo Spam: Does not create an Undo history entry on animation frames. Current position is saved normally when the project is saved.
  - Transform Pause: If the user is actively dragging the sphere via Gumball or running an active transform command, escaping movement pauses so the user does not fight the motion.
  - Stopping Conditions:
    - Locking the sphere (`Can I lock`) immediately stops movement ($0.00\text{ mm/sec}$).
    - Joining or Boolean-unioning the sphere converts its type to `BooleanMesh`, permanently disqualifying it.
    - Unlocking an independent sphere immediately resumes its escape trajectory.
  - Non-spherical objects (boxes, cylinders, polygons, splines) never move.
- **Verification Screenshots**:
  - `cp_f_01_sphere_start_pos.png`: Sphere primitive initialized at $(0, 8, 0)$.
  - `cp_f_02_sphere_moved_and_rolled.png`: Sphere smoothly displaced by $0.20\text{ mm}$ over $4.0\text{ seconds}$ with rolling rotation.
  - `cp_f_03_locked_sphere_stopped.png`: Sphere locked via `Can I lock`, completely halting escape movement.

---

### 16.7 Geometric Kernel Architecture Summary
CADN'T runs on a **hybrid client-side geometric engine** with 4 distinct layers:
1. **CSG BSP Engine (`three-csg-ts`)**: Volumetric boolean union and difference operations using Binary Space Partitioning trees.
2. **Analytical 2-Manifold B-Rep Engine (`buildBoxManifoldCut`, `createPipeSolid`)**: In-house exact boundary representation generator that guarantees watertight 2-manifold closed meshes ($\chi = V - E + F = 2$, 0 open edges, 0 non-manifold edges) for Chamfers, Fillets, and Pipe solids.
3. **2D Sketch & Extrusion Engine**: Three.js `THREE.Shape`, `THREE.Path`, and `THREE.CatmullRomCurve3` with embedded Mapbox Earcut triangulation and `THREE.ExtrudeGeometry` for closed planar sketch extrusion.
4. **CAD Feature Edge Engine**: Dynamic dihedral crease extraction via `THREE.EdgesGeometry` ($24^\circ - 30^\circ$ cutoff) rendering crisp CAD feature lines over shaded models.

---

### 16.8 Verification & Test Runner Guide

#### 1. Running Automated Test Suite (156 Tests)
```bash
cd /Users/andybuck/.gemini/antigravity/single-file-html-app
python3 scripts/get_test_results.py
```
*Expected Result:*
`SAVED test_run_output.json with total: 156 failures: 0`

#### 2. Running Full Interactive Verification & Screenshot Generation
```bash
python3 scripts/verify_checkpoints_b_f.py
```
*Captures all 16 verification screenshots directly into `/Users/andybuck/Desktop/CADNT_Screenshots/`.*

#### 3. Manual Interactive Verification in Browser
1. Open [`index.html`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html) in Chrome or Safari.
2. Type `Can I spline` $\rightarrow$ Click 3+ points on C-Plane $\rightarrow$ Press Enter $\rightarrow$ Spline curve commits.
3. Type `Can I delete michigan` $\rightarrow$ Confirm dialog appears $\rightarrow$ Click `Yes, Proceed` $\rightarrow$ Michigan is deleted.
4. Type `Can I polygon 5` $\rightarrow$ Click center $\rightarrow$ Move cursor to radius $\rightarrow$ Click to commit $\rightarrow$ Extrude with `Can I extrude 20`.
5. Type `Can I box 69` $\rightarrow$ Retro Windows 95 dialog pops up with exact text `"nice."` $\rightarrow$ Dismiss via OK $\rightarrow$ Box is created.
6. Select any object $\rightarrow$ Type `Can I lock` $\rightarrow$ Object shows 🔒 lock badge in FeatureManager $\rightarrow$ Selection and deletion are refused $\rightarrow$ Click 🔒 badge to unlock.
7. Type `Can I sphere` $\rightarrow$ Watch sphere slowly roll across ground plane $\rightarrow$ Type `Can I lock` to freeze it.

---

### 16.9 Current Git State & How to Pick Up

- **Current Git Branch:** `dev`
- **Current Head Commit:** [`5f6d7e7`](file:///Users/andybuck/.gemini/antigravity/single-file-html-app)
- **Status of Checkpoint A:** Merged into `main` (commit `4844d59`).
- **Status of Checkpoints B–F:** Committed to `dev` branch.
- **Action Required to Deploy:**
  When ready to promote Checkpoints B through F to production / GitHub Pages:
  ```bash
  cd /Users/andybuck/.gemini/antigravity/single-file-html-app
  git checkout main
  git merge dev
  git push origin main
  git checkout dev
  ```





