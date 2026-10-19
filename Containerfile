# Steel OS image recipe (STEEL-16).
#
# Steel OS is a custom bootable image built on Bazzite with the Universal Blue
# image template. This file is read by `podman build` in GitHub Actions. The
# real work happens in build_files/build.sh; this file only sets up the base
# image and the files the script can see.
#
# Steel OS is a Steel & Code project in partnership with Blackbox Entertainment.

# The base image for the final stage (see below). Declared before the first
# FROM so that it applies to every stage.
ARG BASE_IMAGE=ghcr.io/ublue-os/bazzite:stable

# Stage "ctx": files the build script may read, without copying them into the
# final image. Keeps the image clean.
FROM scratch AS ctx
COPY build_files /
COPY system_files /system_files
COPY packages /packages
COPY cosign.pub /cosign.pub
COPY branding /branding
COPY tests /tests

# Base image (STEEL-30). Steel OS is built in three editions from this one
# recipe; the build workflow passes BASE_IMAGE:
#   steel-os                bazzite:stable              AMD and Intel graphics
#   steel-os-nvidia         bazzite-nvidia-open:stable  NVIDIA RTX and GTX 16 series
#   steel-os-nvidia-legacy  bazzite-nvidia:stable       NVIDIA GTX 900 and 1000 series
# A PC is moved to the right edition at first boot (steel-os-graphics-check).
FROM ${BASE_IMAGE}

# Build number written into the image (date and commit), shown on the live
# installer's information panel and in /usr/share/steel-os/build.
ARG STEEL_OS_BUILD=local
# Version number, e.g. 0.4.12 (see VERSION and the Justfile build recipe).
ARG STEEL_OS_VERSION=0.0.0

# Run the build script. The mounts give it the ctx stage at /ctx and scratch
# space for package caches and logs that must not end up in the image.
RUN --mount=type=bind,from=ctx,source=/,target=/ctx \
    --mount=type=cache,dst=/var/cache \
    --mount=type=cache,dst=/var/log \
    --mount=type=tmpfs,dst=/tmp \
    bash /ctx/build.sh

# Check the finished image for bootc mistakes before it is pushed.
RUN bootc container lint
