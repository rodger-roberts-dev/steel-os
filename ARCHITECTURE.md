# Steel OS Architecture

This document describes Steel OS as it actually exists in this repository on
2026-10-15. It is written for everyone on the project, including people who do
not write code. Where something does not exist yet, it says so plainly.

Jira: STEEL-1

---

## 1. What Steel OS is

Steel OS is a Linux operating system for everyday people. It is built on top of
**Arch Linux** using **Omarchy**, an opinionated Arch setup made by 37signals
(the Basecamp company). Omarchy gives us a working desktop, an installer, an
updater, and a snapshot system. Steel OS adds the choices, apps, and tools that
make it suitable for a non-technical person.

Steel OS is **not** a fork of Arch or of Omarchy. It is a layer that sits on top
of an Omarchy install and changes what is installed and how it behaves.

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

## 5. Open decisions for rodger-roberts-dev and T

These are not bugs. They are choices nobody has made yet. Each one changes what
gets built, so they should be decided before the related work starts.

### 5.1 Keyboard-first or easy like Windows?

`README.md` says the guiding principle is *"If it takes three clicks, make it
one keystroke"* and describes a minimal, keyboard-first environment. Product
goal 2 says a non-technical user must never need a terminal and should find it
as easy as Windows. Hyprland, Omarchy's desktop, is built for keyboard users.

These pull in different directions. Possible answers:

- Keep Hyprland and the keyboard-first philosophy, and accept that "easy like
  Windows" means "easy once you learn the shortcuts".
- Keep Hyprland but add mouse-friendly pieces (a visible app menu, a settings
  app, a dock).
- Offer a Windows-like desktop (KDE Plasma is the usual choice) as the default,
  and keep Hyprland as an option.

**Rule until decided:** do not change the default desktop. (`CLAUDE.md` says the
same.)

### 5.2 What does "Forge-powered development" mean?

`README.md` lists it as a design point. Nothing in the repo defines it. It
should either be explained in the README or removed.

### 5.3 Where does the repo live?

Today it is under rodger-roberts-dev's personal GitHub account. T is an admin of
the `blackbox-entertainment` GitHub organization. The current plan is to keep
working here on branches and transfer the repo to the organization later, which
rodger-roberts-dev has to do from the repo's settings.

### 5.4 What are the real package names?

`optional.txt` and `review.txt` contain product names, not package names, and
some entries (HEY, Basecamp, Google web-app shortcuts) are web apps rather than
installable packages. Covered by STEEL-4.

---

## 6. Glossary

| Term | Meaning |
|---|---|
| Arch Linux | A do-it-yourself Linux distribution. Fast-moving, always up to date, and unforgiving if updated carelessly. That is why goal 1 exists. |
| Omarchy | 37signals' ready-made Arch setup with the Hyprland desktop. Our foundation. |
| Hyprland | The desktop environment Omarchy uses. Windows are arranged automatically and most things are done with the keyboard. |
| Package | An installable program, as Arch sees it. `pacman` installs packages from the official Arch repos. |
| AUR | Arch User Repository. Community-maintained packages, not official. Many popular apps (Google Chrome, Discord) live here. |
| Flatpak | A separate, cross-distribution way to install desktop apps in a sandbox. One of the "five formats" goal 4 wants to avoid. |
| Snapshot | A saved copy of the system's state that can be restored. Omarchy takes these with a tool called snapper. |
| Limine | The boot loader Omarchy uses. It shows the menu where a user could pick an older snapshot. |
| Migration | A small script that updates an already-installed machine when a default setting changes. Runs once per machine. |
| WezTerm | The terminal program Steel OS prefers. |
| Lua | A small scripting language. Omarchy and WezTerm both use it for configuration files. |
| shellcheck | A tool that finds mistakes in Bash scripts. Every script must pass it before a PR. |
