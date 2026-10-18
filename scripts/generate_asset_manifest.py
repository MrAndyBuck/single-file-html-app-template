#!/usr/bin/env python3
"""
scripts/generate_asset_manifest.py

Automatically scans `assets/ads/` and `assets/audio/` to:
1. Generate `assets/manifest.json` containing all valid image (PNG, JPG, JPEG, WebP) and audio assets.
2. Update the `FILES` offline cache array in `sw.js`.
3. Update `ASSET_MANIFEST` in `index.html`.
4. Preserve exact filenames, extensions, and casing.
"""

import os
import sys
import json
import re
import urllib.parse

SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
SUPPORTED_AUDIO_EXTS = {".m4a", ".mp3", ".wav", ".ogg", ".aac"}

def get_project_root():
    current = os.path.abspath(os.path.dirname(__file__))
    parent = os.path.abspath(os.path.join(current, ".."))
    if os.path.exists(os.path.join(parent, "index.html")):
        return parent
    if os.path.exists(os.path.join(os.getcwd(), "index.html")):
        return os.getcwd()
    return parent

def scan_assets(root_dir):
    ads_dir = os.path.join(root_dir, "assets", "ads")
    audio_dir = os.path.join(root_dir, "assets", "audio")

    ads = []
    if os.path.isdir(ads_dir):
        for fname in sorted(os.listdir(ads_dir)):
            ext = os.path.splitext(fname)[1].lower()
            if ext in SUPPORTED_IMAGE_EXTS and not fname.startswith("."):
                ads.append(f"assets/ads/{fname}")

    audio = []
    if os.path.isdir(audio_dir):
        for fname in sorted(os.listdir(audio_dir)):
            ext = os.path.splitext(fname)[1].lower()
            if ext in SUPPORTED_AUDIO_EXTS and not fname.startswith("."):
                audio.append(f"assets/audio/{fname}")

    return ads, audio

def update_manifest_json(root_dir, ads, audio):
    manifest_path = os.path.join(root_dir, "assets", "manifest.json")
    manifest_data = {
        "ads": ads,
        "audio": audio
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
        f.write("\n")
    print(f"[MANIFEST] Updated {manifest_path} with {len(ads)} ads and {len(audio)} audio track(s).")

def update_sw_js(root_dir, ads, audio):
    sw_path = os.path.join(root_dir, "sw.js")
    if not os.path.exists(sw_path):
        print(f"[WARN] {sw_path} not found.")
        return

    with open(sw_path, "r", encoding="utf-8") as f:
        content = f.read()

    base_files = [
        '"./"',
        '"./index.html"',
        '"./manifest.webmanifest"',
        '"./icon.svg"',
        '"./vendor/three.min.js"',
        '"./vendor/three-csg.js"',
        '"./vendor/three-exporters.js"',
        '"./vendor/three-loaders.js"',
        '"./assets/manifest.json"'
    ]

    if os.path.exists(os.path.join(root_dir, "assets", "Finger.jpg")):
        base_files.append('"./assets/Finger.jpg"')

    ad_entries = [f'"./{ad}"' for ad in ads]
    audio_entries = [f'"./{urllib.parse.quote(a)}"' for a in audio]

    all_files_entries = base_files + ad_entries + audio_entries
    files_code = "const FILES = [\n  " + ",\n  ".join(all_files_entries) + "\n];"

    pattern = r"const FILES = \[\s*[\s\S]*?\s*\];"
    new_content = re.sub(pattern, files_code, content)

    if new_content != content:
        with open(sw_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[SW] Updated {sw_path} with {len(all_files_entries)} cached entries.")
    else:
        print(f"[SW] {sw_path} already up-to-date.")

def update_index_html(root_dir, ads, audio):
    index_path = os.path.join(root_dir, "index.html")
    if not os.path.exists(index_path):
        print(f"[WARN] {index_path} not found.")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    audio_encoded = [urllib.parse.quote(a) if " " in a else a for a in audio]

    manifest_js = "const ASSET_MANIFEST = {\n  ads: [\n"
    manifest_js += ",\n".join(f'    "{a}"' for a in ads)
    manifest_js += "\n  ],\n  audio: [\n"
    manifest_js += ",\n".join(f'    "{a}"' for a in audio_encoded)
    manifest_js += "\n  ]\n};"

    pattern = r"const ASSET_MANIFEST = \{[\s\S]*?\n\};"
    new_content = re.sub(pattern, manifest_js, content)

    # Ensure loadAssetManifest() exists
    if "function loadAssetManifest()" not in new_content:
        fetch_snippet = """
function loadAssetManifest() {
  if (typeof fetch !== "undefined") {
    fetch("./assets/manifest.json?t=" + Date.now())
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && Array.isArray(data.ads) && data.ads.length > 0) {
          ASSET_MANIFEST.ads = data.ads;
        }
        if (data && Array.isArray(data.audio) && data.audio.length > 0) {
          ASSET_MANIFEST.audio = data.audio;
        }
      })
      .catch(() => {});
  }
}
loadAssetManifest();
"""
        new_content = new_content.replace(manifest_js, manifest_js + "\n" + fetch_snippet)

    # Update Test 33 assertion
    new_content = re.sub(
        r'assertTest\("Asset manifest loaded with.*?",.*?\);',
        f'assertTest("Asset manifest loaded with {len(ads)} ads and hold music track", ASSET_MANIFEST.ads.length === {len(ads)} && ASSET_MANIFEST.audio.length >= 1);',
        new_content
    )

    if new_content != content:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[HTML] Updated {index_path} with {len(ads)} ads.")
    else:
        print(f"[HTML] {index_path} already up-to-date.")

def main():
    root_dir = get_project_root()
    ads, audio = scan_assets(root_dir)
    print(f"[SCAN] Found {len(ads)} advertisement(s):")
    for a in ads:
        print(f"  - {a}")
    print(f"[SCAN] Found {len(audio)} audio track(s):")
    for au in audio:
        print(f"  - {au}")

    update_manifest_json(root_dir, ads, audio)
    update_sw_js(root_dir, ads, audio)
    update_index_html(root_dir, ads, audio)
    print("\n[SUCCESS] Asset registration complete!")

if __name__ == "__main__":
    main()
