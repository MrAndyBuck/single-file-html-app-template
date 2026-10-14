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
- **Python**: Python 3.9.6 (available for local preview: `python3 -m http.server 8000`)
- **Git**: 2.39.5
- **Node/NPM**: None installed; conforming strictly to zero-build-step single-file HTML architecture
- **Browser Compatibility**: Chrome, Safari (desktop focus)

---

## 3D & Geometry Library Recommendation
1. **Renderer & Scene Graph: Three.js (r128 UMD)**
   - **Rationale**: Ultra-reliable, zero-dependency browser 3D library with full multi-viewport scissor rendering, raycasting, built-in primitives (`BoxGeometry`, `SphereGeometry`, `CylinderGeometry`, `ConeGeometry`, `ExtrudeGeometry`, `Shape`), and standard matrix math.
   - **Distribution**: Vendored locally in `/vendor/three.min.js` to enable 100% offline PWA operation.
2. **Boolean Engine: ThreeCSG / Constructive Solid Geometry**
   - **Rationale**: Real BSP-tree mesh intersection, union, and difference. Does not fake booleans.
3. **Importers/Exporters: Three.js STLExporter & OBJExporter**
   - **Rationale**: Standard ASCII/binary formats compatible with Blender, Rhino, and 3D printing slicers.

---

## Phased Implementation Status

| Phase | Description | Status | Notes |
|---|---|---|---|
| **Phase 1** | Functional Skeleton | **In Progress** | 4 Viewports (Persp/Top/Front/Right), Request Bar, Michigan starting model, keyboard nav, selection, primitives |
| **Phase 2** | Real Modeling | Pending | 2D Sketches, Extrude, Transforms, CSG Booleans, Layers & Properties |
| **Phase 3** | Data & I/O | Pending | Native `.cadnt` save/open, OBJ/STL import/export, Undo/Redo |
| **Phase 4** | Satire & Friction | Pending | Confirmations, icon relocation, ads, 10s delays, $249 economy, onboarding |
| **Phase 5** | Polish & Deploy | Pending | Themes, audio hooks, full test suite, GitHub Pages sync |

---

## Rules & Invariants
1. **Strict Request Bar Prefix**: Any command typed in the Request Bar without `Can I ` must reply **"Nope."**
2. **Michigan Immunity**: The starting Michigan model cannot be deleted with standard delete keys or commands. Only `Can I remove starting object` removes it.
3. **No Trackpad Navigation**: Mouse/trackpad wheels and drags on the viewports must NOT pan, orbit, or zoom. Viewport navigation is strictly mapped to `W/S/A/D`, arrows, and `Shift+arrows`.
4. **Real Geometry Only**: Primitives, transforms, and booleans must be real 3D geometry objects in the scene graph.
5. **Debug Bypass**: `?debug` URL parameter must disable artificial loading delays and skip confirmation modals for swift automated and manual testing.

---

## What's Next (Immediate Action)
- Construct the Phase 1 Walking Skeleton:
  1. Vendor `three.min.js` into `/vendor/three.min.js` (and include MIT license in `ATTRIBUTION.md`).
  2. Implement `index.html` with Rhino 4-viewport split layout, Request Bar, viewport labels/grids, Michigan extruded 3D model, camera controls, raycast selection, and primitive generation (`box`, `sphere`, `cylinder`, `cone`).
  3. Create PWA `manifest.webmanifest`, `sw.js`, and `icon.svg`.
  4. Test locally with `python3 -m http.server`.
  5. Present running application for user review before proceeding to Phase 2.
