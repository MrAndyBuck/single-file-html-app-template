# BRIEF.md — CADN'T (v0.1)

> **"Functional CAD software with intentionally dysfunctional interactions."**

---

## 2.1 The Seed
- **Q1. In one sentence, what do you want to make?**  
  A satirical, intentionally frustrating browser-based 3D CAD application that looks, feels, and behaves like genuine CAD software (Rhino/Fusion 360/SolidWorks) with real modeling capabilities, but enforces deliberately poor user-experience decisions.
- **Q2. What medium does it work in?**  
  3D form, vector geometry, interactive viewports, and satirical interface mechanics.
- **Q3. What does this grow out of?**  
  Decades of cumulative ergonomic frustration, cryptic error dialogs, expensive feature locks, modal hell, and bizarre conventions in professional CAD software (Rhino 3D, Autodesk Fusion 360, SolidWorks, and Blender).
- **Reference / Anchor:**  
  Rhino 3D's classic 4-viewport layout, dense toolbar hierarchy, and command-line prompt—subverted into an insecure "Request Bar."

---

## 2.2 Raison d'être
- **Q4. What does it let someone do, see or feel that they can't easily do now?**  
  It lets users experience the visceral comedy and frustration of genuine 3D modeling through an adversarial interface: having to politely ask permission for basic operations ("Can I extrude"), dealing with wandering icons, navigating strictly with keyboard orbit/pan while trackpads only select, and managing a starting extruded model of the State of Michigan that refuses to be deleted normally.
- **Q5. What's the ONE thing it should do better than anything else?**  
  Balance real geometric utility with satirical friction—ensuring every operation actually computes real 3D geometry rather than faking it, so the humor lands because it's genuine software fighting back.
- **Q6. What will it deliberately NOT do?**  
  - No real payment processing (strictly fictional currency: $249 starting budget).
  - No continuous geometry drift in v0.1.
  - No voice-over or text-to-speech in v0.1.
  - No mock/fake geometry states: if an advanced geometry operation is unimplemented, it reports so honestly.
  - No server-side storage or tracking: 100% local in-browser execution.
- **Q7. About panel statement:**  
  *CADN'T exists because professional CAD software has spent forty years convincing designers that suffering is an intrinsic property of three-dimensional space.*

---

## 2.3 The User
- **Q8. Primary User:**  
  A 3D designer, architect, CAD modeler, or engineering student on a desktop/laptop with a keyboard and mouse/trackpad who has spent hours wrestling with Rhino or SolidWorks and wants to laugh, suffer, and test their sanity.
- **Q9. Secondary User:**  
  Spectators, colleagues, and social media audiences watching screen recordings of someone attempting to perform a routine CAD task inside CADN'T.
- **Q10. Who is it NOT for?**  
  Production engineers looking for precision aerospace CAM toolpaths or users on small touchscreen phones expecting standard mobile gestures.

---

## 2.4 The Interaction Model
- **Q11. Primary Input:**  
  - Keyboard navigation for viewport camera control:
    - `W` / `S`: Orbit vertically
    - `A` / `D`: Orbit horizontally
    - `Up` / `Down` arrow keys: Pan vertically
    - `Left` / `Right` arrow keys: Pan horizontally
    - `Shift + Up / Down` arrow keys: Zoom in / out
  - Trackpad / Mouse pointer: Strictly restricted to object selection and UI clicks. Viewport navigation **must not** respond to trackpad scrolling or wheel gestures.
  - Text entry: The Request Bar.
- **Q12. Interaction Model:**  
  Conversational-adversarial command dispatch coupled with direct 3D raycast selection and modal confirmation loops.
- **Q13. First 10 Seconds:**  
  Opens directly into a Rhino-inspired 4-viewport matrix (Perspective, Top, Front, Right) displaying an extruded 3D solid outline of the US State of Michigan (both Upper and Lower Peninsulas). An onboarding tutorial appears offering cryptic advice ("The command to delete the starting object exists.").
- **Q14. The Core Loop:**  
  Type polite request (`Can I [command]`) or click wandering toolbar icon → confirm "Are you sure?" → wait through artificial loading delay → inspect real geometric transformation → repeat.
- **Q15. What leaves the app?**  
  - Native CADN'T project JSON files (`.cadnt`).
  - Genuine 3D `.obj` and `.stl` mesh exports.
  - Optional nonuniform export scaling feature.

---

## 2.5 The Request Bar Specification
- All commands typed in the Request Bar must begin with:  
  `Can I [command]` (case-insensitive).
  - Valid examples: `Can I box`, `Can I sphere`, `Can I cylinder`, `Can I cone`, `Can I extrude`, `Can I move`, `Can I rotate`, `Can I scale`, `Can I undo`, `Can I redo`, `Can I remove starting object`, `Can I save`.
- Any command typed without the required prefix receives the curt response:  
  **"Nope."**
- Toolbar button invocations bypass typing the prefix, but trigger an "Are you sure?" confirmation dialog.
- Command icons relocate to another toolbar slot after execution.
- Undo and Redo are **only** accessible through the Request Bar.

---

## 2.6 The Starting Model: Michigan
- Extruded 3D outline of the US State of Michigan with both the Upper Peninsula (UP) and Lower Peninsula (LP).
- Immune to ordinary selection deletion (`Delete` key or standard delete commands do nothing).
- The **only** command capable of deleting it is:  
  `Can I remove starting object`
- Prompts with: **"Are you sure you want to remove this?"** Upon confirmation, the geometry is removed.

---

## 2.7 Visual Identity & Layout
- **Inspiration:** Classic Rhino 3D v5/v6/v7 layout.
- **Viewports:** 4-way split pane:
  - Top-Left: Perspective (3D orbit camera)
  - Top-Right: Top (orthographic, looking down -Z / -Y)
  - Bottom-Left: Front (orthographic, looking forward)
  - Bottom-Right: Right (orthographic, looking from side)
- **Request Bar:** Positioned at the top or bottom of the viewport matrix matching Rhino command prompt.
- **Toolbars:**
  - Top toolbar (Primitives, Transforms, File operations, Economy balance).
  - Left toolbar (Drafting tools, Solids, Booleans).
- **Right Panels:**
  - Layers / Objects tree.
  - Properties panel (coordinates, dimensions, layer assignment).
- **Themes:**
  - Dark Theme (default): CAD dark charcoal `#1a1a1a`, grid lines `#2c2c2c`, Rhino yellow selection `#ffff00`, radioactive green accents `#39ff14`.
  - Light Theme: Classic Rhino gray `#dcdcdc`, charcoal text, yellow/green highlights.
- **Fictional Economy:**
  - Starting balance: **$249** in fictional CADN'T credits.
  - Flat pricing on operations (e.g. $10 import fee).
  - "Buy More" button opens an "UNDER CONSTRUCTION" window.
  - Fillet and Chamfer are premium per-use commands ($49/ea).

---

## 2.8 Technical Choices & Architecture
- **Host Architecture:** Single-file HTML (`index.html`) using PWA standards (`manifest.webmanifest`, `sw.js`).
- **3D Engine:** Three.js (r128 / latest stable UMD vendored locally in `/vendor/three.min.js`).
- **Geometry Operations:** Real Three.js BufferGeometry primitives, CSG (Constructive Solid Geometry) for Boolean Union & Difference.
- **Storage:** LocalStorage for UI settings/theme, IndexedDB for document persistence & autosave.
- **Debug Mode:** Accessible via `?debug` flag to bypass artificial delays and dismiss dialogs for fast automated testing.
- **No external telemetry, analytics, or server calls.**

---

## 2.9 Phased Implementation Plan
- **Phase 1 — Functional Skeleton (Immediate Milestone):**
  - Rhino-inspired 4-viewport layout (Perspective, Top, Front, Right) with viewport labels and coordinate grids.
  - Request Bar with `Can I [command]` parsing and `"Nope."` rejection logic.
  - Default extruded Michigan starting model (Upper + Lower Peninsulas).
  - Restricted keyboard navigation (`W/S/A/D` orbit, arrow pan, `Shift+arrows` zoom).
  - Strict trackpad restriction (no viewport wheel orbit/zoom; click raycast selection only).
  - Basic 3D primitives via Request Bar and wandering toolbar: Box, Sphere, Cylinder, Cone.
  - Object selection highlighting (Rhino neon yellow outline/wireframe).
  - Deletion restriction: Michigan only removable via `Can I remove starting object`.
  - Version chip, PWA manifest, service worker.
  - **Checkpoint: Stop after Phase 1 and present running application for user review.**
- **Phase 2 — Real Modeling & Editing:**
  - 2D sketching (Lines, Rectangles, Circles on construction plane).
  - Profile extrusion into 3D solids.
  - Transformations (Move, Rotate, Scale) with numeric inputs in Properties.
  - Boolean Union and Boolean Difference via CSG.
  - Object & Layer management panel (create, rename, hide, color, select).
- **Phase 3 — Project Data & I/O:**
  - Native project file saving & reopening (`.cadnt` JSON).
  - OBJ and STL genuine export.
  - OBJ and STL import ($10 fictional fee).
  - Remesh / Simplify commands (intentionally replaces imported mesh with sphere).
  - Request Bar Undo/Redo stack.
- **Phase 4 — Satirical Friction & Economy:**
  - Toolbar icon relocation after every execution.
  - "Are you sure?" confirmation dialogs on toolbar clicks.
  - Occasional intrusive satirical ad popups with minuscule close buttons.
  - Artificial loading delays (minimum 10s for heavy operations, with progress bar and gaslighting status messages).
  - Onboarding tutorial popups with vague/cryptic hints.
  - Fictional credit counter ($249) and "Under Construction" purchase modal.
- **Phase 5 — Polish, Audio, & GitHub Pages Deployment:**
  - Theme toggle (Dark / Light with yellow & green accents).
  - Audio system hooks (loading soundscapes, mute toggle).
  - Cross-browser testing (Chrome, Safari).
  - Verified GitHub Pages live deployment.

---

## 2.10 Planned Future Commands — Pipe and Sweep (Roadmap)

> **Important**: In accordance with user specifications, Pipe and Sweep are planned for future implementation and must produce genuine geometric solids (not decorative previews).

### 1. Pipe Command Specification
- **Request Bar Invocations**:
  - `Can I pipe`
  - `Can I pipe [radius]`
- **Intended Functionality**:
  - Generates a tubular 3D solid mesh along a selected 3D curve (Line, Polyline, or Spline Curve entity).
  - User specifies radius or diameter via parameter prompt in the Interactive Command Bar (`#command-bar`) or Request Bar.
  - Generates real manifold solid geometry with watertight planar or spherical end caps.
  - Integrates with the ThreeCSG Boolean engine, allowing the resulting pipe to be used in Boolean Union and Difference operations.
- **Technical Dependencies**:
  - `THREE.CurvePath` / `THREE.CatmullRomCurve3` or polyline segment evaluation.
  - Tubular mesh generator (`THREE.TubeGeometry` or custom variable-radius sweep buffer).
  - Cap geometry synthesis (`THREE.CircleGeometry` or disc triangulation oriented along curve endpoint tangents).
  - Manifold mesh validation before adding to `sceneObjects`.
  - Integration with Command Bar two-step workflow: Step 1 (Select curve), Step 2 (Specify radius/diameter).
  - Audio hook: Play hold music during computation (registered under `CADNT_AUDIO.playHoldMusic()`).

### 2. Sweep Command Specification
- **Request Bar Invocations**:
  - `Can I sweep`
- **Intended Functionality**:
  - Generates a 3D solid or surface by sweeping a selected 2D profile curve (circle, rectangle, or arbitrary closed profile) along a selected 3D rail curve.
  - Must produce authentic manifold geometry, not decorative previews or hollow unclosed shells.
  - Aligns profile normal with the rail tangent at the start point, maintaining parallel transport (Bishop framing or Frenet-Serret frame) along the rail curve to avoid pinching or self-intersection.
  - Produces closed solid if the profile is closed and end caps are enabled.
- **Technical Dependencies**:
  - Curve frame computation (Bishop frame / parallel transport algorithm to prevent topological twisting).
  - Cross-section vertex extrusion and skinning along Frenet coordinate frames into `THREE.BufferGeometry`.
  - CSG boolean compatibility for downstream operations.
  - Interactive Command Bar multi-stage selector:
    - Stage 1: Select Rail Curve.
    - Stage 2: Select Cross-Section Profile.
    - Stage 3: Parameter confirmation (twist angle, scale factor, end capping).
  - Audio hook: Trigger hold music during execution (already configured in `triggerArtificialDelay`).
  - Fictional economy integration ($49.00 premium charge or delay).

