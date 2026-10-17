#!/usr/bin/env python3
"""Steel OS login theme: Plasma's Breeze login screen plus "Forgot your password?".

Copies /usr/share/sddm/themes/breeze to /usr/share/sddm/themes/steel-os and
adds one button next to Restart (STEEL-36). The first click arms it ("Click
again to restart into password reset"); the second writes a request note to
/var/lib/steel-os/recovery-request/request and restarts the PC with the login
screen's own restart. The boot-time service steel-os-recovery-reset does the
rest. The login screen gets no other new abilities.

The note is written with QML's XMLHttpRequest, which needs the greeter
environment QML_XHR_ALLOW_FILE_WRITE=1 (set by build.sh).

Prints "OK" and exits 0 when the theme was made. If Breeze's layout ever
changes so the Restart button can't be found, it exits 2 and the build keeps
the plain Breeze theme.
"""
import re
import shutil
import sys
from pathlib import Path

SRC = Path("/usr/share/sddm/themes/breeze")
DST = Path("/usr/share/sddm/themes/steel-os")

if not (SRC / "Main.qml").is_file():
    print("Steel OS login theme: Breeze theme not found")
    sys.exit(2)

main = (SRC / "Main.qml").read_text(encoding="utf-8")

# A Restart ActionButton: from "ActionButton {" to its closing "}," at the
# same indent, containing sddm.reboot() and no other ActionButton.
restart = re.compile(
    r"(?P<indent>^[ \t]*)ActionButton \{\n"
    r"(?:(?!ActionButton)[\s\S])*?sddm\.reboot\(\)"
    r"(?:(?!ActionButton)[\s\S])*?\n(?P=indent)\},?",
    re.MULTILINE,
)

def button(indent):
    i = indent
    return f"""
{i}ActionButton {{
{i}    // Steel OS (STEEL-36): forgotten password. First click arms, second restarts.
{i}    icon.name: "dialog-password"
{i}    text: root.steelResetArmed ? "Click again to restart into password reset" : "Forgot your password?"
{i}    enabled: sddm.canReboot
{i}    onClicked: {{
{i}        if (!root.steelResetArmed) {{
{i}            root.steelResetArmed = true;
{i}            root.notificationMessage = "Your PC will restart into password reset, where you answer your security questions.";
{i}            return;
{i}        }}
{i}        var xhr = new XMLHttpRequest();
{i}        xhr.onreadystatechange = function() {{
{i}            if (xhr.readyState === XMLHttpRequest.DONE) {{
{i}                sddm.reboot();
{i}            }}
{i}        }};
{i}        xhr.open("PUT", "file:///var/lib/steel-os/recovery-request/request");
{i}        xhr.send("reset");
{i}    }}
{i}}},"""

matches = list(restart.finditer(main))
if not matches:
    print("Steel OS login theme: Restart button not found; keeping Breeze")
    sys.exit(2)

out = []
last = 0
for m in matches:
    block = m.group(0)
    if not block.endswith(","):
        block += ","
    out.append(main[last:m.start()])
    out.append(block + button(m.group("indent")))
    last = m.end()
out.append(main[last:])
patched = "".join(out)

# The "armed" flag on the root item.
root_id = re.compile(r"^(?P<indent>[ \t]*)id: root\n", re.MULTILINE)
rm = root_id.search(patched)
if not rm:
    print("Steel OS login theme: root item not found; keeping Breeze")
    sys.exit(2)
patched = (patched[: rm.end()]
           + f"{rm.group('indent')}property bool steelResetArmed: false  // Steel OS (STEEL-36)\n"
           + patched[rm.end():])

if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, symlinks=True)
(DST / "Main.qml").write_text(patched, encoding="utf-8")

meta = DST / "metadata.desktop"
if meta.is_file():
    text = meta.read_text(encoding="utf-8")
    text = re.sub(r"^Name=.*$", "Name=Steel OS", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^Theme-Id=.*$", "Theme-Id=steel-os", text, count=1, flags=re.MULTILINE)
    meta.write_text(text, encoding="utf-8")

print(f"Steel OS login theme: Forgot your password? added next to {len(matches)} Restart button(s)")
print("OK")
