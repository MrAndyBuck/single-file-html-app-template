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
- After the user evaluates the visual appearance and interaction of Phase 1, proceed to Phase 2:
  1. Add 2D sketch tools (Lines, Rectangles, Circles) onto the active viewport C-Plane.
  2. Implement closed 2D profile extrusion into 3D meshes.
  3. Implement Move, Rotate, and Scale transforms with direct viewport gizmos and properties panel coordinates.
  4. Implement genuine CSG (Constructive Solid Geometry) for Boolean Union and Boolean Difference.
  5. Expand Layer & Object management capabilities.
