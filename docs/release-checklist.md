# Release checklist

Updated: 2026-10-17

The steps for publishing a Steel OS installer, either a preview for testers or
a stable release. Every step is done in a web browser, apart from the tests in
a virtual machine. Nothing is built on a contributor's own PC.

---

## 1. Before building

- [ ] Every pull request meant for this release is merged into `master`.
- [ ] The newest **Build container image** run on `master` is green, and its
      **Sign container image** step succeeded.
- [ ] The version number is decided, for example `0.2.0-preview` or `1.0.0`.

## 2. Build the installer ISO

1. On GitHub, open **Actions**, then **Build disk images**, then **Run workflow**.
2. Branch: `master`. Version: the number from step 1. Leave **Upload to S3**
   unticked for the test build.
3. Wait for it to finish, which takes about 40 minutes. Download the
   **artifact** from the bottom of the run page. It is a zip with the ISO, its
   `.sha256` checksum and its `.sig` signature.

## 3. Test it in a virtual machine

Use a fresh virtual machine: UEFI firmware, 8 GB of memory, 64 GB disk.

- [ ] The ISO boots to the Steel OS live desktop. Nothing says Bazzite or Fedora.
- [ ] The installer runs in Steel OS colours, with **Use entire disk** selected.
- [ ] The last installer screen has no Fedora feedback QR code. **Finish**
      closes it, and the **Steel OS is installed** window's **Restart now**
      restarts into Steel OS.
- [ ] The boot splash, login screen, wallpaper and lock screen are Steel OS.
- [ ] Steel OS Setup appears at first login; every page can be skipped.
- [ ] Choosing one app in Setup installs it, and a notification says so.
- [ ] Within a few minutes Firefox, LibreOffice, OBS Studio, Kdenlive,
      Obsidian, Moonlight and Zed are in the start menu.
- [ ] The Steel OS Portal is on the taskbar and in the start-menu favourites.
- [ ] Super+Enter opens the terminal, Super+Shift+Enter opens Firefox, and
      Super+2 switches desktops.
- [ ] "Visit steel-os.org" in the Portal opens in Firefox.
- [ ] Steel OS Help opens from the start menu.
- [ ] `sudo bootc status` shows `ghcr.io/steel-and-code/steel-os` and nothing else.
- [ ] `sudo bootc upgrade`, restart, then pick the older entry in the boot
      menu: the previous version starts.
- [ ] Hardware releases only, on the test PC: printing, a controller and one
      Steam game.

If anything fails, fix it with a pull request and start again at step 1.

## 4. Publish

1. Run **Build disk images** again with the same version, this time with
   **Upload to S3** ticked. The ISO, checksum and signature go to
   `downloads.steel-os.org`.
2. Open `https://downloads.steel-os.org/<file name>.sha256` and check that it
   matches the one from the test build.
3. On the website repo, edit `releases/latest.json`:
   - **Preview:** add a `preview` block with `version`, `date`, `iso_url`,
     `size_bytes`, `sha256` and `notes_url`. The **Download Preview** button
     appears and the main button still says Coming soon.
   - **Stable release:** set `status` to `released` and fill in `version`,
     `date`, `iso_url`, `size_bytes`, `sha256` and `checksums_url`. The main
     **Download** button switches on.
4. Update the release notes page (`preview.html` for a preview) with what is
   new and the known issues.
5. Merge the website pull request. Cloudflare publishes it within a minute.

## 5. After publishing

- [ ] Download the ISO from steel-os.org and check its checksum on Windows:
      `certutil -hashfile <file>.iso SHA256`.
- [ ] Tag the commit in the Steel OS repo with the version, for example
      `v0.2.0-preview`.
- [ ] Note the Bazzite image the release was built on. It is in the build log
      of the image run.
- [ ] Tell the testers, with the link to the release notes.
