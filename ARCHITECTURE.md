# Steel OS Architecture

This document describes Steel OS as it actually exists in this repository on
2026-10-15. It is written for everyone on the project, including people who do
not write code. Where something does not exist yet, it says so plainly.


---

## 1. What Steel OS is

Steel OS is a **Steel & Code** (steelandcode.com) project, made in partnership
with **Blackbox Entertainment**. Say it that way on anything public.

Steel OS is a Linux operating system for everyday people. It is built as a
**custom image on top of Bazzite**, the Fedora Atomic gaming desktop made by
Universal Blue, using their image template. Bazzite gives us a working KDE
Plasma desktop, an installer, whole-image updates with rollback, and gaming
support out of the box. Steel OS adds the choices, apps, and polish that make
it suitable for a non-technical person. Decided 2026-10-15 (section 5.5);
before that the project was based on Omarchy (Arch + Hyprland).

Steel OS is **not** a fork of Fedora or of Bazzite. It is a short recipe
(section 3) that starts from Bazzite's image and adds our files on top. Every
Steel OS machine runs that one image and updates to the next one as a whole.

### Product goals, in priority order

1. **Safe updates.** Users never get raw package updates. The whole system
   updates as one tested image, automatically every Tuesday, and the previous
   version is always in the boot menu.
2. **Easy like Windows.** A non-technical user must be able to install the OS,
   update it, connect a printer, find network computers, and install apps
   without ever opening a terminal.
3. **Plays games.** Steam and Proton work out of the box. Controllers just work.
4. **One way to install apps.** A single app store or install path, not five
   competing formats.
5. **Built-in security.** Protection is part of the OS, not a third-party add-on.

### Who does what

| Person | Role |
|---|---|
| Steel & Code (S&C) | Project lead. Owns the repo. Final say on every merge. |
| Blackbox Entertainment (BBE) | Product director. Plans the work, tests builds, reviews behaviour. Not a coder. |
| Claude Code | Development assistant. Works only on branches, opens pull requests, never merges. Rules are in `CLAUDE.md`. |

---

## 2. What Bazzite provides vs. what Steel OS adds

Bazzite is the foundation. Everything in the left column already works on a
fresh Bazzite install without any Steel OS code. Steel OS is a thin layer on
top, built as one image.

| Bazzite provides | Steel OS adds (today, version 0.2) | Steel OS will add (planned) |
|---|---|---|
| Fedora Atomic base: the whole system is one image, updated as one, previous version always in the boot menu | The image recipe: `Containerfile`, `build_files/build.sh`, `system_files/` | Tuesday update schedule and plain-English update messages |
| KDE Plasma desktop | S&C's keyboard shortcuts, cascading windows, Konsole as the terminal | Steel OS wallpaper, login screen, boot splash, name in About |
| Automatic updates (`uupd`) for the system, Flatpaks and more | Extra rpm packages: printer drivers and Windows network discovery (`packages/image.txt`) | Guided install and a first-login wizard with Skip |
| Steam, Proton, controller support, Lutris, Waydroid | Our signing key in the image | Steel Apps one-click list built on Bazzite Portal |
| Discover app store with Flatpak | GitHub workflows that build the image daily and the ISO on demand | Printers, scanners and folder sharing without a terminal |
| Bazzite Portal first-login installer | Installer ISO settings (`disk_config/iso.toml`) | One ISO with graphics card detection |
| Secure Boot support, firewall, sandboxed apps | | Security policy and emergency fix path |

The honest summary: **today Steel OS is Bazzite plus our settings files, a
few packages and a signing key, built into an image by GitHub.** That is on
purpose. The less we change, the safer Bazzite's updates are for our users.

---

## 3. How the repository is laid out

```
steel-os/
├── Containerfile             Start from Bazzite, run the build script
├── build_files/
│   └── build.sh              Copies system_files in, installs packages/image.txt, adds the signing key
├── system_files/             Files copied to / in the image, same paths
│   └── etc/
│       ├── xdg/              Plasma defaults: kglobalshortcutsrc, kwinrc, kdeglobals
│       └── containers/registries.d/steel-os.yaml   Where our image signatures live
├── packages/
│   ├── image.txt             rpm packages built into the image
│   ├── flatpaks-default.txt  Apps installed for everyone at first boot
│   ├── steel-apps.txt        The one-click list
│   ├── brew.txt              Command-line tools for developers
│   └── remove.txt            Bazzite things Steel OS leaves out
├── disk_config/
│   ├── iso.toml              Installer settings; points installed machines at our image
│   └── disk.toml             Virtual machine disk settings
├── .github/workflows/
│   ├── build.yml             Build, push and sign the image: PRs, master, daily
│   └── build-disk.yml        Build the ISO and VM disk by hand; optional upload to R2
├── Justfile                  The build commands the workflows call; also works on a Linux PC
├── image-template.env        Image name, owner, description
├── cosign.pub                Public signing key (private half is a GitHub secret, never here)
├── branding/                 Logo, icon, wallpapers and the brand guide
├── docs/                     Plans and research, including docs/building.md
├── README.md, ARCHITECTURE.md, CLAUDE.md, .claude/agents/steel-dev.md
└── .gitignore                Ignores cosign.key and local build output
```

### Each piece, in plain English

**`Containerfile` and `build_files/build.sh`: the recipe.** The Containerfile
says "start from `ghcr.io/ublue-os/bazzite:stable`" and runs `build.sh` once
inside the build. The script copies `system_files/` onto the image, installs
every package named in `packages/image.txt`, and places our public signing
key. Nothing in Bazzite is edited; our files are added next to theirs.

**`system_files/`: our settings.** Laid out exactly as they land on a machine.
Each file starts with a comment saying what it does. Examples: the Plasma
shortcut defaults, the wallpaper and lock screen settings, the update
schedule and the signature location file.

**`packages/*.txt`: the lists.** One name per line, `#` for comments.
`image.txt` is the only one the build reads today. The Flatpak and Steel Apps
lists are read at first boot and by the Steel Apps screen.

**`disk_config/`: how the ISO is made.** `iso.toml` holds the installer
settings and the one command that, after install, points the machine at our
image for updates. `disk.toml` sizes the virtual machine disk.

**`.github/workflows/`: the builders.** GitHub builds the image on every pull
request and every push to `master`, and once a day so Bazzite's fixes flow
through. The ISO is built by hand from the Actions tab. See
`docs/building.md`.

**`cosign.pub`: who signed this.** The public half of the Steel OS signing
key. The private half lives only in the `SIGNING_SECRET` GitHub secret and in
the project's password managers.

**`CLAUDE.md` and `.claude/agents/steel-dev.md`: rules for the AI assistant.**
Not part of the OS. They tell Claude Code how this team works.

### What is not here yet

- No first-boot script: default Flatpaks are not installed automatically.
- No Steel OS look: wallpaper, login screen, name in About still say Bazzite.
- No Tuesday schedule: updates run on Bazzite's daily timer.
- No guided installer or first-login wizard.
- Signature checking of updates is not enforced yet; the key is in the image
  but `/etc/containers/policy.json` does not require it.
- No release workflow: the ISO upload is a manual button.

---

## 4. How a change gets from a planned task to a user's machine

```
Planned task  →  branch  →  pull request (GitHub builds the image as the test)
                                │
                     S&C reviews, merges to master
                                │
            GitHub builds again, pushes ghcr.io/steel-and-code/steel-os:latest, signs it
                                │
        every Steel OS machine fetches it on the next update run and applies it on restart
                                │
             previous image stays in the boot menu in case anything broke
```

1. The work is planned in the project's private tracker, or arrives as a GitHub issue.
2. A branch is created for the change.
3. The change is made and a pull request is opened. GitHub builds the image;
   a pull request whose image does not build does not merge. The PR says what
   changed, why, and how to test it in plain English.
4. BBE tests it in the VM from an ISO built on the Actions tab, or on the test
   machine Command. S&C reviews and merges.
5. The merge builds, pushes and signs the image. Machines pick it up on their
   next update run. Nothing is copied by hand.

The ISO is only for the first install. After that the machine updates itself
from the image; the ISO is never needed again.

---

## 5. Decisions

These four questions were open when this document was first written. BBE
answered all four on 2026-10-15. Each answer is a product decision;
S&C reviews the technical consequences before anything is built.

### 5.1 Keyboard-first or easy like Windows? Decided: both, on KDE Plasma

`README.md` says *"If it takes three clicks, make it one keystroke."* Product
goal 2 says a non-technical user should find it as easy as Windows. BBE's answer
is **both**:

- The default desktop is **KDE Plasma**: windows overlap and cascade like
  Windows, with a start menu, a taskbar, and a System Settings app.
- The terminal is **Konsole**, and the browser **Firefox**; Chrome and WezTerm are one-click installs. (Changed on 2026-10-16 from WezTerm and Chrome.)
- **Hyprland stays installed as a second choice on the login screen** for
  people who prefer tiling and keyboard-only work. Plasma itself supports every
  keyboard shortcut a power user wants.

KDE Plasma is now the default desktop in the Steel OS image.

What the switch changes, for S&C to confirm:

| Keeps working on Plasma | Lost on the Plasma session | Must be tested |
|---|---|---|
| Omarchy's installer, updater, snapshots and rollback, stable mirror, package repo, firewall, full-disk encryption | Omarchy's top bar, Super + Space menu, theme system, web-app launchers, and its Install menu | Omarchy's update restarts its own desktop shell and pauses Hyprland config reloads. On Plasma those steps must fail harmlessly. |
| The SDDM login screen (it is KDE's own, so Plasma slots straight in) | `config/hypr/bindings.lua` only applies when Hyprland is chosen at login | Whether Omarchy migrations assume a Hyprland session |

Why Plasma helps the other goals: System Settings has a Printers page, the
Dolphin file manager can find Windows PCs on the network, and KDE's Discover is
a store screen Windows users recognise. The app install path is revisited in
`docs/app-install-plan.md`.

### 5.2 What does "Forge-powered development" mean? Answered

**Steel & Code Forge** is S&C's own AI-powered software
development platform, a separate project of about 55,000 lines of Python. It
runs several AI agents with distinct jobs (Byte for software engineering,
Neighbor, Hermes, Ember, Fin), routes tasks to different AI models, and has a
terminal interface and an "order board" for tracking agent work. The developer
stays in control: Forge does the repetitive implementation, the human decides
what to build and approves changes.

"Forge-powered development" in the README means Forge is intended to become a
built-in development capability of Steel OS, so a programmer can go from idea
to working software with AI help. Neither project requires the other. Forge is
not in this repository.

The README's status line "Development on Byte" refers to the Byte agent, not to
a machine.

BBE's decision (2026-10-15): Forge is **a one-click optional install, not part
of the default Steel OS**. A non-developer never sees it; a developer picks it
from the Steel Apps list. S&C packages it, since Forge is S&C's code. See `docs/app-install-plan.md`.

### 5.3 Where does the repo live? Decided: here, for now

The repo lives in the Steel & Code GitHub organization, `github.com/steel-and-code/steel-os` (moved from a personal account on 2026-10-17), so the image and links carry the organization name.

### 5.4 What are the real package names? Confirmed

BBE's list, checked against the Arch and Omarchy package databases on 2026-10-15:

| Software | Package | Source |
|---|---|---|
| WezTerm | `wezterm` | Arch extra |
| Neovim | `neovim` | Arch extra |
| Zed | `zed` | Arch extra |
| Docker | `docker` | Arch extra |
| OBS Studio | `obs-studio` | Arch extra |
| Kdenlive | `kdenlive` | Arch extra |
| Steam | `steam` | Arch multilib |
| Nautilus | `nautilus` | Arch extra |
| btop | `btop` | Arch extra |
| Firefox | `firefox` | Arch extra |
| Google Chrome | `google-chrome` | AUR, and also Omarchy's own package repository, so no AUR is needed |

The full lists, including the optional and review entries, were corrected
later in the app install plan.

---

### 5.5 Which base? Decided: Fedora Atomic via Bazzite (Option C)

Proposed by S&C and agreed by BBE on 2026-10-15, with BBE adding
Bazzite as the starting image. S&C's one condition: the existing
keyboard shortcuts stay.

Steel OS becomes a custom bootable image built with the Universal Blue
template: a `Containerfile` that starts from `ghcr.io/ublue-os/bazzite:stable`,
a `build.sh` that adds our packages, and a `system_files/` folder of settings
and branding. GitHub Actions builds the image and the ISO. Two images: standard
and NVIDIA.

Why, once Plasma was chosen: Omarchy's value is its Hyprland desktop, which
Plasma sets aside. What remains of Omarchy (installer, updater, snapshots,
mirror) Bazzite provides already, built for Plasma, with whole-image updates
and rollback, gaming preinstalled, a Flatpak store, automatic background
updates, Secure Boot support, and security fixes days rather than a month
behind. The cost is that Bazzite does not ship a Hyprland session.

Sections 2 and 3 of this document describe the image layout that replaced
the Omarchy-era repo.

## 6. Glossary

| Term | Meaning |
|---|---|
| Arch Linux | A do-it-yourself Linux distribution. Fast-moving, always up to date, and unforgiving if updated carelessly. That is why goal 1 exists. |
| Omarchy | 37signals' ready-made Arch setup with the Hyprland desktop. Our foundation. |
| Hyprland | The desktop environment Omarchy uses. Windows are arranged automatically and most things are done with the keyboard. Steel OS will keep it as a second login option. |
| KDE Plasma | A full desktop environment with a start menu, taskbar, overlapping windows and a System Settings app. The most Windows-like Linux desktop. Steel OS's chosen default (decision 5.1). |
| SDDM | The login screen. Omarchy already uses it, and it is made by the KDE project. |
| Forge | Steel & Code Forge, S&C's AI-assisted development platform. Separate project; see decision 5.2. |
| Fedora Atomic | A version of Fedora Linux where the whole system is one read-only image that updates as a unit and can be rolled back. |
| Bazzite | A Fedora Atomic image made for gaming and desktops, with Plasma, Steam, drivers and automatic updates built in. Steel OS's starting image (decision 5.5). |
| Universal Blue | The community project that publishes Bazzite and the template Steel OS is built from. |
| Flatpak, Flathub | The one app format and the one app store on Steel OS. |
| Containerfile | The recipe file that defines the Steel OS image. |
| Package | An installable program, as Arch sees it. `pacman` installs packages from the official Arch repos. |
| AUR | Arch User Repository. Community-maintained packages, not official. Many popular apps (Google Chrome, Discord) live here. |
| Flatpak | A separate, cross-distribution way to install desktop apps in a sandbox. One of the "five formats" goal 4 wants to avoid. |
| Snapshot | A saved copy of the system's state that can be restored. Omarchy takes these with a tool called snapper. |
| Limine | The boot loader Omarchy uses. It shows the menu where a user could pick an older snapshot. |
| Migration | A small script that updates an already-installed machine when a default setting changes. Runs once per machine. |
| WezTerm | The terminal program Steel OS prefers. |
| Lua | A small scripting language. Omarchy and WezTerm both use it for configuration files. |
| shellcheck | A tool that finds mistakes in Bash scripts. Every script must pass it before a PR. |
