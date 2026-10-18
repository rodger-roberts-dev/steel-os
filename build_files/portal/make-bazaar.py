#!/usr/bin/env python3
"""Build the App Store's Curated page with Steel Apps at the top.

The App Store (Bazaar) shows the rows in /usr/share/ublue-os/bazaar/content.yaml
on its Curated page. This puts a Steel Apps banner and one section per Steel
Apps category first, then keeps the curated rows the base image already had.
Runs during the image build.

Usage: make-bazaar.py steel-apps.txt existing-content.yaml out.yaml
"""
import os
import sys

import yaml

APPS_FILE, EXISTING_FILE, OUT_FILE = sys.argv[1:4]

CATEGORIES = ["Everyday", "Work", "Creative", "Games and Streaming", "Developer", "AI"]
SUBTITLES = {
    "Everyday": "Browsing, email, files and reading",
    "Work": "Chat, meetings and notes",
    "Creative": "Photos, drawing, audio and video",
    "Games and Streaming": "Game stores, cloud gaming and chat",
    "Developer": "Code editors, terminals and virtual machines",
    "AI": "AI assistants, on your PC or online",
}
BANNER = "file:///usr/share/wallpapers/steel-os-waves/contents/images/3840x2160.png"

apps = {c: [] for c in CATEGORIES}
with open(APPS_FILE, encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4 or parts[3] not in apps:
            sys.exit(f"steel-apps.txt: bad line: {line}")
        apps[parts[3]].append(parts[0])

rows = [{
    "banner": {
        "height": 300,
        "image": {"uri": BANNER, "fit": "fill", "can-shrink": True, "alt": "Steel Apps"},
    }
}]
for category in CATEGORIES:
    if not apps[category]:
        continue
    rows.append({
        "section": {
            "title": {"en": f"Steel Apps: {category}"},
            "subtitle": {"string": {"en": SUBTITLES[category]}},
            "appids": {"list": apps[category]},
        }
    })

kept = 0
if os.path.isfile(EXISTING_FILE):
    with open(EXISTING_FILE, encoding="utf-8") as f:
        existing = yaml.safe_load(f) or {}
    for row in existing.get("rows", []):
        rows.append(row)
        kept += 1

out = yaml.safe_dump({"rows": rows}, allow_unicode=True, sort_keys=False)
if "bazzite" in out.lower():
    sys.exit("The App Store's Curated page would mention Bazzite")
yaml.safe_load(out)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("# Steel OS: the App Store's Curated page. Generated at build time by\n")
    f.write("# build_files/portal/make-bazaar.py from packages/steel-apps.txt.\n")
    f.write(out)
total = sum(len(v) for v in apps.values())
print(f"App Store Curated page: {total} Steel Apps in {sum(1 for v in apps.values() if v)} sections, "
      f"then {kept} rows from the base image")
