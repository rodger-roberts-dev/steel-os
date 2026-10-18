// Steel OS: put the Steel OS waves wallpaper back on desktops that ended up
// with the base system's picture (Fedora's, through the "Default" wallpaper)
// because the first wallpaper script ran before the desktop existed.
// Only desktops showing a base-system picture change; a wallpaper the user
// picked is left alone. Runs once per user, like every script in this folder.
const steelBaseImages = ["/usr/share/wallpapers/Default", "/usr/share/wallpapers/F4", "/usr/share/wallpapers/Fedora",
                         "/usr/share/wallpapers/Next", "/usr/share/backgrounds/"];
const steelDesktops = desktops();
for (let i = 0; i < steelDesktops.length; ++i) {
    const d = steelDesktops[i];
    d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    const image = String(d.readConfig("Image", ""));
    const isBase = image === "" || steelBaseImages.some(function (p) { return image.indexOf(p) !== -1; });
    if (d.wallpaperPlugin === "org.kde.image" && isBase) {
        d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
        d.writeConfig("Image", "file:///usr/share/wallpapers/steel-os-waves/");
        d.writeConfig("FillMode", 2);
    }
}
