# CLAUDE.md — steel-os

Rules for contributors and for any AI assistant working in this repository.
Claude Code reads this file at the start of every session.

---

## 1. What Steel OS is

- A Linux distribution for everyday people, built as a **custom bootable image
  on a Fedora Atomic base, starting from Bazzite**, using the Universal Blue
  image template.
- Steel OS is a **Steel & Code** (steelandcode.com) project, in partnership
  with **Blackbox Entertainment**. Say it that way on anything public.
- Roles:
  - **Steel & Code (S&C)** is the project lead. S&C reviews every pull request
    and has the final say on merges. S&C also makes Steel & Code Forge, an AI
    development platform offered as an optional one-click install.
  - **Blackbox Entertainment (BBE)** is the product director. BBE plans the
    work, tests builds and reviews behavior, not code.
- Repo: `github.com/steel-and-code/steel-os` (public). Default branch:
  **`master`**.
- Work is planned in a private issue tracker. Outside contributors use GitHub
  issues and pull requests.

### Product goals (in priority order)
1. **Safe updates.** Users never get raw updates. The whole system updates as
   one image, automatically every Tuesday, and the previous version is always in
   the boot menu.
2. **Easy like Windows.** A non-technical user must be able to install, update,
   connect a printer, find network computers, and install apps without a terminal.
3. **Plays games.** Steam and Proton work out of the box; controllers just work.
4. **One way to install apps.** One store (the App Store) and one format
   (Flatpak), plus one-click Steel Apps in the Steel OS Portal.
5. **Built-in security.** Protection is part of the OS, not a third-party add-on.

### Decisions already made (see `ARCHITECTURE.md` section 5)
- Desktop: **KDE Plasma** with cascading windows. Terminal: **Konsole**
  (WezTerm one click). Steel OS keyboard shortcuts ship as the defaults.
- Base: **Bazzite** (`ghcr.io/ublue-os/bazzite:stable`). One ISO; the graphics
  card is detected at first boot. Plasma only.
- Browser: Firefox by default, Chrome one click. Office suite: LibreOffice.
- Website and downloads: `steel-os.org`, with installer files at
  `downloads.steel-os.org`.

---

## 2. How the repo is built

### Layout (Universal Blue image template)
```
Containerfile             FROM ghcr.io/ublue-os/bazzite:stable, runs build.sh
image-template.env        image name, organization, description
build_files/build.sh      adds packages, settings and branding to the image
build_files/portal/       the Steel OS Portal tabs and the script that builds them
system_files/             files copied verbatim into the image at /
packages/                 plain-text lists: rpm packages, default apps, Steel Apps
branding/                 logos, icons and wallpapers (trademarks of Steel & Code and Blackbox Entertainment)
installer/                the live installer ISO recipe (adapted from Bazzite)
disk_config/              disk image settings
.github/workflows/        build the image; build the ISO and upload it
Justfile                  local build commands (Linux only)
cosign.pub                image signing public key (the private key is a GitHub secret, never in the repo)
```

- **Languages:** Containerfile; Bash for `build.sh` and helper scripts;
  INI-style config files for Plasma; YAML for workflows and the Portal.
- **Build:** GitHub Actions builds the image on every push to `master` and
  every day, and builds the ISO on request. Nothing is built on a contributor's
  own PC unless it runs Linux.
- **Updates:** Bazzite's `uupd` updates the image and all Flatpaks in the
  background; rollback is picking the previous image at boot. Steel OS sets the
  schedule and the wording.
- **Migrations:** mostly unnecessary. Settings live in the image under `/etc`
  and `/usr`, so a change ships in the next image. A few per-user things run
  once at login (shortcuts, taskbar pins, wallpaper).
- **Testing:** the product director installs the image or ISO in a virtual
  machine or on a test PC, following the PR's "How to test" list.

### Relationship to upstream
- Steel OS tracks `bazzite:stable`.
- Never fork or patch Bazzite's own files in place. Everything Steel OS does
  goes in `build.sh`, `system_files/`, `packages/` and `installer/`.
- Files copied from Bazzite or Universal Blue keep a header saying so, and
  `NOTICE` lists them.

---

## 3. Rules to always follow

### Git and GitHub
- **Never commit or push to `master`.** Always work on a branch. (The default
  branch is `master`, not `main`.)
- Branch names and commit messages say what changed, for example
  `printer-setup-wizard` and `Add printer setup wizard`. A tracking key may go
  first when there is one.
- Every change goes through a **pull request** that S&C reviews. The PR
  description says what changed, why, and how to test it.
- Bundle only changes that belong together.
- Docs-only changes (under `docs/` or Markdown files at the top of the repo)
  don't rebuild the image.

### Public text
- The repo is public. README, ARCHITECTURE, `docs/`, `branding/` and this file
  carry no personal names, private account names or internal tracker numbers.
  Refer to roles as Steel & Code (S&C) and Blackbox Entertainment (BBE).
- Nothing user-facing says "Bazzite" except credits. A Bazzite mention in the
  image, the installer or the Portal is a bug.

### Safety — this code builds operating systems
- **Never run image, install or update commands on the host machine.**
  `bootc`, `rpm-ostree`, `dnf`, `podman build`, `just build`, partitioning
  tools and anything with `sudo` run only inside a VM, a container or GitHub
  Actions.
- Never delete files outside the repo.
- Never put secrets, passwords or keys in the repo. The cosign private key,
  storage credentials and any API keys live in GitHub Actions secrets only.

### Code standards
- Bash scripts: `set -euo pipefail` (the template's `build.sh` uses
  `set -ouex pipefail`; match it there), quote variables, pass **shellcheck**.
- Config files under `system_files/` are plain text; keep a comment at the top
  of each saying what it does.
- Anything that changes a per-user setting on existing machines needs a step
  that is safe to run twice.
- Match the existing style of the file you're editing.

### Testing before a PR
1. Run `shellcheck` on every changed script, or let the GitHub Action run it.
2. The image must build in GitHub Actions. The Action is the test.
3. Write a short **"How to test"** checklist in the PR, in plain English, step
   by step, that someone who doesn't code can follow in a virtual machine.

---

## 4. Working with the product director

- BBE is not a coder. Explain what you did in plain English, short and clear.
  No jargon without a one-line explanation.
- BBE works on Windows 11. Testing happens in a virtual machine or on a test
  PC. Say which.
- Hand over complete files, not partial snippets.
- When a task is unclear, ask before coding. When it's clear, just do it.
- At the end of a task, give:
  1. A one-paragraph summary of what changed
  2. The branch or PR link
  3. The "How to test" checklist
  4. Anything that needs a decision from S&C
