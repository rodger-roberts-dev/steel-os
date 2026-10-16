# Steel OS image recipe (STEEL-16).
#
# Steel OS is a custom bootable image built on Bazzite with the Universal Blue
# image template. This file is read by `podman build` in GitHub Actions. The
# real work happens in build_files/build.sh; this file only sets up the base
# image and the files the script can see.
#
# Steel OS is a Steel & Code project in partnership with Blackbox Entertainment.

# Stage "ctx": files the build script may read, without copying them into the
# final image. Keeps the image clean.
FROM scratch AS ctx
COPY build_files /
COPY system_files /system_files
COPY packages /packages
COPY cosign.pub /cosign.pub

# Base image: Bazzite stable, KDE Plasma, AMD and Intel graphics.
# The NVIDIA variants (bazzite-nvidia-open, bazzite-nvidia) are handled by
# STEEL-30, which detects the graphics card at first boot.
FROM ghcr.io/ublue-os/bazzite:stable

# Run the build script. The mounts give it the ctx stage at /ctx and scratch
# space for package caches and logs that must not end up in the image.
RUN --mount=type=bind,from=ctx,source=/,target=/ctx \
    --mount=type=cache,dst=/var/cache \
    --mount=type=cache,dst=/var/log \
    --mount=type=tmpfs,dst=/tmp \
    /ctx/build.sh

# Check the finished image for bootc mistakes before it is pushed.
RUN bootc container lint
