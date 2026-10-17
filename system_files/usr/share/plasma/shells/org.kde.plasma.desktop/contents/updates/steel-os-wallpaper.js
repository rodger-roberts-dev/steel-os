// Steel OS (STEEL-31): set the Steel OS waves wallpaper on every desktop.
// Plasma runs each script in this "updates" folder once per user, the first
// time plasmashell starts after the script appears: for new users at first
// login, for existing users after the update that adds it. A user who picks
// a different wallpaper later keeps it; this never runs again for them.
const allDesktops = desktops();
for (let i = 0; i < allDesktops.length; ++i) {
    const d = allDesktops[i];
    d.wallpaperPlugin = "org.kde.image";
    d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    d.writeConfig("Image", "file:///usr/share/wallpapers/steel-os-waves/");
    d.writeConfig("FillMode", 2);
}
