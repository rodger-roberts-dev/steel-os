# CLAUDE.md — steel-os

This file is read by Claude Code at the start of every session. It describes the
project, the team, and the rules Claude must follow when working in this repo.

---

## 1. What steel-os is

- A Linux distribution for everyday people, built as a **custom bootable image
  on a Fedora Atomic base, starting from Bazzite**, using the Universal Blue
  image template. Decided 2026-10-15 (STEEL-28) by rodger-roberts-dev and T.
- Before that date the project was built on Omarchy (Arch + Hyprland). The
  research from that period (`docs/updates-and-rollback.md`,
  `docs/printers-and-network.md`) is kept as background. Some files in the repo
  still date from the Omarchy era until STEEL-16 lands the image recipe.
- Owner / lead developer: **rodger-roberts-dev** (has final say on all merges).
  Also the author of Steel & Code Forge, an AI development platform that is an
  optional one-click install on Steel OS (STEEL-25).
- Product director: **T** (GitHub: `blackboxentertainment01-sys`). Not a coder —
  writes Jira stories, tests builds, and reviews behavior, not code.
- Repo: `github.com/rodger-roberts-dev/steel-os` (private). Default branch: **`master`**.
- Jira site: `blackboxentertainment.atlassian.net`, project key **STEEL**.
  Epics STEEL-8 to STEEL-15 group the stories. rodger-roberts-dev has no Jira
  account yet, so his tickets carry "Owner:" in the text.

### Product goals (in priority order)
1. **Safe updates.** Users never get raw updates. The whole system updates as
   one image, automatically every Tuesday, and the previous version is always in
   the boot menu.
2. **Easy like Windows.** A non-technical user must be able to install, update,
   connect a printer, find network computers, and install apps without a terminal.
3. **Plays games.** Steam + Proton work out of the box; controllers just work.
4. **One way to install apps.** One store (Discover) and one format (Flatpak).
5. **Built-in security.** Protection is part of the OS, not a third-party add-on.

### Decisions already made (see `ARCHITECTURE.md` section 5)
- Desktop: **KDE Plasma** with cascading windows. Terminal: **WezTerm**.
  rodger-roberts-dev's keyboard shortcuts ship as the defaults (STEEL-29).
- Base: **Bazzite** (`ghcr.io/ublue-os/bazzite:stable`), two Steel OS images,
  standard and NVIDIA.
- Browser: Chrome default, Firefox one click. Office suite: LibreOffice.
- Hosting: download page on `blackbox-entertainment.com`, files in T's
  Cloudflare R2 (STEEL-26).

---

## 2. How the repo is built

### Today (Omarchy era, until STEEL-16)
```
README.md, ARCHITECTURE.md, CLAUDE.md, docs/
config/hypr/bindings.lua, config/wezterm/wezterm.lua
packages/*.txt            app lists, being converted to the image format
scripts/bootstrap.sh      Omarchy-era package audit; to be replaced
```

### Target layout (Universal Blue image template, from STEEL-16)
```
Containerfile             FROM ghcr.io/ublue-os/bazzite:stable, runs build.sh
image-template.env        image name, organisation, description
build_files/build.sh      installs rpm packages into the image, enables units
system_files/             files copied verbatim into the image at /
  etc/xdg/kglobalshortcutsrc     rodger's key bindings (Plasma defaults)
  etc/xdg/kwinrc                 cascading window placement
  etc/xdg/kdeglobals             WezTerm as the terminal
  etc/systemd/system/uupd.timer.d/   Tuesday schedule for automatic updates
  usr/share/...                  branding, wallpaper, Steel Apps catalogue
disk_config/iso-kde.toml  ISO build settings
packages/                 plain-text lists read by build.sh and first boot
.github/workflows/        build the image; build the ISO and upload to R2
Justfile                  local build commands (Linux only)
cosign.pub                image signing public key (the private key is a GitHub secret, never in the repo)
```

- **Languages:** Containerfile; Bash for `build.sh` and first-boot scripts;
  INI-style config files for Plasma; TOML for disk config; YAML for workflows.
- **Build:** GitHub Actions builds the image on every push to `master` and on a
  schedule, and builds the ISO on release. Nothing is built on T's Windows PC.
- **Updates:** Bazzite's `uupd` updates the image and all Flatpaks in the
  background; rollback is `rpm-ostree rollback` or picking the previous image at
  boot. Steel OS only sets the schedule and the notification wording.
- **Migrations:** mostly unnecessary. Settings live in the image under `/etc`,
  so a change ships in the next image. A first-boot script handles the few
  per-user things (Flatpak installs, default browser).
- **Testing:** T installs the ISO in VirtualBox (VM "STEEL") or on the test
  machine, following the PR's how-to-test list.

### Relationship to upstream
- Steel OS tracks `bazzite:stable`. Pin each Steel OS release to the Bazzite
  image digest it was tested on and record it in `ARCHITECTURE.md`.
- Never fork or patch Bazzite's own files. Everything Steel OS does goes in
  `build.sh`, `system_files/`, and `packages/`.

---

## 3. Rules Claude must always follow

### Git and GitHub
- **Never commit or push to `master`.** Always work on a branch. (The default
  branch is `master`, not `main`.)
- Branch names start with the Jira key: `STEEL-12-printer-wizard`.
- Commit messages start with the Jira key: `STEEL-12: add printer setup wizard`.
- Every change goes through a **pull request** for rodger-roberts-dev to review.
  PR description must include: the Jira key, what changed, why, and how to test it.
- One Jira story per branch / PR. Don't bundle unrelated changes.
- `master` has no branch protection; the "never push to master" rule is
  enforced by discipline.

### Safety — this code builds operating systems
- **Never run image, install, or update commands on the host machine.**
  `bootc`, `rpm-ostree`, `dnf`, `podman build`, `just build`, partitioning
  tools, and anything with `sudo` run only inside a VM, a container, or GitHub
  Actions. T's Windows PC cannot run them anyway; do not try.
- Never delete files outside the repo.
- Never put secrets, passwords, or keys in the repo. The cosign private key,
  R2 credentials, and any API keys live in GitHub Actions secrets only.

### Code standards
- Bash scripts: `set -euo pipefail` (the template's `build.sh` uses
  `set -ouex pipefail`; match it there), quote variables, pass **shellcheck**.
- Config files under `system_files/` are plain text; keep a comment at the top
  of each saying what it does and which STEEL story added it.
- Anything that changes a per-user setting on existing machines needs a
  first-boot or post-update step that is safe to run twice.
- Match the existing style of the file you're editing.

### Testing before a PR
1. Run `shellcheck` on every changed script. On T's Windows machine WSL is not
   installed and shellcheck is not on PATH; the GitHub Action runs it.
2. The image must build in GitHub Actions (the Action is the test).
3. Write a short **"How to test"** checklist in the PR that T can follow in the
   VM, in plain English, step by step.

---

## 4. Working with T

- T is a **non-coder product director**. Explain what you did in plain English,
  short and clear. No jargon without a one-line explanation.
- T works on **Windows 11** with VS Code. WSL is **not** installed. Testing
  happens in VirtualBox (VM named STEEL) or on the test machine. Say which.
- T prefers **complete files** over partial snippets when handing off work.
- When a Jira story is unclear, ask T before coding. When it's clear, just do it.
- At the end of a task, give T:
  1. One-paragraph summary of what changed
  2. The branch / PR link
  3. The "How to test" checklist
  4. Anything that needs rodger-roberts-dev's decision

---

## 5. Jira workflow

- Story keys look like `STEEL-12`.
- When starting a story: read it, confirm the acceptance criteria, create the branch.
- When opening the PR: add a comment to the Jira story with the PR link.
- Don't move stories to Done — rodger-roberts-dev or T does that after merge.
- If you find a bug or missing piece that's out of scope, don't fix it silently —
  suggest a new Jira story instead.

### Epics
- STEEL-8 Foundations and documentation
- STEEL-9 Updates and Rollback
- STEEL-10 App Store and Installs
- STEEL-11 Printers and Networking
- STEEL-12 Security
- STEEL-13 First-Boot Setup and Install
- STEEL-14 Gaming
- STEEL-15 Desktop: KDE Plasma
