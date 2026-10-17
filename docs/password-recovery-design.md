# Forgotten password: design

Updated: 2026-10-17. Status: **decisions made by BBE on 2026-10-17** (see the end).
S&C reviews the security details in the pull request that builds it.

Windows users expect security questions and a reset from the login screen. On
Linux a forgotten password means a terminal procedure at the boot menu or a
reinstall, and a non-technical user would conclude the PC is broken. This is
how Steel OS closes that gap without weakening the system, and as close to
Windows as Linux allows.

---

## What the user sees

1. **Setting it up.** One optional page in Steel OS Setup at first login:
   - Choose three questions from a list (first pet, city you were born in,
     favourite teacher and so on) and type the answers.
   - Confirm with your password.

   It can be changed later from "Security questions" in the Steel OS Portal.
2. **At the login screen.** A **Forgot your password?** link sits under the
   password box, like Windows' "Reset password".
3. **Resetting.** Clicking it explains that the PC will restart into password
   reset, with **Restart** and **Cancel** buttons. After the restart:
   - a full-screen Steel OS window, in the same style as Steel OS Setup, asks
     for the user name and the three answers;
   - then it asks for a new password, twice;
   - then the PC continues to the login screen.
4. **No questions set up?** The reset window says so plainly and explains the
   other way back in: another administrator on the PC can set a new password
   in System Settings, Users.

Windows can do the reset without a restart, because its login screen can run
privileged programs. On Linux the login screen deliberately can't, which is a
security boundary worth keeping, so Steel OS does the reset during a short
restart instead.

## How it works

| Part | Design |
|---|---|
| Storing the answers | Answers are trimmed and lower-cased, then hashed with yescrypt, the same scheme as `/etc/shadow`, each with its own salt. They are stored in `/var/lib/steel-os/recovery/<user>`, owned by root, mode 0600. The answers themselves are never stored. |
| Writing them | A small helper, `steel-os-recovery-enrol`, run through pkexec. Its polkit action is `auth_self`: the user must type their own password. |
| Login screen | A Steel OS version of the Plasma login theme (Breeze, SDDM) with a **Forgot your password?** link and a confirmation. |
| Starting the reset | The login screen can only do two things here. It writes a "reset requested" note into a folder that only the login screen and root can use, then restarts the PC with the login screen's built-in restart. It cannot run programs or read any recovery data. |
| The reset itself | At the next boot a system service runs before the login screen. It runs only when the note is present, and deletes the note straight away. As root, it shows the reset window in a minimal full-screen session on the PC's own screen. It checks the answers against the hashes and sets the new password with `chpasswd`. Then the login screen starts. If the graphical window can't start, the same steps run in text mode. |
| Guessing limits | Three wrong attempts lock the reset for 15 minutes, counted per user in a root-only file. Each attempt also waits two seconds. |
| Encrypted disks | The reset changes only the login password. The disk-encryption password is typed before Steel OS starts and **cannot be recovered by anyone**. The setup page, the reset window and the install guide all say so. |

## Security notes

- **Security questions are weaker than a password.** They are a convenience
  for home PCs. The setup page says so, and they are optional.
- **Physical access.** Without disk encryption, anyone with physical access can
  already reset a password, for example from a USB stick. The questions add
  convenience, not new exposure. With encryption, the reset only runs after
  the disk has been unlocked.
- **No remote path.** The reset can only be started from the login screen on
  the PC itself, and it only runs on the PC's own screen. It never runs over
  SSH or remote desktop.
- **The login screen gets no new powers.** It can request a reset and restart,
  which it can already do. It never sees the answers or the hashes.
- **Small code.** Three small, reviewable pieces: the enrol helper, the
  boot-time reset service and the theme change.

## Decisions (BBE, 2026-10-17)

| Question | Decision |
|---|---|
| Hash the answers with yescrypt, as `/etc/shadow` does | Yes |
| Start the reset from the login screen with a restart, rather than an extra entry in the boot menu | Yes, and make it as close to Windows as possible: a link on the login screen and a graphical reset window |
| Allow the reset for administrator accounts | Yes |
| Password hint on the login screen | Dropped |
