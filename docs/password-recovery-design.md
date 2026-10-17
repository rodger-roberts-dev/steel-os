# Forgotten password: design for review

Updated: 2026-10-17. Status: **proposal, waiting for S&C's approval.** Nothing
here is built yet.

Windows users expect a password hint, security questions and a reset. On Linux
a forgotten password means a terminal procedure at the boot menu or a
reinstall, and a non-technical user would conclude the PC is broken. This is
how Steel OS proposes to close that gap without weakening the system.

---

## What the user sees

1. **Setting it up.** One extra page in Steel OS Setup at first login, which
   can be skipped:
   - Choose three questions from a list (first pet, city you were born in,
     favourite teacher and so on) and type the answers.
   - Optionally, type a password hint.
   - Confirm with your password.

   It can be changed later from a "Password recovery" entry in System Settings
   or the Portal.
2. **At the login screen.** After a wrong password, the hint appears under the
   password box, along with a **Forgot your password?** button.
3. **Resetting.** **Forgot your password?** explains that the PC will restart
   into password reset, with **Restart** and **Cancel** buttons. After the
   restart, a full-screen Steel OS page asks for the user name and the three
   answers, then a new password, twice. The PC continues to the login screen.
4. **No questions set up?** The reset page says so plainly and explains the
   other way back in: another administrator on the PC can set a new password
   in System Settings, Users.

## How it works

| Part | Proposal |
|---|---|
| Storing the answers | Answers are trimmed and lower-cased, then hashed with yescrypt, the same scheme as `/etc/shadow`, each with its own salt. They are stored in `/var/lib/steel-os/recovery/<user>`, owned by root, mode 0600. The answers themselves are never stored. |
| Writing them | A small helper, `steel-os-recovery-enrol`, run through pkexec. Its polkit action is `auth_self`: the user must type their own password, which proves they are who they say. |
| The hint | Stored in `/var/lib/steel-os/recovery/hints/<user>`, readable by the login screen. The setup page warns: "Anyone at this PC can see the hint. Don't put your password in it." |
| Login screen | A Steel OS version of the Plasma login theme (Breeze, SDDM) that shows the hint after a failed attempt and adds **Forgot your password?** |
| Starting the reset | The login screen can't run privileged programs, and it shouldn't. The button calls one narrow helper, allowed by a polkit rule for the `sddm` user only. That helper does two things: it writes a "reset requested" flag and restarts the PC. Nothing else is possible through it. |
| The reset itself | At the next boot a system service runs before the login screen. It runs only when the flag is set, and deletes the flag straight away. It shows a full-screen text wizard on the console as root, checks the answers against the hashes, and sets the new password with `chpasswd`. Then the login screen starts. |
| Guessing limits | Three wrong attempts lock the reset for 15 minutes, counted per user in a root-only file. Each attempt also waits two seconds. |
| Encrypted disks | The reset changes only the login password. The disk-encryption password is typed before Steel OS starts and **cannot be recovered by anyone**. The setup page, the reset page and the install guide all say so. |

## Security notes

- **Security questions are weaker than a password.** They are a convenience
  for home PCs. The setup page says so, and they are optional.
- **Physical access.** Without disk encryption, anyone with physical access can
  already reset a password, for example from a USB stick. The questions add
  convenience, not new exposure. With encryption, the reset only runs after
  the disk has been unlocked.
- **No remote path.** The reset can only be started from the login screen on
  the PC itself, and it only runs on the local console. It never runs over SSH
  or remote desktop.
- **Small code.** Three small, reviewable pieces: the enrol helper, the
  "request reset and restart" helper, and the boot-time wizard. Plus one polkit
  rule and a theme change.
- **Administrators.** The reset works for any account that has questions set
  up. An administrator account stays an administrator; nothing is added or
  removed.

## Questions for S&C

1. **Hashing.** Is yescrypt via libxcrypt (the same library that `/etc/shadow`
   uses) acceptable for hashing the answers?
2. **The login-screen button.** Is this mechanism acceptable: flag, restart,
   then a wizard before the login screen? The alternative is a GRUB menu entry,
   which is harder to add on an image-based system.
3. **Who can use it.** Should the reset be allowed for administrator accounts,
   or only for standard accounts?
4. **Hints.** Keep the hint, or drop it as too easy to misuse?

Once approved, this becomes one pull request, tested on a virtual machine with
a deliberate lock-out.
