# Printers, scanners and network computers

Updated: 2026-10-17

How Steel OS handles printing, scanning, finding other computers and sharing
folders with Windows PCs. Steel OS is built on Bazzite (Fedora Atomic) with the
KDE Plasma desktop.

---

## 1. Short answer

| Task | How |
|---|---|
| Print to a network printer | Most appear by themselves. Otherwise: System Settings, Printers, Add |
| Print over USB | Plug it in; Steel OS sets it up by itself |
| Scan | Skanpage, USB or network scanners |
| Open a Windows PC's shared folder | Dolphin, Network, or type `smb://PCNAME` |
| Be seen by Windows PCs | Built in: Steel OS appears in Windows Explorer's Network |
| Share a folder with Windows | Right-click the folder in Dolphin, Properties, **Share** |

## 2. Printers by brand

The four common brands work without downloading a driver.

| Brand | Printing | Scanning |
|---|---|---|
| **HP** | HPLIP, HP's own Linux driver, covers nearly every HP printer | HPLIP |
| **Canon** (PIXMA, MAXIFY, imageCLASS) | Gutenprint for most PIXMA models, including the MG3600 series; driverless (AirPrint) for Wi-Fi models | SANE's PIXMA driver over USB and the network |
| **Brother** | brlaser for Brother laser printers; driverless for newer models over the network or USB | Driverless network scanning (eSCL/WSD) on most Wi-Fi models |
| **Epson** | Gutenprint for hundreds of models; driverless for most since about 2015 | SANE's Epson drivers and Epson scanner firmware; driverless on Wi-Fi models |
| **Others** | Driverless (IPP Everywhere / AirPrint) for most printers made since about 2015; Samsung and some Xerox lasers via SpliX; manufacturer PPDs from the foomatic database | Driverless network scanning |

**Driverless** means the printer itself tells the computer how to print. No
driver is needed. Most printers with Wi-Fi or a network port work this way, and
newer USB printers do too (ipp-usb).

**Not covered:** Brother scanners that only work with Brother's own `brscan`
driver over USB, and a few Canon laser printers that need Canon's CAPT driver.
These drivers aren't free software, so Steel OS can't include them; the help
page explains what to do.

## 3. What is in the Steel OS image

| Piece | What it does |
|---|---|
| CUPS with `cups-browsed` | The print system; network printers that support driverless printing are added by themselves |
| `system-config-printer-udev` | Sets up a USB printer the moment it's plugged in |
| `hplip`, `gutenprint-cups`, `printer-driver-brlaser`, `splix`, `foomatic-db-ppds` | Drivers for HP, Canon, Epson, Brother, Samsung and many more |
| `ipp-usb` | Driverless printing and scanning over USB for newer printers |
| Plasma Printers page | System Settings, Printers: add, remove, manage, see the queue |
| `skanpage`, `sane-backends-drivers-scanners`, `sane-airscan`, `iscan-firmware` | The scanning app and scanner drivers, including driverless network scanners |
| `wsdd` | Steel OS appears in Windows Explorer's Network, and finds Windows PCs |
| `samba`, `samba-usershares`, `kdenetwork-filesharing` | Share a folder with a right-click; Windows PCs open it |
| Firewall | Allows file sharing, printer discovery and Windows network discovery |

File sharing starts only once a folder has actually been shared, so nothing
listens on the file-sharing ports until then. The PC's administrators can
share folders straight away; no extra setup step is needed.

## 4. What a user does

**Add a printer**
1. USB: plug it in and switch it on. It appears in Printers by itself.
2. Network: most appear by themselves. If not, open System Settings,
   **Printers**, click **Add**, and pick it from the list.
3. Print a test page.

Printing to a PDF file works in every app with no printer.

**Scan**
Open **Skanpage** from the start menu, pick the scanner, click **Scan**.

**Open a shared folder on a Windows PC**
1. Open **Dolphin**, the file manager, and click **Network**.
2. If the PC isn't listed, type `smb://PCNAME/` or `smb://192.168.1.20/` in the
   address bar.
3. Sign in with the Windows account name and password.

**Share a folder with Windows PCs**
1. In Dolphin, right-click the folder, then **Properties**, then the **Share**
   tab.
2. Tick **Share with Microsoft Windows (SMB)**. Choose who can open it and
   whether they can change files.
3. On the Windows PC, open File Explorer, **Network**, then this PC. Sign in
   with your Steel OS user name and password.

## 5. How to check (on the test PC)

1. Plug in the Canon MG3620 over USB. Within a few seconds it is listed in
   System Settings, Printers. Print a test page.
2. Open Skanpage with the MG3620 connected. Scan one page.
3. A Brother printer on the same network appears in Printers without clicking
   Add, or after **Add**. Print a test page.
4. Dolphin, Network: the Windows PC is listed, or opens with `smb://` and its
   name.
5. Share a folder from Dolphin. On the Windows PC, File Explorer, Network shows
   the Steel OS PC and the shared folder opens.
