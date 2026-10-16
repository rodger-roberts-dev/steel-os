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
updater. Bazzite already does all of those well. We add our choices (WezTerm,
Chrome, cascading windows, rodger-roberts-dev's keyboard shortcuts), our
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
| Desktop | **KDE Plasma**, cascading windows, WezTerm terminal | T |
| Keyboard | rodger-roberts-dev's bindings ship as the Plasma defaults | rodger-roberts-dev (STEEL-29) |
| Keyboard-first or easy like Windows | Both, on Plasma | T |
| Apps | One store (Discover), one format (Flatpak), plus a curated Steel Apps list | STEEL-4 |
| Browser and office | Chrome default, Firefox one click, LibreOffice built in | T |
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
- `build.sh` installs the packages in `packages/image.txt` (WezTerm first).
- `system_files/` carries the first settings: WezTerm as the terminal, the
  Tuesday update schedule, a Steel OS name in the OS release file.
- The ISO workflow pointed at our image and at T's R2 bucket.
- The old Omarchy-era files (`config/hypr`, `scripts/bootstrap.sh`, the old
  package lists) removed or replaced in the same PR, so the repo has one story.

Tickets: STEEL-16 (image repo and first build), STEEL-18 (WezTerm),
STEEL-27 (Tuesday schedule, the schedule part only), STEEL-26 (R2 upload, the
bucket part only).

Test: T downloads the ISO from R2, installs it in the VM, logs in, opens
WezTerm from the start menu, and runs `sudo bootc status` to see the Steel OS
image name.

### Phase 2: "Desktop defaults" (version 0.3)

Goal: the desktop looks and behaves like Steel OS, not like stock Bazzite.

Deliverables:
- rodger-roberts-dev's keyboard shortcuts as system defaults
  (`/etc/xdg/kglobalshortcutsrc`), including Super+Return for WezTerm and
  Super+Space for the launcher. Every key still changeable by the user.
- Cascading window placement by default; Plasma's built-in tiling on
  Super+T for people who want it.
- Steel OS wallpaper, panel layout, login screen, and boot splash.
- Chrome installed and set as the default browser on first boot; Firefox in
  the Steel Apps list.
- Anything Bazzite ships that we do not want, listed in `packages/remove.txt`
  and removed in the recipe.

Tickets: STEEL-29 (bindings), STEEL-7 (Plasma defaults), STEEL-19 (browsers),
STEEL-20 (removals).

Test: T logs in, sees the Steel OS look, opens three windows that cascade,
presses Super+Return and gets WezTerm, clicks a link and gets Chrome.

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

1. Merge the open PRs (STEEL-1, STEEL-4, STEEL-6 and the CLAUDE.md setup).
   STEEL-2 and STEEL-3 can merge as background research or be closed.
2. rodger-roberts-dev puts his key bindings in the repo (STEEL-29) and creates
   the cosign key.
3. Claude starts STEEL-16: template files into the repo, first build.
4. T downloads the Bazzite ISO now and installs it in the VM, so the first
   Steel OS ISO has a known-good comparison.
