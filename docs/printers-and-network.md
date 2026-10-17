# Printers, scanners and network computers

Updated: 2026-10-17

How Steel OS handles printing, scanning, finding other computers and sharing
folders, what is already in the image, and what is still to build. Steel OS is
built on Bazzite (Fedora Atomic) with the KDE Plasma desktop.

Lines marked **(to confirm)** come from Bazzite's Fedora KDE base and have not
yet been checked on an installed Steel OS machine. Section 5 has the one
command that checks them.

---

## 1. Short answer

| Task | Today | Goal |
|---|---|---|
| Print to a modern network printer | Works: System Settings, Printers, Add | Printer appears without clicking Add |
| Print to an older printer (HP, Canon, Epson) | Drivers included in the image | Same |
| Print over USB | Works for most printers; to be tested with the Canon PIXMA MG3620 | Plug in and print, no driver download |
| Scan | Skanpage scanning app **(to confirm)** | Scan from the MG3620 over USB |
| Open a Windows PC's shared folder | Works in Dolphin by typing `smb://PCNAME` | Windows PCs listed on their own |
| Steel OS appears in Windows Explorer | `wsdd` included in the image | Same, once sharing is on |
| Share a folder to Windows | Not yet | Right-click a folder, Share, done |
| Send a file to a phone or laptop | KDE Connect **(to confirm)**; LocalSend as a Steel App later | Same |

---

## 2. What is in the Steel OS image

**Added by Steel OS** (`packages/image.txt`):

| Package | What it does |
|---|---|
| `hplip` | Drivers for HP printers and scanners that need them |
| `gutenprint-cups` | Drivers for older Canon, Epson and other printers that are not driverless |
| `wsdd` | Makes Steel OS visible in Windows Explorer's Network, and helps find Windows PCs |

**From Bazzite's Fedora KDE base** (to confirm on an installed machine):

| Piece | What it does |
|---|---|
| CUPS | The print system |
| Plasma Printers page (`print-manager`) | System Settings, Printers: add, remove and manage printers, see the print queue |
| Avahi and mDNS | Finds printers and computers on the local network by name |
| Skanpage and SANE | Scanning app and scanner drivers. SANE's `pixma` driver covers most Canon PIXMA scanners |
| Dolphin network support | Opens Windows (SMB) shares from the file manager |
| firewalld | The firewall. Fedora's desktop zone lets local discovery and Windows file-sharing clients through |
| KDE Connect | Send files and notifications between Steel OS and a phone |

---

## 3. What a user does today

**Add a printer**
1. Open System Settings, then **Printers**.
2. Click **Add**. Most network printers and USB printers appear in the list.
3. Pick it. Modern printers use the driverless profile automatically. Older
   ones use a driver from `hplip` or Gutenprint.
4. Print a test page.

Printing to a PDF file works in every app with no printer.

**Scan**
Open **Skanpage** from the start menu, pick the scanner, then click Scan.
**(to confirm)**

**Open a Windows PC's shared folder**
1. Open **Dolphin** (the file manager), then click **Network** in the sidebar.
2. Linux machines, Macs and NAS boxes usually appear on their own. Windows 10
   and 11 PCs often don't, which is true on every Linux system.
3. Type `smb://PCNAME/` or `smb://192.168.1.20/` in the address bar. Sign in
   with the Windows account name and password.

---

## 4. What is still to build

| Gap | Plan |
|---|---|
| Printers appear only after clicking Add | Decide whether to turn on automatic printer discovery for driverless printers. Test it first. |
| Canon PIXMA MG3620 over USB | Make it print and scan over USB with no driver download. Test on the Command test PC. Add `ipp-usb` (driverless printing over USB) if the printer supports it; otherwise use the Gutenprint driver. |
| Windows PCs not listed in Dolphin | Check whether `wsdd` fixes it. If not, the help page says "type the PC's name". |
| No way to share a folder to Windows | A "Share this folder" option on right-click in Dolphin: Samba, with safe defaults and a firewall rule limited to the local network. No terminal. |
| Printers and Scanners are two separate apps | A "Printers and Scanners" entry in the Steel OS Portal that opens both |
| Quick file sending | LocalSend as a one-click Steel App, alongside KDE Connect |

---

## 5. How to check (in a VM or on the test PC)

**Confirm what Bazzite includes.** Run this in the terminal and paste the
output into the team chat:

```
rpm -q cups cups-browsed print-manager skanpage sane-backends ipp-usb samba samba-client kdenetwork-filesharing kio-extras avahi nss-mdns firewalld kdeconnectd; firewall-cmd --get-default-zone
```

Each line says either a version number (installed) or "is not installed".

**Printer** (a real printer is needed, so use the test PC)
1. System Settings, Printers. Is anything listed before clicking Add?
2. Click Add and wait 10 seconds. Does the network printer appear? Does the
   MG3620 appear when plugged in over USB?
3. Add it and print a test page. Did it ask for a password?
4. Print any document to PDF. Does the file appear?

**Scanner**
5. Open Skanpage with the MG3620 plugged in. Is the scanner listed? Scan one page.

**Network**
6. Dolphin, Network. Which machines appear? Is the Windows PC there?
7. Type `smb://` and the Windows PC's name. Do the shares open after signing in?
8. On the Windows PC, open Explorer, Network. Does the Steel OS machine appear?

The answers decide the work in section 4.
