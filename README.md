# CADN'T

> **Functional CAD software with intentionally dysfunctional interactions.**

CADN'T is a satirical, browser-based 3D computer-aided design application inspired by common frustrations with Rhino 3D, Autodesk Fusion 360, SolidWorks, and Blender.

The application looks, behaves, and functions like genuine CAD software, with real 3D modeling capabilities, but introduces deliberately adversarial user-experience decisions.

- **Live Web App**: [https://mrandybuck.github.io/single-file-html-app-template/](https://mrandybuck.github.io/single-file-html-app-template/)
- **Version**: `v0.1.0-alpha` (`v00000-001`)

---

## The Defining Principles

1. **Polite Deference via the Request Bar**:
   The traditional CAD command line is replaced with the Request Bar. All commands must begin with:
   ```text
   Can I [command]
   ```
   *Examples:* `Can I box`, `Can I sphere`, `Can I cylinder`, `Can I remove starting object`.
   Any command entered without the polite prefix receives a cold, unwavering response:
   **"Nope."**

2. **Strict Viewport Navigation**:
   Trackpad and mouse wheels are strictly disabled for viewport navigation.
   - `W` / `S`: Orbit vertically
   - `A` / `D`: Orbit horizontally
   - `Arrow Keys`: Pan vertically and horizontally
   - `Shift + Up/Down`: Zoom in and out
   - Mouse clicks are strictly reserved for raycast selection.

3. **Wandering Toolbars**:
   Command icons initially occupy confusing positions. After any toolbar command is executed, its icon relocates to another toolbar position.

4. **The Starting Model: The State of Michigan**:
   On launch, CADN'T displays a genuine extruded 3D solid of the US State of Michigan (both Upper and Lower Peninsulas). It cannot be deleted through standard delete operations. The only command that can remove it is:
   ```text
   Can I remove starting object
   ```

5. **Fictional Economy**:
   Every new user is endowed with $249.00 in fictional CAD credits. The "Buy More" button is permanently under construction.

---

## Development Status & Phasing

- **Phase 1 (Complete)**:
  - Rhino-inspired 4-viewport matrix (Perspective, Top, Front, Right).
  - Request Bar command interpreter.
  - Extruded 3D State of Michigan model with deletion protection.
  - Restricted keyboard camera navigation and trackpad lock.
  - Basic 3D primitives (`box`, `sphere`, `cylinder`, `cone`).
  - Raycast selection and Rhino-yellow highlighting.
  - Wandering toolbar icon relocation.
  - Onboarding handbook and Help index.
- **Phase 2 (Next)**: Real modeling tools (2D sketch curves, extrusion, transforms, CSG Booleans).
- **Phase 3**: Project saving/loading, STL/OBJ import and export, Undo/Redo.
- **Phase 4**: Satirical friction suite (ads, confirmations, 10s delays, gaslighting toasts).
- **Phase 5**: Polish, themes, audio hooks, and production deployment.

---

## License & Attribution
- Built with Three.js (r128, MIT License).
- See [`ATTRIBUTION.md`](ATTRIBUTION.md) and [`BRIEF.md`](BRIEF.md) for full architectural details.
