#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=================================="
echo "      STEEL OS BOOTSTRAP"
echo "=================================="
echo

check_packages() {
    local manifest="$1"

    echo "Checking $(basename "$manifest")"
    echo "----------------------------------"

    while IFS= read -r package || [[ -n "$package" ]]; do
        [[ -z "$package" || "$package" =~ ^[[:space:]]*# ]] && continue

        if pacman -Qq "$package" &>/dev/null; then
            printf "[OK]      %s\n" "$package"
        elif pacman -Si "$package" &>/dev/null; then
            printf "[MISSING] %s\n" "$package"
        else
            printf "[VERIFY]  %s\n" "$package"
        fi
    done < "$manifest"

    echo
}

check_packages "$ROOT_DIR/packages/core.txt"
check_packages "$ROOT_DIR/packages/development.txt"

echo "Bootstrap audit complete."
echo "No changes made."
