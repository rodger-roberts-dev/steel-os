// Steel OS (STEEL-31): take Bazzite Portal off existing users' taskbars.
// The app itself is removed from the image.
const unpinPanels = panels();
for (let i = 0; i < unpinPanels.length; ++i) {
    const widgets = unpinPanels[i].widgets();
    for (let j = 0; j < widgets.length; ++j) {
        const w = widgets[j];
        if (w.type === "org.kde.plasma.icontasks" || w.type === "org.kde.plasma.taskmanager") {
            w.currentConfigGroup = ["General"];
            const launchers = w.readConfig("launchers", "");
            const list = Array.isArray(launchers) ? launchers : String(launchers).split(",");
            const kept = list.filter(function (l) { return l && l.indexOf("yafti") === -1; });
            if (kept.length !== list.length) {
                w.writeConfig("launchers", kept);
                w.reloadConfig();
            }
        }
    }
}
