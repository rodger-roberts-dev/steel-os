"""Write release-notes.json: what changed in each Steel OS version.

Every merge to master is one version (see docs/versions.md): the n-th merge
since VERSION last changed is MAJOR.(MINOR + n // 10).(n % 10). The title of
each version is its pull request's title (the second paragraph of GitHub's
merge commit message), which is written in plain English. A daily rebuild (a
plain commit on master) keeps the version: it is listed as a "rebuilt" date
under the version it rebuilt.

usage: release-notes.py OUTPUT [CURRENT_VERSION]
"""
import datetime
import json
import re
import subprocess
import sys


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


out = sys.argv[1]
current = sys.argv[2] if len(sys.argv) > 2 else None
major, minor = (int(x) for x in open("VERSION").read().strip().split(".")[:2])
since = git("log", "-1", "--first-parent", "--format=%H", "--", "VERSION").strip()
log = git("log", "--first-parent", "--reverse", "--format=%H%x1f%cI%x1f%s%x1f%b%x1e", f"{since}..HEAD")

entries = []
n = 0
for rec in log.split("\x1e"):
    rec = rec.strip("\n")
    if not rec:
        continue
    sha, date, subject, body = rec.split("\x1f")
    m = re.match(r"Merge pull request #(\d+)", subject)
    if not m:
        # A rebuild (or any plain commit): same version, newer build.
        if not entries:
            entries.append({"version": f"{major}.{minor}.0", "date": date[:10], "pr": None,
                            "title": "Starting point", "commit": sha[:7]})
        entries[-1].setdefault("rebuilt", []).append(date[:10])
        continue
    n += 1
    lines = [l for l in body.strip().splitlines() if l.strip() and not l.startswith("Co-Authored-By")]
    title = lines[0] if lines else subject
    entries.append({
        "version": f"{major}.{minor + n // 10}.{n % 10}",
        "date": date[:10],
        "pr": int(m.group(1)),
        "title": title,
        "commit": sha[:7],
    })

entries.reverse()
with open(out, "w") as f:
    json.dump({
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "current": current,
        "repo": "https://github.com/steel-and-code/steel-os",
        "versions": entries[:80],
    }, f, indent=1)
    f.write("\n")
print(f"release notes: {len(entries)} versions, newest {entries[0]['version'] if entries else '-'}")
