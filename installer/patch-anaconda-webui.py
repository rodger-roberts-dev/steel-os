#!/usr/bin/env python3
# Steel OS (STEEL-35): small changes to the Anaconda installer's web screens.
#
# 1. "Use entire disk" is preselected on the Installation method page.
#    Anaconda has no setting for this: it picks the first available option in
#    a fixed list, which is "Use free space" on any disk that already has
#    partitions. This makes "Use entire disk" the first choice when it is
#    available; the order on screen does not change.
# 2. The button on the last screen says "Finish" instead of "Exit to live
#    desktop". After it, Steel OS shows its own "Restart now" window
#    (installer/system_files/shared/usr/bin/steel-os-install-done).
#
# The installer ships as one minified JavaScript file whose variable names
# change between versions, so each change matches a pattern rather than exact
# names. If a pattern is not found, the installer keeps its own behavior and
# the build log says so; nothing breaks.
#
# Usage: patch-anaconda-webui.py [/usr/share/cockpit/anaconda-webui]

import gzip
import pathlib
import re
import sys

webui = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/usr/share/cockpit/anaconda-webui")
bundle = webui / "index.js.gz"
if not bundle.exists():
    print(f"Steel OS installer patch: {bundle} not found, skipped")
    sys.exit(0)

js = gzip.decompress(bundle.read_bytes()).decode("utf-8")
version = (webui / "VERSION.txt").read_text().strip() if (webui / "VERSION.txt").exists() else "unknown"
print(f"Steel OS installer patch: anaconda-webui version {version}")

# 1. Default to "Use entire disk" (scenario id "erase-all").
# Matches: s=Gc.find(d=>a[d.id].available&&!a[d.id].hidden)
default_pick = re.compile(
    r"(?P<lhs>[\w$]+)=(?P<list>[\w$]+)\.find\((?P<arg>[\w$]+)=>(?P<avail>[\w$]+)\[(?P=arg)\.id\]\.available&&!(?P=avail)\[(?P=arg)\.id\]\.hidden\)"
)
matches = list(default_pick.finditer(js))
if len(matches) == 1:
    m = matches[0]
    lhs, lst, arg, avail = m["lhs"], m["list"], m["arg"], m["avail"]
    usable = f"{avail}[{arg}.id].available&&!{avail}[{arg}.id].hidden"
    replacement = (
        f'{lhs}=({lst}.find({arg}=>{arg}.id==="erase-all"&&{usable})'
        f"||{lst}.find({arg}=>{usable}))"
    )
    js = js[: m.start()] + replacement + js[m.end():]
    print("Steel OS installer patch: 'Use entire disk' is now the default")
else:
    print(f"Steel OS installer patch: WARNING default-disk pattern found {len(matches)} times; not changed")

# 2. Last screen button label.
if js.count('"Exit to live desktop"') >= 1:
    js = js.replace('"Exit to live desktop"', '"Finish"')
    print("Steel OS installer patch: last button now says Finish")
else:
    print("Steel OS installer patch: WARNING 'Exit to live desktop' not found; not changed")

bundle.write_bytes(gzip.compress(js.encode("utf-8"), 9))
