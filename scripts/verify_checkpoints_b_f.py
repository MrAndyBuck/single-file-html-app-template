#!/usr/bin/env python3
import socket, json, urllib.request, subprocess, time, struct, base64, os, math

PORT = 9345
DESKTOP_DIR = '/Users/andybuck/Desktop/CADNT_Screenshots'
ARTIFACT_DIR = '/Users/andybuck/.gemini/antigravity-cli/brain/92f72284-41c5-4687-ab10-0c2aade50fd2/screenshots'

os.makedirs(DESKTOP_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

proc = subprocess.Popen([
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless=new',
    '--use-gl=angle',
    '--use-angle=swiftshader',
    '--enable-unsafe-swiftshader',
    '--window-size=1280,800',
    f'--remote-debugging-port={PORT}',
    'file:///Users/andybuck/.gemini/antigravity/single-file-html-app/index.html?no_auto_onboard=1'
])
time.sleep(3.0)

try:
    tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json').read().decode())
    target = next(t for t in tabs if t.get('type') == 'page')
    ws_url = target['webSocketDebuggerUrl']
    host, port, path = '127.0.0.1', PORT, ws_url.split(f'127.0.0.1:{PORT}')[1]
    s = socket.socket(); s.connect((host, port))
    key = base64.b64encode(b'0123456789abcdef').decode()
    req = f'GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
    s.sendall(req.encode()); s.recv(4096)

    cmd_counter = 1
    def send_cmd(method, params=None):
        global cmd_counter
        cid = cmd_counter
        cmd_counter += 1
        msg = json.dumps({'id': cid, 'method': method, 'params': params or {}}).encode('utf-8')
        frame = bytearray([0x81])
        length = len(msg)
        mask = b'\x11\x22\x33\x44'
        if length < 126: frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(struct.pack('>H', length))
        frame.extend(mask)
        frame.extend(bytearray(b ^ mask[i % 4] for i, b in enumerate(msg)))
        s.sendall(frame)
        while True:
            h = s.recv(2)
            if not h: break
            l = h[1] & 0x7F
            if l == 126: l = struct.unpack('>H', s.recv(2))[0]
            elif l == 127: l = struct.unpack('>Q', s.recv(8))[0]
            raw = bytearray()
            while len(raw) < l: raw.extend(s.recv(l - len(raw)))
            res = json.loads(raw.decode('utf-8'))
            if res.get('id') == cid: return res

    def evaluate(expr):
        r = send_cmd('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        return r.get('result', {}).get('result', {}).get('value')

    def save_screenshot(filename, clip=None):
        params = {'format': 'png'}
        if clip: params['clip'] = clip
        r = send_cmd('Page.captureScreenshot', params)
        data = base64.b64decode(r['result']['data'])
        p1 = os.path.join(DESKTOP_DIR, filename)
        p2 = os.path.join(ARTIFACT_DIR, filename)
        with open(p1, 'wb') as f: f.write(data)
        with open(p2, 'wb') as f: f.write(data)
        print(f"Captured screenshot: {filename} ({len(data)} bytes) saved to Desktop & Artifacts")

    time.sleep(1.0)
    print("=== STARTING CHECKPOINTS B THROUGH F INTERACTIVE VERIFICATION ===")

    # =========================================================================
    # CHECKPOINT B: Michigan Deletion Direct Locator & Confirm
    # =========================================================================
    print("\n--- Verifying Checkpoint B: Michigan Deletion ---")
    # Setup scene: Michigan present + create an unrelated box and select it
    b_setup = evaluate("""
        (() => {
            creditBalance = 249.00;
            createBoxPrimitive();
            const unrelated = sceneObjects[sceneObjects.length - 1];
            unrelated.name = "Unrelated_User_Box";
            selectObject(unrelated);
            const michiganTarget = sceneObjects.find(o => o.userData && o.userData.id === "starting_michigan");
            return {
                michiganExists: !!michiganTarget,
                michiganProtected: michiganTarget ? michiganTarget.userData.protected : null,
                selectedObj: selectedObjects.map(o => o.name)
            };
        })()
    """)
    print("Checkpoint B setup:", b_setup)

    # Trigger 'Can I delete michigan' without selecting Michigan
    b_trigger = evaluate("""
        (() => {
            processRequest("Can I delete michigan");
            const modal = document.getElementById("modal-confirm");
            const title = document.getElementById("confirm-title").textContent;
            const body = document.getElementById("confirm-body").textContent;
            return { modalOpen: modal && modal.open, title: title, body: body };
        })()
    """)
    print("Checkpoint B confirm prompt:", b_trigger)
    assert b_trigger["modalOpen"] == True, "Confirm modal did not open"
    assert b_trigger["title"] == "Are you sure you want to remove this?", f"Expected exact title, got: {b_trigger['title']}"
    save_screenshot('cp_b_01_confirm_remove_dialog.png')

    # Confirm deletion
    b_deleted = evaluate("""
        (() => {
            const okBtn = document.getElementById("btn-confirm-ok");
            okBtn.click();
            const michiganTarget = sceneObjects.find(o => o.userData && o.userData.id === "starting_michigan");
            const unrelated = sceneObjects.find(o => o.name === "Unrelated_User_Box");
            return {
                michiganRemaining: !!michiganTarget,
                michiganModelRef: michiganModel !== null,
                unrelatedRemains: !!unrelated,
                unrelatedSelected: selectedObjects.includes(unrelated)
            };
        })()
    """)
    print("Checkpoint B after deletion:", b_deleted)
    assert b_deleted["michiganRemaining"] == False, "Michigan was not deleted"
    assert b_deleted["unrelatedRemains"] == True, "Unrelated object was removed"
    assert b_deleted["unrelatedSelected"] == True, "Unrelated object lost selection"
    save_screenshot('cp_b_02_michigan_deleted_unrelated_intact.png')

    # Undo deletion
    b_undo = evaluate("""
        (() => {
            processRequest("Can I undo");
            const michiganTarget = sceneObjects.find(o => o.userData && o.userData.id === "starting_michigan");
            return {
                michiganRestored: !!michiganTarget,
                michiganProtected: michiganTarget ? michiganTarget.userData.protected : false
            };
        })()
    """)
    print("Checkpoint B undo restored:", b_undo)
    assert b_undo["michiganRestored"] == True, "Michigan was not restored by Undo"
    assert b_undo["michiganProtected"] == True, "Restored Michigan lost protected flag"
    save_screenshot('cp_b_03_michigan_restored_undo.png')

    # =========================================================================
    # CHECKPOINT C: Polygon Command Workflow & Extrusion
    # =========================================================================
    print("\n--- Verifying Checkpoint C: Polygon Command ---")
    # Clean workspace for clear polygon demonstration
    evaluate("""
        (() => {
            while (sceneObjects.length > 0) {
                scene.remove(sceneObjects[0]);
                sceneObjects.shift();
            }
            selectedObjects = [];
            michiganModel = null;
            renderAllViewports();
        })()
    """)

    # 1. Start polygon command with 5 sides
    c_start = evaluate("""
        (() => {
            processRequest("Can I polygon 5");
            const bar = document.getElementById("command-bar");
            const prompt = document.getElementById("command-prompt").textContent;
            const sidesInp = document.getElementById("poly-param-sides");
            return {
                activeSketchMode: activeSketchMode,
                barVisible: bar.style.display !== "none",
                prompt: prompt,
                sidesValue: sidesInp ? sidesInp.value : null
            };
        })()
    """)
    print("Checkpoint C started:", c_start)
    assert c_start["activeSketchMode"] == "polygon", "Polygon sketch mode not active"

    # 2. Place center point and preview rubberband
    c_center = evaluate("""
        (() => {
            handleSketchClick(new THREE.Vector3(0, 0, 0), "top");
            updateRubberband(new THREE.Vector3(15, 0, 0), "top");
            const rb = rubberbandObj;
            return {
                hasRubberband: !!rb,
                childCount: rb ? rb.children.length : 0,
                sketchPointsCount: sketchPoints.length
            };
        })()
    """)
    print("Checkpoint C center set and rubberband preview:", c_center)
    save_screenshot('cp_c_01_pentagon_rubberband_preview.png')

    # 3. Commit pentagon
    c_commit = evaluate("""
        (() => {
            handleSketchClick(new THREE.Vector3(15, 0, 0), "top");
            const poly = sceneObjects[sceneObjects.length - 1];
            return {
                modeExited: activeSketchMode === null,
                name: poly.name,
                type: poly.userData.type,
                closed: poly.userData.closed,
                sides: poly.userData.sides,
                radius: poly.userData.radius,
                vertexCount: poly.userData.points ? poly.userData.points.length : 0
            };
        })()
    """)
    print("Checkpoint C committed pentagon:", c_commit)
    assert c_commit["modeExited"] == True, "Command did not auto-exit after commit"
    assert c_commit["closed"] == True, "Polygon is not closed profile"
    assert c_commit["sides"] == 5, f"Expected 5 sides, got {c_commit['sides']}"
    assert c_commit["vertexCount"] == 5, "Geometry does not have 5 vertices"
    save_screenshot('cp_c_02_pentagon_profile_committed.png')

    # 4. Extrude pentagon into 3D solid
    c_extrude = evaluate("""
        (() => {
            const poly = sceneObjects[sceneObjects.length - 1];
            selectObject(poly);
            const solid = extrudeSelectedProfile(20);
            return {
                solidCreated: !!solid,
                solidType: solid ? solid.userData.type : null,
                vertexCount: solid ? solid.geometry.attributes.position.count : 0
            };
        })()
    """)
    print("Checkpoint C extruded pentagon solid:", c_extrude)
    assert c_extrude["solidCreated"] == True, "Failed to extrude pentagon"
    assert c_extrude["solidType"] == "ExtrudedSolid", "Extruded object is not ExtrudedSolid"
    save_screenshot('cp_c_03_pentagon_extruded_solid.png')

    # 5. Create Triangle (3 sides) and Hexagon (6 sides)
    c_shapes = evaluate("""
        (() => {
            const tri = createPolygonSketch(new THREE.Vector3(-30, 0, 0), 12, 3, "top");
            const hex = createPolygonSketch(new THREE.Vector3(30, 0, 0), 12, 6, "top");
            renderAllViewports();
            return {
                triSides: tri.userData.sides,
                hexSides: hex.userData.sides
            };
        })()
    """)
    print("Checkpoint C triangle & hexagon:", c_shapes)
    save_screenshot('cp_c_04_triangle_and_hexagon.png')

    # 6. Test DPR 2.0 (Retina)
    send_cmd('Emulation.setDeviceMetricsOverride', {
        'width': 1280, 'height': 800, 'deviceScaleFactor': 2.0, 'mobile': False
    })
    evaluate("resizeRenderer(); renderAllViewports();")
    time.sleep(0.5)
    save_screenshot('cp_c_05_retina_dpr2_polygons.png')
    send_cmd('Emulation.setDeviceMetricsOverride', {
        'width': 1280, 'height': 800, 'deviceScaleFactor': 1.0, 'mobile': False
    })
    evaluate("resizeRenderer(); renderAllViewports();")

    # =========================================================================
    # CHECKPOINT D: Numeric Easter Eggs (67, 69, 420)
    # =========================================================================
    print("\n--- Verifying Checkpoint D: Numeric Easter Eggs ---")
    d_69 = evaluate("""
        (() => {
            modelingCommandCount = 0;
            const adModal = document.getElementById("modal-ad");
            if (adModal && adModal.open) adModal.close();
            processRequest("Can I box 69");
            const modal = document.getElementById("modal-nice-easter-egg");
            const text = document.getElementById("nice-easter-egg-text").textContent.trim();
            const created = sceneObjects[sceneObjects.length - 1];
            return {
                modalOpen: modal && modal.open,
                text: text,
                boxCreated: created && created.userData.type === "Box"
            };
        })()
    """)
    print("Checkpoint D 69 input result:", d_69)
    assert d_69["modalOpen"] == True, "Easter egg modal did not open for 69"
    assert d_69["text"] == "nice.", f"Expected 'nice.', got: '{d_69['text']}'"
    assert d_69["boxCreated"] == True, "Box was not created (modeling operation broken)"
    save_screenshot('cp_d_01_nice_popup_69.png')

    # Close modal and test 420
    d_420 = evaluate("""
        (() => {
            modelingCommandCount = 0;
            const adModal = document.getElementById("modal-ad");
            if (adModal && adModal.open) adModal.close();
            const modal = document.getElementById("modal-nice-easter-egg");
            if (modal && modal.open) modal.close();
            processRequest("Can I cylinder 420");
            const text = document.getElementById("nice-easter-egg-text").textContent.trim();
            const cyl = sceneObjects[sceneObjects.length - 1];
            return {
                modalOpen: modal && modal.open,
                text: text,
                cylCreated: cyl && cyl.userData.type === "Cylinder"
            };
        })()
    """)
    print("Checkpoint D 420 input result:", d_420)
    assert d_420["modalOpen"] == True, "Easter egg modal did not open for 420"
    assert d_420["cylCreated"] == True, "Cylinder was not created"
    save_screenshot('cp_d_02_nice_popup_420.png')

    # Test substrings do NOT trigger
    d_substr = evaluate("""
        (() => {
            const modal = document.getElementById("modal-nice-easter-egg");
            if (modal && modal.open) modal.close();
            checkNumericEasterEgg("167");
            const open167 = modal && modal.open;
            checkNumericEasterEgg("4200");
            const open4200 = modal && modal.open;
            checkNumericEasterEgg("690");
            const open690 = modal && modal.open;
            return { open167, open4200, open690 };
        })()
    """)
    print("Checkpoint D substring check (must all be False):", d_substr)
    assert not d_substr["open167"] and not d_substr["open4200"] and not d_substr["open690"], "Substrings triggered Easter egg!"

    # =========================================================================
    # CHECKPOINT E: Rhino-Style Lock & Unlock
    # =========================================================================
    print("\n--- Verifying Checkpoint E: Rhino-Style Lock ---")
    # Clean workspace, create a box to lock
    evaluate("""
        (() => {
            const modal = document.getElementById("modal-nice-easter-egg");
            if (modal && modal.open) modal.close();
            while (sceneObjects.length > 0) {
                scene.remove(sceneObjects[0]);
                sceneObjects.shift();
            }
            selectedObjects = [];
            createBoxPrimitive();
            const box = sceneObjects[sceneObjects.length - 1];
            box.name = "Locked_Part_Alpha";
            selectObject(box);
            renderAllViewports();
        })()
    """)

    # Lock object
    e_lock = evaluate("""
        (() => {
            processRequest("Can I lock");
            const box = sceneObjects.find(o => o.name === "Locked_Part_Alpha");
            const badge = document.querySelector(`.obj-lock-badge[data-id="${box.userData.id}"]`);
            return {
                isLocked: box.userData.locked,
                selectionCleared: !selectedObjects.includes(box),
                badgeRendered: !!badge,
                badgeText: badge ? badge.textContent : null
            };
        })()
    """)
    print("Checkpoint E locked object:", e_lock)
    assert e_lock["isLocked"] == True, "Object was not locked"
    assert e_lock["selectionCleared"] == True, "Object remained selected"
    assert e_lock["badgeRendered"] == True, "Lock badge not in FeatureManager"
    save_screenshot('cp_e_01_locked_object_feature_manager.png')

    # Try selecting and deleting locked object
    e_protect = evaluate("""
        (() => {
            const box = sceneObjects.find(o => o.name === "Locked_Part_Alpha");
            selectObject(box);
            const selectedAfterDirect = selectedObjects.includes(box);
            // Try simulated delete
            selectedObjects = [box];
            const countBeforeDelete = sceneObjects.length;
            handleDelete();
            selectedObjects = [];
            const countAfterDelete = sceneObjects.length;
            return {
                directSelectRefused: !selectedAfterDirect,
                deleteBlocked: countBeforeDelete === countAfterDelete && sceneObjects.includes(box)
            };
        })()
    """)
    print("Checkpoint E protection check:", e_protect)
    assert e_protect["directSelectRefused"] == True, "Direct selection was permitted"
    assert e_protect["deleteBlocked"] == True, "Deletion was not blocked"
    save_screenshot('cp_e_02_selection_and_deletion_blocked.png')

    # Unlock via FeatureManager click
    e_unlock = evaluate("""
        (() => {
            const box = sceneObjects.find(o => o.name === "Locked_Part_Alpha");
            const badge = document.querySelector(`.obj-lock-badge[data-id="${box.userData.id}"]`);
            if (badge) badge.click();
            return {
                isLockedNow: box.userData.locked
            };
        })()
    """)
    print("Checkpoint E unlocked via FeatureManager:", e_unlock)
    assert e_unlock["isLockedNow"] == False, "Object was not unlocked via badge"
    save_screenshot('cp_e_03_unlocked_via_feature_manager.png')

    # =========================================================================
    # CHECKPOINT F: Slowly Escaping Spheres
    # =========================================================================
    print("\n--- Verifying Checkpoint F: Slowly Escaping Spheres ---")
    # Clean workspace and create Sphere primitive
    f_setup = evaluate("""
        (() => {
            while (sceneObjects.length > 0) {
                scene.remove(sceneObjects[0]);
                sceneObjects.shift();
            }
            selectedObjects = [];
            createSpherePrimitive();
            const sphere = sceneObjects[sceneObjects.length - 1];
            sphere.name = "Escaping_Sphere_Satire";
            sphere.position.set(0, 8, 0);
            sphere.rotation.set(0, 0, 0);
            sphere.updateMatrix();
            sphere.updateMatrixWorld();
            renderAllViewports();
            return {
                type: sphere.userData.type,
                startPos: { x: sphere.position.x, y: sphere.position.y, z: sphere.position.z },
                startRot: { x: sphere.rotation.x, y: sphere.rotation.y, z: sphere.rotation.z }
            };
        })()
    """)
    print("Checkpoint F start state:", f_setup)
    save_screenshot('cp_f_01_sphere_start_pos.png')

    # Simulate 4.0 seconds elapsed (0.05 units/sec -> expected ~0.20 units moved)
    f_move = evaluate("""
        (() => {
            const sphere = sceneObjects.find(o => o.name === "Escaping_Sphere_Satire");
            const p0 = sphere.position.clone();
            // Advance in four 1.0s ticks
            for (let t = 0; t < 4; t++) {
                updateEscapingSpheres(1.0);
            }
            renderAllViewports();
            const p1 = sphere.position.clone();
            const dist = p0.distanceTo(p1);
            const rotDelta = Math.abs(sphere.rotation.x) + Math.abs(sphere.rotation.y) + Math.abs(sphere.rotation.z);
            return {
                distMoved: dist,
                speedUnitsPerSec: dist / 4.0,
                newPos: { x: p1.x, y: p1.y, z: p1.z },
                rotDelta: rotDelta
            };
        })()
    """)
    print("Checkpoint F moved 4 seconds:", f_move)
    assert 0.18 <= f_move["distMoved"] <= 0.22, f"Expected ~0.20 units, got {f_move['distMoved']}"
    assert f_move["rotDelta"] > 0.001, "Subtle rolling rotation was not applied"
    save_screenshot('cp_f_02_sphere_moved_and_rolled.png')

    # Lock sphere and verify movement stops immediately
    f_lock = evaluate("""
        (() => {
            const sphere = sceneObjects.find(o => o.name === "Escaping_Sphere_Satire");
            selectObject(sphere);
            processRequest("Can I lock");
            const posLocked = sphere.position.clone();
            // Advance 2.0 seconds
            updateEscapingSpheres(1.0);
            updateEscapingSpheres(1.0);
            renderAllViewports();
            const posAfterLockedTicks = sphere.position.clone();
            return {
                isLocked: sphere.userData.locked,
                distWhileLocked: posLocked.distanceTo(posAfterLockedTicks)
            };
        })()
    """)
    print("Checkpoint F locked check:", f_lock)
    assert f_lock["isLocked"] == True, "Sphere was not locked"
    assert f_lock["distWhileLocked"] == 0.0, f"Locked sphere moved! Dist: {f_lock['distWhileLocked']}"
    save_screenshot('cp_f_03_locked_sphere_stopped.png')

    # Unlock sphere and verify movement resumes
    f_unlock = evaluate("""
        (() => {
            const sphere = sceneObjects.find(o => o.name === "Escaping_Sphere_Satire");
            processRequest("Can I unlock");
            const pBefore = sphere.position.clone();
            updateEscapingSpheres(1.0);
            renderAllViewports();
            const pAfter = sphere.position.clone();
            return {
                isLocked: sphere.userData.locked,
                distResumed: pBefore.distanceTo(pAfter)
            };
        })()
    """)
    print("Checkpoint F unlocked check:", f_unlock)
    assert f_unlock["isLocked"] == False, "Sphere was not unlocked"
    assert 0.04 <= f_unlock["distResumed"] <= 0.06, f"Resumed sphere didn't move at 0.05/s! Dist: {f_unlock['distResumed']}"

    print("\n=== ALL CHECKPOINTS B THROUGH F MATHEMATICALLY & VISUALLY VERIFIED! ===")

finally:
    proc.terminate()
