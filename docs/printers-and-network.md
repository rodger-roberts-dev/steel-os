# Printers and Network Devices: Evaluation

Jira: STEEL-3
Date: 2026-10-15
Owner: rodger-roberts-dev (code reading by Claude Code; the hands-on VM test is still open)

**How this was researched.** By reading Omarchy's source at commit `51bfd1d`
(version 4.0.0.alpha), its package lists, its firewall setup, its user manual,
and its migration history, and by checking which extra packages exist in the
Arch repositories. **Nothing has been tried on a real machine yet.** The
acceptance criteria for this ticket require that, so section 6 is the test plan
for T on the test machine or for rodger-roberts-dev.

---

## 1. Short answer

**Printers: mostly works, with one click more than Windows.** Omarchy ships the
full printing stack and a graphical "Print Settings" app. A USB printer or a
modern network printer is found when the user presses Add. What is missing is
printers appearing on their own, scanning, and drivers for old printers.

**Finding other computers: works if you type the name, unreliable if you wait
for them to appear.** Files (the file manager) can open Windows and Linux
shares, but Windows PCs usually do not show up in the list on their own. That
is a Linux-wide limitation, not an Omarchy one, and it has a known fix.

**Sharing a folder from Steel OS to a Windows PC: not possible today.** The
server side is not installed and the firewall blocks it. This needs a Steel OS
wizard.

---

## 2. What Omarchy installs and turns on

From `install/omarchy-base.packages` and `install/config/enable-services.sh`.

| Piece | Installed? | Running at boot? | What it does |
|---|---|---|---|
| `cups`, `cups-filters` | Yes | Yes | The print system. |
| `cups-pk-helper` | Yes | n/a | Lets a normal user add printers without typing a root password. |
| `system-config-printer` | Yes | n/a | The "Print Settings" app in the launcher. |
| `avahi`, `nss-mdns` | Yes | Yes | Finds printers and computers on the local network by name. |
| `cups-browsed` | Config shipped | **No** | Would make network printers appear on their own. Deliberately off (see below). |
| `networkmanager` | Yes | Yes | Wi-Fi and wired networking, with a panel in the top bar. |
| `nautilus` (Files) | Yes | n/a | File manager, including "Other Locations" for network shares. |
| `gvfs-smb`, `gvfs-nfs`, `gvfs-mtp` | Yes | n/a | Lets Files open Windows shares, Linux NFS shares, and phones. |
| `localsend` | Yes | n/a | AirDrop-style file sending between devices. Firewall port is open for it. |
| `ufw`, `ufw-docker` | Yes | Yes | Firewall. **Blocks all incoming connections** except LocalSend. |
| `samba` (server) | **No** | | Needed to share a folder to Windows. |
| `wsdd` | **No** | | Makes a Linux machine visible in Windows Explorer, and helps find Windows PCs. |
| `simple-scan` | **No** | | Scanning. |
| `hplip`, `gutenprint` | **No** | | Drivers for older HP and other non-driverless printers. |

---

## 3. Printers: what a user actually sees

From Omarchy's own FAQ ("How do I add a printer?") and the code.

1. Press Super + Space, type "Print", open **Print Settings**.
2. Click **Add**. Give it a moment. A printer plugged in over USB, and most
   network printers, appear in the list.
3. If the printer is not listed, choose Network Printer, then Internet Printing
   Protocol, and type the printer's address (shown on the printer's own screen,
   for example `192.168.1.50`).
4. Click Forward. A modern printer uses the driverless "IPP Everywhere" profile.
   An older one needs its own driver, which may not be installed.
5. Right-click the printer to Set as Default and to set paper size and duplex.

Printing to a PDF file works in every app without any printer.

**Why printers do not appear by themselves.** The component that does that,
`cups-browsed`, used to run. An Omarchy migration dated September 2026
(`migrations/1787815267.sh`) stopped it as part of a security hardening of
printer discovery, and the FAQ says discovery is "temporarily switched off while
it's reworked". Omarchy ships a config for it that would only auto-add modern
driverless printers, so when upstream turns it back on, the behaviour will be
close to Windows.

**Firewall note.** The firewall blocks incoming traffic, but the firewall
package's own built-in rules allow the local-discovery protocol (mDNS) through,
so printer and computer discovery should still work. This is the single most
important thing to confirm in the VM test.

### Gaps compared with Windows

| Gap | Severity | Fix |
|---|---|---|
| Printers do not appear until the user clicks Add | Medium | Wait for upstream to re-enable `cups-browsed`, or enable it ourselves with Omarchy's shipped config. Needs a decision after the VM test. |
| No scanning at all | Medium | Add `simple-scan` (Arch extra). One package. |
| Old printers lacking driverless support need drivers that are not installed | Low to medium | Add `hplip` for HP and `gutenprint` for others (both Arch extra), or install on demand when Add fails. |
| "Print Settings" is a generic Linux app, not a Steel OS screen | Low | Acceptable for v1. A Steel OS settings app is a later epic. |
| Print Settings may ask for a password for some actions | Unknown | Check in VM; `cups-pk-helper` is meant to avoid it. |

---

## 4. Network computers and shares: what a user actually sees

1. Open **Files** (Super + Shift + F), click **Other Locations** in the sidebar.
2. Under Networks, any machine that announces itself over mDNS (most Linux
   machines, NAS boxes, Macs) appears. **Windows 10 and 11 PCs usually do not
   appear**, because Windows no longer uses the old announcement method that
   Linux file managers listen for. This is true on every Linux distribution.
3. At the bottom there is a "Connect to Server" box. Typing
   `smb://PCNAME/` or `smb://192.168.1.20/` opens a Windows PC's shares. It
   asks for the Windows username and password. This works because `gvfs-smb`
   is installed.

### Sharing from Steel OS to other machines

Not possible today. Omarchy has no `samba` server and the firewall closes the
ports. A Windows user expects "right-click folder, Share". Doing that needs:

- `samba` (Arch extra) installed and configured with a safe default
- `wsdd` (Arch extra) so the Steel OS machine shows up in Windows Explorer
- firewall rules for ports 445 and 139 (file sharing) and 3702 and 5357
  (discovery), limited to the local network
- a small Steel OS wizard: pick a folder, pick a password, done

LocalSend already covers the "send this file to that laptop" case well, and it
is on by default. It is worth telling users about it before building sharing.

### Gaps compared with Windows

| Gap | Severity | Fix |
|---|---|---|
| Windows PCs do not appear automatically in Files | Medium | Add `wsdd` and test whether its discovery mode helps Files; otherwise document "type the name". |
| Cannot share a folder from Steel OS | High for goal 2 | Build the sharing wizard above. Its own ticket. |
| Connecting asks for the Windows account password every time | Low | Files can remember it in the keyring; confirm in VM. |
| Phones over USB | Fine | `gvfs-mtp` is installed. Android phones should mount in Files. |

---

## 5. What is a package fix and what needs a Steel OS tool

**Just add packages** (add to `packages/core.txt`, one ticket):
- `simple-scan`: scanning.
- `hplip`, `gutenprint`: drivers for printers that are not driverless.
- `wsdd`: show up in Windows Explorer; helps find Windows machines.

**Needs a Steel OS tool or setting** (separate tickets):
- Folder sharing wizard (samba setup, firewall rules, UI).
- Decide whether to turn `cups-browsed` on so printers appear without Add.
- A "Printers and Scanners" entry in the Steel OS settings menu that opens
  Print Settings and Simple Scan, so users do not have to know the app names.

---

## 6. How to test (in a VM or on the test machine, not done yet)

The acceptance criteria say at least one printer and one share must be tried.
Needs a real printer on the same network, so the test machine (STEEL-5) is
better than a VM for this. Record what you see at each step.

**Printer**
1. On a fresh Omarchy install, press Super + Space, type Print, open Print
   Settings. Note whether any printer is already listed. (Expected: none.)
2. Click Add and wait 10 seconds. Does your network printer appear? Does a
   USB printer appear when plugged in?
3. Add it with the driverless option. Print a test page. Did it ask for a
   password at any point?
4. Open any app and print to PDF. Does the PDF appear in your home folder?

**Network**
5. Open Files, Other Locations. Which machines appear under Networks? Is the
   Windows PC there?
6. In Connect to Server, type `smb://` followed by the Windows PC's name.
   Does it ask for a username and password? Do the shares open?
7. Try to share a folder from the Linux machine. (Expected: there is no way to
   do it.)
8. On the Windows PC, open Explorer, Network. Does the Linux machine appear?
   (Expected: no.)

**Report** the answers as a comment on STEEL-3. They decide the follow-up
tickets in section 5.
