# Keyboard Shortcuts: Omarchy to Steel OS (Plasma)

Jira: STEEL-29
Date: 2026-10-15
Written for: rodger-roberts-dev to review, and for the user manual later

rodger-roberts-dev's condition for the move to Bazzite was keeping his keyboard
shortcuts. His shortcuts are Omarchy's defaults plus one override (ALT+Return
opens WezTerm). This document lists every Omarchy default, taken from Omarchy's
source (`default/hypr/bindings/*.lua`, version 4.0.0.alpha), and what it
becomes on Steel OS. The result is shipped as system defaults in
`system_files/etc/xdg/kglobalshortcutsrc` and `kwinrc`.

**Super** is the Windows key. Plasma calls it **Meta**.

Legend: **Same** = same key, same result. **Changed** = same key, closest
Plasma behaviour. **None** = no Plasma equivalent; the key does nothing until
rodger-roberts-dev picks a replacement.

---

## 1. Apps and launcher

| Key | Omarchy | Steel OS | Status |
|---|---|---|---|
| Super+Space | Omarchy menu | KRunner (search, launch, calculate) | Changed: no menu tree, but the same reflex |
| Super+Alt+Space | Apps grid | Plasma Overview with the app grid | Same |
| Super+Return | Terminal | WezTerm | Same |
| **Alt+Return** | **WezTerm (rodger's override)** | **WezTerm** | **Same** |
| Super+Shift+Return, Super+Shift+B | Browser | Google Chrome | Same |
| Super+Shift+Alt+B | Private browser window | Not bound | None (Ctrl+Shift+N inside Chrome) |
| Super+Shift+F | File manager | Dolphin | Same |
| Super+Alt+Shift+F | File manager in terminal's folder | Not bound | None |
| Super+Shift+N | Editor | Kate | Same |
| Super+Shift+O | Obsidian | Obsidian (Flatpak) | Same |
| Super+Ctrl+Q, calculator key | Calculator | KCalc | Same |
| Super+Ctrl+T | Activity (btop) | System Monitor | Changed: graphical instead of terminal |
| Super+Ctrl+E | Emojis | Plasma emoji selector | Same |
| Super+K | Keybindings list | Shortcuts settings page | Changed |
| Super+Shift+M, Super+Shift+D, Super+Shift+G, Super+Shift+W, Super+Shift+/ | Spotify, Docker TUI, Signal, Omawrite, 1Password | Not bound | None: Omarchy preinstalls; add per app if wanted |
| Super+Shift+A/E/C/Y/P/X and friends | Omarchy web apps (ChatGPT, HEY, YouTube, Maps, X) | Not bound | None: HEY and friends are not Steel OS defaults |
| Super+Alt+Return, Super+Ctrl+Return | Tmux, Herdr | Not bound | None: Omarchy-specific terminal tools |

## 2. Windows

| Key | Omarchy | Steel OS | Status |
|---|---|---|---|
| Super+W, Super+Q | Close window | Close window | Same |
| Ctrl+Alt+Delete | Close all windows | Plasma log-out screen | Changed |
| Super+F | Full screen | Full screen | Same |
| Super+Alt+F | Full width (maximized) | Maximize | Same |
| Super+Ctrl+F | Tiled full screen | Not bound | None |
| Super+T | Toggle floating / tiling | Open Plasma's tile editor | Changed: windows float by default on Steel OS; Super+T is where tiling lives |
| Super+O | Pop window out (float and pin) | Keep window above others | Changed |
| Super+M | Minimize to dock | Minimize to taskbar | Same |
| Super+Left/Right/Up/Down | Focus window in that direction | Same | Same |
| Super+Shift+Left/Right/Up/Down | Swap window in that direction | Snap window to that half of the screen | Changed |
| Alt+Tab, Alt+Shift+Tab | Next / previous window | Same | Same |
| Super+P | Pseudo window | Not bound | None (tiling concept) |
| Super+J | Toggle split direction | Not bound | None (tiling concept) |
| Super+L, Super+Alt+L | Cycle workspace layout | Not bound | None (tiling concept) |
| Super+Home, Super+Alt+Home | Save / restore window width | Not bound | None |
| Super+minus / Super+equals and the Shift, Alt, Ctrl variants | Resize window in steps | Not bound | None: Plasma resizes with Super+right-drag or Alt+F8 |
| Super+G and the group keys | Window grouping | Not bound | None: Plasma has no window groups |
| Super+S, Super+grave, Super+Alt+S | Scratchpad workspace | Not bound | None: no scratchpad in Plasma |
| Super+Backspace, Super+Shift+Backspace, Super+Ctrl+Backspace | Transparency, gaps, square aspect | Not bound | None (Hyprland visual toggles) |
| Super+mouse drag / Super+right-drag | Move / resize window | Same, Plasma default | Same |

## 3. Workspaces and monitors

| Key | Omarchy | Steel OS | Status |
|---|---|---|---|
| Super+1 to 0 | Switch to workspace 1 to 10 | Switch to virtual desktop 1 to 10 | Same |
| Super+Shift+1 to 0 | Move window to workspace | Move window to virtual desktop | Same |
| Super+Shift+Alt+1 to 0 | Move window silently | Not bound | None |
| Super+Tab, Super+Shift+Tab | Next / previous workspace | Same | Same |
| Super+Ctrl+Tab | Former workspace | Walk through desktops | Changed |
| Super+scroll | Scroll workspaces | Not bound | None (Plasma supports it on the desktop edge; off by default) |
| Ctrl+Alt+Tab, Ctrl+Alt+Shift+Tab | Next / previous monitor | Same | Same |
| Super+Shift+Alt+arrows | Move workspace to another monitor | Not bound | None |
| Super+/ and Super+Alt+/ | Monitor scaling up / down | Not bound | None (Display settings) |
| Super+Ctrl+Delete, Super+Ctrl+Alt+Delete | Laptop display toggle / mirror | Not bound | None (Display settings; Plasma's Meta+P offers it) |

## 4. System, settings, and capture

| Key | Omarchy | Steel OS | Status |
|---|---|---|---|
| Super+Escape | System menu | Log-out screen | Changed |
| Super+Ctrl+L | Lock | Lock | Same |
| Super+Ctrl+V | Clipboard manager | Clipboard history | Same |
| Super+C, Super+V, Super+X, Super+A | Universal copy, paste, cut, select-all (works in terminals too) | Not bound | None: Plasma cannot rewrite shortcuts for every app. Ctrl+C/V work everywhere except terminals; WezTerm has Alt+C/Alt+V by Steel OS config. |
| Print | Screenshot | Spectacle | Same |
| Super+Shift+S | Screenshot | Spectacle, rectangular region | Same |
| Alt+Print | Screen recording | Spectacle, record screen | Same |
| Super+Print | Color picker | Not bound | None (KColorChooser can be added) |
| Super+Ctrl+Print | OCR text from screen | Not bound | None |
| Super+Ctrl+A/B/D/W/P | Audio, Bluetooth, Display, Network, Power panels | The matching System Settings page | Changed: a settings page instead of a bar popup |
| Super+Ctrl+1 to 9 | Bar panel by number | Not bound | None |
| Super+Ctrl+N | Night light | Night light | Same |
| Super+Ctrl+I | Toggle idle lock | Not bound | None (Power settings) |
| Super+Ctrl+Z, Super+Ctrl+Alt+Z | Screen zoom in / reset | Same | Same |
| Super+Ctrl+comma | Silence notifications | Do not disturb | Same |
| Super+comma, Super+Shift+comma, Super+Alt+comma, Super+Shift+Alt+comma | Dismiss / history of notifications | Not bound | None: Plasma has no shortcuts for these; the notification popup has the buttons |
| Super+Shift+Space | Toggle top bar | Not bound | None (panel auto-hide is a setting) |
| Super+Ctrl+Space, Super+Shift+Ctrl+Space | Background, theme menus | Not bound | None (Settings) |
| Super+Ctrl+S | Share menu (LocalSend) | Not bound | None: KDE Connect is Plasma's equivalent; could be bound later |
| Super+Ctrl+R and friends | Reminders | Not bound | None |
| Super+Ctrl+Alt+T/B/W | Show time, battery, weather | Not bound | None (on the panel) |
| Super+Ctrl+X, F9, Right Alt | Dictation | Not bound | None |
| Super+Shift+Ctrl+A | AI agent picker | Not bound | None (Forge later) |
| Volume, brightness, media, touchpad keys | Hardware keys | Plasma defaults, same behaviour | Same |
| Shift+volume keys, Alt+volume keys | Switch output, precise steps | Not bound | None |

---

## Summary for rodger-roberts-dev

- **Same or close enough:** everything a Windows user would call a shortcut
  (launcher, terminal, browser, files, close, maximize, minimize, desktops,
  Alt+Tab, lock, screenshots, clipboard history, zoom, night light) and your
  ALT+Return for WezTerm.
- **Changed:** Super+T opens Plasma's tiling instead of toggling float, since
  Steel OS windows float by default. Super+Shift+arrows snap instead of swap.
  Settings keys open a settings page instead of a bar popup.
- **No equivalent:** the tiling-specific keys (splits, groups, scratchpad,
  gaps, layouts), the universal Super+C/V copy and paste, and the Omarchy
  notification and reminder keys.

**What I need from you:** your personal bindings beyond Omarchy's defaults, if
any, and your answer on the "None" rows you actually use. Each one either gets a
Plasma replacement or stays unbound. Add them to this file or to a note in the
repo; I will fold them in.

**To verify on the first image (STEEL-16):** that Plasma reads these three
files from `/etc/xdg` as defaults on a fresh login, and that the Flatpak
desktop file names for Chrome and Obsidian match what Flathub installs.
