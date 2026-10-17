// Steel OS (STEEL-7, STEEL-37): start button and start menu.
// - The start button shows the Steel OS hexagon instead of Fedora's logo.
// - The start menu shows what an app does, then its name:
//   "Web Browser (Firefox)", "File Manager (Dolphin)". Plain English first.
// Runs inside the default layout for new users and once as an update
// script for existing users.
const steelPanels = panels();
for (let i = 0; i < steelPanels.length; ++i) {
    const widgets = steelPanels[i].widgets();
    for (let j = 0; j < widgets.length; ++j) {
        const w = widgets[j];
        if (w.type === "org.kde.plasma.kickoff" || w.type === "org.kde.plasma.kicker") {
            w.currentConfigGroup = ["General"];
            w.writeConfig("icon", "steel-os");
            // 3 = "Generic name (Name)"
            w.writeConfig("appNameFormat", 3);
            w.reloadConfig();
        }
    }
}
