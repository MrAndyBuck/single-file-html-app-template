#!/usr/bin/env python3
"""
Patches generate_command_registry_js.py and index.html to ensure:
1. findInCommandRegistry parses prefix commands with arguments (e.g. Can I move 5 10 -5, Can I fillet 2 6, etc.)
2. COMMAND_REGISTRY entry execution functions forward arguments properly:
   - line: supports 1 arg (length), 4 args (2D coords), 6 args (3D coords), or comma pairs
   - extrude: supports depth argument
   - fillet: supports (val1, val2) for asymmetric fillet, or (val)
   - chamfer: supports (val1, val2) for asymmetric chamfer, or (val)
   - asym: supports 'fillet' or 'chamfer' submode with optional v1, v2
   - move: supports dx, dy, dz with transformSelected
   - rotate: supports axis and deg with transformSelected
   - scale: supports s, sy, sz or factor with transformSelected
   - export: supports 'distorted' and format
3. Updates the fallback switch in executeCommand to match.
4. Regenerates scratch/command_registry_snippet.js and applies to index.html.
"""

import os, re, sys

gen_path = "scripts/generate_command_registry_js.py"
with open(gen_path, "r", encoding="utf-8") as f:
    gen_text = f.read()

# 1. Update line execute
old_line = """  {
    id: "line",
    category: "2. Sketching and curves",
    syntax: "Can I line",
    aliases: ["Can I line", "Can I polyline", "line", "polyline"],
    description: "Enters interactive 2D sketching mode to draw linear vector segments on the construction plane.",
    prerequisites: "Active construction plane",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => startSketch("line")
  },"""

new_line = """  {
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
  },"""

# 2. Update extrude execute
old_extrude = """  {
    id: "extrude",
    category: "3. Extrusion and surface operations",
    syntax: "Can I extrude",
    aliases: ["Can I extrude", "extrude"],
    description: "Extrudes a planar 2D curve or polygon into a watertight 3D solid mesh.",
    prerequisites: "Selected 2D sketch curve",
    cost: "$0.00",
    status: "Working",
    control: "#request-input",
    execute: () => startModelingCommand("extrude")
  },"""

new_extrude = """  {
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
  },"""

# 3. Update fillet, chamfer, asym
old_fillet_chamfer_asym = """  // 5. Fillet, chamfer, and edge modification
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
    execute: () => startModelingCommand("fillet")
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
    execute: () => startModelingCommand("chamfer")
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
    execute: () => startModelingCommand("asym")
  },"""

new_fillet_chamfer_asym = """  // 5. Fillet, chamfer, and edge modification
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
  },"""

# 4. Update move, rotate, scale
old_move_rot_scale = """  // 6. Moving and transforming
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
    execute: () => startModelingCommand("move")
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
    execute: () => startModelingCommand("rotate")
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
    execute: () => startModelingCommand("scale")
  },"""

new_move_rot_scale = """  // 6. Moving and transforming
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
  },"""

# 5. Update findInCommandRegistry
old_find = """function findInCommandRegistry(rawInput) {
  if (!rawInput) return null;
  const trimmed = rawInput.trim();
  const norm = normalizeCommandText(trimmed);

  const matchCanI = trimmed.match(/^can\\s+i\\s+(.*)$/i);
  const withoutCanI = matchCanI ? normalizeCommandText(matchCanI[1]) : null;

  for (let i = 0; i < COMMAND_REGISTRY.length; i++) {
    const entry = COMMAND_REGISTRY[i];

    // 1. Custom matcher if defined
    if (typeof entry.match === "function") {
      const customRes = entry.match(trimmed, norm, withoutCanI);
      if (customRes) return { command: entry, args: customRes.args || [] };
    }

    // 2. Direct syntax / alias matches
    const allSyntaxes = [entry.syntax, ...(entry.aliases || [])];
    for (let j = 0; j < allSyntaxes.length; j++) {
      const s = allSyntaxes[j];
      const sNorm = normalizeCommandText(s);
      if (norm === sNorm) {
        return { command: entry, args: [] };
      }
      if (withoutCanI && normalizeCommandText(s.replace(/^can\\s+i\\s+/i, "")) === withoutCanI) {
        return { command: entry, args: [] };
      }
    }
  }
  return null;
}"""

new_find = """function findInCommandRegistry(rawInput) {
  if (!rawInput) return null;
  const trimmed = rawInput.trim();
  const norm = normalizeCommandText(trimmed);

  const matchCanI = trimmed.match(/^can\\s+i\\s+(.*)$/i);
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
      if (withoutCanI && normalizeCommandText(s.replace(/^can\\s+i\\s+/i, "")) === withoutCanI) {
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
      const sStripped = normalizeCommandText(s.replace(/^can\\s+i\\s+/i, ""));
      if (!sStripped) continue;

      if (queryStr === sStripped) {
        return { command: entry, args: [] };
      } else if (queryStr.startsWith(sStripped + " ")) {
        if (sStripped.length > longestPrefixLen) {
          const rest = queryStr.slice(sStripped.length).trim();
          const args = rest ? rest.split(/\\s+/) : [];
          bestMatch = { command: entry, args };
          longestPrefixLen = sStripped.length;
        }
      }
    }
  }

  return bestMatch;
}"""

# 6. Update fallback switch in executeCommand
old_switch = """    case "extrude": startModelingCommand("extrude"); break;
    case "union": startModelingCommand("union"); break;
    case "difference": case "diff": case "subtract": startModelingCommand("difference"); break;
    case "move": startModelingCommand("move"); break;
    case "rotate": startModelingCommand("rotate"); break;
    case "scale": startModelingCommand("scale"); break;
    case "join": startModelingCommand("join"); break;
    case "chamfer": startModelingCommand("chamfer"); break;
    case "fillet": startModelingCommand("fillet"); break;
    case "asym": case "asymmetric": startModelingCommand("asym"); break;"""

new_switch = """    case "extrude":
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
      break;"""

# Replace in gen_text
replacements = [
    (old_line, new_line, "line"),
    (old_extrude, new_extrude, "extrude"),
    (old_fillet_chamfer_asym, new_fillet_chamfer_asym, "fillet_chamfer_asym"),
    (old_move_rot_scale, new_move_rot_scale, "move_rot_scale"),
    (old_find, new_find, "findInCommandRegistry"),
    (old_switch, new_switch, "fallback_switch")
]

for old, new, label in replacements:
    if old not in gen_text:
        print(f"FAILED to find {label} in {gen_path}")
        sys.exit(1)
    gen_text = gen_text.replace(old, new)
    print(f"Replaced {label} successfully.")

with open(gen_path, "w", encoding="utf-8") as f:
    f.write(gen_text)
print("Updated generate_command_registry_js.py successfully.")

# Execute generate_command_registry_js.py to create scratch/command_registry_snippet.js
os.system("python3 scripts/generate_command_registry_js.py")

with open("scratch/command_registry_snippet.js", "r", encoding="utf-8") as f:
    snippet = f.read()

# Splice into index.html
with open("index.html", "r", encoding="utf-8") as f:
    html_text = f.read()

m1 = "/* =========================================================================\n   COMMAND REGISTRY & CANONICAL DISPATCHER"
m2 = "function handleDelete() {"

idx1 = html_text.find(m1)
idx2 = html_text.find(m2)

if idx1 == -1 or idx2 == -1:
    print(f"Markers not found in index.html! ({idx1}, {idx2})")
    sys.exit(1)

html_text = html_text[:idx1] + snippet + "\n\n" + html_text[idx2:]
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_text)

print("Spliced updated snippet into index.html successfully.")
