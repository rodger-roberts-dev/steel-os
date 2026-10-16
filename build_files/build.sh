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

### 6. Default apps at first boot (STEEL-17)
# The Flatpak list ships inside the image; a small service installs it from
# Flathub after the first boot with a network. See
# system_files/usr/libexec/steel-os-flatpak-install.
install -D -m 0644 /ctx/packages/flatpaks-default.txt /usr/share/steel-os/flatpaks-default.txt
chmod 0755 /usr/libexec/steel-os-flatpak-install
systemctl enable steel-os-flatpak-install.service
