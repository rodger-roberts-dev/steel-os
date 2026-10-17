#!/bin/bash
# Steel OS image build script (STEEL-16).
#
# Runs once, inside the container build, on top of Bazzite. Everything Steel
# OS changes about Bazzite happens here or in system_files/. Never patch
# Bazzite's own files; add ours next to them.
#
# The Universal Blue template uses `set -ouex pipefail` here; we keep it so
# the build stops on the first error and prints every command it runs.

set -ouex pipefail

### 1. Settings files
# Everything under system_files/ is copied to / in the image. Today that is
# the Plasma defaults (STEEL-29): keyboard shortcuts, cascading windows,
# Konsole as the terminal. Later stories add the wallpaper, the update
# schedule and the Steel Apps list the same way.
cp -avf /ctx/system_files/. /

### 2. Extra rpm packages
# packages/image.txt lists Fedora package names, one per line. Lines that
# start with # and blank lines are ignored. Only system pieces belong there;
# apps are Flatpaks and are installed at first boot (STEEL-17).
mapfile -t IMAGE_PACKAGES < <(grep -Ev '^\s*(#|$)' /ctx/packages/image.txt)
if [[ ${#IMAGE_PACKAGES[@]} -gt 0 ]]; then
    dnf5 install -y "${IMAGE_PACKAGES[@]}"
fi

### 3. Image signing key
# The public half of the Steel OS signing key goes into the image so an
# installed machine can check that updates really come from us. The matching
# registries.d file in system_files/ tells the container tools where our
# signatures live. Enforcing the check in /etc/containers/policy.json is a
# follow-up story; today the key is only made available.
install -D -m 0644 /ctx/cosign.pub /etc/pki/containers/steel-os.pub

### 4. Services
# Nothing enabled yet. wsdd (Windows network discovery) is installed above
# but is switched on by STEEL-39 together with the firewall rule it needs.

### 5. Branding (STEEL-31)
# Wallpapers as Plasma wallpaper packages, so both appear in the wallpaper
# chooser with a name. metadata.json for each lives in system_files/.
install -D -m 0644 /ctx/branding/wallpaper/steel-os-wallpaper-waves-3840x2160.png \
    /usr/share/wallpapers/steel-os-waves/contents/images/3840x2160.png
install -D -m 0644 /ctx/branding/wallpaper/steel-os-wallpaper-room-3840x2160.png \
    /usr/share/wallpapers/steel-os-room/contents/images/3840x2160.png

# Default desktop wallpaper, the way Bazzite does it: Fedora's Plasma reads
# /usr/share/backgrounds/default.jxl and default-dark.jxl, and Bazzite points
# those at its own image. We point them at the waves wallpaper. The file is a
# PNG behind a .jxl name; the image loader checks the content, not the name.
# If the VM test shows a blank desktop, convert the wallpapers to JXL.
ln -sf /usr/share/wallpapers/steel-os-waves/contents/images/3840x2160.png /usr/share/backgrounds/default.jxl
ln -sf /usr/share/wallpapers/steel-os-waves/contents/images/3840x2160.png /usr/share/backgrounds/default-dark.jxl
rm -f /usr/share/backgrounds/default.xml

# Logo for System Settings > About (see system_files/etc/xdg/kcm-about-distrorc)
install -D -m 0644 /ctx/branding/icon/png/steel-os-icon-dark-256.png /usr/share/pixmaps/steel-os.png

### 5b. No Bazzite name on the desktop (STEEL-31, STEEL-40)
# Bazzite Portal opens at every first login and says "Bazzite" throughout.
# Steel OS replaces it with the Steel Apps screen (STEEL-40); until then it
# does not start by itself, is hidden from the start menu and is taken off
# the taskbar. Bazzite's announcement pop-up is switched off too.
rm -f /etc/skel/.config/autostart/bazzite-portal.desktop
rm -f /etc/xdg/autostart/bazzite-announcement.desktop
for f in /usr/share/applications/*yafti*.desktop; do
    [[ -f "$f" ]] || continue
    grep -q '^NoDisplay=' "$f" && sed -i 's/^NoDisplay=.*/NoDisplay=true/' "$f" \
        || sed -i '/^\[Desktop Entry\]/a NoDisplay=true' "$f"
done
for f in /usr/share/plasma/shells/org.kde.plasma.desktop/contents/updates/bazzite-pins.js \
         /usr/share/plasma/layout-templates/org.kde.plasma.desktop.defaultPanel/contents/layout.js; do
    [[ -f "$f" ]] && sed -i '/yafti_gtk\.desktop/d' "$f"
done

# New users get Plasma's default layout and Plasma marks every update script
# as already done for them, so the wallpaper script also has to run inside
# the default layout (the same way Bazzite adds its taskbar pins).
LAYOUT=/usr/share/plasma/layout-templates/org.kde.plasma.desktop.defaultPanel/contents/layout.js
sed -i '$r /usr/share/plasma/shells/org.kde.plasma.desktop/contents/updates/steel-os-wallpaper.js' "$LAYOUT"

### 6. Default apps at first boot (STEEL-17)
# The Flatpak list ships inside the image; a small service installs it from
# Flathub after the first boot with a network. See
# system_files/usr/libexec/steel-os-flatpak-install.
install -D -m 0644 /ctx/packages/flatpaks-default.txt /usr/share/steel-os/flatpaks-default.txt
chmod 0755 /usr/libexec/steel-os-flatpak-install
systemctl enable steel-os-flatpak-install.service

### 7. The OS calls itself Steel OS (STEEL-48)
# Bazzite rewrites Fedora's /usr/lib/os-release in its build (see Bazzite's
# build_files/image-info). We do the same on top, changing only the fields
# that name the OS. ID stays "bazzite" and image-info.json stays untouched,
# because Bazzite's own tools read those; checked 2026-10-16, nothing in
# Bazzite reads VARIANT_ID or NAME at run time.
# Fedora's anonymous Count Me statistic reports NAME and VARIANT_ID, which is
# how Steel OS machines are counted (STEEL-33).
OS_RELEASE="/usr/lib/os-release"
sed -i 's/^NAME=.*/NAME="Steel OS"/' "$OS_RELEASE"
sed -i 's/^PRETTY_NAME=.*/PRETTY_NAME="Steel OS"/' "$OS_RELEASE"
sed -i 's/^VARIANT_ID=.*/VARIANT_ID=steel-os/' "$OS_RELEASE"
sed -i 's|^HOME_URL=.*|HOME_URL="https://steel-os.org"|' "$OS_RELEASE"
sed -i 's|^DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://steel-os.org"|' "$OS_RELEASE"
sed -i 's|^SUPPORT_URL=.*|SUPPORT_URL="https://steel-os.org"|' "$OS_RELEASE"
sed -i 's|^BUG_REPORT_URL=.*|BUG_REPORT_URL="https://steel-os.org"|' "$OS_RELEASE"
sed -i 's/^LOGO=.*/LOGO=steel-os/' "$OS_RELEASE"
sed -i 's/^DEFAULT_HOSTNAME=.*/DEFAULT_HOSTNAME="steel-os"/' "$OS_RELEASE"
# Orange, the brand colour, for the terminal banner that reads ANSI_COLOR
sed -i 's/^ANSI_COLOR=.*/ANSI_COLOR="0;38;2;242;100;30"/' "$OS_RELEASE"
# The boot menu entry name
sed -i 's/^BOOTLOADER_NAME=.*/BOOTLOADER_NAME="Steel OS"/' "$OS_RELEASE"
# Bazzite writes this for GRUB; keep the pattern, change the name
echo "Steel OS release $(rpm -E %fedora) (Kinoite)" > /etc/system-release
grep -E '^(NAME|PRETTY_NAME|ID|VARIANT_ID|LOGO|HOME_URL)=' "$OS_RELEASE"

# The icon that LOGO=steel-os points at, in every standard size
for size in 16 32 48 64 128 256 512; do
    install -D -m 0644 "/ctx/branding/icon/png/steel-os-icon-dark-${size}.png" \
        "/usr/share/icons/hicolor/${size}x${size}/apps/steel-os.png"
done
install -D -m 0644 /ctx/branding/icon/steel-os-icon-dark.svg /usr/share/icons/hicolor/scalable/apps/steel-os.svg

### 8. Keep the package repos usable for the ISO builder (STEEL-50)
# bootc-image-builder copies the enabled dnf repos out of the image and runs
# dnf in its own container to assemble the installer. A repo whose signing
# key is a local file (gpgkey=file://...) only works there if that file also
# exists in the builder's container. Fedora's own keys do; Bazzite's extra
# repos (terra, rpmfusion and friends) point at keys that do not, and the ISO
# build stops with "Failed to retrieve GPG key". Repos are not used on an
# installed machine (updates arrive as whole images), so every repo that is
# not Fedora's own and keys from a local file is switched off in the image.
for repo in /etc/yum.repos.d/*.repo; do
    [[ -f "$repo" ]] || continue
    if grep -qE '^gpgkey=file://' "$repo" && ! grep -qE '^gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora' "$repo"; then
        echo "Disabling $repo: its signing key is a local file the ISO builder cannot read"
        sed -i -e 's/^enabled=1/enabled=0/' -e 's/^enabled=true/enabled=false/' "$repo"
    fi
done
grep -l '^enabled=1' /etc/yum.repos.d/*.repo || true

### 10. Desktop polish (STEEL-7, STEEL-20, STEEL-37, STEEL-48)
# Start button icon and plain-English start menu, for new and existing users.
LAYOUT=/usr/share/plasma/layout-templates/org.kde.plasma.desktop.defaultPanel/contents/layout.js
sed -i '$r /usr/share/plasma/shells/org.kde.plasma.desktop/contents/updates/steel-os-panel.js' "$LAYOUT"

# No "Bazzite" in any start-menu name. Desktop files keep their file names
# (other tools refer to them); only the text people read changes.
for f in /usr/share/applications/*.desktop; do
    [[ -f "$f" ]] || continue
    if grep -qE '^(Name|GenericName|Comment)(\[[^]]*\])?=.*Bazzite' "$f"; then
        sed -i -E '/^(Name|GenericName|Comment)(\[[^]]*\])?=/ s/Bazzites?/Steel OS/g' "$f"
    fi
done

# The app store is Bazzite's "Bazaar". Call it what it is.
BAZAAR=/usr/share/applications/io.github.kolunmi.Bazaar.desktop
if [[ -f "$BAZAAR" ]]; then
    sed -i -E 's/^Name=.*/Name=App Store/; s/^GenericName=.*/GenericName=App Store/' "$BAZAAR"
    grep -q '^Keywords=' "$BAZAAR" && sed -i 's/^Keywords=/Keywords=Bazaar;store;apps;install;/' "$BAZAAR" \
        || echo 'Keywords=Bazaar;store;apps;install;' >> "$BAZAAR"
fi

# Things Steel OS does not ship (STEEL-20): rpm packages listed in
# packages/remove.txt are removed, and launchers listed in
# packages/hide.txt stay installed but out of the start menu.
mapfile -t REMOVE_PACKAGES < <(grep -Ev '^\s*(#|$)' /ctx/packages/remove.txt || true)
if [[ ${#REMOVE_PACKAGES[@]} -gt 0 ]]; then
    dnf5 remove -y "${REMOVE_PACKAGES[@]}"
fi
while IFS= read -r launcher; do
    f="/usr/share/applications/${launcher}"
    [[ -f "$f" ]] || { echo "hide.txt: $launcher not found, skipping"; continue; }
    grep -q '^NoDisplay=' "$f" && sed -i 's/^NoDisplay=.*/NoDisplay=true/' "$f" \
        || sed -i '/^\[Desktop Entry\]/a NoDisplay=true' "$f"
done < <(grep -Ev '^\s*(#|$)' /ctx/packages/hide.txt || true)

### 11. Keyboard shortcuts actually applied (STEEL-29)
# Plasma 6 does not read shortcut defaults from /etc/xdg/kglobalshortcutsrc
# (found in T's VM test, 2026-10-17: Super+Enter did nothing). The same file
# is now (a) copied into /etc/skel so every new user starts with it, and
# (b) applied once to existing users at login by steel-os-shortcuts.
# Plasma 6 stores app-launch shortcuts as the plain key list, so the
# "[services]" entries are rewritten from the old "active,default,name" form.
SHORTCUTS=/usr/share/steel-os/kglobalshortcutsrc
install -D -m 0644 /etc/xdg/kglobalshortcutsrc "$SHORTCUTS"
awk '
    /^\[services\]/ { svc = 1; print; next }
    /^\[/           { svc = 0; print; next }
    svc && /^[^#=]+=/ {
        key = substr($0, 1, index($0, "=") - 1)
        val = substr($0, index($0, "=") + 1)
        n = split(val, parts, ",")
        print key "=" parts[1]
        next
    }
    { print }
' "$SHORTCUTS" > "$SHORTCUTS.new" && mv "$SHORTCUTS.new" "$SHORTCUTS"
install -D -m 0644 "$SHORTCUTS" /etc/skel/.config/kglobalshortcutsrc
chmod 0755 /usr/libexec/steel-os-shortcuts
grep -A1 'org.kde.konsole.desktop' "$SHORTCUTS"

### 9. Rebuild the boot image so the boot splash shows Steel OS (STEEL-31)
# The logo shown while the machine starts is read from the initramfs, a small
# boot image Bazzite generated before our files were added. Our watermark in
# /usr/share/plymouth/themes/spinner/ only appears once the initramfs is
# rebuilt. Same command Bazzite uses (its build_files/build-initramfs).
# Keep this the LAST section: anything copied in after it would not reach
# the boot screen.
QUALIFIED_KERNEL="$(rpm -q --queryformat='%{evr}.%{arch}' kernel-core | tail -n 1)"
export DRACUT_NO_XATTR=1
/usr/bin/dracut --no-hostonly --kver "$QUALIFIED_KERNEL" --reproducible --zstd -v \
    --add ostree --add fido2 -f "/usr/lib/modules/$QUALIFIED_KERNEL/initramfs.img"
chmod 0600 "/usr/lib/modules/$QUALIFIED_KERNEL/initramfs.img"
