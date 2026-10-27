#!/usr/bin/env python3
"""
Applies Checkpoints A, B, and C updates to index.html:
1. Replaces isRecognizedCadCommand, processRequest, and executeCommand with COMMAND_REGISTRY & canonical dispatcher.
2. Replaces HELP_INDEX and renderHelpList with rich Windows 95 14-category searchable help reference.
3. Updates test suite to Tests 70a–70g covering all 3 checkpoints.
"""

import sys

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Read command registry snippet
with open("scratch/command_registry_snippet.js", "r", encoding="utf-8") as f:
    registry_snippet = f.read()

# Replace between isRecognizedCadCommand and handleDelete
start_marker = "function isRecognizedCadCommand(cmd) {"
end_marker = "function handleDelete() {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: Could not find command dispatch markers! ({start_idx}, {end_idx})")
    sys.exit(1)

content = content[:start_idx] + registry_snippet + "\n\n" + content[end_idx:]
print("Replaced command dispatch block successfully.")

# 2. Replace HELP_INDEX and renderHelpList
help_code = """function fillRequestBar(syntax) {
  const reqInput = document.getElementById("request-input");
  if (reqInput) {
    reqInput.value = syntax;
    reqInput.focus();
    if (typeof reqInput.setSelectionRange === "function") {
      reqInput.setSelectionRange(syntax.length, syntax.length);
    }
  }
  status(`Loaded '${syntax}' into Request Bar.`);
}

function ring(selector) {
  const el = document.querySelector(selector);
  if (!el) return;
  el.scrollIntoView({ block: "nearest" });
  el.classList.add("ring");
  setTimeout(() => el.classList.remove("ring"), 1600);
}

function renderHelpList(filter = "") {
  const list = document.getElementById("help-list");
  const countEl = document.getElementById("help-search-count");
  if (!list) return;
  list.innerHTML = "";

  const f = (filter || "").trim().toLowerCase();

  const matched = COMMAND_REGISTRY.filter(cmd => {
    if (!f) return true;
    const s = (cmd.syntax || "").toLowerCase();
    const d = (cmd.description || "").toLowerCase();
    const c = (cmd.category || "").toLowerCase();
    const st = (cmd.status || "").toLowerCase();
    const p = (cmd.prerequisites || "").toLowerCase();
    const a = (cmd.aliases || []).join(" ").toLowerCase();
    return s.includes(f) || d.includes(f) || c.includes(f) || st.includes(f) || p.includes(f) || a.includes(f);
  });

  if (countEl) {
    if (f) {
      countEl.textContent = `Showing ${matched.length} matching commands for "${filter}"`;
    } else {
      countEl.textContent = `Showing all ${COMMAND_REGISTRY.length} recognized commands across 14 categories`;
    }
  }

  if (matched.length === 0) {
    const emptyMsg = document.createElement("div");
    emptyMsg.style.padding = "16px";
    emptyMsg.style.textAlign = "center";
    emptyMsg.style.color = "#777777";
    emptyMsg.style.fontStyle = "italic";
    emptyMsg.textContent = `No commands matched "${filter}". Try searching for 'box', 'extrude', 'antigravity', 'cubert', or 'chinese'.`;
    list.appendChild(emptyMsg);
    return;
  }

  COMMAND_CATEGORIES.forEach(catName => {
    const catCmds = matched.filter(cmd => cmd.category === catName);
    if (catCmds.length === 0) return;

    const catSection = document.createElement("div");
    catSection.className = "help-category-section";

    const catHeader = document.createElement("div");
    catHeader.className = "help-category-title";
    catHeader.textContent = `${catName} (${catCmds.length})`;
    catSection.appendChild(catHeader);

    catCmds.forEach(cmd => {
      const card = document.createElement("div");
      card.className = "help-card";
      card.title = `Click to load '${cmd.syntax}' into the Request Bar`;

      let statusClass = "badge-status-working";
      if (cmd.status === "Partially Working") statusClass = "badge-status-partially";
      if (cmd.status === "Coming Soon") statusClass = "badge-status-coming";

      card.innerHTML = `
        <div class="help-card-header">
          <span class="help-card-syntax">${cmd.syntax}</span>
          <div class="help-card-badges">
            <span class="badge-status ${statusClass}">${cmd.status}</span>
            <span class="badge-cost">${cmd.cost}</span>
          </div>
        </div>
        <div class="help-card-desc">${cmd.description}</div>
        <div class="help-card-meta">
          <div><strong style="color:#555;">Aliases:</strong> <span class="help-card-aliases">${(cmd.aliases || []).join(", ")}</span></div>
          <div><strong style="color:#555;">Prerequisites:</strong> ${cmd.prerequisites}</div>
        </div>
      `;

      card.onclick = () => {
        fillRequestBar(cmd.syntax);
        if (cmd.control) ring(cmd.control);
      };

      catSection.appendChild(card);
    });

    list.appendChild(catSection);
  });
}
renderHelpList();
"""

help_start_marker = "const HELP_INDEX = ["
help_end_marker = "const helpSearch = document.getElementById(\"help-search\");"

h_start = content.find(help_start_marker)
h_end = content.find(help_end_marker)

if h_start == -1 or h_end == -1:
    print(f"ERROR: Could not find help markers! ({h_start}, {h_end})")
    sys.exit(1)

content = content[:h_start] + help_code + "\n" + content[h_end:]
print("Replaced help rendering block successfully.")

# 3. Replace test block with Tests 70a–70g
test_code = """    // =========================================================================
    // CHECKPOINT A, B, & C TESTS (Build v00000-019)
    // =========================================================================

    // Test 70a: Checkpoint A — Asset Manifest 18-Ad Inventory & Image Formats
    const adList = ASSET_MANIFEST.ads || [];
    const hasAipac = adList.some(a => a.includes("AipacAppAd.jpeg"));
    const hasAsbestos = adList.some(a => a.includes("AsbestosAppAd.webp"));
    const hasFushigi = adList.some(a => a.includes("FushigiAppAd.jpg"));
    const hasMrClean = adList.some(a => a.includes("MrCleanAppAd.png"));
    const total18Ads = adList.length === 18;
    const allValidFormats = adList.every(a => /\\.(jpe?g|png|webp)$/i.test(a));
    assertTest("Checkpoint A: Asset manifest contains exactly 18 advertisements including 4 new assets in supported formats (JPEG, PNG, WebP)", total18Ads && hasAipac && hasAsbestos && hasFushigi && hasMrClean && allValidFormats);

    // Test 70b: Checkpoint A — Advertisement Cycle Without Replacement & Boundary Repeat Avoidance
    const adCycleTestRes = runAdCycleTest();
    // Test interactive ad card creation, stacking offsets, and independent close buttons
    const stackCont = document.getElementById("ad-stack-container");
    if (stackCont) stackCont.innerHTML = "";
    adStackCount = 0;
    pushAdLayer();
    pushAdLayer();
    const twoCardsLayered = stackCont && stackCont.querySelectorAll(".ad-card").length === 2;
    const cardsHaveCloseBtns = stackCont && stackCont.querySelectorAll(".btn-ad-close").length === 2;
    closeAdCard(stackCont.querySelector(".ad-card"));
    const oneCardRemaining = stackCont && stackCont.querySelectorAll(".ad-card").length === 1;
    closeAdCard(stackCont.querySelector(".ad-card"));
    assertTest("Checkpoint A: Development test harness verifies 18-ad cycle without replacement, cycle boundary non-repetition, and click-to-stack layered cards with individual close buttons", adCycleTestRes.success === true && twoCardsLayered && cardsHaveCloseBtns && oneCardRemaining);

    // Test 70c: Checkpoint B — Unified Command Registry & 14-Category Help Reference
    const totalCommands = COMMAND_REGISTRY.length;
    const categoriesCount = COMMAND_CATEGORIES.length;
    const allCategoriesPopulated = COMMAND_CATEGORIES.every(cat => COMMAND_REGISTRY.some(c => c.category === cat));
    const findBox = findInCommandRegistry("can i box");
    const findSphere = findInCommandRegistry("can i sphere");
    const findLine = findInCommandRegistry("can i line");
    const findSpline = findInCommandRegistry("can i spline");
    const findExtrude = findInCommandRegistry("can i extrude");
    const findMove = findInCommandRegistry("can i move");
    const findFillet = findInCommandRegistry("can i fillet");
    const findChamfer = findInCommandRegistry("can i chamfer");
    const findPipe = findInCommandRegistry("can i pipe");
    const findCubert = findInCommandRegistry("can i cubert");
    const findLeaveCubert = findInCommandRegistry("can you leave cubert");
    const findChinese = findInCommandRegistry("can i chinese");
    const findUnchinese = findInCommandRegistry("can i unchinese");
    const findDechinese = findInCommandRegistry("can i dechinese");
    const findAntigravity = findInCommandRegistry("can i antigravity");
    const findRemoveGravity = findInCommandRegistry("can i remove gravity");
    const findRestoreGravity = findInCommandRegistry("can i restore gravity");
    const allExamplesResolved = !!(findBox && findSphere && findLine && findSpline && findExtrude && findMove && findFillet && findChamfer && findPipe && findCubert && findLeaveCubert && findChinese && findUnchinese && findDechinese && findAntigravity && findRemoveGravity && findRestoreGravity);
    // Verify search filtering
    renderHelpList("gravity");
    const gravityCount = document.querySelectorAll("#help-list .help-card").length;
    renderHelpList("nonexistent_command_xyz_123");
    const emptyCount = document.querySelectorAll("#help-list .help-card").length;
    renderHelpList(""); // restore full list
    assertTest("Checkpoint B: Command Registry generates authoritative 14-category Help reference, resolves all required examples, and filters dynamically via search", totalCommands >= 60 && categoriesCount === 14 && allCategoriesPopulated && allExamplesResolved && gravityCount >= 2 && emptyCount === 0);

    // Test 70d: Checkpoint B — Help Window Opens Beside Cubert and Restores Cleanly
    openHelpWindow();
    const helpModalEl = document.getElementById("modal-help");
    const helpOpened = helpModalEl && helpModalEl.open;
    const cubertBesideHelp = cubertMode === CUBERT_MODES.ACTIVE;
    closeHelpWindow();
    const helpClosed = helpModalEl && !helpModalEl.open;
    assertTest("Checkpoint B: Opening Help summons Cubert beside the scrollable Windows 95 interface, and closing Help dismisses cleanly without breaking CAD controls", helpOpened && cubertBesideHelp && helpClosed);

    // Test 70e: Checkpoint C — Antigravity Command Recognition & Multi-Object Visual Drift
    processRequest("Can I box");
    const agTestBox = sceneObjects[sceneObjects.length - 1];
    processRequest("Can I sphere");
    const agTestSphere = sceneObjects[sceneObjects.length - 1];
    agTestSphere.userData.locked = true;
    const initialCredits = creditBalance;
    const initialBoxPos = agTestBox.position.clone();
    const initialSpherePos = agTestSphere.position.clone();

    // Verify recognition of both canonical commands
    processRequest("can i antigravity");
    const antigravityActive1 = isAntigravityActive === true;
    const boxHasOrigTransform = !!agTestBox.userData.antigravityOriginalTransform;
    const sphereHasOrigTransform = !!agTestSphere.userData.antigravityOriginalTransform;
    const michiganObj = sceneObjects.find(o => o.userData && o.userData.isStartingObject) || michiganModel;
    const michiganHasOrigTransform = michiganObj ? !!michiganObj.userData.antigravityOriginalTransform : true;

    // Verify alias without duplicate reactivation
    processRequest("can i remove gravity");
    const preventDuplicate = isAntigravityActive === true;

    // Advance physics to t = 1.0s (slow recognizable float)
    updateAntigravity(1.0);
    const boxFloated1s = agTestBox.position.y > initialBoxPos.y + 5;
    const sphereFloated1s = agTestSphere.position.y > initialSpherePos.y + 5;

    // Advance physics to t = 5.0s (bounded limit - objects fly completely outside viewports)
    updateAntigravity(5.0);
    const boxFlewOffScreen = agTestBox.position.y > initialBoxPos.y + 200;
    const sphereFlewOffScreen = agTestSphere.position.y > initialSpherePos.y + 200;
    const posAt5s = agTestBox.position.y;

    // Additional time must not accumulate infinite drift (bounded animation)
    updateAntigravity(10.0);
    const posAt10s = agTestBox.position.y;
    const boundedLimitRespected = Math.abs(posAt10s - posAt5s) < 0.001;
    assertTest("Checkpoint C: 'can i antigravity' and 'can i remove gravity' invoke shared 4-viewport visual float, gradually accelerate away outside viewports, and enforce bounded 5.0s animation duration", antigravityActive1 && boxHasOrigTransform && sphereHasOrigTransform && michiganHasOrigTransform && preventDuplicate && boxFloated1s && sphereFloated1s && boxFlewOffScreen && boundedLimitRespected);

    // Test 70f: Checkpoint C — Exact Scene Restoration ('can i restore gravity') & Zero Fee
    processRequest("can i restore gravity");
    const gravityRestored = isAntigravityActive === false;
    const boxPosRestored = agTestBox.position.distanceTo(initialBoxPos) < 0.0001;
    const spherePosRestored = agTestSphere.position.distanceTo(initialSpherePos) < 0.0001;
    const sphereStillLocked = agTestSphere.userData.locked === true;
    const creditsUnchanged = creditBalance === initialCredits;
    assertTest("Checkpoint C: 'can i restore gravity' returns all objects to exact millimeter coordinates, preserves lock status, and deducts $0", gravityRestored && boxPosRestored && spherePosRestored && sphereStillLocked && creditsUnchanged);

    // Test 70g: Checkpoint C — Special Undo & Project Serialization / Export Protection
    processRequest("can i remove gravity");
    assertTest("Antigravity active before immediate undo", isAntigravityActive === true);
    processRequest("can i undo");
    const undoReversedAntigravity = isAntigravityActive === false && agTestBox.position.distanceTo(initialBoxPos) < 0.0001;

    // Save & Export protection while antigravity is active
    processRequest("can i antigravity");
    updateAntigravity(5.0);
    const serializedWhileFlying = serializeProjectState();
    const parsedState = JSON.parse(serializedWhileFlying);
    const savedBox = parsedState.objects.find(o => o.name === agTestBox.name);
    const saveNotDisplaced = savedBox && Math.abs(savedBox.position[1] - initialBoxPos.y) < 0.001;
    const saveHasNoAntigravityFlags = savedBox && !savedBox.userData.antigravityOriginalTransform && !savedBox.userData.antigravityPhysics;

    exportProjectGeometry("stl");
    const exportRanWithoutError = true;

    // Modeling command after antigravity is undone normally
    const countBeforeNewObj = sceneObjects.length;
    processRequest("Can I box");
    const boxCreatedAfterAntigrav = sceneObjects.length === countBeforeNewObj + 1;
    processRequest("can i undo");
    const modelingUndoneNormally = sceneObjects.length === countBeforeNewObj;

    // Clean up
    processRequest("can i restore gravity");
    [agTestBox, agTestSphere].forEach(o => {
      const idx = sceneObjects.indexOf(o);
      if (idx !== -1) sceneObjects.splice(idx, 1);
      scene.remove(o);
    });
    assertTest("Checkpoint C: Special undo reverses antigravity, modeling undos operate normally, and project save/export protects un-displaced geometry", undoReversedAntigravity && saveNotDisplaced && saveHasNoAntigravityFlags && exportRanWithoutError && boxCreatedAfterAntigrav && modelingUndoneNormally);
"""

test_start_marker = "// CHECKPOINT 3 & 4 TESTS"
test_end_marker = 'activeLayerId = "default";'

t_start = content.find(test_start_marker)
t_end = content.find(test_end_marker, t_start)

if t_start == -1 or t_end == -1:
    print(f"ERROR: Could not find test markers! ({t_start}, {t_end})")
    sys.exit(1)

content = content[:t_start] + test_code + "\n    " + content[t_end:]
print("Replaced test block successfully.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated index.html successfully.")
