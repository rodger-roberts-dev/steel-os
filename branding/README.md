# Steel OS branding

Jira: STEEL-31
Steel OS is a Steel & Code (steelandcode.com) project in partnership with
Blackbox Entertainment. The marks belong to Steel & Code; Blackbox
Entertainment uses them under that partnership. Chosen by T on 2026-10-16 from
the "Steel & Code" concept (concept E).

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
| `wallpaper/` | Two chosen drafts (waves = default, room = option) plus the first-kit hexagon PNGs at 3840x2160, 2560x1440, 1920x1080 and the SVG source | Default desktop wallpaper, optional wallpaper, login background |

All SVGs are pure shapes with the lettering converted to outlines, so no font is
needed on the machine. The lettering was set in Saira Stencil One (SIL Open
Font License, free for commercial use).

## Rules

- Keep clear space around the logo of at least half the hexagon's height.
- Do not recolour, stretch, rotate or add shadows. On busy photos use a mono
  version.
- Smallest sizes: mark 16 px, horizontal logo 120 px wide.
- The first-kit `wallpaper/` PNGs predate the final colour choice and use a
  grey hexagon with the orange glow; the chosen wallpapers are the two drafts
  described under Wallpaper candidates.

## Where each file goes in the image

See STEEL-31 in Jira for the full table: Plymouth boot splash, SDDM login
screen, wallpaper, Kickoff start button, `/usr/lib/os-release` logo, fastfetch
terminal banner, installer product name.

## Wallpaper candidates

Decided 2026-10-16 by rodger-roberts-dev and T.

- **Default desktop wallpaper:** `wallpaper/steel-os-wallpaper-waves-draft.png`
  (1672x941). Dark navy with blue and orange light waves, the hex mark and
  `STEEL OS_` centred. Clean, no stray text, matches the brand colours. This is
  also the candidate for the website hero background and the login screen.
- **Optional wallpaper (shipped, user can pick it):**
  `wallpaper/steel-os-wallpaper-room-draft.png` (1631x964). Isometric gaming
  room, second version: person on the couch with a controller, space game on
  the TV, Steel OS on the monitors and a neon sign. rodger-roberts-dev liked
  this one; it stays in the image as a choice in the wallpaper settings.
- `wallpaper/steel-os-wallpaper-3840x2160.png` and smaller sizes: the hexagon
  wallpaper from the first kit, grey hex with orange glow. Kept as the fallback
  until the two above are rendered at full size.

Before either draft ships: regenerate at 3840x2160 (the drafts are about
1600 px wide and will look soft on a 4K screen), keep the logo centred so
Plasma's panel does not cover it, and check the small text on the room
monitors, which is still an AI render and not real UI.
