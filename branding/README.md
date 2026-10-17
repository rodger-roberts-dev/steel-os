# Steel OS branding

Steel OS is a Steel & Code (steelandcode.com) project in partnership with
Blackbox Entertainment. The marks belong to Steel & Code; Blackbox
Entertainment uses them under that partnership.

## The mark

A blue hexagon with an orange stencil S inside. The wordmark is STEEL in white
(or black on light backgrounds) and OS in orange, followed by a blue cursor
bar: `STEEL OS_`. The S is the hex mark on its own for icons.

## Colours

| Name | Hex | Use |
|---|---|---|
| Steel Blue | `#4A90D9` | Hexagon, cursor bar, Plasma accent colour |
| Forge Orange | `#F2641E` | The S, the OS wordmark, highlights |
| White | `#FFFFFF` | STEEL wordmark on dark backgrounds |
| Black | `#000000` | STEEL wordmark on light backgrounds, icon tile |
| Anvil | `#14171C` | Dark backgrounds, wallpaper base |

Forge Orange is for accents and large shapes, not small body text on white.

## Tagline

**Built solid. Plays everything.**

## Files

| Folder | Contents | Used for |
|---|---|---|
| `logo/` | Horizontal logo, SVG, in `color-on-dark`, `color-on-light`, `mono-white`, `mono-black`, plus `png/` at 2000 px wide | Website, login screen, installer, documents |
| `mark/` | The hexagon mark only, same four variants, SVG | Start menu button, boot splash, favicon source |
| `icon/` | Square rounded app icon, SVG in `dark`, `light`, `orange`, `mono-white`, `mono-black`, plus `png/` at 16 to 1024 px | `/usr/share/icons/hicolor/` in the image, the About screen logo, the web app icon |
| `portal/` | The Steel OS Portal app icon: four app tiles inside the hexagon, SVG | `steel-os-portal` icon in `/usr/share/icons/hicolor/`, the Portal's launcher, taskbar pin and window |
| `shield/` | The Steel Shield app icon: a Steel Blue shield with the Forge Orange S, SVG | `steel-shield` icon in `/usr/share/icons/hicolor/`, Steel Shield's window, notifications and menu entry |
| `wallpaper/` | The waves wallpaper at 3840x2160 (default) and the gaming-room wallpaper (second choice) | Default desktop wallpaper, optional wallpaper, login background |

All SVGs are pure shapes with the lettering converted to outlines, so no font is
needed on the machine. The lettering was set in Saira Stencil One (SIL Open
Font License, free for commercial use).

## Rules

- Keep clear space around the logo of at least half the hexagon's height.
- Do not recolour, stretch, rotate or add shadows. On busy photos use a mono
  version.
- Smallest sizes: mark 16 px, horizontal logo 120 px wide.

## Where each file goes in the image

| Surface | File in the image |
|---|---|
| Desktop wallpaper | Set to the waves wallpaper for every user by a Plasma layout script (`steel-os-wallpaper.js`) |
| Lock screen | `/etc/xdg/kscreenlockerrc` points at the waves wallpaper |
| Login screen | `/usr/share/sddm/themes/breeze/theme.conf.user` points at the waves wallpaper |
| Wallpaper chooser | `/usr/share/wallpapers/steel-os-waves/` and `steel-os-room/` as Plasma wallpaper packages |
| Boot splash | `/usr/share/plymouth/themes/spinner/watermark.png`, the logo at 220 px wide |
| Steel OS Portal | The `steel-os-portal` icon from `portal/`, on its launcher, taskbar pin and window |
| Start button | The Steel OS icon, set by a Plasma layout script (`steel-os-panel.js`) |
| About this System | `/etc/xdg/kcm-about-distrorc`, `/usr/lib/os-release` and the `steel-os` icon in the hicolor theme |
| Installer | `installer/system_files/overrides/usr/share/cockpit/branding/fedora/` (logo and colours) |

## Wallpapers

Steel OS ships two wallpapers, both 3840x2160.

- **Default:** `wallpaper/steel-os-wallpaper-waves-3840x2160.png`. Dark navy
  with blue and orange light waves, the hex mark and `STEEL OS_` centred. Used
  on the desktop, the lock screen and the login screen.
- **Alternative:** `wallpaper/steel-os-wallpaper-room-3840x2160.png`. An
  isometric gaming room: someone on the couch with a controller, a space game
  on the TV, Steel OS on the monitors and a neon sign. Available in Plasma's
  wallpaper settings.
