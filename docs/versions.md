# Steel OS version numbers

Every Steel OS build has a version like **0.5.3**, and every merge to
`master` counts one up. The last number rolls over after 9:

0.4.8, 0.4.9, **0.5.0**, 0.5.1 ... 0.5.9, **0.6.0** ... 0.9.9, 0.10.0

- The `VERSION` file at the top of this repository holds the starting point
  (now `0.4`). Counting starts from it: the first build after `VERSION`
  changes is that number with `.0` (for example 1.0.0).
- **1.0 is never reached automatically.** It is a decision: a one-line pull
  request that changes `VERSION` to `1.0` when the release checklist passes.

The version shows in **About this System** ("Steel OS 0.5.3"), on the
installer's information panel, in `/usr/share/steel-os/version`, in the
installer's file name (`steel-os-0.5.3-x86_64.iso`) and `.image.txt` record,
and in the list of builds on steel-os.org/download.

Every installer is built from the exact image of the merge that triggered it.
When several merges land while an installer is building, only the newest one
gets an installer, so the list on steel-os.org/download can skip a number.

## The road to 1.0

| Version | When |
|---|---|
| 0.4.x to 0.9.x | Counts up by itself with every merge: tester fixes and features |
| **1.0** | The release checklist passes, a stranger installs from the guide alone, and the main Download button goes live. Change `VERSION` to `1.0` |
