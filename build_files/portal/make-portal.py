#!/usr/bin/env python3
"""Build the Steel OS Portal settings file.

Reads the one-click app list (packages/steel-apps.txt) and the tabs adapted
from Bazzite Portal (portal/base.yml), and writes the file the portal app
opens: /usr/share/steel-os/portal.yml. Runs during the image build.
"""
import json
import sys

import yaml

APPS_FILE, BASE_FILE, OUT_FILE = sys.argv[1:4]

PAUSE = '; status=$?; echo; echo "Press Enter to close..."; read -r _; exit $status'


def q(text):
    """Quote a string for YAML (JSON strings are valid YAML)."""
    return json.dumps(text, ensure_ascii=False)


def action(id_, title, description, script=None, status_script=None, options=None):
    lines = [
        f"      - id: {q(id_)}",
        f"        title: {q(title)}",
        f"        description: {q(description)}",
        "        default: false",
    ]
    if status_script:
        lines.append(f"        status_script: {q(status_script)}")
    if script:
        lines.append(f"        script: {q(script)}")
    if options:
        lines.append("        options:")
        for opt_id, label, opt_script in options:
            lines += [
                f"          - id: {q(opt_id)}",
                f"            label: {q(label)}",
                f"            script: {q(opt_script)}",
            ]
    return lines


def screen(title, description, actions):
    lines = [f"  - title: {q(title)}", f"    description: {q(description)}", "    actions:"]
    for a in actions:
        lines += a
    return lines


def flatpak_action(app_id, name, description):
    return action(
        f"steel-app-{app_id}",
        name,
        f"{description}. One click, from Flathub.",
        status_script=f"flatpak info {app_id} >/dev/null 2>&1 && echo install || echo uninstall",
        options=[
            ("install", f"Install {name}", f"flatpak install -y flathub {app_id}{PAUSE}"),
            ("uninstall", f"Uninstall {name}", f"flatpak uninstall -y {app_id}{PAUSE}"),
        ],
    )


BREW = 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" && '

welcome = screen("Welcome", "Get started with Steel OS", [
    action("steel-os-website", "Visit steel-os.org",
           "News, help and downloads for Steel OS.",
           script="xdg-open https://steel-os.org"),
    action("app-store", "Open the App Store",
           "Browse thousands more apps. Everything installs with one click.",
           script="nohup setsid gtk-launch io.github.kolunmi.Bazaar >/dev/null 2>&1"),
    action("keyboard-shortcuts", "See and change keyboard shortcuts",
           "Super+Enter opens the terminal, Super+Shift+Enter opens Firefox, Super+1 to 4 switch desktops.",
           script="nohup setsid systemsettings kcm_keys >/dev/null 2>&1"),
    action("printers", "Printers and scanners",
           "Add a printer (most are found in one click, USB printers set themselves up), or scan a document.",
           script="nohup setsid systemsettings kcm_printer_manager >/dev/null 2>&1"),
    action("update-now", "Update now",
           "Steel OS updates itself every Tuesday. Run an update right now instead.",
           script="ujust update" + PAUSE),
    action("help", "Get help",
           "Plain-English help pages: apps, updates, printers, shortcuts, gaming and fixes. Works offline.",
           script="nohup setsid /usr/libexec/steel-os-help >/dev/null 2>&1"),
    action("security-questions", "Security questions",
           "Set up or change the three questions that let you reset a forgotten password from the login screen.",
           script="nohup setsid /usr/libexec/steel-os-recovery-setup >/dev/null 2>&1"),
    action("setup-again", "Run Steel OS Setup again",
           "The first-login welcome steps: updates, choosing apps and printers.",
           script="nohup setsid /usr/libexec/steel-os-setup --again >/dev/null 2>&1"),
    action("report-problem", "Report a problem",
           "Tell the Steel OS team what went wrong.",
           script="xdg-open https://steel-os.org/report"),
])

CATEGORIES = ["Everyday", "Work", "Creative", "Games and Streaming", "Developer"]


def read_steel_apps(path):
    """Return {category: [(id, name, description), ...]} in file order."""
    found = {c: [] for c in CATEGORIES}
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                sys.exit(f"steel-apps.txt: expected 'id | name | description | category': {line}")
            app_id, name, description, category = parts
            if category not in found:
                sys.exit(f"steel-apps.txt: unknown category '{category}' for {app_id}")
            found[category].append((app_id, name, description))
    return found


TWITCH_DESKTOP = "$HOME/.local/share/applications/steel-os-twitch.desktop"
TWITCH_INSTALL = (
    'mkdir -p "$HOME/.local/share/applications" && printf "%s\n" '
    '"[Desktop Entry]" "Type=Application" "Name=Twitch" '
    '"Comment=Watch live streams on twitch.tv" '
    '"Exec=xdg-open https://www.twitch.tv" "Icon=applications-multimedia" '
    '"Categories=AudioVideo;Video;" > "' + TWITCH_DESKTOP + '" && '
    'echo "Twitch is now in your start menu."' + PAUSE
)

# Extra one-click entries that are not Flatpaks, added to a category.
EXTRAS = {
    "Games and Streaming": [action(
        "twitch", "Twitch",
        "Games and Streaming · Watch live streams. Twitch has no Linux app, so this adds a Twitch launcher that opens it in your browser.",
        status_script=f'test -f "{TWITCH_DESKTOP}" && echo install || echo uninstall',
        options=[
            ("install", "Add Twitch to the start menu", TWITCH_INSTALL),
            ("uninstall", "Remove Twitch from the start menu", f'rm -f "{TWITCH_DESKTOP}"' + PAUSE),
        ],
    )],
    "Developer": [action(
        "antigravity", "Antigravity",
        "Developer · Google's AI coding app and IDE. One click, installed with Brew.",
        status_script="test -d /home/linuxbrew/.linuxbrew/Caskroom/antigravity-linux && echo install || echo uninstall",
        options=[
            ("install", "Install Antigravity",
             BREW + "brew trust ublue-os/tap && brew tap ublue-os/tap && brew install --cask antigravity-linux" + PAUSE),
            ("uninstall", "Uninstall Antigravity",
             BREW + "brew uninstall --cask antigravity-linux" + PAUSE),
        ],
    )],
}

apps = []
for category, entries in read_steel_apps(APPS_FILE).items():
    for app_id, name, description in entries:
        apps.append(flatpak_action(app_id, name, f"{category} · {description}"))
    apps.extend(EXTRAS.get(category, []))

steel_apps = screen("Steel Apps", "Popular apps by category, one click each", apps)

with open(BASE_FILE, encoding="utf-8") as f:
    base = "".join(l for l in f if not l.startswith("#"))

out = "\n".join(["title: Steel OS Portal", "screens:"] + welcome + steel_apps) + "\n" + base

# Fail the build rather than ship a broken or Bazzite-branded portal.
parsed = yaml.safe_load(out)
titles = [s["title"] for s in parsed["screens"]]
if "bazzite" in out.lower():
    sys.exit("portal.yml still mentions Bazzite")
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(out)
print(f"Steel OS Portal: {len(apps)} Steel Apps; tabs: {', '.join(titles)}")
