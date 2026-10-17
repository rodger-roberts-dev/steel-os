# Steel OS roadmap

Updated: 2026-10-17

Where Steel OS is today and what comes before version 1.0. Dates are targets,
not promises. Work is planned in the project's private tracker and lands here
as pull requests.

**The strategy in one sentence:** Steel OS is a custom Bazzite image, with
Fedora Atomic underneath and KDE Plasma on top, built from a recipe that GitHub
turns into an image and an installer. We don't fork Bazzite, write our own
installer or updater, or run a package mirror. Bazzite already does those well.
We add our choices, our branding, a Tuesday update schedule, one-click apps and
the polish a Windows user expects.

---

## Done

- **The image.** Built and signed by GitHub Actions every day and after every
  merged change, published at `ghcr.io/steel-and-code/steel-os`.
- **The installer ISO.** Boots to a Steel OS live desktop with Bazzite's modern
  installer in Steel OS colours. Default apps are preloaded.
- **Steel OS everywhere.** The name, logo, boot splash, login and lock screens,
  wallpapers, start button, terminal welcome and hostname say Steel OS, not
  Bazzite or Fedora.
- **Desktop defaults.** KDE Plasma with cascading windows, Konsole as the
  terminal, Firefox as the browser, plain-English app names, four desktops.
- **Keyboard shortcuts.** Super+Enter for the terminal, Super+Shift+Enter for
  Firefox, Super+1 to 4 for desktops, and the rest of the list in
  [keyboard-shortcuts.md](keyboard-shortcuts.md). Applied for every user.
- **Steel OS Portal.** Welcome, one-click Steel Apps (Slack, Zoom, Discord,
  Chrome, GIMP, VS Code, Antigravity and more), and system tools.
- **Virtual machines.** Virtual Machine Manager works right after a one-click
  install.
- **Updates.** Automatic every Tuesday at 4 am, with the previous version kept
  in the boot menu. See [updates-and-rollback.md](updates-and-rollback.md).
- **Licences and credits.** Apache-2.0, a NOTICE file crediting Bazzite,
  Universal Blue and Fedora, and links to all source code.

## Next: 0.2.0 Preview for testers (target: early November 2026)

- The installer defaults to "Use entire disk", ends with **Restart now**, and
  has no Fedora feedback page.
- A welcome screen at first login, where every step can be skipped.
- Steel Apps grouped into Everyday, Work, Creative, Games and Developer tabs.
- An install guide in plain English and a release checklist.
- A **Download Preview** button on steel-os.org, with a SHA-256 checksum,
  release notes and known issues.

## Then: 0.3 to 0.5 (target: 15 January 2027)

- **Accounts.** Forgotten-password recovery with security questions and a hint
  on the login screen.
- **Graphics.** One installer for every PC: it detects an NVIDIA card and
  switches to the right image.
- **Updates and security.** A plain-English restart notice, apps updating daily,
  machines that refuse unsigned updates, and a written patch policy.
- **Printers and network.** Printers and scanners such as the Canon PIXMA
  MG3620 working over USB with no driver download, Windows PCs visible on the
  network, and right-click folder sharing. See
  [printers-and-network.md](printers-and-network.md).
- **Gaming.** Controllers and flight sticks, Star Citizen and World of Warcraft
  that keep working after game patches, and Repair buttons.

## 1.0 (target: 30 January 2027)

- **Steel Shield.** Free, built-in virus protection and an honest security
  dashboard. It scans downloads automatically and USB drives on request, keeps
  a recoverable quarantine, explains findings in plain English, and updates its
  definitions hourly.
- The release checklist run end to end, and a newcomer installing Steel OS from
  the guide alone.
- The main **Download** button on steel-os.org switched on.

## After 1.0

- Disk encryption by default, and Firefox hardening.
- A Hyprland tiling session as a separate image, if people ask for it.
- GNOME only if users ask.
