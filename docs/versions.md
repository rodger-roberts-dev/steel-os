# Steel OS version numbers

Every Steel OS build has a version like **0.5.3**, and every merge to
`master` counts one up. The last number rolls over after 9:

0.4.8, 0.4.9, **0.5.0**, 0.5.1 ... 0.5.9, **0.6.0** ... 0.9.8, **0.9.9**

It never goes past x.9.9: once there, further merges keep the number (with a
newer build date) until `VERSION` is raised by hand. So 0.9.9 is the last
0.x number and the next one is 1.0.0, never 0.10.0.

- The `VERSION` file at the top of this repository holds the starting point
  (now `0.4`). Counting starts from it: the first build after `VERSION`
  changes is that number with `.0` (for example 1.0.0).
- **1.0 is never reached automatically.** It is a decision: a one-line pull
  request that changes `VERSION` to `1.0` when the release checklist passes.

The version shows in **About this System** ("Steel OS 0.5.3"), on the
installer's information panel, in `/usr/share/steel-os/version`, in the
installer's file name (`steel-os-0.5.3-x86_64.iso`) and `.image.txt` record,
and in the list of builds on steel-os.org/download.

A daily rebuild on Bazzite's newest base (Fedora's updates) **keeps the
version**: when the base images have changed, the **Daily rebuild** workflow
records it on `master` (`packages/base-images.txt`, a plain commit, not a
merge), the image and installer are rebuilt with the same version number and a
newer build date (`/usr/share/steel-os/build`, `YYYYMMDD-commit`), and the
installer replaces the one with the same name. A year of rebuilds with no
changes is still the same version. When nothing changed upstream, nothing is
built. Rebuilds are not announced on Discord; new versions are.

Every installer is built from the exact image of the merge that triggered it.
When several merges land while an installer is building, only the newest one
gets an installer, so the list on steel-os.org/download can skip a number.

## The road to 1.0

| Version | When |
|---|---|
| 0.4.x to 0.9.x | Counts up by itself with every merge: tester fixes and features |
| **1.0** | The release checklist passes, a stranger installs from the guide alone, and the main Download button goes live. Change `VERSION` to `1.0` |

## Release notes

Every installer build also publishes `release-notes.json` on
downloads.steel-os.org (made by `.github/scripts/release-notes.py`): one entry
per version with its date and pull request title, plus the dates it was
rebuilt on. steel-os.org/preview shows it as **What's new**. So a pull request's title is its release note: write it
in plain English, for people using Steel OS.
