"""Is the newest base worth its own Steel OS version?

The daily rebuild calls this when Bazzite's stable base images change. It
compares what is underneath now with what was there at the last check
(packages/upstream.json) and decides whether the change is important enough
to tell people about. Important means any of:

- a new Fedora version (44 -> 45)
- a new Linux kernel series (7.2 -> 7.3): support for newer hardware
- a new KDE Plasma series (6.7 -> 6.8): the desktop itself
- a new Mesa series (26.2 -> 26.3): the graphics drivers for AMD and Intel
- a new NVIDIA driver series (615 -> 620), for the NVIDIA editions
- an urgent Fedora security fix for a package that changed in the image

Everything else (the daily stream of small package updates) is not.

The facts come from Bazzite's own release notes on GitHub ("Major packages"
and the per-image package tables) and from Fedora's update system (Bodhi)
for security fixes. Nothing here needs a key; GH_TOKEN, if set, only raises
GitHub's rate limit.

usage: upstream-notes.py BASE_VERSION STATE_FILE OUTPUT_FILE
  BASE_VERSION  the base image's org.opencontainers.image.version, e.g. 44.20261012.1
                (Bazzite's stable release tags are exactly that)
  STATE_FILE    packages/upstream.json: read, then rewritten with today's facts
  OUTPUT_FILE   JSON {"title": "...", "lines": [...]}; title is "" when
                nothing important changed (or on the very first run)
"""
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

REPO = "ublue-os/bazzite"
STABLE_TAG = re.compile(r"^\d+\.\d{8}(\.\d+)?$")
# Package tables that apply to Steel OS: every image, the KDE desktop and the
# NVIDIA editions (not GNOME, not the handheld Deck images).
SECTIONS = ("All Images", "KDE", "Nvidia")


def get(url, github=False):
    headers = {"User-Agent": "steel-os-daily-rebuild", "Accept": "application/json"}
    if github and os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
        return json.load(r)


def series(version, parts):
    """'7.2.9-ogc3.1' -> '7.2' (parts=2); '615.78.08-1' -> '615' (parts=1)."""
    if not version:
        return ""
    return ".".join(re.split(r"[.\-]", version)[:parts])


def major_packages(body):
    """{'Kernel': '7.2.9-ogc3.1', ...} from the "Major packages" table; a cell
    'old ➡️ new' gives new."""
    out = {}
    m = re.search(r"### Major packages\n(.*?)(\n###|\Z)", body, re.S)
    for line in (m.group(1) if m else "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0].startswith("**"):
            out[cells[0].strip("*")] = cells[1].split("➡️")[-1].strip()
    return out


def changed_packages(body):
    """Names of the packages added or updated in the tables that apply to Steel OS."""
    names = set()
    for part in re.split(r"\n(?=### )", body):
        head = part.splitlines()[0] if part else ""
        if not head.startswith("### ") or not any(s in head for s in SECTIONS):
            continue
        for line in part.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and cells[0] in ("🔄", "✨"):
                names.add(cells[1])
    return names


def urgent_security(fedora, since, changed):
    """Source package names with an urgent Fedora security fix pushed since
    `since` (YYYY-MM-DD) that match a package that changed in the image."""
    found = set()
    page = 1
    while page <= 10:
        q = urllib.parse.urlencode({"releases": f"F{fedora}", "type": "security", "severity": "urgent",
                                    "status": "stable", "pushed_since": since, "rows_per_page": 100, "page": page})
        d = get("https://bodhi.fedoraproject.org/updates/?" + q)
        for u in d.get("updates", []):
            for b in u.get("builds", []):
                src = b.get("nvr", "").rsplit("-", 2)[0]
                if src and any(n == src or n.startswith(src + "-") for n in changed):
                    found.add(src)
        if page >= d.get("pages", 1):
            break
        page += 1
    return sorted(found)


def main():
    base_version, state_file, output = sys.argv[1:4]
    today = datetime.date.today().isoformat()
    try:
        with open(state_file) as f:
            prev = json.load(f)
    except (OSError, ValueError):
        prev = {}

    releases = [r for r in get(f"https://api.github.com/repos/{REPO}/releases?per_page=100", github=True)
                if STABLE_TAG.match(r.get("tag_name", "")) and not r.get("prerelease")]
    releases.sort(key=lambda r: r["published_at"])
    by_tag = {r["tag_name"]: r for r in releases}
    newest = by_tag.get(base_version)
    if newest is None:
        print(f"No Bazzite release notes for {base_version}; nothing to compare.")
        json.dump({"title": "", "lines": []}, open(output, "w"))
        return

    major = major_packages(newest.get("body") or "")
    now = {
        "base": base_version,
        "checked": today,
        "fedora": base_version.split(".")[0],
        "kernel": series(major.get("Kernel"), 2),
        "kde": series(major.get("KDE"), 2),
        "mesa": series(major.get("Mesa"), 2),
        "nvidia": series(major.get("Nvidia Open") or major.get("Nvidia"), 1),
        "nvidia_lts": series(major.get("Nvidia LTS"), 1),
    }

    items, lines = [], []
    if prev.get("base") and prev.get("base") != base_version:
        if now["fedora"] != prev.get("fedora"):
            items.append(f"Fedora {now['fedora']}")
            lines.append(f"Steel OS is now built on Fedora {now['fedora']} (was {prev.get('fedora')}).")
        if now["kernel"] and now["kernel"] != prev.get("kernel"):
            items.append(f"Linux kernel {now['kernel']}")
            lines.append(f"Linux kernel {now['kernel']}: support for newer hardware and fixes.")
        if now["kde"] and now["kde"] != prev.get("kde"):
            items.append(f"KDE Plasma {now['kde']}")
            lines.append(f"The desktop is now KDE Plasma {now['kde']}.")
        if now["mesa"] and now["mesa"] != prev.get("mesa"):
            items.append(f"Mesa {now['mesa']} graphics drivers")
            lines.append(f"Mesa {now['mesa']}: newer graphics drivers for AMD and Intel.")
        nv = [now[k] for k in ("nvidia", "nvidia_lts") if now[k] and now[k] != prev.get(k)]
        if nv:
            items.append("NVIDIA driver " + " and ".join(nv))
            lines.append("NVIDIA driver " + " and ".join(nv) + " on the NVIDIA editions.")
        # Every stable release since the last check, for what changed in the image.
        start = by_tag.get(prev.get("base"))
        span = [r for r in releases
                if (start is None or r["published_at"] > start["published_at"]) and r["published_at"] <= newest["published_at"]]
        changed = set()
        for r in span or [newest]:
            changed |= changed_packages(r.get("body") or "")
        try:
            fixes = urgent_security(now["fedora"], prev.get("checked") or today, changed)
        except Exception as e:  # noqa: BLE001 - Bodhi down: still report the rest
            print("Fedora's update system did not answer:", e)
            fixes = []
        if fixes:
            items.append("urgent security fixes" if len(fixes) > 1 else "an urgent security fix")
            lines.append("Urgent security fixes from Fedora: " + ", ".join(fixes) + ".")
    elif not prev.get("base"):
        print("First check: recording what is underneath now, nothing to announce.")

    title = ""
    if items:
        title = "Under the hood: " + (items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1])
    with open(state_file, "w") as f:
        json.dump(now, f, indent=1)
        f.write("\n")
    with open(output, "w") as f:
        json.dump({"title": title, "lines": lines}, f)
    print(json.dumps({"now": now, "title": title, "lines": lines}, indent=1))


if __name__ == "__main__":
    main()
