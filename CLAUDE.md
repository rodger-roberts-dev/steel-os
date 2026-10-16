# CLAUDE.md — steel-os

This file is read by Claude Code at the start of every session. It describes the
project, the team, and the rules Claude must follow when working in this repo.

---

## 1. What steel-os is

- A Linux distribution built on **Arch Linux**, based on **Omarchy**
  (37signals/Basecamp's opinionated Arch + Hyprland setup).
- Owner / lead developer: **rodger-roberts-dev** (has final say on all merges).
- Product director: **T** (GitHub: `blackboxentertainment01-sys`). Not a coder —
  writes Jira stories, tests builds, and reviews behavior, not code.
- Repo: `github.com/rodger-roberts-dev/steel-os` (private). Default branch: **`master`**.
- Jira site: `blackboxentertainment.atlassian.net`. Project key: **STEEL** —
  **the STEEL project has not been created yet** (checked 2026-10-15). Until it
  exists there are no story keys to branch from; ask T before starting work.

### Product goals (in priority order)
1. **Safe updates.** Users never get raw Arch updates. Every update is curated,
   snapshotted first, and can be rolled back from the boot menu.
2. **Easy like Windows.** A non-technical user must be able to install, update,
   connect a printer, find network computers, and install apps without a terminal.
3. **Plays games.** Steam + Proton work out of the box; controllers just work.
4. **One way to install apps.** A single app store / install path, not five formats.
5. **Built-in security.** Protection is part of the OS, not a third-party add-on.

> Note: the repo `README.md` currently describes a different philosophy
> ("keyboard-first", "if it takes three clicks, make it one keystroke", minimal
> apps). The README predates these goals. Goal 2 above vs. the README's
> keyboard-first stance is an open product question for rodger-roberts-dev and T.

### Open product decision
- Default desktop: keep **Hyprland** (Omarchy default, keyboard-driven) or add /
  switch to a Windows-like desktop (e.g. KDE Plasma). **Not decided** — do not
  change the default desktop without an approved Jira story.

---

## 2. How the repo is built

Current state (v0.1, as of 2026-10-15): the repo is a **starting skeleton**. It
contains package manifests, two config overrides, and one audit script. There is
no installer, no updater, no ISO, and no test suite yet.

### Layout
```
README.md
.gitignore              ignores inventory/, editor swap files, Python caches, .env
CLAUDE.md               this file
.claude/agents/         Claude Code agent definitions (steel-dev.md)
config/
  hypr/bindings.lua     Omarchy keybinding overrides (Lua). Currently rebinds
                        ALT+RETURN to launch WezTerm via uwsm.
  wezterm/wezterm.lua   WezTerm config. ALT+C / ALT+V copy and paste.
packages/
  core.txt              core apps (wezterm, neovim, zed, docker, steam, ...)
  development.txt       dev tools (git, python, nodejs, rustup, base-devel, ...)
  optional.txt          approved optional apps. Names are NOT yet real package
                        names (e.g. "Google Chrome", "Battle.net"); need verifying.
  excluded.txt          packages deliberately left out of the default install
  review.txt            candidates for removal after dependency review
scripts/
  bootstrap.sh          read-only audit. For each package in core.txt and
                        development.txt it prints [OK] installed, [MISSING]
                        available in repos but not installed, or [VERIFY] not
                        found in repos. Makes no changes.
```

- **Install method:** intended to be shell scripts run on top of a base
  Omarchy/Arch install. Today only the audit script exists; nothing installs
  anything yet.
- **Languages:** Bash for scripts; Lua for Hyprland and WezTerm config (Omarchy's
  Lua config format: `o.bind(...)`, `hl.unbind(...)`).
- **Package manifests:** `packages/*.txt`, one package per line, `#` comments
  allowed, blank lines ignored. `bootstrap.sh` only reads core and development.
- **Config files:** `config/<app>/...`. These are meant to be copied or linked
  into `~/.config/` on an Omarchy machine.
- **Migrations:** none yet. There is no `migrations/` directory. When the first
  config change that affects existing installs is made, create `migrations/`
  following Omarchy's convention (one timestamped, idempotent script per change,
  run once by the updater).
- **Update command / flow:** not built yet. This is product goal 1.
- **Snapshot + rollback:** not built yet. Omarchy ships Limine + snapper; steel-os
  will inherit that once installs happen on top of Omarchy, but nothing in this
  repo touches it today.
- **Build / test an ISO:** no ISO build exists. The only runnable thing is
  `scripts/bootstrap.sh`, which must be run inside an **Arch/Omarchy VM or
  container**, never on the host.
- **Tests:** none. `shellcheck scripts/*.sh` is the only check available.

### Relationship to upstream Omarchy
- steel-os tracks Omarchy upstream. Keep our changes **separate and clearly
  labeled** so upstream updates can be merged without huge conflicts.
- Prefer adding new files over editing upstream files. When an upstream file must
  change, keep the edit small and add a comment: `# steel-os: <reason> (STEEL-##)`
  (use `-- steel-os: ...` in Lua files).

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
- T's GitHub account has push access but no admin, and `master` has no branch
  protection. The "never push to master" rule is enforced by discipline, not by
  GitHub.

### Safety — this code changes operating systems
- **Never run install, update, or setup scripts on the host machine.** They are
  only run inside a VM or a disposable container.
- Never run `pacman`, `yay`, `snapper`, `mkfs`, `dd`, partitioning tools, or
  anything with `sudo` without asking T first and explaining what it does.
- Never delete files outside the repo.
- Never put secrets, passwords, or keys in the repo.

### Code standards
- Bash scripts: start with `set -euo pipefail` (matches `scripts/bootstrap.sh`),
  quote variables, and pass **shellcheck**.
- Lua config: match the style in `config/hypr/bindings.lua`. Unbind before
  rebinding, and comment each override with what it does.
- Package manifests: one real pacman/AUR package name per line. If a name is not
  yet verified as a real package, say so in a `#` comment above it.
- Any change to a default config that existing users already have **must ship
  with a migration**, so installed systems pick it up on their next update.
- Changes must be safe to run twice (idempotent).
- Match the existing style of the file you're editing.

### Testing before a PR
1. Run `shellcheck` on every changed script. On T's Windows machine WSL is not
   installed and shellcheck is not on PATH, so run it in the VM or install the
   Windows shellcheck binary.
2. There are no automated tests yet. If you add a script, run it in a VM.
3. Write a short **"How to test"** checklist in the PR that T can follow in a VM,
   in plain English, step by step.

---

## 4. Working with T

- T is a **non-coder product director**. Explain what you did in plain English,
  short and clear. No jargon without a one-line explanation.
- T works on **Windows 11** with VS Code. WSL is **not** installed on T's machine.
  Building/testing Linux pieces happens in a **VM**. Say when a step needs one.
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

### Epics (starting backlog)
- Updates & Rollback
- App Store / Installs
- Printers & Networking
- Security
- First-Boot Setup
- Gaming
