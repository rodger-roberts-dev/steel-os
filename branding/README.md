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
| `wallpaper/` | PNG at 3840x2160, 2560x1440, 1920x1080 and the SVG source | Default desktop wallpaper and login background |

All SVGs are pure shapes with the lettering converted to outlines, so no font is
needed on the machine. The lettering was set in Saira Stencil One (SIL Open
Font License, free for commercial use).

## Rules

- Keep clear space around the logo of at least half the hexagon's height.
- Do not recolour, stretch, rotate or add shadows. On busy photos use a mono
  version.
- Smallest sizes: mark 16 px, horizontal logo 120 px wide.
- The `wallpaper/` files predate the final colour choice and use a grey
  hexagon with the orange glow; they are the starting wallpaper until a
  blue-and-orange version is made.

## Where each file goes in the image

See STEEL-31 in Jira for the full table: Plymouth boot splash, SDDM login
screen, wallpaper, Kickoff start button, `/usr/lib/os-release` logo, fastfetch
terminal banner, installer product name.
