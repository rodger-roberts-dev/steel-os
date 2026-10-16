# Steel OS Architecture

This document describes Steel OS as it actually exists in this repository on
2026-10-15. It is written for everyone on the project, including people who do
not write code. Where something does not exist yet, it says so plainly.

Jira: STEEL-1

---

## 1. What Steel OS is

Steel OS is a **Steel & Code** (steelandcode.com) project, made in partnership
with **Blackbox Entertainment**. Say it that way on anything public.

Steel OS is a Linux operating system for everyday people. It is built on top of
**Arch Linux** using **Omarchy**, an opinionated Arch setup made by 37signals
(the Basecamp company). Omarchy gives us a working desktop, an installer, an
updater, and a snapshot system. Steel OS adds the choices, apps, and tools that
make it suitable for a non-technical person.

Steel OS is **not** a fork of Arch or of Omarchy. It is a layer that sits on top
of an Omarchy install and changes what is installed and how it behaves.

In the product director's words: "Steel OS is an Arch/Omarchy-based
distribution. We maintain package manifests for core applications, development
tools, optional software, and excluded packages. The bootstrap script currently
performs a read-only package audit. The project is in early alpha development,
not yet a standalone installer."

### Product goals, in priority order

1. **Safe updates.** Users never get raw Arch updates. Every update is curated,
   a snapshot is taken first, and the user can roll back from the boot menu.
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
| rodger-roberts-dev | Lead developer. Owns the repo. Final say on every merge. |
| T (`blackboxentertainment01-sys`) | Product director. Writes Jira stories, tests builds, reviews behavior. Not a coder. |
| Claude Code | Development assistant. Works only on branches, opens pull requests, never merges. Rules are in `CLAUDE.md`. |

---

## 2. What Omarchy provides vs. what Steel OS adds

Omarchy is the foundation. Everything in the left column already works on a
fresh Omarchy install without any Steel OS code.

| Omarchy provides | Steel OS adds (today) | Steel OS will add (planned) |
|---|---|---|
| Arch Linux base install | A list of which apps to install | Curated, snapshotted updates (goal 1) |
| Hyprland desktop, keyboard-driven | A list of which apps to leave out | Printer and network setup without a terminal (goal 2) |
| Limine boot loader with snapper snapshots | A keybinding change: ALT+RETURN opens WezTerm | Steam, Proton, and controller setup (goal 3) |
| `omarchy-update` and migrations | WezTerm copy and paste on ALT+C and ALT+V | One app store or install path (goal 4) |
| Theme system and app launcher | A script that checks which apps are installed | Built-in security (goal 5) |
| Its own ISO and installer | | A Steel OS installer or install script |

The honest summary: **today Steel OS is a set of preferences written down, plus
one audit script.** Nothing in this repo installs, updates, or configures a
machine yet. That is expected for version 0.1.

Decision on 2026-10-15 (section 5.1): the default desktop will be **KDE
Plasma**, not Hyprland, with Hyprland kept as a second choice on the login
screen. The "Omarchy provides" column above still applies to the base system,
but the Hyprland desktop row becomes optional once that is built.

---

## 3. How the repository is laid out

```
steel-os/
├── README.md                 One-paragraph project description
├── ARCHITECTURE.md           This file
├── CLAUDE.md                 Rules and context for Claude Code
├── .gitignore                Ignores inventory/, editor temp files, Python caches, .env
├── .claude/
│   └── agents/
│       └── steel-dev.md      The Claude Code agent that works a STEEL story end to end
├── config/
│   ├── hypr/
│   │   └── bindings.lua      Hyprland keybinding overrides (Omarchy's Lua format)
│   └── wezterm/
│       └── wezterm.lua       WezTerm terminal config
├── packages/
│   ├── core.txt              10 apps every Steel OS machine gets
│   ├── development.txt       14 developer tools
│   ├── optional.txt          7 approved extras (names not yet verified)
│   ├── excluded.txt          3 packages deliberately left out
│   └── review.txt            6 candidates for removal
└── scripts/
    └── bootstrap.sh          Read-only package audit
```

### Each piece, in plain English

**`packages/*.txt`: the app lists.** One package name per line. Lines starting
with `#` are comments. These lists are the heart of Steel OS today: they say
what a Steel OS machine should have on it.

- `core.txt`: wezterm (terminal), neovim and zed (editors), docker, obs-studio,
  kdenlive (video), steam, nautilus (file manager), btop (system monitor),
  gnome-disk-utility.
- `development.txt`: git, python, python-pip, nodejs, npm, rustup, base-devel,
  github-cli, jq, ripgrep, fd, lazygit, lazydocker, docker-compose.
- `optional.txt`: Google Chrome, Obsidian, Discord, Zoom, Moonlight, Battle.net,
  Google web-app shortcuts. **These are display names, not package names.** The
  file itself says they still need verifying. STEEL-4 covers this.
- `excluded.txt`: foot (a terminal Omarchy may ship; we use WezTerm instead),
  libreoffice-fresh, libreoffice-still.
- `review.txt`: chromium, xournalpp, pinta, HEY, Basecamp, libreoffice-fresh.
  Things Omarchy installs that we may remove. HEY and Basecamp are 37signals
  web apps, not packages.

**`config/hypr/bindings.lua`: keyboard shortcuts.** Omarchy lets you override
its default shortcuts in a Lua file. Ours does one thing: it unbinds ALT+RETURN
and rebinds it to open WezTerm. The rest of the file is Omarchy's own commented
examples. The file depends on Omarchy's Lua helpers (`o.bind`, `hl.unbind`) and
will not work outside Omarchy.

**`config/wezterm/wezterm.lua`: terminal settings.** Makes ALT+C copy and ALT+V
paste, the way Windows users expect from CTRL+C and CTRL+V. Nothing else.

**`scripts/bootstrap.sh`: the audit script.** Reads `core.txt` and
`development.txt` and, for each package, prints one of:

| Output | Meaning |
|---|---|
| `[OK]` | Installed on this machine |
| `[MISSING]` | Exists in the Arch repos but is not installed |
| `[VERIFY]` | Not found in the Arch repos. Wrong name, or comes from somewhere else (AUR, Flatpak) |

It **makes no changes** and says so when it finishes. It does not read
`optional.txt`, `excluded.txt`, or `review.txt`. It must be run on an Arch or
Omarchy machine because it calls `pacman`, Arch's package tool.

**`CLAUDE.md` and `.claude/agents/steel-dev.md`: rules for the AI assistant.**
Not part of the OS. They tell Claude Code how this team works: one Jira story
per branch, every change through a pull request, never run install scripts on
a real machine.

### What is not here yet

- No installer or install script. Omarchy's installer is used as-is.
- No update command. Omarchy's `omarchy-update` is used as-is.
- No `migrations/` folder. Omarchy uses migrations to update existing machines
  when a config changes; Steel OS will need the same once it has users.
- No ISO. You cannot download and boot Steel OS.
- No automated tests. The only check is `shellcheck` on the one script.
- No mechanism to copy `config/` files onto a machine. Today a person would do
  that by hand.

---

## 4. How a change gets from a Jira ticket to a user's machine

### Today (version 0.1)

```
Jira ticket  →  branch  →  pull request  →  rodger reviews  →  merge to master
                                                                     │
                              (manual, by hand)  ←───────────────────┘
                                     │
                     person copies files onto an Omarchy machine
```

1. A story is written in Jira (project STEEL).
2. A branch is created named after it, for example `STEEL-4-package-names`.
3. The change is made and a pull request is opened. The PR says what changed,
   why, and how to test it in plain English.
4. T tests it on the test machine (see STEEL-5). rodger-roberts-dev reviews the
   code and merges.
5. Getting the change onto a real machine is manual. There is no updater yet.

### Planned (once goal 1 is built)

```
merge to master  →  Steel OS updater  →  snapshot taken  →  packages + configs applied
                                                                      │
                                              boot menu offers rollback if anything broke
```

The exact design of the updater is the subject of STEEL-2. The intent is that a
user clicks "Update", a snapshot is taken first, the curated set of changes is
applied, and if anything goes wrong they pick the previous snapshot from the
boot menu.

---

## 5. Decisions

These four questions were open when this document was first written. T
answered all four on 2026-10-15. Each answer is a product decision;
rodger-roberts-dev reviews the technical consequences before anything is built.

### 5.1 Keyboard-first or easy like Windows? Decided: both, on KDE Plasma

`README.md` says *"If it takes three clicks, make it one keystroke."* Product
goal 2 says a non-technical user should find it as easy as Windows. T's answer
is **both**:

- The default desktop is **KDE Plasma**: windows overlap and cascade like
  Windows, with a start menu, a taskbar, and a System Settings app.
- The terminal is **Konsole**, and the browser **Firefox**; Chrome and WezTerm are one-click installs. (Changed 2026-10-16 by rodger-roberts-dev and T from the README's WezTerm and Chrome; both use Firefox and Konsole.)
- **Hyprland stays installed as a second choice on the login screen** for
  people who prefer tiling and keyboard-only work. Plasma itself supports every
  keyboard shortcut a power user wants.

This is tracked in STEEL-7 and needs rodger-roberts-dev's technical review
before it is built. **Until STEEL-7 is merged, the default desktop stays
Hyprland.**

What the switch changes, for rodger-roberts-dev to confirm:

| Keeps working on Plasma | Lost on the Plasma session | Must be tested |
|---|---|---|
| Omarchy's installer, updater, snapshots and rollback, stable mirror, package repo, firewall, full-disk encryption | Omarchy's top bar, Super + Space menu, theme system, web-app launchers, and its Install menu | Omarchy's update restarts its own desktop shell and pauses Hyprland config reloads. On Plasma those steps must fail harmlessly. |
| The SDDM login screen (it is KDE's own, so Plasma slots straight in) | `config/hypr/bindings.lua` only applies when Hyprland is chosen at login | Whether Omarchy migrations assume a Hyprland session |

Why Plasma helps the other goals: System Settings has a Printers page, the
Dolphin file manager can find Windows PCs on the network, and KDE's Discover is
a store screen Windows users recognise. The app install path is revisited in
`docs/app-install-plan.md`.

### 5.2 What does "Forge-powered development" mean? Answered

**Steel & Code Forge** is rodger-roberts-dev's own AI-powered software
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

T's decision (2026-10-15): Forge is **a one-click optional install, not part
of the default Steel OS**. A non-developer never sees it; a developer picks it
from the Steel Apps list. Packaging it is rodger-roberts-dev's story
(STEEL-25), since Forge is his code. See `docs/app-install-plan.md`.

### 5.3 Where does the repo live? Decided: here, for now

The repo stays at `github.com/rodger-roberts-dev/steel-os`. Work happens on
branches there. T is an admin of the `blackbox-entertainment` GitHub
organisation, and because no fork was made, the repo can be transferred there
later with no cleanup. Only rodger-roberts-dev can do the transfer.

### 5.4 What are the real package names? Confirmed

T's list, checked against the Arch and Omarchy package databases on 2026-10-15:

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

The full lists, including the optional and review entries, were corrected in
STEEL-4.

---

### 5.5 Which base? Decided: Fedora Atomic via Bazzite (Option C)

Proposed by rodger-roberts-dev and agreed by T on 2026-10-15, with T adding
Bazzite as the starting image. rodger-roberts-dev's one condition: he keeps his
keyboard shortcuts (STEEL-29). Tracked in STEEL-28.

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

**Sections 2 and 3 of this document describe the Omarchy-era repo.** They stay
until STEEL-16 lands the image recipe, then get rewritten. `docs/roadmap.md`
already reflects the new base.

## 6. Glossary

| Term | Meaning |
|---|---|
| Arch Linux | A do-it-yourself Linux distribution. Fast-moving, always up to date, and unforgiving if updated carelessly. That is why goal 1 exists. |
| Omarchy | 37signals' ready-made Arch setup with the Hyprland desktop. Our foundation. |
| Hyprland | The desktop environment Omarchy uses. Windows are arranged automatically and most things are done with the keyboard. Steel OS will keep it as a second login option. |
| KDE Plasma | A full desktop environment with a start menu, taskbar, overlapping windows and a System Settings app. The most Windows-like Linux desktop. Steel OS's chosen default (decision 5.1). |
| SDDM | The login screen. Omarchy already uses it, and it is made by the KDE project. |
| Forge | Steel & Code Forge, rodger-roberts-dev's AI-assisted development platform. Separate project; see decision 5.2. |
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
