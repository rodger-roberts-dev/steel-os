# Installing Steel OS

Updated: 2026-10-17

From "I have a PC" to "I am looking at Steel OS", with no terminal at any
point. It takes about 30 minutes.

---

## What you need

- A 64-bit PC from the last ten years, with 8 GB of memory (4 GB at least) and
  64 GB of free disk space.
- A PC that starts in **UEFI** mode, which is every PC from roughly 2012 on.
  PCs that only have old BIOS (Legacy or CSM) can't start the Steel OS
  installer. If yours has a choice, set it to UEFI in the firmware settings.
- A USB stick of 16 GB or more (the installer is about 8.5 GB). Everything on it
  will be erased.
- **A backup of everything on the PC you are installing to.** Installing
  Steel OS with "Use entire disk" erases that disk.
- An internet connection, ideally a cable for the first start.

## 1. Download

1. Go to **steel-os.org** and click **Download** (or **Download Preview** for a
   test build).
2. Note the **SHA-256** shown next to the button.
3. Optional but wise: check the download. On Windows, open Command Prompt in
   your Downloads folder and run:
   ```
   certutil -hashfile steel-os-preview-x86_64.iso SHA256
   ```
   The long number it prints must match the one on the website.

## 2. Make the USB stick

1. On Windows, download **Rufus** (rufus.ie). Fedora Media Writer and
   balenaEtcher work too: choose the file, choose the stick, click **Write**.
2. In Rufus, pick your USB stick under **Device**. Everything on it is erased.
3. Click **SELECT** and choose the Steel OS file.
4. A box says **ISOHybrid image detected**. That is normal: click **OK**. (If
   Rufus asks instead, choose **Write in DD Image mode**.)
5. Leave the rest as it is: **GPT** and **UEFI** are right, and the greyed-out
   settings are not used.
6. Click **START**, then **OK** on the warning that the stick will be erased.
7. When it says **READY**, click **CLOSE** and take the stick out. Windows may
   say the stick needs formatting afterwards: don't, that is normal.

Installing in a virtual machine instead? Attach the downloaded file as the
virtual machine's CD drive, use UEFI firmware, 8 GB of memory and a 64 GB disk,
and skip to step 4.

## 3. Start the PC from the USB stick

1. Plug the stick into the PC you are installing to and turn it on.
2. Straight away, press the **boot menu** key. It is usually **F12**, **F11**,
   **F8** or **Esc**; the PC's start-up screen often says which.
3. Pick the USB stick from the list.

**Secure Boot** can stay on. If a blue screen asks to **enrol a key**, choose
**Enroll MOK**, then **Continue**, then **Yes**, type the password
`steelos`, and restart.

## 4. The Steel OS live desktop

Steel OS starts from the stick. **Nothing on the PC has been changed yet.** A
welcome window offers **Install Steel OS**, **Try Steel OS first** and
**Repair the startup menu**. Click **Install Steel OS**. If you chose to try it
first, the installer is also on the desktop.

A PC with an NVIDIA graphics card shows a short note first. Click **Continue**.
After installation, Steel OS fetches NVIDIA's own driver by itself and asks you
to restart once.

## 5. The installer

1. **Language:** pick yours and click **Next**.
2. **Installation method:** **Use entire disk** is already selected. Check
   that the disk shown is the right one, then click **Next**. Want to keep
   Windows next to Steel OS? Choose the option to share the disk instead, and
   make sure you have a backup.
3. **Disk encryption** (optional): tick it to protect your files with a
   password if the PC is stolen. You type that password at every start.
   **Nobody can recover it if you forget it.**
4. **Create account:** your name, a user name and a password. This account is
   the computer's administrator.
5. **Review** the summary and click **Install**. It takes 10 to 20 minutes.
6. When it says the installation is complete, click **Finish**. A window says
   **Steel OS is installed**. Remove the USB stick and click **Restart now**.

## 6. First start

1. Log in with the password you just made.
2. **Steel OS Setup** opens: how updates work, which apps you want, and your
   printer. Every page has **Skip**.
3. Leave the PC online for a few minutes. Firefox, LibreOffice and the other
   default apps install themselves and appear in the start menu.
4. The **Steel OS Portal** on the taskbar has one-click apps, **Update now**
   and **Get help**.

That's it. Steel OS updates itself every Tuesday from now on.

---

## If something goes wrong

| What you see | What to do |
|---|---|
| The PC starts Windows instead of the USB stick | Restart and press the boot menu key again. Some PCs need **Secure Boot** or **Fast Boot** turned off in the firmware settings to see the stick. |
| A blue screen about a key (MOK) | Choose **Enroll MOK**, **Continue**, **Yes**, type `steelos`, restart. |
| The installer says the disk is too small | Steel OS needs 64 GB. Pick a bigger disk, or free up space. |
| The default apps never appear | Check the internet connection, then restart. They retry by themselves. |

Still stuck? Report it at **steel-os.org/report** with a photo of the screen.

---

## Privacy: the weekly device count

Like Fedora and Bazzite, Steel OS takes part in Fedora's anonymous weekly
device count (DNF Count Me). Once a week, one update check carries a flag
saying "a Steel OS machine of this version". The totals Fedora publishes
contain no names, serial numbers or IP addresses, and steel-os.org shows the
Steel OS line.

To switch it off, open a terminal and run:

```
sudo systemctl mask --now rpm-ostree-countme.timer
```
