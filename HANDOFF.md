# HANDOFF.md — CADN'T Development Status

## Project Overview
- **Project**: CADN'T — Satirical Functional 3D CAD
- **Version**: `v0.1.0-alpha` (Build `v00000-003`)
- **Repository**: [MrAndyBuck/single-file-html-app-template](https://github.com/MrAndyBuck/single-file-html-app-template)
- **Live URL**: [https://mrandybuck.github.io/single-file-html-app-template/](https://mrandybuck.github.io/single-file-html-app-template/)
- **Local Directory**: `/Users/andybuck/.gemini/antigravity/single-file-html-app`

---

## Environment & Tooling
- **OS**: macOS (Darwin arm64)
- **Runtime**: HTML5, Canvas 2D/WebGL, Web Audio API, Service Worker Cache
- **Dependencies (Vendored Locally in `/vendor/`)**:
  - `vendor/three.min.js`: Three.js r128 3D rendering core
  - `vendor/three-csg.js`: ThreeCSG Constructive Solid Geometry engine (Union & Difference)
  - `vendor/three-exporters.js`: Three.js OBJExporter & STLExporter (Wavefront OBJ & Binary STL)
  - `vendor/three-loaders.js`: Three.js STLLoader & OBJLoader
- **Testing Engine**: Python headless Chrome with SwiftShader WebGL & Chrome DevTools Protocol (`scratch/run_unit_tests.py`, `scratch/capture_phase4_screenshots.py`)

---

## Phased Implementation Status

| Phase | Description | Status | Verification |
|---|---|---|---|
| **Phase 1** | Functional Skeleton | **Complete** | 4-viewport scissor rendering, starting Michigan model, Request Bar (`Can I [cmd]`), keyboard-only navigation (WASD/arrows, wheel blocked), primitive creation, wandering toolbars. |
| **Phase 2** | Real Modeling | **Complete** | 2D sketch entities (Line, Rect, Circle on C-Planes), closed profile extrusion into 3D solids, 3D transformations (`Can I move/rotate/scale`), CSG Booleans (Union & Difference), full Layer management (Add, Lock, Hide, Color). |
| **Phase 3** | Data & I/O | **Complete** | Native `.cadnt` project serialization/deserialization, two-stage confirmed Save & Open, Wavefront OBJ & Binary STL export with optional satirical nonuniform scaling, STL/OBJ import with $10 fee & geometry lock, Remesh/Simplify sphere replacement, Request Bar Undo/Redo stack. |
| **Phase 4** | Satire & Friction | **Complete** | 10-second artificial loading delay on heavy operations with animated progress and gaslighting status texts, ad popups with 10px close buttons, $249 starting credit economy with "+ Buy More" Under Construction modal, Web Audio synthesizer (nope buzz, drone hum) with mute toggle, Dark & Light themes with WebGL clearColor sync, `?debug` mode bypass. |
| **Phase 5** | Verification & Deployment | **Complete** | 45/45 automated unit tests passing, visual verification snapshots captured, Service Worker cache bumped to `v00000-003`, git staged and committed. |

---

## Architecture & Systems

### 1. Rhino-Inspired 4-Viewport Matrix
- A single WebGL `<canvas>` split into 4 viewports using hardware scissor testing:
  1. **Top-Left**: 3D Perspective (Orbit with `W/S/A/D`, Pan with `Arrows`, Zoom with `Shift+Arrows`)
  2. **Top-Right**: Top Orthographic (XZ Plane)
  3. **Bottom-Left**: Front Orthographic (XY Plane)
  4. **Bottom-Right**: Right Orthographic (ZY Plane)
- Dynamic C-Plane grids, coordinate tripod, active viewport tracking, and raycast left-click object selection.
- Trackpad wheel gestures are strictly prevented on the viewport canvas to prevent accidental zoom/pan drift.

### 2. The Request Bar
- Replaces the traditional command line with an adversarial conversational bar.
- All typed commands **must** begin with `Can I [command]` (e.g. `Can I box`, `Can I undo`, `Can I remove starting object`).
- Commands lacking polite deference receive a curt **"Nope."** response accompanied by a 120Hz sawtooth audio buzz and an animated CSS shake.
- Command matching is case-insensitive.
- Command history dropdown displays recent requests and system log responses.

### 3. The Michigan Starting Model
- On first launch, displays genuine 3D extruded geometry of the State of Michigan, featuring both the Upper and Lower Peninsulas with beveled boundaries.
- Protected against ordinary `Delete` keys and commands.
- Removable strictly via the secret command `Can I remove starting object` followed by an *"Are you sure you want to remove this?"* confirmation modal.

### 4. 2D Sketching & 3D Extrusion
- **Lines**: `createLineSketch(points, plane)` creates genuine 3D curve paths.
- **Rectangles**: `createRectSketch(corner1, corner2, plane)` constructs closed coplanar profiles containing `THREE.Shape` topology.
- **Circles**: `createCircleSketch(center, radius, plane)` generates closed circular boundary curves with parametric shapes.
- **Extrude**: `extrudeSelectedProfile(depth)` extrudes selected closed 2D profiles into real 3D solid meshes using `THREE.ExtrudeGeometry` with automatic normal computation and edge outlines.

### 5. Object Transformations & CSG Booleans
- **Move**: `Can I move [dx] [dy] [dz]` translates object position coordinates in 3D world space.
- **Rotate**: `Can I rotate [axis] [degrees]` rotates geometry around X, Y, or Z axes.
- **Scale**: `Can I scale [factor]` resizes object geometry uniformly.
- **Constructive Solid Geometry (CSG)**:
  - `Can I union`: Computes a genuine Boolean Union between two selected solids using ThreeCSG, generating a unified manifold mesh with merged topology.
  - `Can I difference`: Computes a genuine Boolean Difference, subtracting the secondary object from the primary object to form hollows or cutouts.

### 6. Document Serialization & Undo/Redo Engine
- **Native `.cadnt` Format**: Complete JSON archive of project metadata, credit balance, layer hierarchy, and full object geometry (types, vertices, normals, indices, transforms, materials).
- **Two-Stage Save**: Saving requires completing Stage 1 and Stage 2 confirmations, followed by a simulated 10-second export pipeline (bypassed in debug mode).
- **Reopen / Deserialization**: Restores scene meshes, wireframe edge helpers, and layer assignments from `.cadnt` archives or localStorage autosave.
- **Request Bar Undo/Redo**: Deep state capture stack accessible exclusively via `Can I undo` and `Can I redo` (strictly forbidden from toolbar buttons).

### 7. Export Engine & Nonuniform Scaling Satire
- Exports genuine Wavefront OBJ (`.obj`) and Standard Triangle Language binary STL (`.stl`) files.
- Export scope selectable: All Solids vs Selected Objects Only.
- **Intentional Nonuniform Scaling**: Checkbox option applies anisotropic deformation (X * 1.35, Y * 0.72, Z * 1.18) exclusively to an isolated export clone group, keeping internal project geometry 100% unaltered.

### 8. Import Engine & Geometry Lock
- Imports external `.stl` and `.obj` geometry via `STLLoader` and `OBJLoader`.
- Deducts a flat **$10.00** fee from the user's fictional credit balance.
- Marks imported meshes as `userData.isImported = true`.
- Enforces an adversarial geometry lock: imported meshes cannot undergo Booleans or Extrusions (*"Imported meshes are read-only geometries"*).
- **Remesh & Simplify**: Both commands intentionally replace the target imported mesh with a sphere primitive (*"the optimal topological manifold"*).

### 9. Fictional Economy & Friction Mechanics
- **Credits**: Users begin with $249.00 in fictional CAD tokens.
- **Token Fees**: Import costs $10.00; Fillet & Chamfer commands are billed at $49.00 per execution.
- **Buy More**: Opens an *"UNDER CONSTRUCTION"* modal requesting certified money orders to the Friction Division.
- **Artificial Delay**: Heavy operations (Union, Difference, Save, Import) enforce a 10-second loading dialog with an animated progress bar and rotating gaslighting status text (bypassed in `?debug` mode).
- **Wandering Toolbars**: Executing any toolbar command shuffles icon positions across the toolbar.
- **Satirical Ads**: Intermittent ad modal featuring a microscopic 10px close button and a blank placeholder.
- **Web Audio**: Synthesizer produces error buzzes and loading drone hums with a toggleable mute control.
- **Theme Engine**: Toggle between Rhino Dark theme and Light theme, synchronizing UI stylesheets and WebGL background clear colors.

---

## Verification & Test Results

### Automated Test Suite (`?debug&run_tests=1`)
Executed in headless Chrome via SwiftShader WebGL:
- **Total Tests**: 45
- **Passed**: 45
- **Failed**: 0

```
=== AUTOMATED TEST SUITE OUTPUT ===
=== STARTING CADN'T COMPREHENSIVE AUTOMATED TESTS ===
[TEST-PASS] App Name is CADN'T
[TEST-PASS] Version chip initialized
[TEST-PASS] 4 Cameras initialized
[TEST-PASS] Canvas WebGL context active
[TEST-PASS] Starting Michigan model loaded
[TEST-PASS] Michigan model has Upper & Lower peninsulas
[TEST-PASS] Michigan model is protected
[TEST-PASS] Command without 'Can I' receives 'Nope.'
[TEST-PASS] Unprefixed command created no geometry
[TEST-PASS] 'Can I box' creates box primitive
[TEST-PASS] 'Can I sphere' creates sphere primitive
[TEST-PASS] 'Can I cylinder' creates cylinder primitive
[TEST-PASS] 'Can I cone' creates cone primitive
[TEST-PASS] Michigan cannot be deleted via standard delete
[TEST-PASS] 'Can I remove starting object' successfully deletes Michigan
[TEST-PASS] Toolbar icon relocation shifts layout order
[TEST-PASS] Trackpad wheel event is strictly cancelled/prevented
[TEST-PASS] Tutorial contains exact quote: 'The command to delete the starting object exists.'
[TEST-PASS] Starting balance is $249.00
[TEST-PASS] 2D Line Sketch creates Curve entity
[TEST-PASS] 2D Rectangle creates ClosedProfile with 2D Shape
[TEST-PASS] 2D Circle creates ClosedProfile with 2D Shape
[TEST-PASS] Extrude creates real 3D solid mesh with geometry
[TEST-PASS] Can I move transforms object coordinates
[TEST-PASS] Can I rotate rotates object around axis
[TEST-PASS] Can I scale resizes object geometry
[TEST-PASS] Boolean Union produces computed 3D CSG mesh
[TEST-PASS] Boolean Difference produces computed 3D cut CSG mesh
[TEST-PASS] Add Layer creates layer in model
[TEST-PASS] Toggle Layer Lock locks layer
[TEST-PASS] Toggle Layer Visibility hides layer
[TEST-PASS] Object created before undo test
[TEST-PASS] Can I undo removes the created object
[TEST-PASS] Can I redo restores the undone object
[TEST-PASS] Project serialization and deserialization roundtrip succeeded
[TEST-PASS] OBJ Exporter produces valid OBJ text containing vertices and faces
[TEST-PASS] STL Exporter produces valid binary DataView/ArrayBuffer with non-zero size
[TEST-PASS] Distorted export leaves internal scene object scale intact
[TEST-PASS] Import deducts exactly $10.00 from fictional credit balance
[TEST-PASS] Boolean operation on imported mesh is blocked
[TEST-PASS] Remesh command replaces target mesh with Sphere primitive
[TEST-PASS] Theme toggle successfully toggles light-theme class on body
[TEST-PASS] Audio synthesizer mute toggle functions correctly
[TEST-PASS] Artificial delay is bypassed immediately in DEBUG mode
[TEST-PASS] Ad modal contains tiny close button and blank ad placement placeholder
=== TEST SUMMARY: 45/45 PASSED, 0 FAILED ===
```

### Visual Verification Artifacts
1. `phase4_light_export.png`: Demonstrates Light theme, real extruded 3D geometry in all 4 viewports alongside Michigan, layer tree, properties inspector, and the Export dialog.
2. `phase4_loading_delay.png`: Demonstrates the 10-second artificial loading modal with animated gradient progress bar and rotating gaslighting status text.
3. `phase2_modeling.png`: Demonstrates multi-viewport 3D modeling, profile extrusion, and CSG booleans.
4. `phase1_onboarding.png`: Demonstrates the onboarding handbook with exact required phrasing.

---

## How to Run & Test
1. **Local Server**:
   ```bash
   cd /Users/andybuck/.gemini/antigravity/single-file-html-app
   python3 -m http.server 8000
   ```
2. **Open in Browser**:
   - Standard Mode: `http://localhost:8000/index.html`
   - Debug Mode (bypasses delays, shows debug button): `http://localhost:8000/index.html?debug`
   - Run Full Automated Tests: `http://localhost:8000/index.html?debug&run_tests=1`
