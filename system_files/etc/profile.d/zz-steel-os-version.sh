# Steel OS: the version under the terminal's welcome message (T, 2026-10-19).
# Off together with the welcome message (ujust toggle-user-motd).
if [[ $- == *i* && -z "${STEEL_OS_VERSION_SHOWN:-}" && ! -e "$HOME/.config/no-show-user-motd" ]] \
    && command -v steel-os-version >/dev/null 2>&1; then
    export STEEL_OS_VERSION_SHOWN=1
    printf '  \033[1m%s\033[0m\n\n' "$(steel-os-version --short 2>/dev/null)"
fi
