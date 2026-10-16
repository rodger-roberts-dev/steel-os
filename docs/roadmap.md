# Steel OS Build Roadmap

Jira: STEEL-6
Date: 2026-10-15
Written for: T and rodger-roberts-dev

This is the plan to go from today's repo (package lists and one audit script) to
a Steel OS a stranger can install, update, and use. It is built on the findings
in `ARCHITECTURE.md` (STEEL-1), `docs/updates-and-rollback.md` (STEEL-2),
`docs/printers-and-network.md` (STEEL-3), and `docs/app-install-plan.md`
(STEEL-4).

---

## The one-sentence strategy

**Steel OS is Omarchy's stable channel plus a Steel OS layer on top.** We do
not fork Omarchy, build an installer, run a package mirror, or write an
updater. Omarchy already does all of those well. We add the choices, the
polish, and the tools a non-technical Windows user needs, and we ship them in a
way that survives every Omarchy update.

What that means in practice: a Steel OS machine is an Omarchy machine with a
`steel-os` package installed. That package carries our configs, our scripts,
our menu entries, and our migrations. Installing Steel OS is "install Omarchy,
then install the Steel OS package". Updating is Omarchy's updater, which runs
our migrations through its post-update hook.

---

## Phases

Each phase ends with something T can test on the test machine and something a
user would notice. Phases are in order; later ones depend on earlier ones.

### Phase 0: Foundations (in progress, October 2026)

Goal: everyone works from the same facts, and there is a machine to test on.

| Done when | Ticket |
|---|---|
| Architecture written down | STEEL-1 (PR open) |
| Updates and rollback researched | STEEL-2 (PR open) |
| Printers and network evaluated | STEEL-3 (PR open) |
| App lists verified and install path chosen | STEEL-4 (PR open) |
| Test machine ready | STEEL-5 (T) |
| Three decisions recorded in ARCHITECTURE.md | new ticket, rodger-roberts-dev and T |

The three decisions that block later phases:
1. **Default desktop:** keep Hyprland, Hyprland plus mouse-friendly additions,
   or KDE Plasma. Affects phases 3 and 4 heavily.
2. **Security patch policy:** accept Omarchy stable's one-month lag, or not.
3. **Repo home:** stay under rodger-roberts-dev or transfer to the
   blackbox-entertainment organisation. Low effort, but affects the package
   build setup in phase 1.

### Phase 1: "Configured Omarchy" (version 0.2)

Goal: one command turns a fresh Omarchy install into Steel OS, and running it
again changes nothing.

Deliverables:
- `scripts/install.sh`: run on a fresh Omarchy machine. Installs everything in
  `core.txt` and `development.txt` using Omarchy's own package commands,
  installs Chrome and sets it as default, copies the `config/` files into
  place, applies the agreed removals from `review.txt`, and sets WezTerm as
  the default terminal. Safe to run twice. Must pass shellcheck.
- `migrations/` folder and a runner hooked into Omarchy's `post-update` hook,
  so any later change to a config reaches machines that already ran install.
- `docs/install.md`: the plain-English "how to install Steel OS" page.

Tickets to create: install script; migrations runner and hook; WezTerm as
default terminal; Chrome default and Firefox optional; apply review.txt
decisions; install guide.

Test: T installs Omarchy on the test machine, runs one command, and ends up
with WezTerm, Chrome, Steam and the rest. Runs it a second time; nothing
changes.

### Phase 2: "Safe Updates" (version 0.3)

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

### Phase 3: "Easy Like Windows" (version 0.4)

Goal: printers, scanners, network shares, and app installs without a terminal.

Deliverables (from STEEL-3 and STEEL-4):
- Scanning (`simple-scan`), printer drivers (`hplip`, `gutenprint`), and
  `wsdd` added to the default packages. Decision on turning on automatic
  printer discovery.
- Folder sharing wizard: pick a folder, set a password, firewall opened for
  the local network only, machine visible in Windows Explorer.
- Steel Apps install menu and the Advanced submenu.
- A "Printers and Scanners" and a "Sharing" entry in the Setup menu.
- If the desktop decision was "Hyprland plus mouse-friendly", this is where a
  visible app menu or dock lands.

Test: T adds a printer, scans a page, opens a share on a Windows PC, shares a
folder back, and installs Discord, all without opening a terminal.

### Phase 4: "Plays Games" (version 0.5)

Goal: product goal 3.

Deliverables:
- Steam and Xbox controller support installed by `install.sh` by default (both
  use Omarchy's installers).
- Battle.net offered in the Steel Apps menu.
- A short "gaming on Steel OS" page: Proton, what works, what does not.

Test: T plays a Steam game and a Battle.net game with a controller, following
only the page.

### Phase 5: "Built-in Security" (version 0.6)

Goal: product goal 5, defined concretely.

This phase needs a design ticket first, because "built-in security" is not yet
specific. Candidates to evaluate and decide on, not to build blindly:
- Keep Omarchy's defaults (full-disk encryption, firewall closed, no SSH):
  already strong. Document them for users.
- The security patch policy decided in phase 0, implemented.
- Whether an antivirus (ClamAV) adds real protection for this audience or
  just reassurance. Many Linux experts say it does not.
- Browser hardening through Chrome's policy files, which Omarchy already
  supports.
- Automatic snapshot before any Steel OS tool makes a system change.

Test: defined by the design ticket.

### Phase 6: "Steel OS ISO" (version 1.0)

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
becomes `pacman -S steel-os`.

Test: a person outside the team installs Steel OS from the download page using
only the install guide.

---

## Ways of working that keep this on the rails

- **Track Omarchy stable, not edge.** Omarchy is at version 4.0.0 alpha and
  changes daily. Pin every Steel OS release to the Omarchy stable release it
  was tested on, and record it in `ARCHITECTURE.md`.
- **Never edit Omarchy's files.** Everything Steel OS does goes through the
  extension points Omarchy provides: the menu extension file, the hooks
  directory, `~/.config` overrides, and our own package. This is what makes
  upstream updates safe.
- **One story, one branch, one PR, one "how to test" list.** Already the rule.
- **T tests every phase on the test machine before it is called done.**
- **Automated checks** as soon as there is a script to check: shellcheck in a
  GitHub Action on every PR, and later an unattended VM install.

## Risks

| Risk | What we do about it |
|---|---|
| Omarchy changes an extension point we rely on | Pin to stable; read upstream release notes before each Steel OS release; keep our layer thin. |
| Two people, limited time | Phases are small and each ends with something usable. Stop after any phase and still have a working OS. |
| The desktop decision drags | Phases 1 and 2 do not depend on it. Decide before phase 3. |
| "Easy like Windows" turns out to need a full settings app | Phase 3 uses menu entries and small wizards first. A settings app is a version 2 idea. |

## What happens next

1. Merge the STEEL-1 to STEEL-4 pull requests.
2. T finishes STEEL-5 (test machine).
3. rodger-roberts-dev and T make the three phase 0 decisions.
4. Create the phase 1 tickets and start with the install script.
