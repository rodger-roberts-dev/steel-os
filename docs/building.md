# How Steel OS is built

Written for: T and rodger-roberts-dev

Steel OS is not installed piece by piece. It is built as one image, the way a
phone's operating system is, and that image is what every machine runs and
updates to. This page says what builds it, where the result goes, and how to
get an ISO out of it.

## The three files that matter

| File | What it does |
|---|---|
| `Containerfile` | Says "start from Bazzite" and runs the build script. |
| `build_files/build.sh` | Copies our settings files in, installs our extra packages, adds our signing key. |
| `system_files/` | Our settings, laid out exactly as they land on the machine. `system_files/etc/xdg/kwinrc` becomes `/etc/xdg/kwinrc`. |

Supporting files: `packages/image.txt` (extra rpm packages),
`image-template.env` (image name and description), `disk_config/iso.toml`
(installer settings), `disk_config/disk.toml` (virtual machine disk settings),
`Justfile` (the build commands, used by the workflows and on a Linux PC),
`cosign.pub` (public signing key; the private key is a GitHub secret).

## What happens on GitHub

Two workflows under `.github/workflows/`.

**Build container image** (`build.yml`). Runs on every pull request, on every
push to `master`, and every day at 10:05 UTC. It builds the image, and on
`master` only, pushes it to `ghcr.io/steel-and-code/steel-os:latest` and
signs it with the key in the `SIGNING_SECRET` secret. The daily run is how
Bazzite's fixes reach us without anyone doing anything.

**Build disk images** (`build-disk.yml`). Started by hand from the Actions tab
with the Run workflow button. Pick `amd64`, and tick "Upload to S3" to send
the result to T's Cloudflare R2 bucket `steel-os-downloads`, which is public
at `downloads.steel-os.org`. Leave it unticked to get the files as a download
on the workflow page instead. It makes two things: an installer ISO and a
`qcow2` virtual machine disk.

Neither workflow runs on T's Windows PC. GitHub does the building.

## One-time setup already done (2026-10-16)

- Seven repository secrets: `SIGNING_SECRET` and the six `S3_*` values.
- R2 bucket `steel-os-downloads` with the custom domain `downloads.steel-os.org`.

## One-time setup still to do after the first push

The image lands in GitHub's container registry as a **private** package,
because the repo is private. An installed machine cannot pull updates from a
private package, and the ISO's install step would fail. Make the package
public once: on GitHub go to the steel-and-code organization, Packages,
`steel-os`, Package settings, Change visibility, Public. This exposes only the
built image, not the repo.

## Testing a build in the VM

1. Actions tab, "Build disk images", Run workflow, platform `amd64`, upload
   unticked. Wait about 40 minutes.
2. Download the ISO from the Artifacts box at the bottom of the run page.
3. In VirtualBox, attach it to the STEEL VM as the optical drive and start.
4. Install, log in, open Konsole, run `sudo bootc status`. The image name must
   be `ghcr.io/steel-and-code/steel-os:latest`.

## On a Linux PC (optional, rodger-roberts-dev)

`just build` builds the image with podman. `just build-iso` makes the ISO.
`just run-vm-qcow2` boots the result in a local virtual machine. Needs
`just`, `podman` and a few gigabytes of free space. See the Justfile.
