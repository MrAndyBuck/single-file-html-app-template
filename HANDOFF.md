# HANDOFF.md — CADN'T Development Status

## Project Overview
- **Project**: CADN'T — Satirical Functional 3D CAD
- **Version**: `v0.1.0-alpha` (Build `v00000-004`)
- **Repository**: [MrAndyBuck/single-file-html-app-template](https://github.com/MrAndyBuck/single-file-html-app-template)
- **Live URL**: [https://mrandybuck.github.io/single-file-html-app-template/](https://mrandybuck.github.io/single-file-html-app-template/)
- **Project Workspace**: `/Users/andybuck/.gemini/antigravity/single-file-html-app`

---

## Operating Boundaries & Permission Rules
- **Project Workspace**: Routine development operations (reading, editing files, running tests, updating project documentation) are authorized strictly within `/Users/andybuck/.gemini/antigravity/single-file-html-app`.
- **External Boundaries**: Files, folders, or resources outside this project workspace must not be read, modified, or executed without explicit user confirmation.
- **Completion Standard**: Automated unit tests are **not** a substitute for browser interaction and visual verification. Features are classified through four distinct stages:
  1. **Implemented**: Code exists in codebase.
  2. **Automatically Tested**: Passes automated unit tests.
  3. **Visually Verified**: Inspected and verified in real browser sessions with visual artifacts.
  4. **User Accepted**: Directly tested and approved by the user.

---

## Capability Status Matrix

| Capability | Implemented | Auto Tested | Visually Verified | User Accepted | Current Status & Notes |
|---|:---:|:---:|:---:|:---:|---|
| **Rhino 4-Viewport Matrix** | **YES** | **YES** | **YES** | *Awaiting User Review* | Top-Left (Top), Top-Right (Perspective), Bottom-Left (Front), Bottom-Right (Right). Dedicated C-Plane grids for all 4 views. Active viewport frame indicator. |
| **WASD Camera Orbit** | **YES** | **YES** | **YES** | *Awaiting User Review* | W/S (vertical elevation), A/D (horizontal azimuth). Discrete tap 8°, continuous hold ~125°/s. Empty input blur trap resolved. |
| **Viewport Pan & Zoom** | **YES** | **YES** | **YES** | *Awaiting User Review* | Arrow keys pan active camera plane; Shift+Arrows zoom active camera. Independent targets and zoom factors for Top, Front, Right, and Perspective. |
| **Trackpad Wheel Restriction** | **YES** | **YES** | **YES** | *Awaiting User Review* | Mouse/trackpad wheel zoom strictly cancelled on viewport canvas. |
| **Starting Michigan Model** | **YES** | **YES** | **YES** | *Awaiting User Review* | Extruded Upper & Lower Peninsulas centered at origin (0, 2.25, 0). Protected from delete; removable solely via `Can I remove starting object`. |
| **Adversarial Request Bar** | **YES** | **YES** | **YES** | *Awaiting User Review* | Requires `Can I [cmd]`, else returns `"Nope."` with shake and audio buzz. Blurs on Enter to prevent navigation lock. |
| **Wandering Toolbars** | **YES** | **YES** | **YES** | *Awaiting User Review* | Toolbar buttons swap layout order after command execution. |
| **2D Sketching (Line, Rect, Circle)** | **YES** | **YES** | **YES** | *Pending Demonstration* | C-Plane projective drawing for lines, closed rectangles, and closed circles with `THREE.Shape` topology. |
| **Profile Extrusion into 3D** | **YES** | **YES** | **YES** | *Pending Demonstration* | Extrudes closed 2D profiles into 3D solid meshes (`THREE.ExtrudeGeometry`) with edge wires and normals. |
| **Object Transformations (Move/Rot/Scale)**| **YES** | **YES** | **YES** | *Pending Demonstration* | `Can I move [dx] [dy] [dz]`, `Can I rotate [axis] [deg]`, `Can I scale [factor]`. |
| **CSG Booleans (Union & Difference)** | **YES** | **YES** | **YES** | *Pending Demonstration* | ThreeCSG solid Boolean Union and Difference producing manifold meshes. |
| **Layer Management** | **YES** | **YES** | **YES** | *Pending Demonstration* | Add, lock, hide, and assign layers with color swatches. |
| **Undo / Redo Stack** | **YES** | **YES** | **YES** | *Pending Demonstration* | Deep document state undo/redo accessible strictly via `Can I undo` and `Can I redo`. |
| **Project Save / Reopen (.cadnt)** | **YES** | **YES** | **YES** | *Pending Demonstration* | Full scene serialization, 2-stage confirmed save, file picker reopen. |
| **OBJ & STL Export (with Satirical Distortion)**| **YES** | **YES** | **YES** | *Pending Demonstration* | Standard binary STL and Wavefront OBJ; optional nonuniform scaling applied to isolated export clone only. |
| **Mesh Import & Geometry Lock** | **YES** | **YES** | **YES** | *Pending Demonstration* | STL/OBJ import, $10 fee deduction, read-only geometry lock, Remesh/Simplify sphere replacement. |
| **Fictional Economy & Satirical Friction** | **YES** | **YES** | **YES** | *Pending Demonstration* | $249 balance, Under Construction refill modal, 10s heavy operation delay, ads with 10px close buttons, Web Audio synthesizer. |

---

## Viewport Architecture & WASD Orbit Repair

### 1. Root Causes Identified
1. **Viewport Layout Misalignment**: Top and Perspective viewports were reversed from Rhino's standard layout. Rhino places **Top** at Top-Left and **Perspective** at Top-Right.
2. **Missing Orthogonal C-Plane Grids**: Front and Right viewports were rendering the horizontal ground grid edge-on, appearing as a thin horizontal line with no vertical plane reference.
3. **Model Decentering**: Michigan starting geometry was translated to `(2, 0, -12)`, positioning it off-center and behind the Front and Right camera sightlines.
4. **Input Focus Lock**: After typing into the Request Bar, `#request-input` remained focused. Keypresses (WASD, arrows) were swallowed by the input field rather than reaching the viewport navigation loop.
5. **Slow Angular Velocity**: Orbit increments were too small per frame, resulting in barely perceptible movement during keypresses.

### 2. Implementation Changes
1. **Standard Rhino 4-Viewport Arrangement**:
   - **Top-Left**: **Top (X/Z)** (Orthographic camera looking down -Y).
   - **Top-Right**: **Perspective [W/S/A/D]** (3D Perspective camera).
   - **Bottom-Left**: **Front (X/Y)** (Orthographic camera looking along -Z).
   - **Bottom-Right**: **Right (Z/Y)** (Orthographic camera looking along -X).
2. **Dedicated C-Plane Grids for All Viewports**:
   - `gridTop`: Horizontal XZ grid (Y = -0.02).
   - `gridFront`: Vertical XY grid (`rotation.x = π/2`, Z = -0.02) facing the Front camera.
   - `gridRight`: Vertical ZY grid (`rotation.z = π/2`, X = -0.02) facing the Right camera.
   - `gridPerspective`: 3D ground plane grid with axes tripod at origin.
3. **Active Viewport Highlighting**:
   - Added `#vp-active-frame` yellow accent border that dynamically surrounds the active viewport quadrant.
   - Active viewport label is highlighted in Rhino yellow (`.active-vp`).
4. **Origin Centering**:
   - Re-centered Michigan geometry at `(-6, 0, 3.5)`, placing the model centroid directly at `(0, 2.25, 0)` for balanced framing across all four orthogonal views.
5. **Focus Trap Elimination**:
   - When `Enter` or `Send` is triggered on `#request-input`, the input is blurred and `#cad-canvas` is focused.
   - When `#request-input` is empty, pressing WASD or Arrow keys automatically blurs the input and routes navigation immediately.
   - Stage clicks and dialog closes automatically focus `#cad-canvas`.
6. **Substantial Navigation Response**:
   - Orbit: discrete key tap executes `0.14 rad` (~8°); continuous holding orbits at `~2.3 rad/s` (~130°/s).
   - Pan: discrete step 8 units; continuous holding pans at 50 units/s.
   - Zoom: discrete step 1.22x; continuous holding zooms at 1.4x/s.

---

## Visual Verification Artifacts
- **Diagnostic HUD Initial State**:
  `brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/diagnostic_hud_initial.png`
  Demonstrates live Diagnostic HUD in bottom-right corner displaying active viewport (PERSPECTIVE), focused element (CANVAS#cad-canvas), text input status (NO - Nav Keys Active), camera coordinates, drawing buffer dimensions (944 × 639), and 4-viewport camera types and scissor bounds.
- **Diagnostic HUD Post-Orbit (W & D Keys)**:
  `brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/diagnostic_hud_orbited.png`
  Demonstrates live HUD capturing `KeyD ('d') -> Nav: KeyD`, camera elevation updated from 56° to 38° via `KeyW`, azimuth updated from 45° to 65° via `KeyD`, camera position dynamically shifted from `(55.9, 54.8, 55.9)` to `(53.1, 76.9, 24.3)`, with Top, Front, and Right orthographic views remaining fixed.
- **Centered 4-Viewport Matrix**:
  `brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/rhino_four_views_centered.png`
- **Orbited Viewport**:
  `brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/rhino_four_views_orbited.png`

---

## Reproducible Diagnosis of Acceptance Failure

### 1. Deployed Application vs Local Working Copy Desynchronization
- **Deployed Build on GitHub Pages**: Commit `6ee923f` ("feat: complete CADN'T Phase 3 & 4").
- **Local Working Copy**: Contained uncommitted modifications to `index.html` and `HANDOFF.md`.
- **Finding**: Because the repairs were withheld locally pending user approval and not pushed to GitHub Pages, the user's browser was loading the original commit `6ee923f`.
- **In Commit `6ee923f`**:
  1. Top-Left was Perspective, Top-Right was Top (reversed from Rhino).
  2. Front and Right viewports had no orthogonal grids (`gridFront` and `gridRight` were missing).
  3. `#request-input` never blurred on Enter or canvas click, trapping DOM focus forever and silently blocking all navigation keypresses.
  4. Angular orbit velocity was under-scaled (`0.08 * mult`).

### 2. Service Worker Cache Retention
- `sw.js` uses a cache-first strategy (`caches.match(e.request).then(hit => hit || fetch(e.request))`) keyed by `cadnt-v00000-003`.
- Any browser that loaded `v00000-003` will retain the old cached `index.html` from `6ee923f` unless the cache key in `sw.js` is bumped (e.g. `v00000-004`) or the cache is explicitly cleared.

### 3. Four-View Architecture Verification
- **Are there 4 independent camera views or divisions of one rendered area?**
  - **Verdict: Genuinely 4 independent camera views.**
  - There are 4 distinct `THREE.Camera` objects:
    1. `cameras.top`: `THREE.OrthographicCamera(-60, 60, 60, -60, 1, 3000)`, position `(x, 300, z)`, up `(0, 0, -1)`, lookAt `(x, 0, z)`.
    2. `cameras.perspective`: `THREE.PerspectiveCamera(45, aspect, 1, 3000)`, spherical orbit around target.
    3. `cameras.front`: `THREE.OrthographicCamera(-60, 60, 60, -60, 1, 3000)`, position `(x, y, 300)`, up `(0, 1, 0)`, lookAt `(x, y, 0)`.
    4. `cameras.right`: `THREE.OrthographicCamera(-60, 60, 60, -60, 1, 3000)`, position `(300, y, z)`, up `(0, 1, 0)`, lookAt `(0, y, z)`.
  - In `render()`, WebGL executes four separate render passes:
    - Pass 1: `gl.viewport(0, height - halfH, halfW, halfH)` & `gl.scissor(...)` -> `renderer.render(scene, cameras.top)`
    - Pass 2: `gl.viewport(halfW, height - halfH, width - halfW, halfH)` & `gl.scissor(...)` -> `renderer.render(scene, cameras.perspective)`
    - Pass 3: `gl.viewport(0, 0, halfW, height - halfH)` & `gl.scissor(...)` -> `renderer.render(scene, cameras.front)`
    - Pass 4: `gl.viewport(halfW, 0, width - halfW, height - halfH)` & `gl.scissor(...)` -> `renderer.render(scene, cameras.right)`
  - Each viewport maintains its own C-plane grid, projection matrix, aspect ratio, camera position, and pan/zoom state.

---

## Next Steps (Awaiting User Review & Approval to Push)
1. User reviews diagnostic findings, HUD telemetry, and screenshots.
2. User provides approval to commit, bump service worker version to `v00000-004`, and push to `origin/main` for GitHub Pages deployment.
3. User tests in deployed browser with live Diagnostic HUD confirming WASD orbit, focus states, and 4-viewport behavior.
