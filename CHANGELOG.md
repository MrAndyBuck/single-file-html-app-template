# CHANGELOG

## [v00000-001] — 2026-10-14 (Phase 1 Walking Skeleton)

### Added
- **Rhino-Inspired 4-Viewport Matrix**:
  - Perspective, Top, Front, and Right viewports rendered simultaneously on a single WebGL canvas with viewport scissors.
  - Viewport quadrant labels with active viewport selection.
  - Ground C-Plane grids and coordinate axes helper.
- **The Request Bar**:
  - Replaces traditional CAD command line.
  - Requires `Can I [command]` prefix (case-insensitive).
  - Responds with **"Nope."** and input shake animation for any command lacking the prefix.
- **Starting Model: State of Michigan**:
  - Extruded 3D solid geometry of both the Upper and Lower Peninsulas.
  - Immune to standard delete commands and keys.
  - Removable solely via `Can I remove starting object`.
- **Keyboard Navigation & Trackpad Lock**:
  - Viewport camera navigation mapped to `W/S` (vertical orbit), `A/D` (horizontal orbit), `Arrow Keys` (pan), and `Shift + Arrows` (zoom).
  - Wheel and scroll trackpad events locked to prevent navigation.
  - Mouse clicks reserved for 3D raycast selection.
- **3D Primitives**:
  - `Can I box`: creates Box primitive.
  - `Can I sphere`: creates Sphere primitive.
  - `Can I cylinder`: creates Cylinder primitive.
  - `Can I cone`: creates Cone primitive.
- **Selection & Inspector**:
  - Raycast selection with Rhino-yellow highlight edges.
  - Layers panel and dynamic Objects tree.
  - Properties panel displaying name, type, layer, position, and protection status.
- **Wandering Toolbars**:
  - Toolbar icons relocate to random positions after each execution.
- **Satirical Economy & Onboarding**:
  - $249.00 starting credit counter with "Under Construction" purchase modal.
  - Onboarding handbook dialog featuring: *"The command to delete the starting object exists."*
- **PWA Architecture**:
  - Single-file HTML layout with local Three.js r128 vendoring for 100% offline support.
  - `manifest.webmanifest`, `sw.js`, and SVG icon.
  - Automated headless test suite passing 19/19 checks.
