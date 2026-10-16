# Steel OS Build Roadmap

Jira: STEEL-6
Date: 2026-10-15
Written for: T and rodger-roberts-dev

This is the plan to go from today's repo (package lists and one audit script) to
a Steel OS a stranger can install, update, and use. It is built on the findings
in `ARCHITECTURE.md` (STEEL-1), `docs/updates-and-rollback.md` (STEEL-2),
`docs/printers-and-network.md` (STEEL-3), and `docs/app-install-plan.md`
(STEEL-4), and on the decisions T made on 2026-10-15 (ARCHITECTURE.md section 5).

---

## The one-sentence strategy

**Steel OS is Omarchy's stable channel plus a Steel OS layer on top, with KDE
Plasma as the desktop.** We do not fork Omarchy, build an installer, run a
package mirror, or write an updater. Omarchy already does all of those well. We
swap the desktop for one that behaves like Windows, keep Hyprland as a second
choice at login, and add the choices, polish, and tools a non-technical Windows
user needs, shipped in a way that survives every Omarchy update.

What that means in practice: a Steel OS machine is an Omarchy machine with a
`steel-os` package installed. That package carries our configs, our scripts,
our app list, and our migrations. Installing Steel OS is "install Omarchy,
then install the Steel OS package". Updating is Omarchy's updater, which runs
our migrations through its post-update hook.

---

## Decisions already made (2026-10-15)

| Decision | Answer | Who |
|---|---|---|
| Default desktop | **KDE Plasma**, cascading windows, WezTerm terminal. Hyprland kept as a second login option. | T, pending rodger-roberts-dev's technical review (STEEL-7) |
| Keyboard-first or easy like Windows | Both. Plasma for the mouse, Hyprland session and shortcuts for the keyboard. | T |
| Repo home | Stays at rodger-roberts-dev/steel-os for now. Transfer to blackbox-entertainment later. | T |
| Package names | Confirmed. See ARCHITECTURE.md 5.4 and STEEL-4. | T, verified |
| App store | A Steel Apps list inside the steel-os package. No server. | Recommended in STEEL-4 |

**Still open:** the security patch policy (accept Omarchy stable's one-month lag
or not). rodger-roberts-dev decides. It does not block phases 1 to 3.

---

## Phases

Each phase ends with something T can test on the test machine and something a
user would notice. Phases are in order; later ones depend on earlier ones.

### Phase 0: Foundations (in progress, October 2026)

Goal: everyone works from the same facts, and there is a machine to test on.

| Done when | Ticket |
|---|---|
| Architecture written down, decisions recorded | STEEL-1 (PR open) |
| Updates and rollback researched | STEEL-2 (PR open) |
| Printers and network evaluated | STEEL-3 (PR open) |
| App lists verified and install path chosen | STEEL-4 (PR open) |
| Test machine ready | STEEL-5 (T) |
| rodger-roberts-dev has reviewed the KDE Plasma decision | STEEL-7 |

### Phase 1: "Configured Omarchy" (version 0.2)

Goal: one command turns a fresh Omarchy install into Steel OS, and running it
again changes nothing. Desktop is still Hyprland in this phase; the point is
the install mechanism.

Deliverables:
- `scripts/install.sh`: run on a fresh Omarchy machine. Installs everything in
  `core.txt` and `development.txt` using Omarchy's own package commands,
  installs Chrome and sets it as default, installs Firefox, copies the
  `config/` files into place, applies the agreed removals from `review.txt`,
  and sets WezTerm as the default terminal. Safe to run twice. Passes
  shellcheck.
- `migrations/` folder and a runner hooked into Omarchy's `post-update` hook,
  so any later change to a config reaches machines that already ran install.
- `docs/install.md`: the plain-English "how to install Steel OS" page.

Tickets to create: install script; migrations runner and hook; WezTerm as
default terminal; Chrome default plus Firefox; apply review.txt decisions;
install guide.

Test: T installs Omarchy on the test machine, runs one command, and ends up
with WezTerm, Chrome, Firefox, Steam and the rest. Runs it a second time;
nothing changes.

### Phase 2: "Windows-like desktop" (version 0.3)

Goal: the machine boots into KDE Plasma with cascading windows, a start menu,
a taskbar, and WezTerm, and Hyprland is still there as a login choice.

This phase comes before the update work on purpose: every later test must run
on the real desktop, and the biggest unknown in the whole plan is how Omarchy's
updater behaves on a Plasma session.

Deliverables:
- Plasma installed by `install.sh` (`plasma-desktop` and the pieces of the
  `plasma` group we want, `dolphin`, `konsole` left out in favour of WezTerm,
  `print-manager`, `kde-gtk-config`). SDDM, which Omarchy already uses, set to
  default to Plasma with Hyprland in its session list.
- Plasma defaults shipped by Steel OS: cascading window placement, WezTerm as
  the terminal shortcut, a Steel OS wallpaper and panel layout.
- Confirmed: `omarchy update` runs to completion from a Plasma session, takes
  its snapshot, and any Hyprland-shell steps fail harmlessly. If they do not,
  the fix (a wrapper or a hook) lands here.
- A Plasma widget or notification that says "an update is ready", replacing
  Omarchy's top-bar icon.

Tickets to create: STEEL-7 (the decision and technical review), Plasma
install, SDDM default session, Plasma defaults, update-on-Plasma test and fix,
update-ready notification.

Test: T logs in, sees a Windows-like desktop, opens three windows that
overlap, opens WezTerm from the start menu, logs out, picks Hyprland at the
login screen, and gets the tiling desktop. Then runs an update from Plasma.

### Phase 3: "Safe Updates" (version 0.4)

Goal: product goal 1 is true in a way a non-technical user can actually use.

Deliverables (from STEEL-2 section 7):
- Boot menu shows for 3 to 5 seconds with Steel OS branding and a "press any
  key for recovery options" line. Snapshots entry renamed to plain English.
- Stable channel locked; the channel switcher hidden or guarded.
- Friendly update window around `omarchy update`.
- A post-update health check that offers rollback in plain words when the
  desktop fails to start.
- A one-page "Something went wrong after an update?" guide.

Test: T updates, then deliberately rolls back from the boot menu using only the
guide. Then T breaks the desktop on purpose (rodger-roberts-dev supplies a safe
way) and sees the rollback offer.

### Phase 4: "Easy Like Windows" (version 0.5)

Goal: printers, scanners, network shares, and app installs without a terminal.

Deliverables (from STEEL-3 and STEEL-4, now on Plasma):
- Printers: Plasma's System Settings Printers page (`print-manager`) is the
  front door. Add `simple-scan` or KDE's Skanpage for scanning, and `hplip`
  and `gutenprint` for older printers. Decide on automatic printer discovery.
- Network: Dolphin can find Windows PCs by WS-Discovery, so add `wsdd` and
  confirm it. Folder sharing wizard: pick a folder, set a password, firewall
  opened for the local network only, machine visible in Windows Explorer.
  Plasma's own "Share" tab in folder properties may cover most of this.
- Apps: the Steel Apps list (STEEL-4, option A) as a Plasma app, with the
  approved apps and an Install button each. Raw package search is for the
  terminal only.

Test: T adds a printer, scans a page, opens a share on a Windows PC, shares a
folder back, and installs Discord, all without opening a terminal.

### Phase 5: "Plays Games" (version 0.6)

Goal: product goal 3.

Deliverables:
- Steam and Xbox controller support installed by `install.sh` by default (both
  use Omarchy's installers, which work without the Hyprland shell).
- Battle.net offered in the Steel Apps list.
- A short "gaming on Steel OS" page: Proton, what works, what does not.

Test: T plays a Steam game and a Battle.net game with a controller, following
only the page.

### Phase 6: "Built-in Security" (version 0.7)

Goal: product goal 5, defined concretely.

This phase needs a design ticket first, because "built-in security" is not yet
specific. Candidates to evaluate and decide on, not to build blindly:
- Keep Omarchy's defaults (full-disk encryption, firewall closed, no SSH):
  already strong. Document them for users.
- The security patch policy, implemented.
- Whether an antivirus (ClamAV) adds real protection for this audience or
  just reassurance. Many Linux experts say it does not.
- Browser hardening through Chrome's policy files, which Omarchy already
  supports.
- Automatic snapshot before any Steel OS tool makes a system change.

Test: defined by the design ticket.

### Phase 7: "Steel OS ISO" (version 1.0)

Goal: a stranger downloads one file, boots it, and gets Steel OS with no extra
steps.

Two routes, cheapest first:
1. **Omarchy's unattended install.** Omarchy's ISO installs itself from a
   small config drive and can run a post-install step. Steel OS provides that
   config and the step. Zero ISO building. Good enough for most people.
2. **Our own ISO.** Omarchy publishes its ISO builder. Fork it, add the Steel
   OS package and branding, build on a schedule. Needed only if route 1 proves
   awkward for non-technical people.

Also in this phase: publish the `steel-os` package in our own small package
repository (Omarchy publishes its build tooling), so phase 1's install script
becomes `pacman -S steel-os`. This is a static set of files on GitHub Releases
or similar. It is not an app server; nothing needs to run.

Test: a person outside the team installs Steel OS from the download page using
only the install guide.

---

## Ways of working that keep this on the rails

- **Track Omarchy stable, not edge.** Omarchy is at version 4.0.0 alpha and
  changes daily. Pin every Steel OS release to the Omarchy stable release it
  was tested on, and record it in `ARCHITECTURE.md`.
- **Never edit Omarchy's files.** Everything Steel OS does goes through the
  extension points Omarchy provides: the hooks directory, `~/.config`
  overrides, and our own package. Swapping the desktop is additive: Plasma is
  installed next to Hyprland, not instead of it.
- **One story, one branch, one PR, one "how to test" list.** Already the rule.
- **T tests every phase on the test machine before it is called done.**
- **Automated checks** as soon as there is a script to check: shellcheck in a
  GitHub Action on every PR, and later an unattended VM install.

## Risks

| Risk | What we do about it |
|---|---|
| Omarchy's updater or migrations assume the Hyprland shell and misbehave on Plasma | Phase 2 tests exactly this before anything else is built on top. Keep Hyprland installed so the Omarchy session always still works. |
| Omarchy changes an extension point we rely on | Pin to stable; read upstream release notes before each Steel OS release; keep our layer thin. |
| Two people, limited time | Phases are small and each ends with something usable. Stop after any phase and still have a working OS. |
| Plasma pulls in a lot of KDE packages and a second set of settings | Install only the Plasma pieces we need; document which. |
| "Easy like Windows" turns out to need custom tools beyond Plasma's | Phase 4 uses Plasma's own settings pages first. Custom wizards only where Plasma has nothing. |

## What happens next

1. Merge the STEEL-1 to STEEL-4 and STEEL-6 pull requests.
2. rodger-roberts-dev reviews STEEL-7 (KDE Plasma) and answers its technical questions.
3. T finishes STEEL-5 (test machine).
4. Create the phase 1 tickets and start with the install script.
