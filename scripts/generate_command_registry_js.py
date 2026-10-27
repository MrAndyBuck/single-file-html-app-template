#!/usr/bin/env python3
"""
Generates the authoritative COMMAND_CATEGORIES and COMMAND_REGISTRY JavaScript blocks for index.html.
Ensures every recognized command is listed, categorized into all 14 categories, and mapped to its execution handler.
"""

import sys

js_code = """/* =========================================================================
   COMMAND REGISTRY & CANONICAL DISPATCHER (CHECKPOINT B & C SINGLE SOURCE OF TRUTH)
   ========================================================================= */

const COMMAND_CATEGORIES = [
  "1. Geometry primitives",
  "2. Sketching and curves",
  "3. Extrusion and surface operations",
  "4. Boolean operations",
  "5. Fillet, chamfer, and edge modification",
  "6. Moving and transforming",
  "7. Object and layer management",
  "8. Saving, importing, and exporting",
  "9. Viewport and navigation controls",
  "10. Cubert commands",
  "11. Localization commands",
  "12. Satirical/special commands",
  "13. Debugging and development commands",
  "14. Coming Soon commands"
];

function normalizeCommandText(str) {
  if (!str) return "";
  return str.trim().toLowerCase().replace(/[?!.,;。！]+$/, "").trim();
}

const COMMAND_REGISTRY = [
  // 1. Geometry primitives
  {
    id: "box",
    category: "1. Geometry primitives",
    syntax: "Can I box",
    aliases: ["Can I box", "Can I cube", "box", "cube"],
    description: "Creates a solid 3D box primitive centered on the construction grid.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#tool-box",
    execute: () => createBoxPrimitive()
  },
  {
    id: "sphere",
    category: "1. Geometry primitives",
    syntax: "Can I sphere",
    aliases: ["Can I sphere", "sphere"],
    description: "Generates a parametric 3D sphere primitive.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#tool-sphere",
    execute: () => createSpherePrimitive()
  },
  {
    id: "cylinder",
    category: "1. Geometry primitives",
    syntax: "Can I cylinder",
    aliases: ["Can I cylinder", "Can I cyl", "cylinder", "cyl"],
    description: "Creates a solid 3D cylinder primitive.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#tool-cylinder",
    execute: () => createCylinderPrimitive()
  },
  {
    id: "cone",
    category: "1. Geometry primitives",
    syntax: "Can I cone",
    aliases: ["Can I cone", "cone"],
    description: "Creates a solid 3D cone primitive.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#tool-cone",
    execute: () => createConePrimitive()
  },
  {
    id: "torus",
    category: "1. Geometry primitives",
    syntax: "Can I torus",
    aliases: ["Can I torus", "torus"],
    description: "Generates a circular 3D torus solid primitive.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => {
      const geom = new THREE.TorusGeometry(8, 3, 16, 40);
      const mat = new THREE.MeshStandardMaterial({ color: 0x39ff14, roughness: 0.4, metalness: 0.1 });
      const mesh = new THREE.Mesh(geom, mat);
      mesh.name = `Torus ${sceneObjects.length + 1}`;
      mesh.position.set(0, 10, 0);
      mesh.userData = { id: `torus_${Date.now()}`, type: "primitive", layer: activeLayerId };
      scene.add(mesh);
      sceneObjects.push(mesh);
      selectObject(mesh);
      updatePropertiesPanel();
      updateObjectsTree();
      recordUndoState("Create Torus");
      status("Torus created.");
      addLog("Torus primitive generated.", "log-success");
      recordModelingCommand();
      renderAllViewports();
    }
  },
  {
    id: "plane",
    category: "1. Geometry primitives",
    syntax: "Can I plane",
    aliases: ["Can I plane", "plane"],
    description: "Constructs a 2D planar construction surface.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => {
      const geom = new THREE.PlaneGeometry(30, 30);
      const mat = new THREE.MeshStandardMaterial({ color: 0x808080, side: THREE.DoubleSide });
      const mesh = new THREE.Mesh(geom, mat);
      mesh.rotation.x = -Math.PI / 2;
      mesh.name = `Plane ${sceneObjects.length + 1}`;
      mesh.userData = { id: `plane_${Date.now()}`, type: "primitive", layer: activeLayerId };
      scene.add(mesh);
      sceneObjects.push(mesh);
      selectObject(mesh);
      updatePropertiesPanel();
      updateObjectsTree();
      recordUndoState("Create Plane");
      status("Plane created.");
      addLog("Planar construction surface created.", "log-success");
      recordModelingCommand();
      renderAllViewports();
    }
  },

  // 2. Sketching and curves
  {
    id: "line",
    category: "2. Sketching and curves",
    syntax: "Can I line",
    aliases: ["Can I line", "Can I polyline", "line", "polyline"],
    description: "Enters interactive 2D sketching mode to draw linear vector segments on the construction plane.",
    prerequisites: "Active construction plane",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: (args) => {
      if (args && args.length === 1 && !isNaN(parseFloat(args[0]))) {
        const len = parseFloat(args[0]);
        let p1 = new THREE.Vector3(0, 0, 0);
        let p2 = new THREE.Vector3(len, 0, 0);
        if (activeViewport === "front") p2 = new THREE.Vector3(len, 0, 0);
        else if (activeViewport === "right") p2 = new THREE.Vector3(0, 0, len);
        else p2 = new THREE.Vector3(len, 0, 0);
        createLineSketch([p1, p2], activeViewport, false);
      } else if (args && args.length === 4 && args.every(a => !isNaN(parseFloat(a)))) {
        const nums = args.map(Number);
        let p1, p2;
        if (activeViewport === "front") {
          p1 = new THREE.Vector3(nums[0], nums[1], 0);
          p2 = new THREE.Vector3(nums[2], nums[3], 0);
        } else if (activeViewport === "right") {
          p1 = new THREE.Vector3(0, nums[1], nums[0]);
          p2 = new THREE.Vector3(0, nums[3], nums[2]);
        } else {
          p1 = new THREE.Vector3(nums[0], 0, nums[1]);
          p2 = new THREE.Vector3(nums[2], 0, nums[3]);
        }
        createLineSketch([p1, p2], activeViewport, false);
      } else if (args && args.length === 6 && args.every(a => !isNaN(parseFloat(a)))) {
        const nums = args.map(Number);
        const p1 = new THREE.Vector3(nums[0], nums[1], nums[2]);
        const p2 = new THREE.Vector3(nums[3], nums[4], nums[5]);
        createLineSketch([p1, p2], activeViewport, false);
      } else if (args && args.length >= 2 && args[0].includes(",")) {
        const pts = args.map(arg => {
          const coords = arg.split(",").map(Number);
          if (activeViewport === "front") return new THREE.Vector3(coords[0] || 0, coords[1] || 0, 0);
          if (activeViewport === "right") return new THREE.Vector3(0, coords[1] || 0, coords[0] || 0);
          return new THREE.Vector3(coords[0] || 0, 0, coords[1] || 0);
        });
        createLineSketch(pts, activeViewport, false);
      } else {
        startSketch("line");
      }
    }
  },
  {
    id: "rectangle",
    category: "2. Sketching and curves",
    syntax: "Can I rect",
    aliases: ["Can I rect", "Can I rectangle", "rect", "rectangle"],
    description: "Draws a closed 2D rectangular sketch profile on the construction plane.",
    prerequisites: "Active construction plane",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => startSketch("rect")
  },
  {
    id: "circle",
    category: "2. Sketching and curves",
    syntax: "Can I circle",
    aliases: ["Can I circle", "circle"],
    description: "Draws a closed circular planar sketch curve.",
    prerequisites: "Active construction plane",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => startSketch("circle")
  },
  {
    id: "spline",
    category: "2. Sketching and curves",
    syntax: "Can I spline",
    aliases: ["Can I spline", "spline"],
    description: "Constructs smooth cubic Catmull-Rom spline curves with interactive tangent handles.",
    prerequisites: "Active construction plane",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => startSketch("spline")
  },
  {
    id: "polygon",
    category: "2. Sketching and curves",
    syntax: "Can I polygon [sides]",
    aliases: ["Can I polygon", "Can I poly", "Can I ngon", "polygon", "poly", "ngon"],
    description: "Generates regular n-sided polygon sketches (3 to 12 sides) centered at origin.",
    prerequisites: "Active construction plane",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    match: (raw, norm, withoutCanI) => {
      const q = withoutCanI || norm;
      const m = q.match(/^(?:poly(?:gon|ngon)?|ngon)(?:\s+(\d+))?$/i);
      if (m) return { args: m[1] ? [parseInt(m[1], 10)] : [] };
      return null;
    },
    execute: (args) => {
      const sides = args && args[0] ? args[0] : 6;
      startSketch("polygon", sides);
    }
  },

  // 3. Extrusion and surface operations
  {
    id: "extrude",
    category: "3. Extrusion and surface operations",
    syntax: "Can I extrude",
    aliases: ["Can I extrude", "extrude"],
    description: "Extrudes a planar 2D curve or polygon into a watertight 3D solid mesh.",
    prerequisites: "Selected 2D sketch curve",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: (args) => {
      if (args && args.length >= 1 && selectedObjects.some(o => o.userData && o.userData.closed && o.userData.shape)) {
        const depth = parseFloat(args[0]);
        extrudeSelectedProfile(isNaN(depth) ? 10 : depth);
      } else {
        const depth = args && args[0] ? parseFloat(args[0]) : undefined;
        startModelingCommand("extrude", { depth: isNaN(depth) ? undefined : depth });
      }
    }
  },
  {
    id: "pipe",
    category: "3. Extrusion and surface operations",
    syntax: "Can I pipe",
    aliases: ["Can I pipe", "pipe"],
    description: "Sweeps a circular profile around a 2D or 3D path curve.",
    prerequisites: "Selected path curve",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    match: (raw, norm, withoutCanI) => {
      const q = withoutCanI || norm;
      const m = q.match(/^pipe(?:\s+([\d.]+))?(?:\s+(diameter|radius))?$/i);
      if (m) {
        let pArgs = null;
        if (m[1]) {
          pArgs = { val: parseFloat(m[1]), mode: m[2] && m[2].toLowerCase() === "diameter" ? "diameter" : "radius" };
        }
        return { args: pArgs ? [pArgs] : [] };
      }
      return null;
    },
    execute: (args) => {
      const pipeArgs = args && args[0] ? args[0] : null;
      startModelingCommand("pipe", pipeArgs);
    }
  },
  {
    id: "sweep",
    category: "3. Extrusion and surface operations",
    syntax: "Can I sweep",
    aliases: ["Can I sweep", "sweep"],
    description: "Sweeps cross-sectional geometry along a trajectory curve.",
    prerequisites: "Selected trajectory curve",
    cost: "$49.00",
    status: "Working",
    control: "#request-input",
    execute: () => attemptPaidOperation("sweep", 49.00)
  },

  // 4. Boolean operations
  {
    id: "union",
    category: "4. Boolean operations",
    syntax: "Can I union",
    aliases: ["Can I union", "Can I boolean union", "Can I join", "union", "boolean union", "join"],
    description: "Performs exact Constructive Solid Geometry (CSG) union combining intersecting meshes.",
    prerequisites: "Two or more intersecting solid meshes selected",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => startModelingCommand("union")
  },
  {
    id: "difference",
    category: "4. Boolean operations",
    syntax: "Can I difference",
    aliases: ["Can I difference", "Can I diff", "Can I subtract", "Can I boolean diff", "difference", "diff", "subtract"],
    description: "Performs CSG Boolean difference, subtracting secondary meshes from the base mesh.",
    prerequisites: "Two intersecting solid meshes selected",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => startModelingCommand("difference")
  },

  // 5. Fillet, chamfer, and edge modification
  {
    id: "fillet",
    category: "5. Fillet, chamfer, and edge modification",
    syntax: "Can I fillet",
    aliases: ["Can I fillet", "fillet"],
    description: "Rounds sharp polyhedral solid edges with exact B-Rep cylindrical bevel patches.",
    prerequisites: "Selected solid mesh with selectable edges, $49.00 credit balance",
    cost: "$49.00",
    status: "Working",
    control: "#request-input",
    execute: (args) => {
      if (args && args.length >= 2 && !isNaN(parseFloat(args[0])) && !isNaN(parseFloat(args[1]))) {
        startModelingCommand("fillet", { val1: parseFloat(args[0]), val2: parseFloat(args[1]), isAsymmetric: true });
      } else {
        startModelingCommand("fillet", args && args.length >= 1 && !isNaN(parseFloat(args[0])) ? { val: parseFloat(args[0]) } : {});
      }
    }
  },
  {
    id: "chamfer",
    category: "5. Fillet, chamfer, and edge modification",
    syntax: "Can I chamfer",
    aliases: ["Can I chamfer", "chamfer"],
    description: "Bevels solid edges with planar transition facets at a 45-degree angle.",
    prerequisites: "Selected solid mesh with selectable edges, $49.00 credit balance",
    cost: "$49.00",
    status: "Working",
    control: "#request-input",
    execute: (args) => {
      if (args && args.length >= 2 && !isNaN(parseFloat(args[0])) && !isNaN(parseFloat(args[1]))) {
        startModelingCommand("chamfer", { val1: parseFloat(args[0]), val2: parseFloat(args[1]), isAsymmetric: true });
      } else {
        startModelingCommand("chamfer", args && args.length >= 1 && !isNaN(parseFloat(args[0])) ? { val: parseFloat(args[0]) } : {});
      }
    }
  },
  {
    id: "asym",
    category: "5. Fillet, chamfer, and edge modification",
    syntax: "Can I asym",
    aliases: ["Can I asym", "Can I asymmetric", "asym", "asymmetric"],
    description: "Applies asymmetric edge transitions with independent setbacks on adjacent faces.",
    prerequisites: "Selected solid mesh with selectable edges, $49.00 credit balance",
    cost: "$49.00",
    status: "Working",
    control: "#request-input",
    execute: (args) => {
      if (args && (args[0] === "fillet" || args[0] === "chamfer")) {
        const subMode = args[0];
        const v1 = args[1] && !isNaN(parseFloat(args[1])) ? parseFloat(args[1]) : (subMode === "fillet" ? 2.5 : 2.0);
        const v2 = args[2] && !isNaN(parseFloat(args[2])) ? parseFloat(args[2]) : v1 * 2;
        startModelingCommand(subMode, { val1: v1, val2: v2, isAsymmetric: true });
      } else {
        status("Specify 'asym fillet' or 'asym chamfer'.");
      }
    }
  },

  // 6. Moving and transforming
  {
    id: "move",
    category: "6. Moving and transforming",
    syntax: "Can I move",
    aliases: ["Can I move", "move"],
    description: "Translates selected objects along Cartesian axes with numeric coordinate entry.",
    prerequisites: "Selected object(s)",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: (args) => {
      if (args && args.length >= 1 && selectedObjects.length > 0) {
        const dx = parseFloat(args[0]) || 0;
        const dy = args[1] !== undefined ? (parseFloat(args[1]) || 0) : 0;
        const dz = args[2] !== undefined ? (parseFloat(args[2]) || 0) : 0;
        transformSelected("move", { dx, dy, dz });
      } else {
        const dx = args && args[0] !== undefined ? parseFloat(args[0]) : undefined;
        const dy = args && args[1] !== undefined ? parseFloat(args[1]) : undefined;
        const dz = args && args[2] !== undefined ? parseFloat(args[2]) : undefined;
        startModelingCommand("move", { dx, dy, dz });
      }
    }
  },
  {
    id: "rotate",
    category: "6. Moving and transforming",
    syntax: "Can I rotate",
    aliases: ["Can I rotate", "rotate"],
    description: "Rotates selected objects around the specified origin in degrees.",
    prerequisites: "Selected object(s)",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: (args) => {
      let rAxis = "y";
      let rDeg = 45;
      if (args && args.length === 1) {
        if (isNaN(args[0])) rAxis = args[0];
        else rDeg = parseFloat(args[0]);
      } else if (args && args.length >= 2) {
        rAxis = args[0];
        rDeg = parseFloat(args[1]) || 45;
      }
      if (args && args.length >= 1 && selectedObjects.length > 0) {
        transformSelected("rotate", { axis: rAxis, deg: rDeg });
      } else {
        startModelingCommand("rotate", { axis: rAxis, deg: rDeg });
      }
    }
  },
  {
    id: "scale",
    category: "6. Moving and transforming",
    syntax: "Can I scale",
    aliases: ["Can I scale", "scale"],
    description: "Applies uniform or non-uniform scaling factors to selected geometry.",
    prerequisites: "Selected object(s)",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: (args) => {
      const s = args && args[0] !== undefined ? parseFloat(args[0]) : 1.5;
      const sy = args && args[1] !== undefined ? parseFloat(args[1]) : s;
      const sz = args && args[2] !== undefined ? parseFloat(args[2]) : s;
      if (args && args.length >= 1 && selectedObjects.length > 0) {
        transformSelected("scale", { sx: isNaN(s) ? 1.5 : s, sy: isNaN(sy) ? s : sy, sz: isNaN(sz) ? s : sz });
      } else {
        startModelingCommand("scale", { factor: isNaN(s) ? 1.5 : s });
      }
    }
  },
  {
    id: "gumball",
    category: "6. Moving and transforming",
    syntax: "Can I gumball",
    aliases: ["Can I gumball", "Can I please gumball", "gumball", "gumball please"],
    description: "Summons interactive 3D transformation widget on the selected object.",
    prerequisites: "Selected object",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => {
      if (selectedObjects.length === 0) {
        addLog("Gumball requested, but no object is selected. Select an object first.", "log-warn");
        status("Select an object to display Gumball.");
        isGumballActive = false;
        updateGumball();
        return;
      }
      isGumballActive = true;
      updateGumball();
      addLog("Gumball activated.", "log-success");
      status("Gumball activated on selected object.");
    }
  },

  // 7. Object and layer management
  {
    id: "remove_starting_object",
    category: "7. Object and layer management",
    syntax: "Can I remove starting object",
    aliases: [
      "Can I remove starting object",
      "Can I delete michigan",
      "Can I remove michigan",
      "Can I delete starting object",
      "remove starting object",
      "delete michigan",
      "remove michigan"
    ],
    description: "The sole authorized secret procedure for removing the Michigan starting solid.",
    prerequisites: "Michigan starting object present; confirmation required",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => {
      const targetObj = sceneObjects.find(o => o.userData && o.userData.id === "starting_michigan")
        || sceneObjects.find(o => o.userData && o.userData.isStartingObject)
        || michiganModel
        || diagnosticCube;

      if (!targetObj || !sceneObjects.includes(targetObj)) {
        addLog("Starting object is already gone.", "log-warn");
        status("Starting object does not exist.");
        return;
      }
      showConfirmModal(
        "Are you sure you want to remove this?",
        "Are you sure you want to remove this?",
        () => {
          recordUndoState("Remove Starting Object");
          scene.remove(targetObj);
          const idx = sceneObjects.indexOf(targetObj);
          if (idx !== -1) sceneObjects.splice(idx, 1);
          selectedObjects = selectedObjects.filter(o => o !== targetObj);
          if (targetObj === michiganModel) michiganModel = null;
          if (targetObj === diagnosticCube) diagnosticCube = null;
          updateGumball();
          updateObjectsTree();
          updatePropertiesPanel();
          addLog("Starting object removed. You can restore it using 'Can I undo'.", "log-success");
          status("Starting object removed.");
          recordModelingCommand();
          renderAllViewports();
        }
      );
    }
  },
  {
    id: "delete",
    category: "7. Object and layer management",
    syntax: "Can I delete",
    aliases: ["Can I delete", "Can I remove", "delete", "remove"],
    description: "Deletes selected user-created objects (locked objects and Michigan starting solid are protected).",
    prerequisites: "Selected user-created object",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => handleDelete()
  },
  {
    id: "lock",
    category: "7. Object and layer management",
    syntax: "Can I lock",
    aliases: ["Can I lock", "lock"],
    description: "Locks selected objects, preventing raycast selection, editing, and accidental deletion.",
    prerequisites: "Selected object",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => handleLockCommand()
  },
  {
    id: "unlock",
    category: "7. Object and layer management",
    syntax: "Can I unlock",
    aliases: ["Can I unlock", "unlock"],
    description: "Unlocks selected locked objects, restoring interactive selection and editing.",
    prerequisites: "Selected locked object",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => handleUnlockCommand()
  },
  {
    id: "add_layer",
    category: "7. Object and layer management",
    syntax: "Can I add layer",
    aliases: ["Can I add layer", "Can I layer", "add layer", "layer"],
    description: "Creates a new organizational CAD layer with color tagging and visibility control.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => {
      const layerId = "layer_" + Date.now();
      const colors = ["#ff0055", "#00d4ff", "#ffbb00", "#ff00ff", "#00ff66"];
      const col = colors[layers.length % colors.length];
      const name = "Layer " + (layers.length + 1);
      layers.push({ id: layerId, name: name, color: col, visible: true, locked: false });
      renderLayersList();
      recordUndoState("Add Layer");
      addLog(`Added layer '${name}'.`, "log-success");
      status(`Layer '${name}' created.`);
    }
  },

  // 8. Saving, importing, and exporting
  {
    id: "save",
    category: "8. Saving, importing, and exporting",
    syntax: "Can I save",
    aliases: ["Can I save", "save"],
    description: "Serializes complete 3D scene state, layers, and properties into native .cadnt JSON file.",
    prerequisites: "Active scene",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => saveProjectToFile()
  },
  {
    id: "open",
    category: "8. Saving, importing, and exporting",
    syntax: "Can I open",
    aliases: ["Can I open", "open"],
    description: "Reopens and reconstructs 3D geometry from a saved .cadnt project archive.",
    prerequisites: "Valid .cadnt file",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => openProjectFromFile()
  },
  {
    id: "export",
    category: "8. Saving, importing, and exporting",
    syntax: "Can I export [stl|obj]",
    aliases: ["Can I export", "export", "export stl", "export obj"],
    description: "Generates production-grade STL or OBJ 3D mesh files (protects un-displaced geometry).",
    prerequisites: "Active scene objects",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    match: (raw, norm, withoutCanI) => {
      const q = withoutCanI || norm;
      const m = q.match(/^export(?:\s+(stl|obj))?$/i);
      if (m) return { args: m[1] ? [m[1].toLowerCase()] : ["stl"] };
      return null;
    },
    execute: (args) => {
      const fmt = args && args[0] ? args[0] : "stl";
      exportProjectGeometry(fmt);
    }
  },
  {
    id: "import",
    category: "8. Saving, importing, and exporting",
    syntax: "Can I import",
    aliases: ["Can I import", "import"],
    description: "Imports external STL or OBJ 3D models into CADN'T workspace.",
    prerequisites: "Valid STL/OBJ file, $10.00 credit balance",
    cost: "$10.00",
    status: "Working",
    control: "#request-input",
    execute: () => importProjectGeometry()
  },
  {
    id: "remesh",
    category: "8. Saving, importing, and exporting",
    syntax: "Can I remesh",
    aliases: ["Can I remesh", "Can I simplify", "remesh", "simplify"],
    description: "Satirical geometry optimization: re-tessellates any mesh into a generic sphere.",
    prerequisites: "Selected mesh",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => remeshSelectedObject()
  },

  // 9. Viewport and navigation controls
  {
    id: "orbit",
    category: "9. Viewport and navigation controls",
    syntax: "W / S / A / D",
    aliases: ["can i orbit", "orbit", "W", "S", "A", "D"],
    description: "Orbits the 3D Perspective viewport camera (W/S vertical pitch, A/D horizontal yaw). Trackpad wheel orbit intentionally blocked.",
    prerequisites: "Viewport focus",
    cost: "$0.00",
    status: "Working",
    control: "#cad-canvas",
    execute: () => {
      status("Perspective orbit: Press W/S for pitch, A/D for yaw. Trackpad orbit is blocked.");
      addLog("Navigation reminder: Use W/S/A/D keyboard keys to orbit camera.", "log-info");
    }
  },
  {
    id: "pan",
    category: "9. Viewport and navigation controls",
    syntax: "Arrow Keys",
    aliases: ["can i pan", "pan", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"],
    description: "Pans the active viewport camera along the viewport plane.",
    prerequisites: "Viewport focus",
    cost: "$0.00",
    status: "Working",
    control: "#cad-canvas",
    execute: () => {
      status("Viewport pan: Use Up/Down/Left/Right arrow keys.");
      addLog("Navigation reminder: Use arrow keys to pan active viewport camera.", "log-info");
    }
  },
  {
    id: "zoom",
    category: "9. Viewport and navigation controls",
    syntax: "Shift + Arrow Keys",
    aliases: ["can i zoom", "zoom", "Shift+Up", "Shift+Down"],
    description: "Zooms the active viewport camera in or out.",
    prerequisites: "Viewport focus",
    cost: "$0.00",
    status: "Working",
    control: "#cad-canvas",
    execute: () => {
      status("Viewport zoom: Hold Shift and press Up or Down arrow key.");
      addLog("Navigation reminder: Use Shift+Up/Down arrow keys to zoom camera.", "log-info");
    }
  },
  {
    id: "view",
    category: "9. Viewport and navigation controls",
    syntax: "Can I view [top|perspective|front|right]",
    aliases: ["can i view", "view top", "view front", "view right", "view perspective"],
    description: "Focuses the specified CAD quadrant viewport.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#cad-canvas",
    match: (raw, norm, withoutCanI) => {
      const q = withoutCanI || norm;
      const m = q.match(/^view(?:\s+(top|perspective|front|right))?$/i);
      if (m) return { args: m[1] ? [m[1].toLowerCase()] : ["perspective"] };
      return null;
    },
    execute: (args) => {
      const vp = args && args[0] ? args[0] : "perspective";
      activeViewportKey = vp;
      focusActiveCanvas();
      status(`Focused ${vp.toUpperCase()} viewport.`);
      addLog(`Viewport switched to ${vp}.`, "log-info");
    }
  },

  // 10. Cubert commands
  {
    id: "cubert_summon",
    category: "10. Cubert commands",
    syntax: "Can I cubert",
    aliases: ["Can I cubert", "Can I help", "Can I talk to cubert", "cubert", "help cubert"],
    description: "Summons the Cubert desktop assistant with authentic speech bubbles and audio voiceover.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#cubert-standby-avatar",
    execute: () => {
      cubertConsecutiveFailures = 0;
      showCubertPopup("How can I help you?", "cheerful");
      cubertConvStage = "AWAITING_DESCRIPTION";
      status("Cubert: 'How can I help you?'");
      addLog("Cubert summoned.", "log-info");
    }
  },
  {
    id: "cubert_dismiss",
    category: "10. Cubert commands",
    syntax: "Can you leave Cubert",
    aliases: [
      "Can you leave Cubert",
      "Can I ask you to leave Cubert",
      "Can I leave Cubert",
      "leave cubert",
      "bye cubert",
      "dismiss cubert",
      "关闭小方",
      "让小方走"
    ],
    description: "Politely or firmly dismisses the Cubert assistant.",
    prerequisites: "Cubert assistant active",
    cost: "$0.00",
    status: "Working",
    control: "#btn-close-cubert",
    execute: () => dismissCubertByCommand()
  },
  {
    id: "cubert_tip",
    category: "10. Cubert commands",
    syntax: "Cubert Tip ($1, $5, $10, $0)",
    aliases: ["tip cubert", "$1", "$5", "$10", "$0", "tip $1", "tip $5", "tip $10", "tip $0"],
    description: "Submits a gratuity to Cubert, deducting from fictional credit balance. $0 deducts nothing; insufficient funds triggers indignant voice line.",
    prerequisites: "Cubert tip prompt active",
    cost: "$0.00 – $10.00",
    status: "Working",
    control: "#cubert-tip-row",
    execute: () => {
      showCubertPopup("So are you gonna tip me?", "helpful");
      status("Cubert tip buttons available in assistant dialog.");
      addLog("Cubert prompted for a tip ($1, $5, $10, $0).", "log-info");
    }
  },

  // 11. Localization commands
  {
    id: "chinese",
    category: "11. Localization commands",
    syntax: "Can I chinese",
    aliases: [
      "Can I chinese",
      "Can I zh",
      "Can I zh-hans",
      "Can I simplified chinese",
      "switch to chinese",
      "chinese",
      "切换中文",
      "中文"
    ],
    description: "Switches the entire user interface to Simplified Chinese, presents a 5-second spinning PRC flag celebration, and loops ChinaMusic.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => activateChineseMode({ celebrate: true })
  },
  {
    id: "english",
    category: "11. Localization commands",
    syntax: "Can I english",
    aliases: [
      "Can I english",
      "Can I unchinese",
      "Can I un-chinese",
      "Can I dechinese",
      "Can I de-chinese",
      "switch to english",
      "english",
      "unchinese",
      "dechinese",
      "切换英文",
      "英文"
    ],
    description: "Restores the original English interface, immediately stops ChinaMusic, and removes any active flag celebration.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => deactivateChineseMode()
  },

  // 12. Satirical/special commands
  {
    id: "antigravity",
    category: "12. Satirical/special commands",
    syntax: "Can I antigravity",
    aliases: [
      "Can I antigravity",
      "Can I remove gravity",
      "Can I anti-gravity",
      "Can I disable gravity",
      "Can I turn off gravity",
      "Can I no gravity",
      "Can I please antigravity",
      "Can I remove the gravity",
      "antigravity",
      "remove gravity",
      "anti-gravity",
      "no gravity",
      "disable gravity",
      "移除重力",
      "反重力"
    ],
    description: "Activates a non-destructive visual antigravity effect across all 4 viewports; geometry floats upward, accelerates away, and parks off-screen without geometry damage.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => activateAntigravity()
  },
  {
    id: "restore_gravity",
    category: "12. Satirical/special commands",
    syntax: "Can I restore gravity",
    aliases: [
      "Can I restore gravity",
      "Can I enable gravity",
      "Can I reset gravity",
      "Can I turn on gravity",
      "restore gravity",
      "enable gravity",
      "reset gravity",
      "turn on gravity",
      "恢复重力",
      "还原重力"
    ],
    description: "Stops active antigravity simulation and restores all objects to their exact original millimeter coordinates, preserving locks and layer states.",
    prerequisites: "Antigravity active",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => restoreGravity()
  },
  {
    id: "undo",
    category: "12. Satirical/special commands",
    syntax: "Can I undo",
    aliases: ["Can I undo", "undo", "撤销"],
    description: "Reverses the most recent undoable action (special priority: reverses Antigravity or Chinese mode if latest, or geometry operations normally).",
    prerequisites: "Action recorded on undo stack",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => executeUndo()
  },
  {
    id: "redo",
    category: "12. Satirical/special commands",
    syntax: "Can I redo",
    aliases: ["Can I redo", "redo", "重做"],
    description: "Reapplies the most recently undone action.",
    prerequisites: "Action recorded on redo stack",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => executeRedo()
  },
  {
    id: "crash",
    category: "12. Satirical/special commands",
    syntax: "Can I crash",
    aliases: ["Can I crash", "Can I send a crash report", "Can I send crash report", "crash", "crash report"],
    description: "Opens the authentic Windows 95 Unhandled Exception & Memory Dump modal.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => openCrashReportModal()
  },
  {
    id: "easter_eggs",
    category: "12. Satirical/special commands",
    syntax: "Numeric Easter Eggs (69, 420, 666, 1337)",
    aliases: ["69", "420", "666", "1337", "42", "007", "911", "404"],
    description: "Entering specific cultural numbers in coordinate inputs or Request Bar triggers humorous Cubert reactions and log commentaries.",
    prerequisites: "Input field or Request Bar",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    match: (raw, norm, withoutCanI) => {
      const q = withoutCanI || norm;
      const eggs = ["69", "420", "666", "1337", "42", "007", "911", "404"];
      if (eggs.includes(q)) return { args: [q] };
      return null;
    },
    execute: (args) => {
      const egg = args && args[0] ? args[0] : "69";
      checkNumericEasterEgg(egg);
    }
  },

  // 13. Debugging and development commands
  {
    id: "clear",
    category: "13. Debugging and development commands",
    syntax: "Can I clear",
    aliases: ["Can I clear", "clear"],
    description: "Clears the command history log buffer.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => {
      requestLogBox.innerHTML = "";
      addLog("Command log cleared.", "log-success");
      status("Command log cleared.");
    }
  },
  {
    id: "tutorial",
    category: "13. Debugging and development commands",
    syntax: "Can I tutorial",
    aliases: ["Can I tutorial", "tutorial"],
    description: "Displays the onboarding handbook window.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => {
      document.getElementById("modal-onboarding").showModal();
      showCubertPopup("How can I help you?", "cheerful");
      cubertConvStage = "AWAITING_DESCRIPTION";
      addLog("Onboarding handbook presented.", "log-success");
    }
  },
  {
    id: "theme",
    category: "13. Debugging and development commands",
    syntax: "Can I theme",
    aliases: ["Can I theme", "light", "dark", "theme light", "theme dark"],
    description: "Satirical theme switcher: permanently enforces the authentic retro Windows 95 theme.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Partially Working",
    control: "#request-input",
    execute: () => {
      status("Fixed Windows 95 theme active.");
      addLog("Theme switching is removed. The retro Windows 95 interface theme is permanent.", "log-system");
    }
  },
  {
    id: "mute",
    category: "13. Debugging and development commands",
    syntax: "Can I mute",
    aliases: ["Can I mute", "mute", "unmute"],
    description: "Toggles all background music, hold audio, and sound effects.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#tool-mute",
    execute: () => CADNT_AUDIO.setMute(!CADNT_AUDIO.mute)
  },
  {
    id: "ad",
    category: "13. Debugging and development commands",
    syntax: "Can I ad",
    aliases: ["Can I ad", "ad", "commercial"],
    description: "Forces an immediate unsolicited commercial break from the 18-advertisement shuffle bag.",
    prerequisites: "None",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => showAdPopup()
  },
  {
    id: "test_ads",
    category: "13. Debugging and development commands",
    syntax: "Can I test ads",
    aliases: ["Can I test ads", "test ads"],
    description: "Development test harness: verifies the 18-advertisement cycle without replacement, asset loading, and cycle boundary non-repetition.",
    prerequisites: "Development mode",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => {
      const res = runAdCycleTest();
      if (res.success) {
        addLog(`Ad test passed: All ${res.totalRegistered} ads cycled without repetition. No boundary repeat.`, "log-success");
        status(`Ad test PASSED: 18 unique ads verified.`);
      } else {
        addLog(`Ad test failed: ${res.error || "Cycle test assertion error"}`, "log-warn");
        status(`Ad test FAILED.`);
      }
    }
  },

  // 14. Coming Soon commands
  {
    id: "loft",
    category: "14. Coming Soon commands",
    syntax: "Can I loft",
    aliases: ["Can I loft", "loft"],
    description: "Skinning between two or more closed curves.",
    prerequisites: "Multiple closed planar curves",
    cost: "$0.00",
    status: "Coming Soon",
    control: "#request-input",
    execute: () => {
      addLog("Feature 'Can I loft' is currently in active development (Coming Soon).", "log-info");
      status("'Can I loft' is Coming Soon.");
    }
  },
  {
    id: "offset_surface",
    category: "14. Coming Soon commands",
    syntax: "Can I offset surface",
    aliases: ["Can I offset surface", "offset surface"],
    description: "Offsets a surface along its normal vector.",
    prerequisites: "Selected surface",
    cost: "$0.00",
    status: "Coming Soon",
    control: "#request-input",
    execute: () => {
      addLog("Feature 'Can I offset surface' is currently in active development (Coming Soon).", "log-info");
      status("'Can I offset surface' is Coming Soon.");
    }
  },
  {
    id: "shell",
    category: "14. Coming Soon commands",
    syntax: "Can I shell",
    aliases: ["Can I shell", "shell"],
    description: "Hollows out a solid model leaving a specified wall thickness.",
    prerequisites: "Selected solid mesh",
    cost: "$0.00",
    status: "Coming Soon",
    control: "#request-input",
    execute: () => {
      addLog("Feature 'Can I shell' is currently in active development (Coming Soon).", "log-info");
      status("'Can I shell' is Coming Soon.");
    }
  },
  {
    id: "draft_analysis",
    category: "14. Coming Soon commands",
    syntax: "Can I draft analysis",
    aliases: ["Can I draft analysis", "draft analysis"],
    description: "Calculates mold pull angles for injection molding feasibility.",
    prerequisites: "Selected solid part",
    cost: "$0.00",
    status: "Coming Soon",
    control: "#request-input",
    execute: () => {
      addLog("Feature 'Can I draft analysis' is currently in active development (Coming Soon).", "log-info");
      status("'Can I draft analysis' is Coming Soon.");
    }
  },
  {
    id: "generative_design",
    category: "14. Coming Soon commands",
    syntax: "Can I generative design",
    aliases: ["Can I generative design", "generative design"],
    description: "AI-driven topology optimization via distributed cloud solvers.",
    prerequisites: "Enterprise Cloud Subscription ($999/mo)",
    cost: "$999.00",
    status: "Coming Soon",
    control: "#request-input",
    execute: () => {
      addLog("Feature 'Can I generative design' is currently in active development (Coming Soon).", "log-info");
      status("'Can I generative design' is Coming Soon.");
    }
  },
  {
    id: "cloud_render",
    category: "14. Coming Soon commands",
    syntax: "Can I cloud render",
    aliases: ["Can I cloud render", "cloud render"],
    description: "Photorealistic ray-traced rendering on remote GPU cluster.",
    prerequisites: "Cloud render credits",
    cost: "$149.00",
    status: "Coming Soon",
    control: "#request-input",
    execute: () => {
      addLog("Feature 'Can I cloud render' is currently in active development (Coming Soon).", "log-info");
      status("'Can I cloud render' is Coming Soon.");
    }
  }
];

function findInCommandRegistry(rawInput) {
  if (!rawInput) return null;
  const trimmed = rawInput.trim();
  const norm = normalizeCommandText(trimmed);

  const matchCanI = trimmed.match(/^can\s+i\s+(.*)$/i);
  const withoutCanI = matchCanI ? normalizeCommandText(matchCanI[1]) : null;

  // 1. Custom matchers
  for (let i = 0; i < COMMAND_REGISTRY.length; i++) {
    const entry = COMMAND_REGISTRY[i];
    if (typeof entry.match === "function") {
      const customRes = entry.match(trimmed, norm, withoutCanI);
      if (customRes) return { command: entry, args: customRes.args || [] };
    }
  }

  // 2. Exact syntax / alias matches (full phrase, zero arguments)
  for (let i = 0; i < COMMAND_REGISTRY.length; i++) {
    const entry = COMMAND_REGISTRY[i];
    const allSyntaxes = [entry.syntax, ...(entry.aliases || [])];
    for (let j = 0; j < allSyntaxes.length; j++) {
      const s = allSyntaxes[j];
      const sNorm = normalizeCommandText(s);
      if (norm === sNorm) {
        return { command: entry, args: [] };
      }
      if (withoutCanI && normalizeCommandText(s.replace(/^can\s+i\s+/i, "")) === withoutCanI) {
        return { command: entry, args: [] };
      }
    }
  }

  // 3. Prefix matching for parameterized commands (e.g. "move 5 10 -5", "rotate y 90", "fillet 2 6", "chamfer 2 6", "asym fillet")
  const queryStr = withoutCanI !== null ? withoutCanI : norm;
  let bestMatch = null;
  let longestPrefixLen = -1;

  for (let i = 0; i < COMMAND_REGISTRY.length; i++) {
    const entry = COMMAND_REGISTRY[i];
    const allSyntaxes = [entry.syntax, ...(entry.aliases || [])];
    for (let j = 0; j < allSyntaxes.length; j++) {
      const s = allSyntaxes[j];
      const sStripped = normalizeCommandText(s.replace(/^can\s+i\s+/i, ""));
      if (!sStripped) continue;

      if (queryStr === sStripped) {
        return { command: entry, args: [] };
      } else if (queryStr.startsWith(sStripped + " ")) {
        if (sStripped.length > longestPrefixLen) {
          const rest = queryStr.slice(sStripped.length).trim();
          const args = rest ? rest.split(/\s+/) : [];
          bestMatch = { command: entry, args };
          longestPrefixLen = sStripped.length;
        }
      }
    }
  }

  return bestMatch;
}

function isRecognizedCadCommand(cmd) {
  if (!cmd) return false;
  return !!findInCommandRegistry(cmd) || isCubertDismissRequest(cmd) || isCubertSummonRequest(cmd);
}

function processRequest(raw) {
  const text = raw.trim();
  if (!text) return;

  requestLogBox.style.display = "block";
  addLog(`> ${text}`, "log-user");

  // Profanity check
  if (containsProfanity(text)) {
    showCubertPopup("Watch your fucking language.", "scolding");
    addLog("Cubert: 'Watch your fucking language.'", "log-nope");
    status("Cubert: 'Watch your fucking language.'");
    return;
  }

  // Cubert Dismiss Command: "Can you leave Cubert" (case-insensitive, optional punctuation & variations)
  if (isCubertDismissRequest(text)) {
    dismissCubertByCommand();
    return;
  }

  // Chinese language commands without prefix
  if (
    /^(?:切换|切换到|切换至|切换为)?英文[?！!。]*$/i.test(text) ||
    /^switch\s+to\s+english[?!.]*$/i.test(text) ||
    /^(?:un-?chinese|de-?chinese)[?!.]*$/i.test(text)
  ) {
    deactivateChineseMode();
    return;
  }
  if (/^(?:切换|切换到|切换至|切换为)?中文[?！!。]*$/i.test(text) || /^switch\s+to\s+chinese[?!.]*$/i.test(text)) {
    activateChineseMode({ celebrate: true });
    return;
  }

  // Antigravity Chinese aliases without prefix
  if (
    /^(?:移除|去除|取消|关掉)?重力[?！!。]*$/.test(text) ||
    /^(?:开启|激活)?反重力[?！!。]*$/.test(text)
  ) {
    activateAntigravity();
    return;
  }
  if (/^(?:恢复|还原|重置)?重力[?！!。]*$/.test(text)) {
    restoreGravity();
    return;
  }

  // Check prefix 'Can I ' (case-insensitive)
  const match = text.match(/^can\s+i\s+(.*)$/i);
  if (!match) {
    // If not polite prefix, but it's an unrecognized command, still say Nope
    addLog("Nope.", "log-nope");
    status("Nope. Request lacked polite prefix.");
    shakeRequestBar();
    cubertConsecutiveFailures++;
    if (cubertConsecutiveFailures >= 2) {
      showCubertPopup("How can I help you?", "cheerful");
      cubertConvStage = "AWAITING_DESCRIPTION";
      status("Cubert: 'How can I help you?'");
      addLog("Cubert triggered by consecutive command failures.", "log-info");
    }
    return;
  }

  const query = match[1].trim();
  const normalizedQuery = query.replace(/[?!.,;]+$/, "").trim().toLowerCase();

  // Check in unified COMMAND_REGISTRY
  const found = findInCommandRegistry(text);
  if (found) {
    if (cubertMode === CUBERT_MODES.ACTIVE) {
      hideCubertPopup();
    }
    cubertConsecutiveFailures = 0;
    found.command.execute(found.args, text);
    return;
  }

  // Manual Cubert summon triggers
  if (isCubertSummonRequest(query)) {
    cubertConsecutiveFailures = 0;
    showCubertPopup("How can I help you?", "cheerful");
    cubertConvStage = "AWAITING_DESCRIPTION";
    status("Cubert: 'How can I help you?'");
    addLog("Cubert summoned.", "log-info");
    return;
  }

  // Fallback to executeCommand for any edge-cases
  executeCommand(query);
}

function executeCommand(rawCmd) {
  const trimmed = rawCmd.trim();
  const normalized = normalizeCommandText(trimmed);

  // Check in unified registry with or without 'can i '
  const found = findInCommandRegistry(trimmed) || findInCommandRegistry("can i " + trimmed);
  if (found) {
    found.command.execute(found.args, rawCmd);
    return;
  }

  const tokens = trimmed.split(/\\s+/);
  const verb = tokens[0].toLowerCase();
  const args = tokens.slice(1);

  if (isCubertDismissRequest(rawCmd) || isCubertDismissRequest(normalized)) {
    dismissCubertByCommand();
    return;
  }

  if (isRecognizedCadCommand(rawCmd)) {
    cubertConsecutiveFailures = 0;
  }

  // Numeric Easter Egg check
  if (Array.isArray(tokens)) {
    tokens.forEach(t => checkNumericEasterEgg(t));
  }

  // Crash report command
  if (normalized === "send a crash report" || normalized === "send crash report" || normalized === "crash report") {
    openCrashReportModal();
    return;
  }

  // Gumball command
  if (normalized === "gumball" || normalized === "please gumball" || normalized === "gumball please") {
    if (selectedObjects.length === 0) {
      addLog("Gumball requested, but no object is selected. Select an object first.", "log-warn");
      status("Select an object to display Gumball.");
      isGumballActive = false;
      updateGumball();
      return;
    }
    isGumballActive = true;
    updateGumball();
    addLog("Gumball activated.", "log-success");
    status("Gumball activated on selected object.");
    return;
  }

  // Michigan deletion commands
  if (
    normalized === "remove starting object" ||
    normalized === "delete michigan" ||
    normalized === "remove michigan" ||
    normalized === "delete starting object"
  ) {
    const targetObj = sceneObjects.find(o => o.userData && o.userData.id === "starting_michigan")
      || sceneObjects.find(o => o.userData && o.userData.isStartingObject)
      || michiganModel
      || diagnosticCube;

    if (!targetObj || !sceneObjects.includes(targetObj)) {
      addLog("Starting object is already gone.", "log-warn");
      status("Starting object does not exist.");
      return;
    }
    showConfirmModal(
      "Are you sure you want to remove this?",
      "Are you sure you want to remove this?",
      () => {
        recordUndoState("Remove Starting Object");
        scene.remove(targetObj);
        const idx = sceneObjects.indexOf(targetObj);
        if (idx !== -1) sceneObjects.splice(idx, 1);
        selectedObjects = selectedObjects.filter(o => o !== targetObj);
        if (targetObj === michiganModel) michiganModel = null;
        if (targetObj === diagnosticCube) diagnosticCube = null;
        updateGumball();
        updateObjectsTree();
        updatePropertiesPanel();
        addLog("Starting object removed. You can restore it using 'Can I undo'.", "log-success");
        status("Starting object removed.");
        recordModelingCommand();
        renderAllViewports();
      }
    );
    return;
  }

  // Legacy fallback switch
  switch (verb) {
    case "box": createBoxPrimitive(); break;
    case "sphere": createSpherePrimitive(); break;
    case "cylinder": case "cyl": createCylinderPrimitive(); break;
    case "cone": createConePrimitive(); break;
    case "line": case "polyline": startSketch("line"); break;
    case "rect": case "rectangle": startSketch("rect"); break;
    case "circle": startSketch("circle"); break;
    case "spline": startSketch("spline"); break;
    case "polygon": case "poly": case "ngon": startSketch("polygon", args[0] ? parseInt(args[0], 10) : 6); break;
    case "lock": handleLockCommand(); break;
    case "unlock": handleUnlockCommand(); break;
    case "delete": case "remove": handleDelete(); break;
    case "undo": executeUndo(); break;
    case "redo": executeRedo(); break;
    case "save": saveProjectToFile(); break;
    case "open": openProjectFromFile(); break;
    case "export": exportProjectGeometry(args[0] || "stl"); break;
    case "import": importProjectGeometry(); break;
    case "remesh": case "simplify": remeshSelectedObject(); break;
    case "extrude":
      if (args.length >= 1 && selectedObjects.some(o => o.userData && o.userData.closed && o.userData.shape)) {
        const depth = parseFloat(args[0]);
        extrudeSelectedProfile(isNaN(depth) ? 10 : depth);
      } else {
        const depth = args[0] ? parseFloat(args[0]) : undefined;
        startModelingCommand("extrude", { depth: isNaN(depth) ? undefined : depth });
      }
      break;
    case "union": startModelingCommand("union"); break;
    case "difference": case "diff": case "subtract": startModelingCommand("difference"); break;
    case "move":
      if (args.length >= 1 && selectedObjects.length > 0) {
        const dx = parseFloat(args[0]) || 0;
        const dy = args[1] !== undefined ? (parseFloat(args[1]) || 0) : 0;
        const dz = args[2] !== undefined ? (parseFloat(args[2]) || 0) : 0;
        transformSelected("move", { dx, dy, dz });
      } else {
        const dx = args[0] !== undefined ? parseFloat(args[0]) : undefined;
        const dy = args[1] !== undefined ? parseFloat(args[1]) : undefined;
        const dz = args[2] !== undefined ? parseFloat(args[2]) : undefined;
        startModelingCommand("move", { dx, dy, dz });
      }
      break;
    case "rotate":
      let rAxis = "y";
      let rDeg = 45;
      if (args.length === 1) {
        if (isNaN(args[0])) rAxis = args[0];
        else rDeg = parseFloat(args[0]);
      } else if (args.length >= 2) {
        rAxis = args[0];
        rDeg = parseFloat(args[1]) || 45;
      }
      if (args.length >= 1 && selectedObjects.length > 0) {
        transformSelected("rotate", { axis: rAxis, deg: rDeg });
      } else {
        startModelingCommand("rotate", { axis: rAxis, deg: rDeg });
      }
      break;
    case "scale":
      const s = args[0] !== undefined ? parseFloat(args[0]) : 1.5;
      const sy = args[1] !== undefined ? parseFloat(args[1]) : s;
      const sz = args[2] !== undefined ? parseFloat(args[2]) : s;
      if (args.length >= 1 && selectedObjects.length > 0) {
        transformSelected("scale", { sx: isNaN(s) ? 1.5 : s, sy: isNaN(sy) ? s : sy, sz: isNaN(sz) ? s : sz });
      } else {
        startModelingCommand("scale", { factor: isNaN(s) ? 1.5 : s });
      }
      break;
    case "join": startModelingCommand("join"); break;
    case "fillet":
      if (args.length >= 2 && !isNaN(parseFloat(args[0])) && !isNaN(parseFloat(args[1]))) {
        startModelingCommand("fillet", { val1: parseFloat(args[0]), val2: parseFloat(args[1]), isAsymmetric: true });
      } else {
        startModelingCommand("fillet", args.length >= 1 && !isNaN(parseFloat(args[0])) ? { val: parseFloat(args[0]) } : {});
      }
      break;
    case "chamfer":
      if (args.length >= 2 && !isNaN(parseFloat(args[0])) && !isNaN(parseFloat(args[1]))) {
        startModelingCommand("chamfer", { val1: parseFloat(args[0]), val2: parseFloat(args[1]), isAsymmetric: true });
      } else {
        startModelingCommand("chamfer", args.length >= 1 && !isNaN(parseFloat(args[0])) ? { val: parseFloat(args[0]) } : {});
      }
      break;
    case "asym": case "asymmetric":
      if (args[0] === "fillet" || args[0] === "chamfer") {
        const subMode = args[0];
        const v1 = args[1] && !isNaN(parseFloat(args[1])) ? parseFloat(args[1]) : (subMode === "fillet" ? 2.5 : 2.0);
        const v2 = args[2] && !isNaN(parseFloat(args[2])) ? parseFloat(args[2]) : v1 * 2;
        startModelingCommand(subMode, { val1: v1, val2: v2, isAsymmetric: true });
      } else {
        status("Specify 'asym fillet' or 'asym chamfer'.");
      }
      break;
    case "pipe": startModelingCommand("pipe"); break;
    case "sweep": attemptPaidOperation("sweep", 49.00); break;
    case "theme": case "light": case "dark":
      status("Fixed Windows 95 theme active.");
      addLog("Theme switching is removed. The retro Windows 95 interface theme is permanent.", "log-system");
      break;
    case "mute": CADNT_AUDIO.setMute(!CADNT_AUDIO.mute); break;
    case "ad": showAdPopup(); break;
    case "help": openHelpWindow(); addLog("Help index presented.", "log-success"); break;
    case "tutorial":
      document.getElementById("modal-onboarding").showModal();
      showCubertPopup("How can I help you?", "cheerful");
      cubertConvStage = "AWAITING_DESCRIPTION";
      addLog("Onboarding handbook presented.", "log-success");
      break;
    case "clear":
      requestLogBox.innerHTML = "";
      addLog("Command log cleared.", "log-success");
      break;
    default:
      addLog(`Request refused: Unknown operation '${trimmed}'.`, "log-nope");
      status(`Unknown operation '${trimmed}'`);
      shakeRequestBar();
      cubertConsecutiveFailures++;
      if (cubertConsecutiveFailures >= 2) {
        cubertConsecutiveFailures = 0;
        showCubertPopup("How can I help you?", "cheerful");
        cubertConvStage = "AWAITING_DESCRIPTION";
        status("Cubert: 'How can I help you?'");
        addLog("Cubert triggered by consecutive command failures.", "log-info");
      }
      break;
  }
}
"""

with open("scratch/command_registry_snippet.js", "w") as f:
    f.write(js_code)
print("Saved scratch/command_registry_snippet.js successfully. Length:", len(js_code))
