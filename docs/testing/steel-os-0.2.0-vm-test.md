# Steel OS 0.2.0 Preview — VM Installation Test

**Date:** October 16, 2026  
**Host:** MSI Katana GF66 12UGSK, Bazzite 44 (NVIDIA Open)  
**Guest:** Steel OS 0.2.0 Preview  
**Outcome:** PASS — installed graphical desktop boot in virt-manager; broader acceptance tests pending.

## Summary

Steel OS 0.2.0 Preview was installed and booted to its branded KDE Plasma login and desktop in QEMU/KVM using virt-manager on Katana. Screenshots confirmed the custom Steel OS boot splash, login background, wallpaper, taskbar, and launcher icon.

An earlier GNOME Boxes test reached the installer but subsequent VM startups were unreliable. Host journal diagnostics revealed an NVIDIA UVM memory-allocation warning, which is **not proven to be the cause**.

## Test environment

| Item | Value |
| --- | --- |
| Hardware | MSI Katana GF66 12UGSK |
| Host OS | Bazzite 44 NVIDIA Open, image `44.20261012.1` |
| Host kernel | `7.2.9-ogc3.1.fc44.x86_64` |
| Host RAM | ~31 GiB |
| Host logical CPU threads | 20 |
| Host graphics | Intel iGPU, NVIDIA dGPU |
| Hypervisor | QEMU/KVM via libvirt |
| VM name | `Steel-OS-0.2.0` (one later console title showed `fedora43`) |
| Installation ISO | `steel-os-0.2.0-preview-x86_64.iso` (~5.77 GiB) |
| OS profile | Fedora Linux 43 (Fedora 44 absent from picker; only affects virtual hardware presets) |
| Machine / firmware | Q35, UEFI OVMF `OVMF_CODE_4M.qcow2`, non-Secure Boot |
| VM CPUs / RAM | 4 vCPUs, host passthrough / 8192 MiB |
| VM disk | 64 GiB QCOW2, VirtIO |
| Display | SPICE with VirtIO video |
| Networking | libvirt default NAT |
| Boot | SATA installation CD-ROM and VirtIO disk |

## Attempt 1 — GNOME Boxes

GNOME Boxes 50.0 Flatpak successfully opened the Steel OS 44 Anaconda installer. Remaining Fedora branding and technical warnings were visible. The installation was run using a virtual disk.

During initial boot, the display appeared stuck at:

```text
Starting initrd-switch-root.service - Switch Root...
```

The Katana host later became unresponsive. Additional Boxes attempts showed a gray loading screen or disconnected during boot:

```text
Boxes-Message: machine.vala:201: display steel-os-0 disconnected
```

After one occurrence, no `qemu-system` process was detected. The GNOME Boxes QCOW2 disk was preserved: ~30.5 GiB virtual capacity and ~8.3 GB allocated at inspection. Boxes originally used 18 vCPUs / 8 GiB RAM; for diagnosis, allocations were reduced to 2 vCPUs / 4 GiB with 3D acceleration off.

### Host diagnostic observation

Previous-boot kernel logs at 20:25:28 showed:

```text
gst-plugin-scan: vmemmap alloc failure: order:9
```

The trace referenced NVIDIA UVM functions such as `devmem_alloc_pagemap` and `uvm_devmem_init`. This is a host-side memory allocation warning, not definitive evidence of the VM failure's root cause.

## Attempt 2 — virt-manager / libvirt

Executed Bazzite's setup:

```bash
ujust setup-virtualization
```

This installed the virt-manager Flatpak and QEMU Flatpak extension, enabled `bazzite-libvirtd-setup.service`, and added the user to the `libvirt` group. Initially, virt-manager displayed **QEMU/KVM — Not Connected**.

Inspection confirmed that host libvirt services were missing, and Bazzite's setup service skipped its run due to an unmet `ConditionPathExists` for `libvirtd.service`.

Installed host packages and rebooted:

```bash
sudo rpm-ostree install qemu-kvm libvirt
```

After restart, `rpm-ostree status` showed `LayeredPackages: libvirt qemu-kvm`, and `libvirtd.service` was enabled and **active (running)**. The default virtual NAT network and DHCP (`dnsmasq`) were running. virt-manager could connect to QEMU/KVM.

### ISO access issue

The first virt-manager launch failed because system QEMU could not read the ISO under Downloads:

```text
Could not open '/var/home/<user>/Downloads/artifact/steel-os-0.2.0-preview-x86_64.iso': Permission denied
```

Copied ISO into system libvirt image storage and set permissions/SELinux label:

```bash
sudo cp ~/Downloads/artifact/steel-os-0.2.0-preview-x86_64.iso /var/lib/libvirt/images/
sudo chmod 644 /var/lib/libvirt/images/steel-os-0.2.0-preview-x86_64.iso
sudo restorecon -v /var/lib/libvirt/images/steel-os-0.2.0-preview-x86_64.iso
```

Refreshed the virt-manager `default` storage pool, selected the ISO, and configured UEFI, 4 vCPUs, 8 GiB RAM, 64 GiB disk, and CD-ROM boot.

## Successful installation evidence

Screenshots showed:

1. Steel OS logo during graphical boot.
2. Steel OS-themed graphical login screen, displaying the test user.
3. KDE Plasma desktop with Steel OS blue/orange wallpaper.
4. Branded Steel OS application launcher icon and visible panel.

This verifies a successful *installed graphical desktop boot*, rather than complete OS or release certification.

## Acceptance checklist

| Test | Status |
| --- | --- |
| ISO boot / installer launch | PASS |
| Virtual disk installation and login | PASS |
| UEFI installed graphical boot | PASS |
| Steel OS splash and login wallpaper | PASS |
| KDE Plasma desktop / launcher branding | PASS |
| `cat /etc/os-release` | PENDING |
| `sudo bootc status` | PENDING |
| Konsole and Firefox launch | PENDING |
| Keyboard shortcuts | PENDING |
| Repeated cold boot without ISO | PENDING |
| Clean shutdown / reboot | PENDING |
| Updates, signature enforcement and rollback | PENDING |
| App installs, printers, games, hardware | PENDING |

## Product feedback

- **STEEL-35, installer:** Replace remaining Fedora Anaconda branding with a consistent guided Steel OS flow. Investigate Kickstart warnings rather than just masking them.
- **STEEL-31, branding:** Continue validating boot splash, login, desktop, and app launcher after updates.
- **Virtualization:** Consider virt-manager as an optional Steel Apps developer tool; validate host libvirt/QEMU services, permissions, and connection as part of setup.
- **ISO import:** Document libvirt storage location and SELinux context so imported media is readable.
- **STEEL-50, release test:** Verify identity, `bootc status`, basic apps and shortcuts, repeat reboot, ISO removal, updates and rollback; investigate GNOME Boxes separately.

## Conclusion

**Milestone:** Steel OS 0.2.0 Preview reached its branded KDE Plasma desktop in QEMU/KVM using virt-manager on Katana on October 16, 2026. This is an initial VM smoke-test pass with additional release acceptance checks outstanding.
