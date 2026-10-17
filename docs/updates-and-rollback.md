# Updates and rollback

## Steel OS today (Bazzite base)

Steel OS inherits Bazzite's updater. Every Steel OS machine runs one image;
an update is the next image, downloaded in the background and applied at the
next restart. The previous image stays in the boot menu.

- **When:** every **Tuesday at 4 am** local time. If the machine was off, the
  update runs at the next boot instead. A random delay of up to 15 minutes
  spreads the load. Set by `system_files/etc/systemd/system/uupd.timer.d/steel-os-tuesday.conf`.
- **What:** the system image, Flatpak apps, firmware and Bazzite's extras, in
  one run of Bazzite's `uupd` tool.
- **Applying it:** the new image takes effect at the next restart. Nothing
  changes under a running session.
- **Going back:** at the boot menu pick the previous entry, or run
  `sudo bootc rollback` in Konsole. Tested in the VM on 2026-10-16.
- **Checking by hand:** `systemctl list-timers uupd.timer` shows the next run;
  `sudo uupd` runs an update now.

Still to come: plain-English restart notification, daily Flatpak
updates between Tuesdays, the security patch policy.

---

## Background: the Omarchy-era research (2026-10-15)

The rest of this page was written when Steel OS was planned on Omarchy (Arch
Linux). It is kept because the user-facing requirements still apply.


Date: 2026-10-15

> **Status: background.** Later the same day the team chose a Fedora Atomic
> base via Bazzite. This document describes Omarchy's update system
> and is kept because it shaped the requirements: a snapshot before every
> update, rollback from the boot menu, a visible boot menu, and automatic
> Tuesday updates. On Bazzite those come from `uupd` and `rpm-ostree`: the
> whole image updates at once, the previous image stays in the boot menu, and
> the updater runs daily at 4 am by default (Steel OS sets it to Tuesday). See
> `docs/roadmap.md` phase 3.
Owner: rodger-roberts-dev (research done by Claude Code from source; VM test still open)

**How this was researched.** By reading the Omarchy source code at commit
`51bfd1d` (version 4.0.0.alpha, dated 2026-10-15), its user manual, and its
internal update design document, and by checking Omarchy's package servers
directly. Nothing was run on a real machine. The "how to test" section at the
end is what still needs doing in a VM.

---

## 1. The short answer

Omarchy already does almost everything product goal 1 asks for. On a fresh
Omarchy install today:

- Users **do not** get raw Arch updates. They get packages from Omarchy's own
  mirror, which is deliberately held about one month behind Arch.
- A **snapshot is taken before every update**, automatically.
- The user **can roll back from the boot menu** to any of the last five
  snapshots.
- Running the raw Arch update command by hand is **blocked** with a message
  pointing back to the Omarchy updater.

**Recommendation: do not build a Steel OS updater or package mirror.** Adopt
Omarchy's update system exactly as it is, lock Steel OS to Omarchy's stable
channel, and spend our effort on the gaps that matter to a non-technical user.
The biggest of those gaps is that the boot menu shows for **one second**, so a
normal person will never find the rollback option. Section 5 lists the gaps and
section 7 lists the follow-up tickets.

---

## 2. What happens when a user updates, step by step

This is what Omarchy's `omarchy update` command does today, in order, taken
from its source. A user reaches it by clicking the circle-arrow icon that
appears next to the clock when an update is available, or from the menu
(Super + Space, then Update, then Omarchy).

| Step | What happens | Why it matters |
|---|---|---|
| 1 | A box asks "ready to update?" and warns not to interrupt it. Password asked once. | One password prompt, not many. |
| 2 | Checks there is at least 10 GB free on the system disk. Refuses otherwise. | A full disk can't snapshot safely. |
| 3 | Trims the download cache to the last two versions of each package. | Keeps an offline "downgrade" copy. |
| 4 | **Takes a snapshot** of the system disk with snapper, labelled with the Omarchy version. Keeps the newest 5. Adds it to the boot menu. | This is the rollback point. |
| 5 | Stops the machine from going to sleep. | A laptop lid closing mid-update is dangerous. |
| 6 | Makes sure the package signing keys are current. | Prevents "invalid signature" failures. |
| 7 | **Updates every package** on the system from Omarchy's mirror and Omarchy's own package repository. | The main event. |
| 8 | **Runs migrations**: small one-time scripts that fix up settings when a default changed. Each runs once per user and is remembered. | How config changes reach existing machines. |
| 9 | Removes packages nothing needs any more. Scans the log for a known boot-image failure. | Housekeeping. |
| 10 | Restarts services that changed and restarts the desktop shell. | So the new versions are actually running. |
| 11 | Runs the user's `post-update` hook, if one exists. | **This is where Steel OS can attach its own steps.** |
| 12 | Updates any AUR (community) packages, last, with a separate password prompt. | Community packages run untrusted build code, so they are isolated. |
| 13 | Checks the boot files are valid. If not, says "do not reboot" and stops. | Prevents an unbootable machine. |
| 14 | Offers a reboot if one is needed. | Done. |

Everything is written to a log at `/tmp/omarchy-update.log`.

### What stops people from bypassing it

Omarchy installs a hook into the package manager itself. If anyone runs
`sudo pacman -Syu` (the raw Arch update) they get a message that starts
"Woah partner..." and the update is cancelled before anything changes. There is
an escape hatch for experts, but it has to be typed deliberately.

---

## 3. How Omarchy curates updates: the channels

This is the part most people do not know, and it is the answer to "how would
Steel OS curate updates?"

Omarchy has **four update channels**. A machine is on exactly one.

| Channel | Who it is for | Where packages come from |
|---|---|---|
| **stable** (default for new installs) | Everyone | Omarchy's own Arch mirror, frozen about **one month behind** Arch, plus Omarchy's stable package repo |
| rc | Testers before a release | A mirror one step ahead of stable |
| edge | Experienced Linux users | Latest Arch, latest Omarchy builds |
| dev | People working on Omarchy itself | A live source checkout |

**Verified:** on 2026-10-15 the stable mirror's package index was last updated
2026-09-08, 37 days earlier. The one-month lag is real and current.

Omarchy also runs its **own package repository** with 237 packages on the
stable channel. It carries things Arch does not ship, so they do not have to
come from the untrusted AUR. Relevant to us: `google-chrome`,
`xpadneo-dkms` (Xbox controllers), `umu-launcher` (Battle.net),
`heroic-games-launcher-bin`, `minecraft-launcher`, `spotify`, `1password`,
`dropbox`, and Omarchy's own kernel `linux-omarchy`.

So "users never get raw Arch updates" is **already true on the stable
channel**. Steel OS inherits it for free.

### The trade-off to decide

A month-old mirror means a security fix published by Arch today reaches a
stable-channel machine up to a month later. Omarchy accepts that. Product goal
5 (built-in security) may not. Options, for rodger-roberts-dev to decide:

- Accept the lag (simplest, what Omarchy does).
- Run on edge instead (defeats goal 1).
- Ask upstream whether security-only packages could be fast-tracked on stable.

---

## 4. How rollback works today

1. Restart the computer.
2. At the Omarchy boot menu, pick **Snapshots**, then the snapshot dated just
   before the update. The Omarchy version it was taken on is shown.
3. The machine boots into that snapshot. A notification appears saying you are
   in a snapshot; clicking it starts the restore. (Or run
   `omarchy-snapshot restore`.)
4. The system disk is put back to how it was. **Your personal files in /home
   are not touched**, and your settings under `~/.config` are kept as-is.

Facts that shape what we can promise users:

- Rollback restores the **system**, not personal files. It is not a backup.
- Only the last **5** snapshots are kept. No scheduled "timeline" snapshots.
- It only works on installs using the Limine boot loader on a btrfs disk, which
  has been the Omarchy default since version 2.0. Every fresh install qualifies.
- If a user turns on "Direct Boot" (skips the boot menu), rollback requires
  picking Limine from the BIOS boot list first.
- If snapper is somehow not configured, the update **continues without a
  snapshot** and prints a warning. It does not refuse.
- Two bigger resets also exist: `omarchy reinstall` puts packages and configs
  back to stable defaults, and Setup, then Reset Computer, restores the
  factory snapshot the installer took (wipes users, like a phone reset).

---

## 5. Gaps for a non-technical user

Ordered by how much they matter to goal 1 and goal 2.

1. **The boot menu shows for one second.** Omarchy's Limine config sets
   `timeout: 1`. A user who does not know to hammer a key at power-on will
   never see "Snapshots". This single setting makes rollback effectively
   invisible to the people we are building for.
2. **Nothing offers a rollback after a bad update.** If the desktop fails to
   start after an update, the user sees a black screen or a login loop and no
   prompt saying "the last update may have caused this; restore?".
3. **The update runs in a terminal window.** It works, but it is a wall of
   scrolling text, and the failure message is "review the output above". A
   Windows user will not know what to do with that.
4. **The 10 GB free-space refusal has no guidance.** It just stops.
5. **Config-file leftovers are not handled.** Omarchy's own design notes list
   `.pacnew` / `.pacsave` handling as still missing. Over time these pile up
   silently.
6. **Snapshots are not backups.** We must say so clearly or users will assume
   their documents are protected.
7. **Community (AUR) packages prompt for the password a second time** at the
   end of an update. Confusing, and a reason to avoid AUR packages in the
   default Steel OS set.
8. **Channel switching is one menu click away** (Update, then Channel). A
   curious user can move themselves to edge and lose the curation.
9. **KDE Plasma was chosen as the default desktop after this research**
   (ARCHITECTURE.md, decision 5.1). Omarchy's update restarts its own desktop
   shell and pauses and resumes Hyprland config reloads. On a Plasma session
   those steps must be confirmed to fail harmlessly, and the "update available"
   icon in Omarchy's top bar will not exist, so Steel OS needs its own way to
   tell a Plasma user an update is ready.

---

## 6. Options compared

| Option | What it means | Verdict |
|---|---|---|
| **A. Adopt Omarchy's updater and stable channel, add a Steel OS layer on top** | Keep `omarchy update`. Lock the channel. Fix the boot-menu timeout. Add friendly wrapping and a rollback prompt. Ship Steel OS's own migrations through Omarchy's `post-update` hook. | **Recommended.** Gets 90% of goal 1 for almost no code, and stays compatible with every upstream Omarchy release. |
| B. Run our own Arch mirror and pin packages ourselves | Duplicate Omarchy's mirror infrastructure under our control. | Rejected. Omarchy already runs exactly this, with Cloudflare in front. Two people cannot maintain a mirror. |
| C. Write a Steel OS updater | Replace `omarchy update`. | Rejected. Omarchy actively guards its update path; we would be fighting upstream on every release, and we would lose migrations, snapshots and boot verification that already work. |

**Why A:** the problems a non-technical user actually hits are presentation and
discoverability, not the update engine. Option A spends our time there.

### How Steel OS attaches to the update (for the build tickets)

Omarchy runs `~/.config/omarchy/hooks/post-update` and every file in
`~/.config/omarchy/hooks/post-update.d/` near the end of each update. Steel OS
can drop a script there that runs Steel OS's own migrations (a `migrations/`
folder in this repo, same idea as Omarchy's: one timestamped idempotent script,
remembered once run). No change to Omarchy code is needed.

---

## 7. Follow-up tickets to create

Each is sized to be finished in about a week.

1. **Make rollback discoverable at boot.** Raise the Limine timeout to 3 to 5
   seconds and brand the menu: "Steel OS" with a line like "Press any key for
   recovery options". Rename the Snapshots entry to something like "Restore an
   earlier version". Ship as a Steel OS config plus migration.
2. **Lock the stable channel.** Hide or guard the Update, then Channel menu
   entry on Steel OS so a user cannot accidentally leave stable. Decide whether
   an "Advanced" path remains.
3. **Steel OS migrations through the post-update hook.** Create
   `migrations/` in this repo and the hook script that runs pending ones.
   Idempotent, remembered per user, mirrors Omarchy's own mechanism.
4. **Friendly update window.** Wrap `omarchy update` with plain-English
   messages: before (what will happen, how long), the free-space check with
   advice, and after (success, or "something went wrong, here is how to roll
   back").
5. **Post-update health check.** On the first boot after an update, detect a
   desktop that fails to start, or a boot that did not reach login, and offer
   the rollback in plain words. Needs design: a boot counter or a "last update
   succeeded" marker.
6. **Decide the security patch policy.** rodger-roberts-dev and T decide
   between accepting the one-month lag, or asking upstream about fast-tracked
   security updates. Record the decision in `ARCHITECTURE.md`.
7. **VM test of a full update and rollback cycle.** The acceptance test this
   research could not do (see below). Produce screenshots for the manual.
8. **Automatic updates every Tuesday, Windows-style** (added by T on
   2026-10-15). Omarchy's updater has an unattended mode (`omarchy update -y`)
   but expects a logged-in user with sudo and a terminal, so a background
   timer needs its own authorisation path and a "restart now or later"
   notification. Depends on tickets 4 and 5.

---

## 8. How to test (in a VM, not done yet)

For T on the test machine, or rodger-roberts-dev.

1. Install Omarchy from its ISO in a VM with at least 40 GB disk. Confirm it is
   on the stable channel: open a terminal and run `omarchy-channel-current`.
   Expect `stable`.
2. Open Super + Space, Update, Omarchy. Watch an update run. Note whether the
   snapshot step prints "Create system snapshot".
3. Restart. At power-on, hold or tap a key immediately and note whether the
   boot menu appears and how long it stays. Confirm a "Snapshots" entry exists.
4. Pick the newest snapshot, boot it, click the notification, restore. Confirm
   the machine comes back and personal files in the home folder are intact.
5. In a terminal, run `sudo pacman -Syu`. Expect the "Woah partner" refusal.
6. Once KDE Plasma exists: log in to the Plasma session and run
   `omarchy update` from a terminal. Note any errors about the shell or
   Hyprland. The update must still finish and the snapshot must still exist.
7. Write down anything that confused you. That list becomes the wording for
   ticket 4 above.
