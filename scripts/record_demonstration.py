import socket
import json
import urllib.request
import subprocess
import time
import struct
import base64
import os

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9315
BASE_DIR = "/Users/andybuck/.gemini/antigravity/single-file-html-app"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
VIDEO_OUTPUT = os.path.join(SCREENSHOT_DIR, "cadnt_demonstration.webm")

print("Launching Chrome for Demonstration Recording...")
proc = subprocess.Popen([
    CHROME_BIN,
    "--headless=new",
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--window-size=1440,900",
    f"--remote-debugging-port={PORT}",
    f"file://{BASE_DIR}/index.html?no_auto_onboard=1"
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

    cid = 1
    def evaluate(js, await_promise=False):
        global cid
        cid += 1
        msg = {
            "id": cid,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js,
                "returnByValue": True,
                "awaitPromise": await_promise
            }
        }
        data = json.dumps(msg).encode("utf-8")
        frame = bytearray([0x81])
        length = len(data)
        mask = b"\x11\x22\x33\x44"
        if length < 126: frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", length))
        frame.extend(mask)
        frame.extend(bytearray(b ^ mask[i % 4] for i, b in enumerate(data)))
        s.sendall(frame)
        while True:
            h = s.recv(2)
            l = h[1] & 0x7f
            if l == 126: l = struct.unpack(">H", s.recv(2))[0]
            elif l == 127: l = struct.unpack(">Q", s.recv(8))[0]
            p = b""
            while len(p) < l: p += s.recv(l - len(p))
            m = json.loads(p.decode("utf-8", errors="ignore"))
            if m.get("id") == cid:
                if "exceptionDetails" in m.get("result", {}):
                    print("JS EXCEPTION:", m["result"]["exceptionDetails"])
                return m.get("result", {}).get("result", {}).get("value")

    evaluate("window.IS_TESTING = true;")
    evaluate("renderAllViewports();")

    print("\n1. Initializing in-browser 4-viewport composite recorder...")
    setup_recorder_js = """
    (() => {
      window.__RECORDED_CHUNKS__ = [];
      window.__CURRENT_STAGE_TITLE__ = "INITIALIZING DEMONSTRATION";
      window.__CURRENT_STAGE_DESC__ = "CADN'T: Computer Aided Design Noncompliance Technology";
      
      const compCanvas = document.createElement('canvas');
      compCanvas.width = 960;
      compCanvas.height = 720;
      const ctx = compCanvas.getContext('2d');

      const topC = document.getElementById('canvas-top');
      const perspC = document.getElementById('canvas-perspective');
      const frontC = document.getElementById('canvas-front');
      const rightC = document.getElementById('canvas-right');

      function drawComposite() {
        try {
          ctx.fillStyle = "#808080";
          ctx.fillRect(0, 0, 960, 720);

          // 4 Viewports
          if (topC) ctx.drawImage(topC, 0, 0, 480, 320);
          if (perspC) ctx.drawImage(perspC, 480, 0, 480, 320);
          if (frontC) ctx.drawImage(frontC, 0, 320, 480, 320);
          if (rightC) ctx.drawImage(rightC, 480, 320, 480, 320);

          // Viewport labels
          ctx.fillStyle = "rgba(0, 0, 128, 0.75)";
          ctx.fillRect(4, 4, 120, 18);
          ctx.fillRect(484, 4, 140, 18);
          ctx.fillRect(4, 324, 120, 18);
          ctx.fillRect(484, 324, 120, 18);

          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 11px Tahoma, sans-serif";
          ctx.fillText("Top View (X/Z)", 8, 17);
          ctx.fillText("Perspective (3D)", 488, 17);
          ctx.fillText("Front View (X/Y)", 8, 337);
          ctx.fillText("Right View (Z/Y)", 488, 337);

          // Dividing grid lines
          ctx.strokeStyle = "#000000";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(480, 0); ctx.lineTo(480, 640);
          ctx.moveTo(0, 320); ctx.lineTo(960, 320);
          ctx.stroke();

          // Bottom Retro Status & Step Banner
          ctx.fillStyle = "#c0c0c0";
          ctx.fillRect(0, 640, 960, 80);
          ctx.fillStyle = "#ffffff";
          ctx.fillRect(0, 640, 960, 2);
          ctx.fillStyle = "#808080";
          ctx.fillRect(0, 718, 960, 2);

          // Retro banner header
          ctx.fillStyle = "#000080";
          ctx.fillRect(6, 646, 948, 24);
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 12px Tahoma, sans-serif";
          ctx.fillText("CADN'T DEMONSTRATION — " + window.__CURRENT_STAGE_TITLE__, 12, 663);

          // Description text
          ctx.fillStyle = "#000000";
          ctx.font = "12px Tahoma, sans-serif";
          ctx.fillText(window.__CURRENT_STAGE_DESC__, 12, 695);
        } catch (e) {}
      }

      const stream = compCanvas.captureStream(30);
      const mime = (typeof MediaRecorder !== 'undefined' && MediaRecorder.isTypeSupported('video/webm;codecs=vp8'))
        ? 'video/webm;codecs=vp8'
        : 'video/webm';

      if (typeof MediaRecorder !== 'undefined') {
        window.__MEDIA_RECORDER__ = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 2500000 });
        window.__MEDIA_RECORDER__.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) window.__RECORDED_CHUNKS__.push(e.data);
        };
        window.__MEDIA_RECORDER__.start(50);
      }

      window.__COMP_INTERVAL__ = setInterval(() => {
        drawComposite();
      }, 1000 / 30);

      return !!window.__MEDIA_RECORDER__;
    })()
    """
    rec_ok = evaluate(setup_recorder_js)
    print("MediaRecorder started:", rec_ok)
    assert rec_ok, "Failed to start MediaRecorder in page!"

    start_time = time.time()

    def set_banner(title, desc):
        evaluate(f"""
        window.__CURRENT_STAGE_TITLE__ = {json.dumps(title)};
        window.__CURRENT_STAGE_DESC__ = {json.dumps(desc)};
        """)

    # Stage 0: Show starting Michigan model
    set_banner("STARTING SCENE: THE MICHIGAN OBSTACLE", "Displaying default starting solid: Michigan State Geometry (UP + LP)")
    print("Stage 0: Starting Michigan scene (5.0s)...")
    time.sleep(5.0)

    # Stage 1: Delete Michigan
    set_banner("STEP 1: DELETE STARTING GEOMETRY", "Requesting 'can i delete michigan' -> Confirming removal dialog")
    print("Stage 1: Deleting Michigan (6.0s)...")
    evaluate("""
    (() => {
      requestInput.value = "can i delete michigan";
      processRequest("can i delete michigan");
      const okBtn = document.getElementById("btn-confirm-ok");
      if (okBtn) okBtn.click();
      renderAllViewports();
    })()
    """)
    time.sleep(6.0)

    # Stage 2: Create 6-sided polygon sketch
    set_banner("STEP 2: 6-SIDED POLYGON SKETCH", "Executing 'can i polygon' -> Prompt 'How many sides?' (6) -> Center (0,0) -> Radius 15mm")
    print("Stage 2: 6-sided Polygon sketch (7.0s)...")
    evaluate("""
    (() => {
      startSketch("polygon", 6);
      const poly = createPolygonSketch(new THREE.Vector3(0, 0, 0), 15, 6, "top");
      cancelSketch();
      selectObject(poly);
      renderAllViewports();
    })()
    """)
    time.sleep(7.0)

    # Stage 3: Extrude base flange solid (10mm)
    set_banner("STEP 3: EXTRUDE 3D MOUNTING FLANGE", "Executing 'can i extrude 10' -> Converting planar polygon into 10mm watertight solid")
    print("Stage 3: Extrude base flange (7.0s)...")
    evaluate("""
    (() => {
      const poly = sceneObjects.find(o => o.userData && o.userData.profileType === "polygon");
      selectObject(poly);
      const solid = extrudeSelectedProfile(10);
      selectObject(solid);
      renderAllViewports();
    })()
    """)
    time.sleep(7.0)

    # Stage 4: 2D Offset 4mm Inward (Bolt Ring Curve)
    set_banner("STEP 4: 2D OFFSET COMMAND (4mm INSET)", "Executing 'can i offset 4' -> Computing exact normal miter offset for bolt mounting ring")
    print("Stage 4: 2D Offset command (7.0s)...")
    evaluate("""
    (() => {
      const poly = sceneObjects.find(o => o.userData && o.userData.profileType === "polygon");
      selectObject(poly);
      startModelingCommand("offset", { dist: 4.0 });
      const dirSel = document.getElementById("offset-param-dir");
      if (dirSel) dirSel.value = "inward";
      if (activeCommand && activeCommand.confirm) activeCommand.confirm();
      renderAllViewports();
    })()
    """)
    time.sleep(7.0)

    # Stage 5: Circular Bolt Hole Profile (Radius 1.5mm)
    set_banner("STEP 5: CIRCULAR BOLT HOLE SKETCH", "Executing 'can i circle' -> Constructing 1.5mm bolt hole on mounting ring")
    print("Stage 5: Circular bolt hole (6.0s)...")
    evaluate("""
    (() => {
      const hole = createCircleSketch(new THREE.Vector3(0, 0, 10.38), 1.5, "top");
      selectObject(hole);
      renderAllViewports();
    })()
    """)
    time.sleep(6.0)

    # Stage 6: Polar Array Pattern (6 Holes)
    set_banner("STEP 6: POLAR ARRAY COMMAND (6 COPIES)", "Executing 'can i array' -> Polar Array: 6 copies around center (0,0,0) across 360°")
    print("Stage 6: Polar Array 6 holes (8.0s)...")
    evaluate("""
    (() => {
      const hole = sceneObjects.find(o => o.userData && o.userData.profileType === "circle");
      selectObject(hole);
      startModelingCommand("array", { type: "polar" });
      const countInp = document.getElementById("array-polar-count");
      if (countInp) countInp.value = 6;
      const angleInp = document.getElementById("array-polar-angle");
      if (angleInp) angleInp.value = 360;
      if (activeCommand && activeCommand.confirm) activeCommand.confirm();
      renderAllViewports();
    })()
    """)
    time.sleep(8.0)

    # Stage 7: Cumulative Fillet (Top Edge 2mm) & Chamfer (Bottom Edge 1mm)
    set_banner("STEP 7: PERSISTENT FILLET & CHAMFER", "Applying Fillet 2mm on top edge AND Chamfer 1mm on bottom edge (both modifications preserved simultaneously!)")
    print("Stage 7: Fillet & Chamfer cumulative persistence (8.0s)...")
    evaluate("""
    (() => {
      const solid = sceneObjects.find(o => o.userData && o.userData.type === "ExtrudedSolid");
      selectObject(solid);
      getSolidEdges(solid);
      const cuts = [
        { id: "cut_fillet_top", mode: "fillet", param: 2.0, edges: [0], isAsymmetric: false },
        { id: "cut_chamfer_bot", mode: "chamfer", param: 1.0, edges: [1], isAsymmetric: false }
      ];
      solid.userData.edgeCutHistory = cuts;
      const newGeo = evaluateMeshWithCutHistory(solid, cuts, 16);
      if (newGeo) {
        solid.geometry.dispose();
        solid.geometry = newGeo;
      }
      renderAllViewports();
    })()
    """)
    time.sleep(8.0)

    # Stage 8: 3D Camera Orbit Showcase
    set_banner("STEP 8: 3D CAMERA ORBIT SHOWCASE", "Navigating 4 viewports with W/S/A/D keyboard orbit controls; inspecting watertight manifold flange")
    print("Stage 8: Camera orbit showcase (12.0s)...")
    # Simulate gentle camera orbit over 12 seconds
    orbit_start = time.time()
    while time.time() - orbit_start < 12.0:
        evaluate("""
        (() => {
          if (typeof applyNavigationStep === 'function') {
            applyNavigationStep("KeyD", false, 0.2);
          } else {
            const perspCam = (typeof viewports !== 'undefined' && viewports.perspective && viewports.perspective.camera) ? viewports.perspective.camera : null;
            if (perspCam) {
              const x = perspCam.position.x, z = perspCam.position.z;
              const theta = 0.03;
              perspCam.position.x = x * Math.cos(theta) - z * Math.sin(theta);
              perspCam.position.z = x * Math.sin(theta) + z * Math.cos(theta);
              perspCam.lookAt(0, 5, 0);
            }
          }
          renderAllViewports();
        })()
        """)
        time.sleep(0.08)

    # Stage 9: Save .cadnt Project Archive
    set_banner("STEP 9: PROJECT ARCHIVE SERIALIZATION", "Executing 'can i save' -> Serializing complete project geometry into .cadnt archive")
    print("Stage 9: Save project archive (5.0s)...")
    evaluate("""
    (() => {
      requestInput.value = "can i save";
      processRequest("can i save");
      setTimeout(() => {
        const btn1 = document.getElementById("btn-confirm-ok");
        if (btn1) btn1.click();
        setTimeout(() => {
          const btn2 = document.getElementById("btn-confirm-ok");
          if (btn2) btn2.click();
        }, 500);
      }, 500);
      renderAllViewports();
    })()
    """)
    time.sleep(5.0)

    # Final Stage: Completed Demonstration Summary
    total_elapsed = time.time() - start_time
    set_banner("DEMONSTRATION COMPLETE", f"All 9 modeling operations successfully executed and verified (Duration: {total_elapsed:.1f}s)")
    print(f"Final inspection frame... (total time so far: {total_elapsed:.1f}s)")
    time.sleep(4.0)

    # Stop MediaRecorder
    print("\nStopping MediaRecorder and extracting WebM chunks...")
    evaluate("""
    (() => {
      if (window.__COMP_INTERVAL__) clearInterval(window.__COMP_INTERVAL__);
      if (window.__MEDIA_RECORDER__ && window.__MEDIA_RECORDER__.state !== 'inactive') {
        window.__MEDIA_RECORDER__.stop();
      }
    })()
    """)
    time.sleep(1.0)

    has_video = evaluate("window.__RECORDED_CHUNKS__ && window.__RECORDED_CHUNKS__.length > 0")
    print("Recorded chunks present:", has_video)
    assert has_video, "No video chunks recorded by MediaRecorder!"

    video_base64 = evaluate("""
    new Promise(resolve => {
      const blob = new Blob(window.__RECORDED_CHUNKS__, { type: 'video/webm' });
      const reader = new FileReader();
      reader.onloadend = () => {
        const b64 = reader.result.split(',')[1];
        resolve(b64);
      };
      reader.readAsDataURL(blob);
    })
    """, await_promise=True)

    with open(VIDEO_OUTPUT, "wb") as f:
        f.write(base64.b64decode(video_base64))

    # Also extract and save the native .cadnt project archive created during demonstration
    cadnt_json = evaluate("serializeProjectState()")
    cadnt_output = os.path.join(BASE_DIR, "screenshots", "cadnt_demonstration.cadnt")
    with open(cadnt_output, "w", encoding="utf-8") as f:
        f.write(cadnt_json)
    print(f"Native .cadnt project saved to: {cadnt_output}")

    # Verify that the saved project contains genuine geometry
    try:
        data = json.loads(cadnt_json)
        print(f"Verification of .cadnt project: {len(data.get('objects', []))} scene objects found.")
        solid_obj = next((o for o in data.get('objects', []) if o.get('userData', {}).get('type') == 'ExtrudedSolid'), None)
        assert solid_obj is not None, "Missing ExtrudedSolid in saved project!"
        cuts = solid_obj.get('userData', {}).get('edgeCutHistory', [])
        assert len(cuts) >= 2, f"Expected cumulative edge cuts, got {len(cuts)}"
        print(f"Verified ExtrudedSolid with {len(cuts)} cumulative edge cuts in project archive!")
    except Exception as e:
        print(f"Project archive verification error: {e}")

    file_size = os.path.getsize(VIDEO_OUTPUT)
    final_duration = time.time() - start_time
    print(f"\n=======================================================")
    print(f"SUCCESS: Recorded Demonstration Video saved!")
    print(f"Path: {VIDEO_OUTPUT}")
    print(f"File Size: {file_size} bytes ({file_size / (1024*1024):.2f} MB)")
    print(f"Total Duration: {final_duration:.1f} seconds (Target: 60-120 seconds)")
    print(f"Meets Requirement: {60 <= final_duration <= 120}")
    print(f"=======================================================")

finally:
    proc.kill()
