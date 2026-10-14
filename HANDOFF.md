# HANDOFF.md — CADN'T Development Status

## Project Overview
- **Project**: CADN'T — Satirical Functional 3D CAD
- **Version**: `v0.1.0-alpha` (Build `v00000-005`)
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

## Viewport Architecture & WASD Orbit Repair (v00000-004 Acceptance Failure Diagnosis)

### 1. Root Cause: Retina High-DPI Double-Scaling Bug in WebGL Viewport
- **User Acceptance Failure**: In Safari Private Window on macOS (Retina display, `devicePixelRatio = 2.0`), the canvas had focus and the HUD was active, but:
  1. WASD orbit produced zero visible camera movement.
  2. The four-view layout visually displayed the Michigan model as a single horizontal extrusion across the center.
- **Investigation Finding**:
  - In `vendor/three.min.js`, `renderer.setViewport(x, y, w, h)` and `renderer.setScissor(x, y, w, h)` are wrappers around WebGL that internally multiply coordinates by `_pixelRatio` (`T.copy(N).multiplyScalar(P).floor()`).
  - `render()` in `index.html` was passing physical canvas buffer dimensions (`canvas.width`, `canvas.height`) instead of CSS logical dimensions (`stageContainer.clientWidth`, `stageContainer.clientHeight`).
  - On standard DPR 1.0 displays, `canvas.width == stageContainer.clientWidth`, masking the bug.
  - On macOS Retina displays (`DPR = 2.0`):
    - `canvas.width` is already $2\times$ CSS width (e.g. $944 \times 2 = 1888$).
    - Passing `(halfW, height - halfH, ...)` caused Three.js to scale by $2\times$ a second time ($2 \times 2 = 4\times$).
    - **Bottom-Left (Front Viewport)**: Scaled to `(0, 0, 1888, 1278)`, blowing up across 100% of the physical canvas! In Front view, the extruded Michigan model is viewed edge-on parallel to the plane, causing it to display as a flat horizontal extrusion band across the center of the entire screen.
    - **Top-Right (Perspective Viewport)**: Scaled to $X = 1888$, placing the viewport completely outside the canvas drawing buffer! WASD orbit updated the camera orientation in JavaScript, but rendered off-screen into void space, producing zero visible motion on screen.
    - **Top and Right Viewports**: Similarly scissored off-screen above and to the right.

### 2. The Minimal Repair
1. **Pass CSS Logical Dimensions in `render()`**:
   ```javascript
   const width = stageContainer.clientWidth || 800;
   const height = stageContainer.clientHeight || 600;
   const halfW = Math.floor(width / 2);
   const halfH = Math.floor(height / 2);
   ```
   Three.js now scales `halfW` ($472$) by $2.0 \to 944$, exactly placing the four quadrants in the physical $1888 \times 1278$ buffer.
2. **Explicit Depth Clear Between Passes**:
   Added `renderer.clearDepth();` before each of the four quadrant render calls to ensure complete depth buffer isolation.
3. **Safari Event Capture & Telemetry**:
   - Automated `safaridriver` requires manual administrator authorization and "Allow Remote Automation" in Safari Preferences; headless Chrome with `--force-device-scale-factor=2` was used to reproduce Retina DPR behavior.
   - Added `defaultPrevented`, `Last Orbit Δ`, and `CSS vs Buffer sizing (DPR)` to the diagnostic HUD.

### 3. Diagnostic Test Mode (Independent 4-View Primitives)
- Centered at `(0, 2.25, 0)` on dedicated Three.js layers:
  - **Top Viewport (Layer 1)**: Bright Yellow Box (`THREE.BoxGeometry(14, 14, 14)`)
  - **Perspective Viewport (Layer 2)**: Bright Cyan Sphere (`THREE.SphereGeometry(9, 24, 24)`)
  - **Front Viewport (Layer 3)**: Bright Magenta Cone (`THREE.ConeGeometry(9, 18, 24)`)
  - **Right Viewport (Layer 4)**: Bright Lime Green Cylinder (`THREE.CylinderGeometry(7, 7, 18, 24)`)
  - **Layer 0 (Shared)**: Extruded 3D Michigan starting geometry and coordinate axes visible across all 4 views.
- Toggled via `[Toggle 4-View Test Primitives [ON/OFF]]` button in HUD or URL `?test_viewports=1`.
- Non-destructive: does NOT replace or delete the Michigan starting model.

---

## Visual Verification Artifacts (Retina DPR 2.0)
- **Repaired 4-View Layout (Michigan Model)**:
  `brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/dpr2_repaired_michigan_4views.png`
  Demonstrates Top (top-left plan view), Perspective (top-right 3D isometric), Front (bottom-left edge view), and Right (bottom-right side view) correctly framed under DPR 2.0.
- **Diagnostic Test Mode (Unobscured 4-View Primitives)**:
  `brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/dpr2_diagnostic_primitives_unobscured.png`
  Demonstrates all 4 independent viewports rendering their unique colored test primitives (Yellow Box, Cyan Sphere, Magenta Cone, Lime Cylinder) centered on the shared Michigan model.
- **Post-WASD Orbit (Perspective Rotated)**:
  `brain/706b2fcb-0d73-41fc-9916-c493cfe958dc/dpr2_orbited_primitives.png`
  Demonstrates live HUD capturing `KeyD ('d') -> Nav: KeyD`, camera azimuth shifted from 45° to 65°, elevation shifted from 56° to 37°, and the Cyan Sphere and Michigan model visibly orbited in the top-right viewport while the 3 orthographic viewports remain static.

---

## Next Steps (Awaiting User Review & Approval to Push)
1. User reviews diagnostic findings, Retina DPR explanation, and visual verification artifacts.
2. User provides approval to bump application and service worker versions to `v00000-005`, commit, and push to `origin/main` for GitHub Pages deployment.
3. User tests deployed build on macOS Safari in Private Window.
