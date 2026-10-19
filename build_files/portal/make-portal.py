#!/usr/bin/env python3
"""Build the Steel OS Portal settings file.

Reads the one-click app list (packages/steel-apps.txt) and the tabs adapted
from Bazzite Portal (portal/base.yml), and writes the file the portal app
opens: /usr/share/steel-os/portal.yml. Runs during the image build.
"""
import shlex
import json
import os
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
        # Buttons that only open an app or a web page don't need a terminal
        # window (T, 2026-10-18: Steel Shield opened Konsole too). Needs the
        # "terminal: false" support build.sh adds to the Portal program.
        if script.startswith(("nohup setsid ", "xdg-open ")):
            lines.append("        terminal: false")
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
    # A small window, not a terminal (T, 2026-10-19): "Installing Name… 45%",
    # then "Name is installed" with an Open button. setsid -w waits, so the
    # Portal refreshes the row's Installed / Not installed when it's done.
    def run(verb):
        return f"nohup setsid -w /usr/libexec/steel-os-app {verb} {app_id} {shlex.quote(name)} >/dev/null 2>&1"
    return action(
        f"steel-app-{app_id}",
        name,
        f"{description}. One click, from Flathub.",
        status_script=f"flatpak info {app_id} >/dev/null 2>&1 && echo install || echo uninstall",
        options=[
            ("install", f"Install {name}", run("install")),
            ("open", f"Open {name}", run("open")),
            ("uninstall", f"Uninstall {name}", run("uninstall")),
        ],
    )


BREW = 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" && '

welcome = screen("Welcome", "Get started with Steel OS", [
    # Order (T, 2026-10-18): website, help, update, report a problem, then the rest.
    action("steel-os-website", "Visit steel-os.org",
           "News, help and downloads for Steel OS.",
           script="xdg-open https://steel-os.org"),
    action("help", "Get help",
           "Plain-English help pages: apps, updates, printers, shortcuts, gaming and fixes. Works offline.",
           script="nohup setsid /usr/libexec/steel-os-help >/dev/null 2>&1"),
    action("update-now", "Update now",
           "Steel OS updates itself every Tuesday. Run an update right now instead.",
           script="nohup setsid /usr/libexec/steel-os-update-now >/dev/null 2>&1"),
    action("report-problem", "Report a problem or idea",
           "Tell the Steel OS team what went wrong or what you would like, with a screenshot. No account needed.",
           script="nohup setsid /usr/libexec/steel-os-report >/dev/null 2>&1"),
    action("app-store", "Open the App Store",
           "Browse thousands more apps. Everything installs with one click.",
           script="nohup setsid gtk-launch io.github.kolunmi.Bazaar >/dev/null 2>&1"),
    action("keyboard-shortcuts", "See and change keyboard shortcuts",
           "Super+Enter opens the terminal, Super+Shift+Enter opens Firefox, Super+1 to 4 switch desktops.",
           script="nohup setsid systemsettings kcm_keys >/dev/null 2>&1"),
    action("printers", "Printers and scanners",
           "Add a printer (most are found in one click, USB printers set themselves up), or scan a document.",
           script="nohup setsid systemsettings kcm_printer_manager >/dev/null 2>&1"),
    action("steel-shield", "Steel Shield (virus protection)",
           "See your protection, scan a file or folder, and manage quarantine. Downloads are scanned automatically.",
           script="nohup setsid /usr/bin/steel-shield >/dev/null 2>&1"),
    action("security-questions", "Security questions",
           "Set up or change the three questions that let you reset a forgotten password from the login screen.",
           script="nohup setsid /usr/libexec/steel-os-recovery-setup >/dev/null 2>&1"),
    action("night-restart", "Automatic restarts for updates",
           "When an update is waiting, Steel OS restarts between 2 and 5 am, only if nobody is using the computer and no game is running, with a 15-minute warning.",
           status_script='test -f "$HOME/.config/steel-os/no-night-restart" && echo off || echo on',
           options=[
               ("on", "On: restart at night when it's safe",
                'rm -f "$HOME/.config/steel-os/no-night-restart" && echo "Automatic restarts are on."' + PAUSE),
               ("off", "Off: I'll restart myself",
                'mkdir -p "$HOME/.config/steel-os" && touch "$HOME/.config/steel-os/no-night-restart" && echo "Automatic restarts are off."' + PAUSE),
           ]),
    action("setup-again", "Run Steel OS Setup again",
           "The first-login welcome steps: updates, choosing apps and printers.",
           script="nohup setsid /usr/libexec/steel-os-setup --again >/dev/null 2>&1"),
])

CATEGORIES = ["Everyday", "Work", "Creative", "Games and Streaming", "Developer", "AI"]


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

def web_launcher(id_, name, url, description, category="AI"):
    """One click adds a start-menu entry that opens the site in the browser."""
    desktop = f"$HOME/.local/share/applications/steel-os-{id_}.desktop"
    install = (
        'mkdir -p "$HOME/.local/share/applications" && printf "%s\n" '
        f'"[Desktop Entry]" "Type=Application" "Name={name}" '
        f'"Comment={description}" '
        f'"Exec=xdg-open {url}" "Icon=internet-web-browser" '
        f'"Categories=Network;Office;" > "{desktop}" && '
        f'echo "{name} is now in your start menu."' + PAUSE
    )
    return action(
        id_, name,
        f"{category} · {description}. Adds {name} to the start menu; it opens in your web browser.",
        status_script=f'test -f "{desktop}" && echo install || echo uninstall',
        options=[
            ("install", f"Add {name} to the start menu", install),
            ("uninstall", f"Remove {name} from the start menu", f'rm -f "{desktop}"' + PAUSE),
        ],
    )


# Extra one-click entries that are not Flatpaks, added to a category.
EXTRAS = {
    # OneDrive has no Linux app from Microsoft (T, 2026-10-18): the web version
    # here, and RClone Manager in steel-apps.txt shows it as a folder.
    "Everyday": [
        web_launcher("onedrive", "OneDrive", "https://onedrive.live.com",
                     "Microsoft OneDrive in your browser: your files, plus Word, Excel and PowerPoint online", "Everyday"),
    ],
    "AI": [
        web_launcher("copilot", "Microsoft Copilot", "https://copilot.microsoft.com", "Microsoft's AI assistant (free; sign in with a Microsoft account for more)"),
        web_launcher("chatgpt", "ChatGPT", "https://chatgpt.com", "OpenAI's AI assistant (free tier, or your subscription)"),
        web_launcher("claude", "Claude", "https://claude.ai", "Anthropic's AI assistant (free tier, or your subscription)"),
        web_launcher("gemini", "Gemini", "https://gemini.google.com", "Google's AI assistant (free with a Google account)"),
    ],
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

# Steel & Code Forge (STEEL-25): a one-click entry once its public package
# address is in packages/forge-source.txt; hidden while that file is empty.
FORGE_SOURCE = os.path.join(os.path.dirname(os.path.abspath(APPS_FILE)), "forge-source.txt")
if os.path.exists(FORGE_SOURCE) and any(
        l.strip() and not l.strip().startswith("#") for l in open(FORGE_SOURCE, encoding="utf-8")):
    EXTRAS["Developer"].append(action(
        "steel-and-code-forge", "Steel & Code Forge",
        "Developer · Steel & Code's AI agents in one terminal: Byte (software engineering), Neighbor "
        "(general assistant), the Forge terminal interface and the browser Workbench, with optional Hermes. "
        "Every command an agent wants to run goes through Forge's safety checks first. Early alpha. "
        "Needs an OpenRouter key; the installer asks for it.",
        status_script="/usr/libexec/steel-os-forge status | grep -qx installed && echo install || echo uninstall",
        options=[
            ("install", "Install Steel & Code Forge", "/usr/libexec/steel-os-forge install" + PAUSE),
            ("uninstall", "Uninstall Steel & Code Forge", "/usr/libexec/steel-os-forge uninstall" + PAUSE),
        ],
    ))
    print("Steel OS Portal: Steel & Code Forge listed")
else:
    print("Steel OS Portal: Steel & Code Forge not listed yet (packages/forge-source.txt is empty)")

# Developer apps get their own tab (T, 2026-10-17): code editors, AI coding
# tools and virtual machines. The other categories stay on Steel Apps.
apps = []
developer = []
ai = []
for category, entries in read_steel_apps(APPS_FILE).items():
    target = developer if category == "Developer" else ai if category == "AI" else apps
    for app_id, name, description in entries:
        target.append(flatpak_action(app_id, name, f"{category} · {description}"))
    target.extend(EXTRAS.get(category, []))
# Zed is installed by default; listing it here lets people remove or reinstall it.
developer.insert(0, flatpak_action("dev.zed.Zed", "Zed", "Developer · Fast code editor, installed by default (zeditor in a terminal)"))

# Gaming tab (STEEL-32, STEEL-45, STEEL-46): devices, macros and game fixes.
def launch(cmd):
    return f"nohup setsid {cmd} >/dev/null 2>&1"


gaming = screen("Gaming", "Controllers, flight sticks, macros and game fixes", [
    action("controller-test", "Test a controller or flight stick",
           "See every button, axis and hat respond: gamepads, flight sticks such as the X52 and X56, throttles and pedals.",
           script=launch("jstest-gtk")),
    action("macros", "Macros for keyboards, mice, keypads and controllers",
           "Remap any key or button and record macros (Input Remapper): gaming keyboards and mice, Razer Tartarus, Nostromo N52 and other keypads, controllers.",
           script=launch("input-remapper-gtk")),
    action("antimicrox", "Use a controller in keyboard-and-mouse games",
           "Map controller buttons and sticks to keys and the mouse (AntiMicroX), for games without controller support.",
           script=launch("antimicrox")),
    action("logitech", "Logitech wireless keyboards and mice",
           "Pair devices to a Logitech receiver, check battery levels and change settings (Solaar).",
           script=launch("solaar")),
    action("razer", "Razer devices",
           "Lights, keys and DPI for Razer keyboards, mice and keypads such as the Tartarus (OpenRazer with Polychromatic).",
           status_script="ujust install-openrazer status",
           options=[
               ("install", "Install Razer support",
                "ujust install-openrazer install-polychromatic" + PAUSE),
               ("uninstall", "Remove Razer support", "ujust install-openrazer uninstall" + PAUSE),
           ]),
    action("star-citizen", "Star Citizen: install or update the LUG Helper",
           "The community tool that installs Star Citizen and keeps it working after patches. Adds \"Star Citizen LUG Helper\" to the start menu.",
           script="/usr/libexec/steel-os-lug-helper" + PAUSE),
    action("repair-star-citizen", "Repair Star Citizen",
           "Clears shader and DXVK caches, the usual fix for crashes or stutter after a patch. Your game and settings are kept.",
           script=launch("/usr/libexec/steel-os-repair-game star-citizen")),
    action("repair-battlenet", "Repair Battle.net and World of Warcraft",
           "Clears Battle.net's own files and WoW's cache, the usual fix when Battle.net won't open or WoW won't start after a patch.",
           script=launch("/usr/libexec/steel-os-repair-game battlenet")),
    action("proton-ge", "Get the newest GE-Proton",
           "GE-Proton runs many Windows games better than the default, including Battle.net games. Opens ProtonPlus (installs it first if needed).",
           script="flatpak info com.vysp3r.ProtonPlus >/dev/null 2>&1 || flatpak install -y flathub com.vysp3r.ProtonPlus; nohup setsid flatpak run com.vysp3r.ProtonPlus >/dev/null 2>&1"),
])

steel_apps = screen("Steel Apps", "Popular apps by category, one click each", apps)
developer_tab = screen("Developer", "Code editors, AI coding tools and virtual machines, one click each", developer)
ai_tab = screen("AI", "AI assistants: private ones that run on your PC, and Copilot, ChatGPT, Claude and Gemini", ai)

with open(BASE_FILE, encoding="utf-8") as f:
    base = "".join(l for l in f if not l.startswith("#"))

out = "\n".join(["title: Steel OS Portal", "screens:"] + welcome + steel_apps + ai_tab + developer_tab + gaming) + "\n" + base

# Fail the build rather than ship a broken or Bazzite-branded portal.
parsed = yaml.safe_load(out)
titles = [s["title"] for s in parsed["screens"]]
if "bazzite" in out.lower():
    sys.exit("portal.yml still mentions Bazzite")
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(out)
print(f"Steel OS Portal: {len(apps)} Steel Apps, {len(ai)} AI apps, {len(developer)} developer apps; tabs: {', '.join(titles)}")
