// Steel OS (STEEL-40): pin the Steel OS Portal on the taskbar for people who
// already had Steel OS before the portal arrived. New users get the pin from
// the default layout. Runs once per user.
const pinPanels = panels();
for (let i = 0; i < pinPanels.length; ++i) {
    const widgets = pinPanels[i].widgets();
    for (let j = 0; j < widgets.length; ++j) {
        const w = widgets[j];
        if (w.type === "org.kde.plasma.icontasks" || w.type === "org.kde.plasma.taskmanager") {
            w.currentConfigGroup = ["General"];
            const launchers = w.readConfig("launchers", "");
            const list = Array.isArray(launchers) ? launchers : String(launchers).split(",").filter(function (l) { return l; });
            const pin = "applications:steel-os-portal.desktop";
            if (list.indexOf(pin) === -1) {
                const at = list.indexOf("applications:org.kde.konsole.desktop");
                if (at === -1) { list.push(pin); } else { list.splice(at + 1, 0, pin); }
                w.writeConfig("launchers", list);
                w.reloadConfig();
            }
        }
    }
}
