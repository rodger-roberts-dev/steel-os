# Steel OS version numbers

Every Steel OS build has a version like **0.4.12**:

- **0.4** is the milestone. It lives in the `VERSION` file at the top of this
  repository and changes only when someone decides a milestone is reached:
  a one-line pull request.
- **12** counts the merges to `master` since `VERSION` last changed. It goes up
  by itself with every merge, so every installer has its own number.

The version shows in **About this System** ("Steel OS 0.4.12"), on the
installer's information panel, in `/usr/share/steel-os/version`, in each
installer's `.image.txt` record, and in the list of builds on
steel-os.org/download.

## The road to 1.0

| Milestone | When to move to it |
|---|---|
| 0.4 | The Katana test follow-ups shipped: shortcuts, taskbar, developer apps, behaviour watching (October 2026) |
| 0.5 | The preview passes the VM test and the hardware tests on Command and Katana |
| 0.6 and on | Each further set of fixes and features from testers, as decided |
| **1.0** | The release checklist passes, a stranger installs from the guide alone, and the main Download button goes live |

To move to the next milestone, change `VERSION` (for example to `0.5`) in a
pull request. The first build after it is 0.5.0.
