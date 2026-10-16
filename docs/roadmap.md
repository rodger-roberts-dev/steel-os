# Steel OS Build Roadmap

Jira: STEEL-6
Date: 2026-10-15 (rewritten the same day for the Bazzite decision, STEEL-28)
Written for: T and rodger-roberts-dev

This is the plan to go from today's repo to a Steel OS a stranger can download,
install, update, and use. It is built on the findings in `ARCHITECTURE.md`
(STEEL-1), `docs/app-install-plan.md` (STEEL-4), and the decisions in
`ARCHITECTURE.md` section 5. The Omarchy research (STEEL-2, STEEL-3) is kept as
background; the parts about printers, sharing, and what users expect still apply.

---

## The one-sentence strategy

**Steel OS is a custom Bazzite image: Fedora Atomic underneath, KDE Plasma on
top, built from a recipe file that GitHub turns into an image and an ISO.** We
do not fork Bazzite, write an installer, run a package mirror, or write an
updater. Bazzite already does all of those well. We add our choices (Firefox,
Konsole, cascading windows, rodger-roberts-dev's keyboard shortcuts), our
branding, our Tuesday update schedule, a curated list of one-click apps, and
the printer and sharing polish a Windows user expects.

What that means in practice: the whole operating system is defined by a short
recipe (a `Containerfile` plus `build.sh` plus a folder of settings files).
Universal Blue provides the template. Every push builds a new image; every
release builds an ISO and uploads it to T's Cloudflare R2 storage. Users
install once from the ISO and then update automatically.

---

## Decisions already made (2026-10-15)

| Decision | Answer | Who |
|---|---|---|
| Base | Fedora Atomic via **Bazzite** (`ghcr.io/ublue-os/bazzite:stable`), Universal Blue template. Plasma only (no GNOME unless users ask). Three image variants for GPUs (standard, NVIDIA newer, NVIDIA older), but one ISO: the graphics card is detected at first boot (STEEL-30). | rodger-roberts-dev proposed, T agreed (STEEL-28) |
| Desktop | **KDE Plasma**, cascading windows, Konsole terminal (WezTerm one click; changed 2026-10-16) | T and rodger-roberts-dev |
| Keyboard | rodger-roberts-dev's bindings ship as the Plasma defaults | rodger-roberts-dev (STEEL-29) |
| Keyboard-first or easy like Windows | Both, on Plasma | T |
| Apps | One store (Discover), one format (Flatpak), plus a curated Steel Apps list | STEEL-4 |
| Browser and office | Firefox default, Chrome one click (changed 2026-10-16), LibreOffice built in | T and rodger-roberts-dev |
| Updates | Automatic every Tuesday, Windows-style | T (STEEL-27) |
| Forge | One-click optional install, never default | T (STEEL-25) |
| Hosting | `steel-os.org` (T owns it, plus `steelos.org`), files in T's R2 at `downloads.steel-os.org` | T (STEEL-26) |
| Repo | Stays at rodger-roberts-dev/steel-os | T |

**Still open:** the rebuild cadence (track Bazzite's stable images as they
come, or hold each a few days for our own test). STEEL-23. Does not block
phase 1.

---

## Phases

Each phase ends with something T can test in the VM and something a user would
notice. Later phases depend on earlier ones.

### Phase 0: Foundations (October 2026, nearly done)

| Done when | Ticket |
|---|---|
| Architecture written down, decisions recorded | STEEL-1 (PR open) |
| App list verified and install path chosen | STEEL-4 (PR open) |
| Test VM ready | STEEL-5 (T) |
| Base decided | STEEL-28 (done) |
| rodger-roberts-dev's key bindings in the repo | STEEL-29 |

### Phase 1: "First image" (version 0.2)

Goal: a Steel OS image builds in GitHub Actions, an ISO comes out, and T boots
it in the VM and sees a Plasma desktop that says Steel OS.

Deliverables:
- The Universal Blue template files copied into this repo: `Containerfile`
  starting from `bazzite:stable`, `build.sh`, `system_files/`, `disk_config/`,
  `Justfile`, and the GitHub workflows.
- A cosign signing key created by rodger-roberts-dev; the private half stored
  as a GitHub secret.
- `build.sh` installs the packages in `packages/image.txt`.
- `system_files/` carries the first settings: Konsole pinned as the terminal with Alt+C / Alt+V, the
  Tuesday update schedule, a Steel OS name in the OS release file.
- The ISO workflow pointed at our image and at T's R2 bucket.
- The old Omarchy-era files (`config/hypr`, `scripts/bootstrap.sh`, the old
  package lists) removed or replaced in the same PR, so the repo has one story.

Tickets: STEEL-16 (image repo and first build), STEEL-18 (Konsole defaults),
STEEL-27 (Tuesday schedule, the schedule part only), STEEL-26 (R2 upload, the
bucket part only).

Test: T downloads the ISO from R2, installs it in the VM, logs in, opens
Konsole from the start menu, and runs `sudo bootc status` to see the Steel OS
image name.

### Phase 2: "Desktop defaults" (version 0.3)

Goal: the desktop looks and behaves like Steel OS, not like stock Bazzite.

Deliverables:
- rodger-roberts-dev's keyboard shortcuts as system defaults
  (`/etc/xdg/kglobalshortcutsrc`), including Super+Return for Konsole and
  Super+Space for the launcher. Every key still changeable by the user.
- Cascading window placement by default; Plasma's built-in tiling on
  Super+T for people who want it.
- Steel OS wallpaper, panel layout, login screen, and boot splash.
- Firefox confirmed as the default browser on first boot; Chrome and WezTerm in
  the Steel Apps list.
- Anything Bazzite ships that we do not want, listed in `packages/remove.txt`
  and removed in the recipe.
- A first-login setup wizard like Windows, every page skippable: welcome,
  updates toggle, choose your apps from the Steel Apps list, printers, done.
  Based on Bazzite Portal, which already appears at first login (STEEL-35).
  T's request after installing Bazzite: it was not clear whether it had
  installed. The matching ISO-side fix, a full-screen "Install Steel OS"
  screen instead of a live desktop, lands in phase 7.

Tickets: STEEL-29 (bindings), STEEL-7 (Plasma defaults), STEEL-19 (browsers),
STEEL-20 (removals).

Test: T logs in, sees the Steel OS look, opens three windows that cascade,
presses Super+Return and gets Konsole, clicks a link and gets Firefox.

### Phase 3: "Safe updates" (version 0.4)

Goal: product goal 1 as a user experiences it. Most of it is inherited.

Deliverables:
- Automatic update every Tuesday at 4 am local time, or on next boot if the
  machine was off, mains power only on laptops. Inherited from Bazzite's
  updater; Steel OS sets the day (STEEL-27).
- A plain-English notification when a restart is needed, with Restart now and
  Later.
- The boot menu entry for the previous version worded in plain English, and a
  one-page "Something went wrong after an update?" guide.
- The rebuild cadence decided (STEEL-23) and the GitHub schedule set to match.
- VM test of update, rollback at the boot menu, and rollback by command
  (STEEL-24).

Test: T triggers an update in the VM, restarts, then rolls back from the boot
menu using only the guide.

### Phase 4: "Easy like Windows" (version 0.5)

Goal: printers, scanners, network shares, and app installs without a terminal.

Deliverables (from STEEL-3's findings, now on Plasma):
- Printers through Plasma's System Settings Printers page, which Bazzite
  ships. Add drivers for older printers (`hplip`, `gutenprint-cups`) to the
  image. Skanpage for scanning, built in.
- `wsdd` in the image so the machine appears in Windows Explorer and Windows
  PCs appear in Dolphin. A folder-sharing wizard on top of Plasma's own share
  tab, with the firewall opened for the local network only.
- The Steel Apps list: a first-boot and Settings screen showing the approved
  apps from `packages/steel-apps.txt` with one Install button each, installing
  from Flathub. Discover remains for everything else.

Tickets: new stories under STEEL-10 and STEEL-11 once phase 2 is merged.

Test: T adds a printer, scans a page, opens a share on a Windows PC, shares a
folder back, and installs Discord from the Steel Apps list.

### Phase 5: "Plays games" (version 0.6)

Goal: product goal 3. Almost entirely inherited from Bazzite.

Deliverables:
- Confirm Steam, controllers, and Proton work on the test machine with a real
  GPU. Bazzite ships them.
- Controllers, joysticks and flight sticks work when plugged in (T,
  2026-10-15): Bazzite covers Xbox, PlayStation, Nintendo and most joysticks;
  Steel OS adds udev rules for the awkward flight sticks, a "Test your
  controller" entry, Oversteer for wheels, and an honest compatibility page.
  Tested on the physical machine with real devices (STEEL-32).
- Lutris (for the EA app), Heroic, and GeForce NOW in the Steel Apps list.
  Battle.net through Lutris.
- A short "gaming on Steel OS" page that says plainly: Xbox Game Pass is cloud
  streaming only on Linux.

Test: T plays a Steam game and an EA game with a controller, following only
the page.

### Phase 6: "Built-in security" (version 0.7)

Goal: product goal 5, defined concretely. Needs a design ticket first.
Bazzite already gives: read-only system files, sandboxed Flatpak apps, Secure
Boot support, a firewall. Candidates to evaluate: full-disk encryption on by
default in the installer, browser hardening through Chrome's policy files,
whether an antivirus adds anything for this audience, and the rebuild cadence
as the security patch policy.

### Phase 7: "Release" (version 1.0)

Goal: a stranger downloads one file from steel-os.org, installs Steel OS, and
never needs the team.

Deliverables:
- One ISO per release (the GPU variants are picked at first boot, STEEL-30), built by the workflow, signed,
  with checksums, uploaded to R2 (STEEL-26).
- The download page at steel-os.org, one Download button (one ISO, GPU detected
  at first boot, STEEL-30).
- The ISO boots into a full-screen "Install Steel OS" screen with a "Try it
  first" option, instead of a live desktop that looks installed (STEEL-35).
- `docs/install.md`, the plain-English install guide (STEEL-21).
- Forge as a one-click install if rodger-roberts-dev has packaged it
  (STEEL-25).
- A release checklist: pin the Bazzite digest, build, test in the VM and on
  the test machine, publish.

Test: a person outside the team installs Steel OS from the download page using
only the install guide.

---

## Size of the work

Roughly 1,500 to 2,500 lines, mostly settings files, Bash, and workflow YAML.
The install script, updater, desktop install, and app store that the Omarchy
plan needed are all inherited. The biggest pieces left are the Steel Apps
screen, the sharing wizard, and the branding.

## Ways of working that keep this on the rails

- **Never patch Bazzite's files.** Everything Steel OS does goes in
  `build.sh`, `system_files/`, and `packages/`. This is what makes upstream
  updates safe.
- **Pin and record.** Each Steel OS release names the Bazzite image digest it
  was tested on.
- **One story, one branch, one PR, one how-to-test list.**
- **The GitHub Action is the test.** A PR whose image does not build does not
  merge.
- **T tests every phase in the VM, and hardware things on the test machine.**

## Risks

| Risk | What we do about it |
|---|---|
| Bazzite changes something we depend on | Pin to a digest per release; read Bazzite's release notes before rebuilding; keep our layer thin. |
| The image is large (Bazzite carries gaming pieces for everyone) | Accepted for goal 3. Revisit if download size becomes a complaint. |
| Two people, limited time | Phases are small and each ends with something usable. |
| rodger-roberts-dev misses the Hyprland session | Bazzite does not ship one. If it matters, a separate Hyprland-based image is possible later but out of scope for 1.0. |
| NAPS2 has no Flatpak | Skanpage is built in; NAPS2 can be layered from its rpm if T insists. |

## What happens next

See the story-by-story plan below; step 1 is the list.

---

## Story-by-story plan to 1.0 (2026-10-16)

Every open STEEL story, in the order it should be done, with who does it and
what it waits on. Dates are targets for a two-person team working part time,
not promises. The phases above still describe *what* each release contains;
this section is the *to-do list* that gets us there.

### Where things stand today

| Story | State | Next action |
|---|---|---|
| STEEL-1, 2, 3, 4, 6 | Written, PRs #2 to #6 open | rodger-roberts-dev merges, T moves to Done |
| STEEL-28 base decision | Decided (Bazzite) | T moves to Done |
| STEEL-24 update and rollback test | Passed on stock Bazzite in the VM | Repeat once on the first Steel OS image, then Done |
| STEEL-5 test machine | VirtualBox VM "STEEL" ready; Command untouched | Install the first Steel OS ISO on Command in step 2 |
| STEEL-29 shortcuts | Translated files in PR #7; rodger's own Katana files still to come | rodger exports `~/.config/kglobalshortcutsrc` and his Konsole profile |
| STEEL-31 branding | Logo kit and both 4K wallpapers in PR #8 | Wire into the image in step 2 |
| STEEL-26 download site | steel-os.org live, Download button says "coming soon" | R2 upload workflow in step 6 |
| Everything else | To Do | Below |

### Step 1: Unblock (week of 2026-10-19)

Nothing here needs code. It needs three people to answer and click.

| Who | Story | Do this |
|---|---|---|
| rodger-roberts-dev | PRs #1 to #8 | Review and merge, or comment what to change |
| rodger-roberts-dev | STEEL-16 | Create the cosign signing key and store the private half as the GitHub secret `SIGNING_SECRET`; commit `cosign.pub` |
| rodger-roberts-dev | STEEL-29 | Export the shortcut and Konsole files from the Katana checkpoint |
| rodger-roberts-dev | STEEL-23, STEEL-25 | Decide the rebuild cadence; say how Forge will be packaged (Flatpak, AppImage, container) |
| T | STEEL-26 | Create an R2 API token for the `downloads.steel-os.org` bucket; rodger adds it as GitHub secrets (never in the repo) |
| T | STEEL-20 | From the Bazzite VM, list the start-menu apps Steel OS should not ship |
| T | STEEL-43 | USPTO trademark search for "Steel OS" |
| T | STEEL-42 | Steel OS card on blackbox-entertainment.com |
| T | STEEL-1, 2, 3, 4, 6, 28 | Move to Done after the merges |

### Step 2: First image, version 0.2 (target 2026-11-06)

| Order | Story | What | Who | Waits on |
|---|---|---|---|---|
| 1 | STEEL-16 | Universal Blue template in the repo: `Containerfile` from `bazzite:stable`, `build.sh`, `system_files/`, `disk_config/`, workflows. Old Omarchy-era files removed. Image builds in GitHub Actions; ISO lands in R2 | Claude | cosign key, R2 secrets |
| 2 | STEEL-27 | Tuesday 4 am update schedule: drop-in for `uupd.timer` | Claude | STEEL-16 |
| 3 | STEEL-18 | Konsole as the terminal with Alt+C / Alt+V; WezTerm in the one-click list | Claude | STEEL-16 |
| 4 | STEEL-29 | rodger's shortcuts as the Plasma defaults | Claude, from rodger's files | STEEL-16, rodger's export |
| 5 | STEEL-31 | Wallpapers, logos, `os-release` name and `VARIANT_ID=steel-os`, boot splash, login screen | Claude | STEEL-16 |
| 6 | STEEL-5, STEEL-24 | Install the ISO in the VM and on Command; run the update and rollback test once on the real image | T | the ISO |

Test for the step: T boots the ISO, sees the waves wallpaper, presses
Super+Enter and gets Konsole, and `sudo bootc status` names the Steel OS image.

### Step 3: A desktop that says Steel OS, version 0.3 (target 2026-11-20)

| Order | Story | What | Who | Waits on |
|---|---|---|---|---|
| 1 | STEEL-7 | Panel layout, cascading windows confirmed, Plasma look | Claude | STEEL-16 |
| 2 | STEEL-19 | Firefox confirmed default browser on first boot; Chrome one click | Claude | STEEL-17 for the per-user part |
| 3 | STEEL-17 | First-boot script: default Flatpaks and per-user settings, safe to run twice | Claude | STEEL-16 |
| 4 | STEEL-20 | Remove what T listed in step 1 (`packages/remove.txt`). Decision recorded here: Waydroid, Bazzite's Android app runner, stays but off by default | Claude | T's list |
| 5 | STEEL-37 | Plain-English app names and menu categories | Claude | STEEL-20 |
| 6 | STEEL-22 | README rewritten for Bazzite, Firefox, Konsole | Claude | STEEL-16 merged |

### Step 4: Install like Windows, version 0.4 (target 2026-12-11)

| Order | Story | What | Who | Waits on |
|---|---|---|---|---|
| 1 | STEEL-35 | Full-screen "Install Steel OS" on the ISO; first-login wizard with Skip on every page | Claude | STEEL-16 |
| 2 | STEEL-40 | Steel Apps screen inside the wizard and in the start menu, built from `packages/steel-apps.txt` | Claude | STEEL-35 |
| 3 | STEEL-44 | Google Antigravity as a one-click install from a script; Google ships only a tar.gz, no Flatpak | Claude | STEEL-40 |
| 4 | STEEL-36 | Forgotten password: three security questions, hint on the login screen, recovery guide | Claude | STEEL-35 |
| 5 | STEEL-30 | One ISO: detect the graphics card at first boot, switch to the NVIDIA image | Claude | STEEL-16; T tests on Command with its real GPU |
| 6 | STEEL-21 | `docs/install.md`, plain English, screenshots from the VM | Claude writes, T follows it cold | STEEL-35 |

### Step 5: Easy like Windows and plays games, version 0.5 (target 2027-01-15)

| Order | Story | What | Who | Waits on |
|---|---|---|---|---|
| 1 | STEEL-38 | Printers and scanners from System Settings; `hplip`, `gutenprint-cups`, Skanpage | Claude; T tests with a real printer | STEEL-16 |
| 2 | STEEL-39 | Windows PCs visible, folder sharing without a terminal; `wsdd`, Samba, firewall rule | Claude; T tests with a Windows PC | STEEL-16 |
| 3 | STEEL-32 | Controllers, joysticks, flight sticks; Oversteer; compatibility page | Claude; T tests on Command | Command running Steel OS |
| 4 | STEEL-34 | Crew and Voxlore run on Steel OS from Steam | T | Command running Steel OS |
| 5 | STEEL-25 | Forge as a one-click install | rodger-roberts-dev packages, Claude adds to Steel Apps | rodger's answer from step 1 |

### Step 6: Release 1.0 (target 2027-01-30)

| Order | Story | What | Who | Waits on |
|---|---|---|---|---|
| 1 | STEEL-23 | Security patch policy written down: rebuild cadence and how fast a Bazzite fix reaches users | rodger decides, Claude writes | nothing |
| 2 | STEEL-26 | Release workflow uploads the signed ISO and checksums to R2 and updates `releases/latest.json` on steel-os.org | Claude | R2 secrets |
| 3 | STEEL-33 | Weekly Active Devices chart on steel-os.org from Fedora's Count Me data | Claude | `VARIANT_ID` live in the image for a few weeks |
| 4 | STEEL-41 | Release checklist run once: pin the Bazzite digest, build, test, sign, publish, flip the Download button | rodger signs and tags, T tests and flips, Claude writes the checklist | all of the above |

### Epics after 1.0

STEEL-12 Security has only the policy task today. After 1.0 it gets real
stories: full-disk encryption by default, Firefox policy hardening, and
whether an antivirus adds anything. That is on purpose; shipping a solid 1.0
comes first.

### How to read the order

- Steps 2 to 4 are a chain: each needs the one before. Step 5 only needs step
  2, so its stories can run alongside steps 3 and 4 when someone has time.
- Within a step, the order is the dependency order. Two people can work two
  rows at once if neither waits on the other.
- Every row is one branch, one PR, one "How to test" list for T.
