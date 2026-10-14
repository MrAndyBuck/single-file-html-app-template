# HANDOFF.md — CADN'T Development Status

## Project Overview
- **Project**: CADN'T — Satirical Functional 3D CAD
- **Version**: `v0.1.0-alpha` (Build `v00000-001`)
- **Repository**: [MrAndyBuck/single-file-html-app-template](https://github.com/MrAndyBuck/single-file-html-app-template)
- **Live URL**: [https://mrandybuck.github.io/single-file-html-app-template/](https://mrandybuck.github.io/single-file-html-app-template/)
- **Local Directory**: `/Users/andybuck/.gemini/antigravity/single-file-html-app`

---

## Environment & Tooling
- **OS**: macOS (Darwin arm64)
- **Python**: Python 3.9.6 (local preview: `python3 -m http.server 8000`)
- **Git**: 2.39.5
- **Engine**: Three.js r128 vendored locally in `/vendor/three.min.js`
- **Headless Chrome**: Verified via SwiftShader WebGL rendering and automated test suite

---

## Phased Implementation Status

| Phase | Description | Status | Verification |
|---|---|---|---|
| **Phase 1** | Functional Skeleton | **Complete** (Awaiting Review) | 19/19 automated tests passing. 4 viewports, Michigan model, Request Bar, keyboard nav, primitives, wandering toolbar. |
| **Phase 2** | Real Modeling | Ready to Begin | 2D Sketches (Line/Rect/Circle), Profile Extrude, Transforms, CSG Booleans (Union/Diff), Layers. |
| **Phase 3** | Data & I/O | Pending | Native `.cadnt` save/reopen, OBJ/STL import/export, Undo/Redo stack. |
| **Phase 4** | Satire & Friction | Pending | 10s artificial loading delays, ad popups, mini close buttons, gaslighting toasts. |
| **Phase 5** | Polish & Deploy | Pending | Themes, audio hooks, multi-browser validation. |

---

## Navigation Repair (Resolved)

### 1. Root Cause Analysis
- **Focus Trap & Canvas Unfocusability**: `<canvas>` element lacked `tabindex="0"`, making it non-focusable by standard DOM rules. When user clicked into the Request Bar `<input>`, subsequent clicks on the canvas did not trigger a `blur` event on the input. Consequently, `e.target.matches("input, textarea")` remained true and swallowed all WASD and arrow keypresses.
- **macOS Press-and-Hold Keystroke Suppression**: On macOS, holding letter keys (WASD) defaults to opening an accent picker, suppressing repeat `keydown` events. Single-tap discrete handlers moved only a negligible amount per physical tap.
- **Planar Viewport Orbit Refusal**: Top, Front, and Right orthographic viewports were completely locked against W/S/A/D, displaying an error toast instead of gracefully routing orbit to the 3D perspective camera.
- **Matrix Desynchronization in Pan**: `cam.matrix.extractBasis()` in `panActiveCamera()` was extracting stale local matrix data rather than up-to-date world basis vectors (`cam.matrixWorld.extractBasis()`).

### 2. Remediation Applied
- Added `tabindex="0"` to `#cad-canvas` and `tabindex="-1"` to `#stage-container`.
- Bound `pointerdown` listener on `#stage-container` and `#cad-canvas` that explicitly blurs `requestInput` and forces focus to the canvas with `{ preventScroll: true }`.
- Implemented continuous per-frame navigation loop (`updateContinuousNavigation()`) inside `render()` alongside immediate discrete keydown action, using a `pressedKeys` Set to handle macOS hold suppression smoothly at 60fps.
- Added `Escape` key handling inside the Request Bar input to instantly blur and return focus to the modeling canvas.
- Automatically redirects W/S/A/D orbit to the 3D Perspective camera when in orthographic views with an informative toast (*"Active view switched to Perspective for 3D orbit"*).
- Synced matrix world updates (`cam.updateMatrixWorld(true)`) and scaled pan distance for crisp, visible movement.
- Added real-time numeric readout in the bottom status bar displaying live camera Azimuth, Elevation, Distance, Pan coordinates, and Zoom factor.

### 3. Verification & Evidence
- **Automated Headless Chrome Test (`scratch/test_nav_vis.py`)**:
  - Before: `scratch/nav_before.png` (MD5: `b2ee05c42cfea16415f37d4a0684385f`)
  - After: `scratch/nav_after.png` (MD5: `d80bc0c8056dcb71ae469396e4a60dc3`)
  - Perspective camera Azimuth visibly rotated from 45° to 91° and Elevation tilted from 30° to 10°.
  - Status readout updated live: `PERSP | Az: 91° El: 10° | Dist: 95`.
- **Automated Unit Test Suite (`scratch/run_unit_tests.py`)**:
  - 19/19 tests passing.

### 4. Remaining Limitations
- Orthographic viewports (Top, Front, Right) intentionally do not orbit (standard CAD behavior; W/S/A/D redirects to Perspective).
- Active typing in Request Bar captures text input; clicking canvas or pressing `Escape` returns focus to navigation.

---

## Sketching & Extrusion Audit

| Capability | Classification | Current Implementation Details |
|---|---|---|
| **1. Draw 2D lines, circles, and rectangles** | **MISSING** | No 2D curve drawing tools or interactive click-drag vertex generators exist. Viewport clicks only perform camera focus / object raycasting selection. Toolbar "Spline" button emits a placeholder warning. |
| **2. Choose a sketch plane** | **MISSING** | Visual grids exist for Top (XZ), Front (XY), and Right (ZY), and clicking a viewport changes `activeViewport`. However, there is no interactive "sketch plane" concept, no C-Plane selector or alignment command, and no mechanism allowing users to define an active sketching plane on a 3D face or arbitrary coordinate plane. |
| **3. Create a closed profile** | **MISSING** | No data structure for 2D curve segments, no vertex snapping, no topology graph, and no algorithm or UI to detect or construct a closed profile (e.g. `THREE.Shape`). The only closed 2D shapes that exist in the codebase are the hardcoded Michigan boundary point arrays (`lpPoints` and `upPoints`) in lines 880-915 used to build the startup model. |
| **4. Profile recognition as extrudable** | **MISSING** | No profile validation logic, coplanarity check, self-intersection check, or closure detection in the codebase. When `Can I extrude` or the Extrude toolbar button is invoked, lines 1324-1326 and 1452-1454 simply emit a static warning: *"Extrude command accepted. Select a planar 2D curve (Phase 2 capability)."* No checks or geometry queries occur. |
| **5. Extrude generates new 3D geometry** | **MISSING** | For user interactions, `Extrude` produces no 3D geometry; it logs a placeholder notice. The only place `THREE.ExtrudeGeometry` is invoked is during initialization for the default Michigan starting model (Upper and Lower peninsulas). The user cannot run `extrude` on any user entity to generate new 3D geometry. |
| **6. Resulting object selectable, transformable, exported** | **PARTIAL** | **Selection: WORKING** (Raycasting selection (`selectObject`) and Shift-multiselect function reliably on meshes in the scene, highlighting them with yellow wireframes and listing them in Properties/Objects).<br>**Transformation: MISSING** (Move, Rotate, Scale have no viewport gizmos or properties panel edit fields).<br>**Export: MISSING** (No OBJ, STL, or file export routines exist yet; scheduled for Phase 3). |

---

## What Works in Phase 1
1. **Rhino-Inspired 4-Viewport Matrix**:
   - Single WebGL canvas with hardware scissor splitting into Perspective, Top, Front, and Right views.
   - Dynamic C-Plane grids, origin axes tripod, and clickable active viewport indicators.
2. **The Request Bar**:
   - Requires `Can I [command]` prefix (case-insensitive).
   - Any command entered without `Can I ` receives the curt response **"Nope."** with an animated shake effect.
   - History dropdown log records previous queries and system responses.
3. **The Michigan Starting Model**:
   - Genuine extruded 3D geometry of both the Upper and Lower Peninsulas with beveled edges.
   - Immune to standard `Delete` commands.
   - Successfully removable **only** via `Can I remove starting object` through a confirmation dialog.
4. **Navigation**:
   - Camera orbit: `W / S` (vertical), `A / D` (horizontal).
   - Camera pan: `Up / Down / Left / Right` arrows.
   - Camera zoom: `Shift + Up / Down` arrows.
   - Trackpad wheel scrolling strictly prevented for camera navigation (emits user advisory toast).
   - Left-click raycasting selects objects and highlights them with Rhino-yellow glowing wireframes.
5. **Primitive Geometry Creation**:
   - Real Three.js meshes created via Request Bar: `Can I box`, `Can I sphere`, `Can I cylinder`, `Can I cone`.
   - Also invokable via toolbar icons.
6. **Wandering Toolbars**:
   - Executing any toolbar command swaps button positions to promote "neural elasticity".
7. **Fictional Economy & Onboarding**:
   - $249.00 credit balance readout with an "UNDER CONSTRUCTION" refill modal.
   - First-launch handbook containing the exact phrase: *"The command to delete the starting object exists."*
8. **Automated Verification**:
   - 19/19 automated test suite passing in headless Chrome with SwiftShader WebGL (`?run_tests=1`).

---

## Instructions for Next Session (Phase 2 Entry)
- Awaiting user review and authorization before building Phase 2 features:
  1. Add 2D sketch tools (Lines, Rectangles, Circles) onto the active viewport C-Plane.
  2. Implement closed 2D profile extrusion into 3D meshes.
  3. Implement Move, Rotate, and Scale transforms with direct viewport gizmos and properties panel coordinates.
  4. Implement genuine CSG (Constructive Solid Geometry) for Boolean Union and Boolean Difference.
  5. Expand Layer & Object management capabilities.
