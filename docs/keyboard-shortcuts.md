# Keyboard shortcuts

Updated: 2026-10-17

Every keyboard shortcut Steel OS sets up out of the box. **Super** is the
Windows key. Any shortcut can be changed in System Settings, Shortcuts, and
**Super+K** opens that page directly.

The shortcuts are set in `system_files/etc/xdg/kglobalshortcutsrc` and applied
for every user before the desktop starts. Konsole's copy and paste keys are set
in `system_files/etc/skel/.local/share/kxmlgui6/konsole/sessionui.rc`.

---

## Apps

| Keys | Opens |
|---|---|
| Super+Enter or Alt+Enter | Terminal (Konsole). Ctrl+Alt+T also works |
| Super+Shift+Enter or Super+Shift+B | Web browser (Firefox) |
| Super+F or Super+Shift+F | File manager (Dolphin) |
| Super+Shift+N | Text editor (Kate) |
| Super+Shift+O | Obsidian |
| Super+Space, Alt+Space or Alt+F2 | Search and app launcher (KRunner) |
| Super+Ctrl+Q or the Calculator key | Calculator |
| Super+Ctrl+T | System Monitor |
| Super+Ctrl+E | Emoji picker |
| Super+K | Shortcuts settings (this list, editable) |

An app's shortcut does nothing until that app is installed.

## Windows

| Keys | Does |
|---|---|
| Super+W, Super+Q or Alt+F4 | Close the window |
| Super+F11 | Full screen |
| Super+T | Show or auto-hide the taskbar |
| Super+Shift+D | Virtual desktops off (one desktop, no boxes on the taskbar) or on (four) |
| Super+Alt+F | Maximise |
| Super+M | Minimise |
| Super+O | Keep the window above others |
| Super+Left, Right, Up or Down | Move focus to the window in that direction |
| Alt+Tab, Alt+Shift+Tab | Switch between windows |
| Super+Alt+Space | Overview of all windows and desktops |

Windows open floating and cascading, like Windows. Quick-tiling shortcuts are
switched off.

## Desktops

Steel OS starts with four virtual desktops in one row.

| Keys | Does |
|---|---|
| Super+1 to Super+4 | Go to desktop 1 to 4 |
| Super+Shift+1 to Super+Shift+4 | Move the current window to desktop 1 to 4 |
| Super+Tab, Super+Shift+Tab | Next or previous desktop |
| Ctrl+Alt+Tab | Move focus to the next screen (multi-monitor) |

Super+5 to Super+0 work too if more desktops are added in System Settings.

## Terminal (Konsole)

| Keys | Does |
|---|---|
| Alt+C or Ctrl+Shift+C | Copy |
| Alt+V or Ctrl+Shift+V | Paste |

The menu bar is hidden so that Alt+V pastes instead of opening a menu.

## Screen and system

| Keys | Does |
|---|---|
| Print | Screenshot tool |
| Super+Shift+S | Screenshot of a selected area |
| Alt+Print | Record the screen |
| Super+Ctrl+V | Clipboard history |
| Super+Ctrl+Z, Super+Ctrl+Shift+Z | Zoom the screen in, out |
| Super+Ctrl+Alt+Z | Zoom back to normal |
| Super+Ctrl+N | Night light on or off |
| Super+Ctrl+Comma | Do not disturb on or off |
| Super+L or Super+Ctrl+L | Lock the screen |
| Super+Esc or Ctrl+Alt+Del | Log out, restart or shut down |

## Settings pages

| Keys | Opens |
|---|---|
| Super+Ctrl+A | Sound |
| Super+Ctrl+B | Bluetooth |
| Super+Ctrl+D | Displays |
| Super+Ctrl+W | Wi-Fi and network |
| Super+Ctrl+P | Power |

---

## Where they came from

The set started from the keyboard-first layout of Omarchy, the system Steel OS
was first built on, and was translated to KDE Plasma when Steel OS moved to
Bazzite. Tiling-window shortcuts were left out because Steel OS uses floating
windows.
