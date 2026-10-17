# Installing Steel OS

Updated: 2026-10-17

From "I have a PC" to "I am looking at Steel OS", with no terminal at any
point. It takes about 30 minutes.

---

## What you need

- A 64-bit PC from the last ten years, with 8 GB of memory (4 GB at least) and
  64 GB of free disk space.
- A USB stick of 8 GB or more. Everything on it will be erased.
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
   certutil -hashfile steel-os-0.2.0-preview-x86_64.iso SHA256
   ```
   The long number it prints must match the one on the website.

## 2. Make the USB stick

1. On Windows, download **Fedora Media Writer**, **Rufus** or **balenaEtcher**.
2. Open it, choose the Steel OS file you downloaded, choose your USB stick,
   and click **Write** (or **Start** in Rufus; pick DD mode if it asks).
3. When it finishes, take the stick out.

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
`universalblue`, and restart.

## 4. The Steel OS live desktop

Steel OS starts from the stick. **Nothing on the PC has been changed yet.** A
welcome window offers **Install Steel OS**, **Try Steel OS first** and
**Repair the startup menu**. Click **Install Steel OS**. If you chose to try it
first, the installer is also on the desktop.

A PC with an NVIDIA graphics card shows a short note first: this edition uses
the open-source NVIDIA driver. Click **Continue**.

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
6. When it says Steel OS is installed, click **Restart now** and remove the
   USB stick when the screen goes dark.

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
| A blue screen about a key (MOK) | Choose **Enroll MOK**, **Continue**, **Yes**, type `universalblue`, restart. |
| The installer says the disk is too small | Steel OS needs 64 GB. Pick a bigger disk, or free up space. |
| The default apps never appear | Check the internet connection, then restart. They retry by themselves. |

Still stuck? Report it at **steel-os.org/report** with a photo of the screen.
