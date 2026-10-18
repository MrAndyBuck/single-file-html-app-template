#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, shutil

SS_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app/screenshots"
ART_DIR = "/Users/andybuck/.gemini/antigravity-cli/brain/706b2fcb-0d73-41fc-9916-c493cfe958dc"
os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9308

print(f"Launching Chrome on port {PORT} for Geometry Verification...")
proc = subprocess.Popen([
    CHROME_BIN,
    "--headless=new",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--window-size=1440,900",
    f"--remote-debugging-port={PORT}",
    "file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1"
])
time.sleep(2.5)

try:
    tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json").read().decode("utf-8"))
    target = next(t for t in tabs if t.get("type") == "page")
    ws_url = target["webSocketDebuggerUrl"]
    host, port, path = "127.0.0.1", PORT, ws_url.split(f"127.0.0.1:{PORT}")[1]

    s = socket.socket()
    s.connect((host, port))
    key = base64.b64encode(b"0123456789abcdef").decode()
    req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    s.sendall(req.encode())
    s.recv(4096)

    cmd_counter = 1
    def send_cmd(method, params=None):
        global cmd_counter
        cid = cmd_counter
        cmd_counter += 1
        msg = {"id": cid, "method": method}
        if params: msg["params"] = params
        data = json.dumps(msg).encode("utf-8")
        frame = bytearray([0x81])
        length = len(data)
        mask_key = b"\x11\x22\x33\x44"
        if length < 126:
            frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", length))
        frame.extend(mask_key)
        frame.extend(bytearray(b ^ mask_key[i % 4] for i, b in enumerate(data)))
        s.sendall(frame)
        return cid

    def recv_msg(target_id):
        while True:
            header = s.recv(2)
            if not header: return None
            length = header[1] & 0x7f
            if length == 126:
                length = struct.unpack(">H", s.recv(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", s.recv(8))[0]
            payload = b""
            while len(payload) < length:
                payload += s.recv(length - len(payload))
            msg = json.loads(payload.decode("utf-8", errors="ignore"))
            if msg.get("id") == target_id:
                return msg

    def eval_js(js):
        cid = send_cmd("Runtime.evaluate", {"expression": js, "returnByValue": True})
        res = recv_msg(cid)
        if "result" in res and "result" in res["result"]:
            val = res["result"]["result"].get("value")
            if val is not None:
                return val
            if "description" in res["result"]["result"]:
                return res["result"]["result"]["description"]
        return str(res)

    def get_element_clip(elem_id):
        js = f"""
        (() => {{
          const el = document.getElementById("{elem_id}");
          if (!el) return null;
          const r = el.getBoundingClientRect();
          return JSON.stringify({{ x: Math.round(r.left), y: Math.round(r.top), width: Math.round(r.width), height: Math.round(r.height), scale: 1 }});
        }})()
        """
        raw = eval_js(js)
        if isinstance(raw, str):
            return json.loads(raw)
        return raw

    def capture_screenshot(filename, clip=None):
        params = {"format": "png"}
        if clip:
            if isinstance(clip, str):
                clip = json.loads(clip)
            clip_param = dict(clip)
            clip_param["scale"] = 1
            params["clip"] = clip_param
        cid = send_cmd("Page.captureScreenshot", params)
        res = recv_msg(cid)
        img_bytes = base64.b64decode(res["result"]["data"])
        p1 = os.path.join(SS_DIR, filename)
        p2 = os.path.join(ART_DIR, filename)
        with open(p1, "wb") as f: f.write(img_bytes)
        with open(p2, "wb") as f: f.write(img_bytes)
        print(f"Captured {filename} ({len(img_bytes)} bytes)")
        return p1

    captured_files = []

    # Hide debug overlay HUD during captures so viewports are unobstructed
    eval_js("""
    (() => {
      const hud = document.getElementById("debug-overlay");
      if (hud) hud.style.display = "none";
    })()
    """)

    # 1. TEST CASE 1: FILLET (2.0mm on 1 edge of 20x20x20 box, side-by-side with original)
    print("\n=== SETTING UP TEST CASE 1: FILLET 2.0MM SIDE-BY-SIDE (20x20x20 BOXES) ===")
    setup_fillet_js = """
    (() => {
      window.IS_TESTING = true;
      while(sceneObjects.length > 0) {
        const o = sceneObjects.pop();
        scene.remove(o);
      }
      creditBalance = 500.0;
      updateEconomyDisplay();

      // Box 1: Original reference solid (Left, X = -22)
      createBoxPrimitive();
      const origBox = sceneObjects[sceneObjects.length - 1];
      origBox.name = "Original_Box_20mm";
      origBox.geometry.dispose();
      origBox.geometry = new THREE.BoxGeometry(20, 20, 20);
      origBox.position.set(-22, 10, 0);
      origBox.material = new THREE.MeshStandardMaterial({ color: 0x8298a8, roughness: 0.35, metalness: 0.15 });
      origBox.updateMatrix();
      origBox.updateMatrixWorld(true);

      const origEdges = new THREE.LineSegments(
        new THREE.EdgesGeometry(origBox.geometry, 15),
        new THREE.LineBasicMaterial({ color: 0x111111, linewidth: 2 })
      );
      origBox.add(origEdges);

      // Box 2: Target for Fillet (Right, X = +22)
      createBoxPrimitive();
      const filletBox = sceneObjects[sceneObjects.length - 1];
      filletBox.name = "Filleted_Box_2mm";
      filletBox.geometry.dispose();
      filletBox.geometry = new THREE.BoxGeometry(20, 20, 20);
      filletBox.position.set(22, 10, 0);
      filletBox.material = new THREE.MeshStandardMaterial({ color: 0x8298a8, roughness: 0.35, metalness: 0.15 });
      filletBox.updateMatrix();
      filletBox.updateMatrixWorld(true);

      // Start Fillet command, select Edge 0 (+X, +Z corner vertical edge)
      selectObject(filletBox);
      startModelingCommand("fillet", { val: 2.0 });
      activeCommand.toggleEdge(0);

      // Apply 2.0mm Fillet
      activeCommand.confirm();

      const filletedSolid = selectedObjects[0];
      const filletedWire = new THREE.LineSegments(
        new THREE.EdgesGeometry(filletedSolid.geometry, 5),
        new THREE.LineBasicMaterial({ color: 0x111111, linewidth: 2 })
      );
      filletedSolid.add(filletedWire);

      selectedObjects = [];
      updateObjectsTree();
      updatePropertiesPanel();
      renderAllViewports();

      return {
        origName: origBox.name,
        filletName: filletedSolid.name,
        filletType: filletedSolid.userData.type
      };
    })()
    """
    res1 = eval_js(setup_fillet_js)
    print("Fillet setup result:", res1)
    time.sleep(1.0)

    # Topological & Geometric Telemetry for Fillet
    telemetry_fillet_js = """
    (() => {
      const origBox = sceneObjects.find(o => o.name === "Original_Box_20mm");
      const filletBox = sceneObjects.find(o => o.name.startsWith("Fillet_"));

      function getMeshDetails(geo) {
        const pos = geo.attributes.position;
        const index = geo.index;
        geo.computeBoundingBox();
        const bbox = geo.boundingBox;
        const eps = 1e-4;

        const uVerts = [];
        const vmap = [];
        for (let i = 0; i < pos.count; i++) {
          const vx = pos.getX(i), vy = pos.getY(i), vz = pos.getZ(i);
          let f = -1;
          for (let j = 0; j < uVerts.length; j++) {
            if (Math.abs(uVerts[j].x - vx) < eps && Math.abs(uVerts[j].y - vy) < eps && Math.abs(uVerts[j].z - vz) < eps) {
              f = j; break;
            }
          }
          if (f === -1) {
            f = uVerts.length;
            uVerts.push({ x: vx, y: vy, z: vz });
          }
          vmap.push(f);
        }

        const edgeMap = new Map();
        const count = index ? index.count : pos.count;
        for (let i = 0; i < count; i += 3) {
          const i0 = index ? index.getX(i) : i;
          const i1 = index ? index.getX(i+1) : i+1;
          const i2 = index ? index.getX(i+2) : i+2;
          const v0 = vmap[i0], v1 = vmap[i1], v2 = vmap[i2];
          const e1 = v0 < v1 ? `${v0}_${v1}` : `${v1}_${v0}`;
          const e2 = v1 < v2 ? `${v1}_${v2}` : `${v2}_${v1}`;
          const e3 = v2 < v0 ? `${v2}_${v0}` : `${v0}_${v2}`;
          edgeMap.set(e1, (edgeMap.get(e1) || 0) + 1);
          edgeMap.set(e2, (edgeMap.get(e2) || 0) + 1);
          edgeMap.set(e3, (edgeMap.get(e3) || 0) + 1);
        }

        let open = 0, nonM = 0, manifold = 0;
        for (const [k, c] of edgeMap.entries()) {
          if (c === 2) manifold++;
          else if (c === 1) open++;
          else nonM++;
        }

        const V = uVerts.length;
        const E = edgeMap.size;
        const F = count / 3;
        const chi = V - E + F;

        // Check arc vertices (along the +X, +Z corner)
        // Center of arc is (10 - 2, 10 - 2) = (8, 8)
        const arcVerts = uVerts.filter(v => v.x >= 7.99 && v.z >= 7.99 && (v.x < 9.99 || v.z < 9.99));
        const arcRadii = arcVerts.map(v => Math.hypot(v.x - 8.0, v.z - 8.0));
        const minRadius = arcRadii.length > 0 ? Math.min(...arcRadii) : 0;
        const maxRadius = arcRadii.length > 0 ? Math.max(...arcRadii) : 0;

        return {
          triangles: F,
          uniqueVertices: V,
          totalEdges: E,
          manifoldEdges: manifold,
          openEdges: open,
          nonManifoldEdges: nonM,
          eulerCharacteristic: chi,
          isWatertight: open === 0,
          isManifold: open === 0 && nonM === 0,
          bbox: {
            min: { x: bbox.min.x, y: bbox.min.y, z: bbox.min.z },
            max: { x: bbox.max.x, y: bbox.max.y, z: bbox.max.z }
          },
          arcSampleCount: arcVerts.length,
          measuredRadiusMin: minRadius,
          measuredRadiusMax: maxRadius
        };
      }

      return {
        original: getMeshDetails(origBox.geometry),
        fillet: getMeshDetails(filletBox.geometry)
      };
    })()
    """
    telemetry_fillet = eval_js(telemetry_fillet_js)
    print("Fillet Mesh Telemetry:", json.dumps(telemetry_fillet, indent=2))

    # Angle 1: 4-Viewport Overview Side-by-Side (shows Top, Front, Right, and Persp simultaneously)
    eval_js("renderAllViewports()")
    f1 = capture_screenshot("geom_01_fillet_4viewports_side_by_side.png")
    captured_files.append(f1)

    # Angle 2: Perspective Viewport Close-Up (Top-Right viewport: vp-perspective)
    clip_persp = get_element_clip("vp-perspective")
    eval_js("""
    (() => {
      const cam = cameras["persp"];
      cam.position.set(24, 28, 44);
      cam.lookAt(0, 10, 0);
      cam.updateProjectionMatrix();
      renderAllViewports();
      return true;
    })()
    """)
    f2 = capture_screenshot("geom_02_fillet_perspective_closeup_side_by_side.png", clip=clip_persp)
    captured_files.append(f2)

    # Angle 3: Top Viewport Close-Up (Top-Left viewport: vp-top)
    clip_top = get_element_clip("vp-top")
    eval_js("""
    (() => {
      const cam = cameras["top"];
      cam.position.set(0, 100, 0);
      cam.zoom = 2.0;
      cam.updateProjectionMatrix();
      renderAllViewports();
      return true;
    })()
    """)
    f3 = capture_screenshot("geom_03_fillet_top_view_corner_contour.png", clip=clip_top)
    captured_files.append(f3)

    # Angle 4: Right Viewport Close-Up (Bottom-Right viewport: vp-right)
    clip_right = get_element_clip("vp-right")
    eval_js("""
    (() => {
      const cam = cameras["right"];
      cam.position.set(100, 10, 0);
      cam.zoom = 2.0;
      cam.updateProjectionMatrix();
      renderAllViewports();
      return true;
    })()
    """)
    f4 = capture_screenshot("geom_04_fillet_right_view_unaffected_profile.png", clip=clip_right)
    captured_files.append(f4)


    # 2. TEST CASE 2: CHAMFER (2.0mm on 1 edge of 20x20x20 box, side-by-side with original)
    print("\n=== SETTING UP TEST CASE 2: CHAMFER 2.0MM SIDE-BY-SIDE (20x20x20 BOXES) ===")
    setup_chamfer_js = """
    (() => {
      window.IS_TESTING = true;
      while(sceneObjects.length > 0) {
        const o = sceneObjects.pop();
        scene.remove(o);
      }
      creditBalance = 500.0;
      updateEconomyDisplay();

      // Box 1: Original reference solid (Left, X = -22)
      createBoxPrimitive();
      const origBox = sceneObjects[sceneObjects.length - 1];
      origBox.name = "Original_Box_20mm";
      origBox.geometry.dispose();
      origBox.geometry = new THREE.BoxGeometry(20, 20, 20);
      origBox.position.set(-22, 10, 0);
      origBox.material = new THREE.MeshStandardMaterial({ color: 0x8298a8, roughness: 0.35, metalness: 0.15 });
      origBox.updateMatrix();
      origBox.updateMatrixWorld(true);

      const origEdges = new THREE.LineSegments(
        new THREE.EdgesGeometry(origBox.geometry, 15),
        new THREE.LineBasicMaterial({ color: 0x111111, linewidth: 2 })
      );
      origBox.add(origEdges);

      // Box 2: Target for Chamfer (Right, X = +22)
      createBoxPrimitive();
      const chamferBox = sceneObjects[sceneObjects.length - 1];
      chamferBox.name = "Chamfered_Box_2mm";
      chamferBox.geometry.dispose();
      chamferBox.geometry = new THREE.BoxGeometry(20, 20, 20);
      chamferBox.position.set(22, 10, 0);
      chamferBox.material = new THREE.MeshStandardMaterial({ color: 0x8298a8, roughness: 0.35, metalness: 0.15 });
      chamferBox.updateMatrix();
      chamferBox.updateMatrixWorld(true);

      // Start Chamfer command, select Edge 0 (+X, +Z corner vertical edge)
      selectObject(chamferBox);
      startModelingCommand("chamfer", { val: 2.0 });
      activeCommand.toggleEdge(0);

      // Apply 2.0mm Chamfer
      activeCommand.confirm();

      const chamferedSolid = selectedObjects[0];
      const chamferedWire = new THREE.LineSegments(
        new THREE.EdgesGeometry(chamferedSolid.geometry, 10),
        new THREE.LineBasicMaterial({ color: 0x111111, linewidth: 2 })
      );
      chamferedSolid.add(chamferedWire);

      selectedObjects = [];
      updateObjectsTree();
      updatePropertiesPanel();
      renderAllViewports();

      return {
        origName: origBox.name,
        chamferName: chamferedSolid.name,
        chamferType: chamferedSolid.userData.type
      };
    })()
    """
    res2 = eval_js(setup_chamfer_js)
    print("Chamfer setup result:", res2)
    time.sleep(1.0)

    # Topological & Geometric Telemetry for Chamfer
    telemetry_chamfer_js = """
    (() => {
      const origBox = sceneObjects.find(o => o.name === "Original_Box_20mm");
      const chamferBox = sceneObjects.find(o => o.name.startsWith("Chamfer_"));

      function getMeshDetails(geo) {
        const pos = geo.attributes.position;
        const index = geo.index;
        geo.computeBoundingBox();
        const bbox = geo.boundingBox;
        const eps = 1e-4;

        const uVerts = [];
        const vmap = [];
        for (let i = 0; i < pos.count; i++) {
          const vx = pos.getX(i), vy = pos.getY(i), vz = pos.getZ(i);
          let f = -1;
          for (let j = 0; j < uVerts.length; j++) {
            if (Math.abs(uVerts[j].x - vx) < eps && Math.abs(uVerts[j].y - vy) < eps && Math.abs(uVerts[j].z - vz) < eps) {
              f = j; break;
            }
          }
          if (f === -1) {
            f = uVerts.length;
            uVerts.push({ x: vx, y: vy, z: vz });
          }
          vmap.push(f);
        }

        const edgeMap = new Map();
        const count = index ? index.count : pos.count;
        for (let i = 0; i < count; i += 3) {
          const i0 = index ? index.getX(i) : i;
          const i1 = index ? index.getX(i+1) : i+1;
          const i2 = index ? index.getX(i+2) : i+2;
          const v0 = vmap[i0], v1 = vmap[i1], v2 = vmap[i2];
          const e1 = v0 < v1 ? `${v0}_${v1}` : `${v1}_${v0}`;
          const e2 = v1 < v2 ? `${v1}_${v2}` : `${v2}_${v1}`;
          const e3 = v2 < v0 ? `${v2}_${v0}` : `${v0}_${v2}`;
          edgeMap.set(e1, (edgeMap.get(e1) || 0) + 1);
          edgeMap.set(e2, (edgeMap.get(e2) || 0) + 1);
          edgeMap.set(e3, (edgeMap.get(e3) || 0) + 1);
        }

        let open = 0, nonM = 0, manifold = 0;
        for (const [k, c] of edgeMap.entries()) {
          if (c === 2) manifold++;
          else if (c === 1) open++;
          else nonM++;
        }

        const V = uVerts.length;
        const E = edgeMap.size;
        const F = count / 3;
        const chi = V - E + F;

        // Check bevel endpoints in local coordinates
        // Should connect (10, y, 8) and (8, y, 10)
        const bevelP1 = uVerts.find(v => Math.abs(v.x - 10.0) < eps && Math.abs(v.z - 8.0) < eps);
        const bevelP2 = uVerts.find(v => Math.abs(v.x - 8.0) < eps && Math.abs(v.z - 10.0) < eps);
        const bevelWidth = bevelP1 && bevelP2 ? Math.hypot(bevelP1.x - bevelP2.x, bevelP1.z - bevelP2.z) : 0;

        return {
          triangles: F,
          uniqueVertices: V,
          totalEdges: E,
          manifoldEdges: manifold,
          openEdges: open,
          nonManifoldEdges: nonM,
          eulerCharacteristic: chi,
          isWatertight: open === 0,
          isManifold: open === 0 && nonM === 0,
          bbox: {
            min: { x: bbox.min.x, y: bbox.min.y, z: bbox.min.z },
            max: { x: bbox.max.x, y: bbox.max.y, z: bbox.max.z }
          },
          bevelEndpointA: bevelP1 ? { x: bevelP1.x, z: bevelP1.z } : null,
          bevelEndpointB: bevelP2 ? { x: bevelP2.x, z: bevelP2.z } : null,
          bevelPlanarWidth: bevelWidth,
          expectedBevelWidth: 2.0 * Math.SQRT2
        };
      }

      return {
        original: getMeshDetails(origBox.geometry),
        chamfer: getMeshDetails(chamferBox.geometry)
      };
    })()
    """
    telemetry_chamfer = eval_js(telemetry_chamfer_js)
    print("Chamfer Mesh Telemetry:", json.dumps(telemetry_chamfer, indent=2))

    # Angle 5: 4-Viewport Overview Side-by-Side for Chamfer
    eval_js("renderAllViewports()")
    f5 = capture_screenshot("geom_05_chamfer_4viewports_side_by_side.png")
    captured_files.append(f5)

    # Angle 6: Perspective Viewport Close-Up (Top-Right viewport: vp-persp)
    eval_js("""
    (() => {
      const cam = cameras["persp"];
      cam.position.set(24, 28, 44);
      cam.lookAt(0, 10, 0);
      cam.updateProjectionMatrix();
      renderAllViewports();
      return true;
    })()
    """)
    f6 = capture_screenshot("geom_06_chamfer_perspective_closeup_side_by_side.png", clip=clip_persp)
    captured_files.append(f6)

    # Angle 7: Top Viewport Close-Up (Top-Left viewport: vp-top)
    eval_js("""
    (() => {
      const cam = cameras["top"];
      cam.position.set(0, 100, 0);
      cam.zoom = 2.0;
      cam.updateProjectionMatrix();
      renderAllViewports();
      return true;
    })()
    """)
    f7 = capture_screenshot("geom_07_chamfer_top_view_bevel_cut.png", clip=clip_top)
    captured_files.append(f7)

    # Angle 8: Right Viewport Close-Up (Bottom-Right viewport: vp-right)
    eval_js("""
    (() => {
      const cam = cameras["right"];
      cam.position.set(100, 10, 0);
      cam.zoom = 2.0;
      cam.updateProjectionMatrix();
      renderAllViewports();
      return true;
    })()
    """)
    f8 = capture_screenshot("geom_08_chamfer_right_view_unaffected_profile.png", clip=clip_right)
    captured_files.append(f8)

    print("\nAll 8 geometry verification screenshots captured successfully!")

    # Open screenshots in macOS Preview for user visual inspection
    for f in captured_files:
        subprocess.run(["open", f])

finally:
    proc.kill()
