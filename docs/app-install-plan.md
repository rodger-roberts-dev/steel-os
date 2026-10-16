# Application Installation Plan

Jira: STEEL-4
Date: 2026-10-15
Owners: T (which apps, what the user sees) and rodger-roberts-dev (how each is installed)

**How this was researched.** Every name in `packages/*.txt` was checked against
the official Arch package database, the Arch User Repository (AUR), and
Omarchy's own package repository on 2026-10-15. Omarchy's installer scripts
and menu definition were read to see what install paths already exist.

---

## 1. The one way to install apps (recommendation)

Product goal 4 says one install path, not five formats. Omarchy already has a
single front door: press **Super + Space**, choose **Install**, and pick from
Browser, Gaming, Service, Editor, Web App, Package, and so on. Each entry runs
a small installer script and shows progress in a floating window. The menu is
defined in a text file and can be extended without changing Omarchy's code.

**Recommendation: make the Omarchy Install menu the Steel OS app store.**

- Add a **Steel Apps** submenu listing the approved optional apps, one click
  each. Each entry runs Omarchy's own installer for that app.
- Keep Omarchy's Gaming, Browser, and Service entries as they are. They already
  cover Steam, Battle.net, Chrome, Firefox, Xbox controllers, Spotify, and more.
- Move the raw **Package** and **AUR** entries under an **Advanced** submenu so a
  non-technical user is not offered ten thousand package names.
- Do not add Flatpak, Snap, or AppImage. Every app on our lists is available
  without them.

### Why this and not the alternatives

| Option | Verdict |
|---|---|
| **Omarchy Install menu, curated by Steel OS** | **Recommended for the Hyprland session.** Zero new software to build. Uses installers Omarchy already tests. Theme-aware, keyboard and mouse friendly. |
| A graphical store (GNOME Software or KDE Discover with Flatpak) | Not as the main path. Adds a second package format, which is what goal 4 forbids. Flatpak apps also ignore Omarchy's theming. Fallback option on Plasma, see below. |
| A Steel OS store app built from scratch | Not a full store. But a small Plasma-native list of approved apps is cheap, see below. |

### Update after the desktop decision (2026-10-15)

T decided the default desktop is **KDE Plasma**, with Hyprland as a second
login option (ARCHITECTURE.md, decision 5.1). Omarchy's Install menu is part of
its Hyprland desktop shell, so **it does not exist on the Plasma session**. The
recommendation above still holds for Hyprland users. For Plasma, the default,
the single install path becomes:

| Option on Plasma | What it is | Verdict |
|---|---|---|
| **A. Steel Apps list** | A small Steel OS app with one row per approved app and an Install button. Each button runs the same Omarchy installer command listed in section 2. The list of apps is a text file shipped inside the steel-os package. | **Recommended.** Small to build, one format (pacman), uses Omarchy's tested installers, and the catalogue updates with every Steel OS update. |
| B. KDE Discover with Flatpak | KDE's own store app, showing Flatpak apps from Flathub. | Fallback if A is too much work. Familiar to Windows users, but it is a second package format, installs bypass Omarchy, and apps do not follow the system theme. |
| C. KDE Discover driving pacman directly | Discover with the PackageKit backend. | Rejected. The Arch wiki warns it is unreliable on Arch, and it would bypass Omarchy's update guard and installers. |

**Does the app store need a server?** No. Apps come from the Arch mirrors and
Omarchy's package repository, which Arch and Omarchy already host. Steel OS
only ships the list of approved apps and a button for each. There is nothing to
run on fly.io or anywhere else. The only hosting Steel OS will ever need is a
place to publish the steel-os package itself (roadmap phase 7), and that is a
static file on GitHub Releases, not a server.

---

## 2. Where every app comes from

Sources, in order of trust:
- **Arch official** (`core`, `extra`, `multilib`): maintained by Arch. Safest.
- **Omarchy Package Repository** (OPR, `pkgs.omarchy.org`): built and signed by
  Omarchy. Also safe. Installed with the same commands as Arch packages.
- **AUR**: community-uploaded build scripts. Not vetted. Avoid in defaults.
- **Not a package**: installed by an Omarchy script or added as a web app.

### Core (installed on every Steel OS machine)

| App | Package | Source | Note |
|---|---|---|---|
| WezTerm (terminal) | `wezterm` | Arch extra | Steel OS default terminal. Not in Omarchy base; Omarchy ships `foot`. |
| Neovim | `neovim` | Arch extra | Omarchy base ships it as `nvim` plus `omarchy-nvim` config. |
| Zed (editor) | `zed` | Arch extra | Omarchy has `omarchy install editor zed`. |
| Docker | `docker` | Arch extra | In Omarchy base. |
| OBS Studio | `obs-studio` | Arch extra | |
| Kdenlive (video editor) | `kdenlive` | Arch extra | Pulls in KDE libraries. Large. |
| Steam | `steam` | Arch multilib | **Install with `omarchy install gaming steam`**, not plain pacman: it picks the right 32-bit graphics drivers first, otherwise NVIDIA drivers land on non-NVIDIA machines. |
| Files (Nautilus) | `nautilus` | Arch extra | In Omarchy base. |
| btop (system monitor) | `btop` | Arch extra | In Omarchy base. |
| Disks | `gnome-disk-utility` | Arch extra | In Omarchy base. |

### Development

All 14 entries in `packages/development.txt` are in Arch `core` or `extra`.
`git`, `jq`, `ripgrep`, `fd`, `lazygit`, `docker-compose`, and `base-devel`
are already in the Omarchy base install.

### Optional (offered in the Steel Apps menu, not installed by default)

| App | Package or method | Source | How to install |
|---|---|---|---|
| Google Chrome (default browser) | `google-chrome` | **OPR** (also AUR) | `omarchy install browser chrome`, then `omarchy default browser chrome` |
| Firefox (for rodger-roberts-dev) | `firefox` | Arch extra | `omarchy install browser firefox` |
| Obsidian | `obsidian` | Arch extra | Already in Omarchy base |
| Discord | `discord` | Arch extra | `omarchy install app Discord discord` |
| Zoom | web app, or `zoom` | AUR only | **Recommend the web app**: Omarchy has a built-in handler that opens Zoom meeting links in a web app. The AUR package is the fallback for people who need the full desktop client. |
| Slack | `slack-desktop` | **OPR** (also AUR) | `omarchy install app Slack slack-desktop`. Omarchy's own menu already offers this. |
| Dropbox | `dropbox` (plus `dropbox-cli`, `nautilus-dropbox`) | **OPR** (also AUR) | `omarchy install service dropbox`. Note: its Omarchy top-bar plugin does not exist on Plasma; the Dropbox tray icon works there. |

**T's must-haves (2026-10-15):** Slack, Zoom, and Dropbox must each be a
one-click install, or at least an easy one. All three are covered: Slack and
Dropbox come from Omarchy's own repository with existing installers, and Zoom
works as a web app out of the box. They are the first three rows of the Steel
Apps list.
| Moonlight (game streaming) | `moonlight-qt` | Arch extra | Already in Omarchy base |
| Battle.net | not a package | Blizzard installer via `umu-launcher` (OPR) | `omarchy install gaming battlenet` |
| Google web apps (Gmail, Calendar, Drive, Docs) | not packages | web apps | `omarchy webapp install` with each URL. Omarchy fetches the icon. |
| Xbox controllers | `xpadneo-dkms` | OPR | `omarchy install gaming xbox-controllers` (goal 3) |

**Browser rule, from the README:** Chrome is the Steel OS default; Firefox is
installed for rodger-roberts-dev. Both can coexist. Note that Omarchy's web
apps open in a Chromium-family browser, so Chrome, not Firefox, must be present
on every machine that uses web apps.

---

## 3. Changes made to the package lists in this PR

`packages/core.txt` and `packages/development.txt`: **no changes**. Every name
is a real package in the official repositories, so the audit script should
print only `[OK]` or `[MISSING]` for them, never `[VERIFY]`.

`packages/optional.txt`: rewritten. Display names replaced with real package
names, a comment above each entry giving its source, and a comment pointing
here for the two items that are not packages (Battle.net, web apps).

`packages/review.txt`: each entry now has a comment with the recommended
decision. HEY and Basecamp, which are not packages, are explained in a comment.

`packages/excluded.txt`: comments added. `libreoffice-fresh` appears in both
`excluded.txt` and `review.txt`, which contradict each other. Left in both,
flagged, for T to decide.

---

## 4. Decisions needed from T and rodger-roberts-dev

These are the "Part 1" decisions the ticket assigns to people, not to Claude.

| Item | Recommendation | Why |
|---|---|---|
| `chromium` (review) | Remove **after** Chrome is installed and set as default | Omarchy ships it as the default browser; web apps need a Chromium-family browser, which Chrome satisfies. |
| `xournalpp` (review) | Remove | Handwriting and PDF annotation. Niche. |
| `pinta` (review) | **Keep** | A Windows user expects a Paint. |
| `libreoffice-fresh` (review and excluded) | **Keep** | "Easy like Windows" users open Word and Excel files. If removed, nothing on the system opens a `.docx`. |
| HEY, Basecamp (review) | Remove the web-app launchers | 37signals products most users will not have. `omarchy webapp remove HEY` and `omarchy webapp remove Basecamp`. |
| `foot` (excluded) | Remove only after WezTerm is the default terminal | Omarchy's terminal launcher must point at WezTerm first. |
| Zoom | Web app, not the AUR package | Keeps the AUR out of the default set. |

---

## 5. Verification

- Arch official repository check: done 2026-10-15 for all 46 entries using the
  Arch package search API. Results are in section 2.
- Omarchy Package Repository check: done 2026-10-15 by downloading the stable
  repository index (237 packages). `google-chrome`, `xpadneo-dkms`,
  `umu-launcher` confirmed present.
- AUR check: `zoom`, `google-chrome` confirmed present.
- **Not done:** running `scripts/bootstrap.sh` in an Omarchy VM. That is the
  acceptance test for T on the test machine. Expected result: only `[OK]` and
  `[MISSING]` lines, no `[VERIFY]`.

---

## 6. Follow-up tickets

1. **Steel Apps install menu.** Add a menu extension file
   (`~/.config/omarchy/extensions/omarchy-menu.jsonc`) shipped by Steel OS with
   the Steel Apps submenu and the Advanced submenu. Each entry calls the
   Omarchy installer command from section 2.
2. **Browser setup step.** A Steel OS setup script that installs Chrome and
   sets it as default, and installs Firefox when asked for. Idempotent.
3. **Extend the audit script** to read `optional.txt` and to recognise OPR
   packages, so `[VERIFY]` means "really unknown".
4. **Apply the review.txt decisions** once T and rodger-roberts-dev confirm
   them: a script that removes the agreed packages and web apps on a Steel OS
   machine, safe to run twice.
5. **Google web apps pack.** One command that adds Gmail, Calendar, Drive and
   Docs web apps with icons.
