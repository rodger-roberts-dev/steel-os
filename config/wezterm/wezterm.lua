local wezterm = require("wezterm")
local config = wezterm.config_builder()

config.keys = {
    {
        key = "c",
        mods = "ALT",
        action = wezterm.action.CopyTo("Clipboard"),
    },
    {
        key = "v",
        mods = "ALT",
        action = wezterm.action.PasteFrom("Clipboard"),
    },
}

return config
