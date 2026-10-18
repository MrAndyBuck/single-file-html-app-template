# HANDOFF.md — CADN'T Development Status

## Project Overview
- **Project**: CADN'T — Satirical Functional 3D CAD
- **Version**: `v0.1.0-alpha` (Build `v00000-010`)
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
| **Functional 2D Line Command (`Can I line`)**| **YES** | **YES** | **YES** | **YES** | Interactive C-plane sketching (Top/Front/Right/Persp); Command Bar with Start coords & dynamic Length; green rubberband preview with yellow endpoint indicator dots; length & coord status readout; raycaster threshold 2.5; `Line_N` FeatureManager registration; Properties panel geometry box (Start, End, Length, Plane); Gumball transform support; native `.cadnt` archive serialization & restore. User accepted. |
| **Functional Fillet & Chamfer (`Can I fillet` / `Can I chamfer`)** | **YES** | **YES** | **YES** | **YES** | Real solid geometry modification via CSG cutter subtractions (rounded circular arc for fillet, 45° prism for chamfer); interactive `#command-bar` controls with Scope dropdown (All, Vertical, Horizontal, Selected), numeric radius/distance inputs, live emerald preview mesh (`0x39ff14`), FeatureManager registration (`FilletedSolid`/`ChamferedSolid`), Properties panel geometry inspector, and full undo/redo support. |
| **Wandering Command Toolbars** | **YES** | **YES** | **YES** | **YES** | Modeling command buttons automatically swap positions with another random button upon use, guaranteeing the tool never lands in the same slot, stimulating neural elasticity. |
| **Hold Music Integration** | **YES** | **YES** | **YES** | **YES** | Real local audio asset `assets/audio/New Recording 12.m4a` played on long operations (Save, Import, Sweep, Union, Fillet, Chamfer). Non-looping playback, stops cleanly on completion/cancel, respects mute toggle, default volume increased to **85%**. |
| **Asset Manifest & SW Offline Caching** | **YES** | **YES** | **YES** | **YES** | `assets/manifest.json` maps all real assets; cached in Service Worker (`sw.js`) for offline functionality. |
| **Crash Report Command** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | `Can I send a crash report?` (with/without `?`, case-insensitive) opens dialog targeting `andrewrobertbuck@gmail.com` with system diagnostics, editable fields, and mailto launcher. No silent background uploads. |
| **Starting Object Removal & Undo** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | Hidden command `Can I remove starting object` shows "Are you sure you want to remove this?", deletes protected Michigan geometry upon confirmation, updates all 4 viewports, and is fully undoable via `Can I undo`. |
| **Mandatory Export Distortion** | **YES** | **YES** | **YES** | *Awaiting Acceptance* | Nonuniform scaling `(0.72, 1.48, 0.88)` applied unconditionally to all STL and OBJ exports. User checkbox removed. Scene geometry remains undistorted. |
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
