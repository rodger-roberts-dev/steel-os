#!/usr/bin/python3
"""Ask Flathub about every app Steel OS offers: does it still exist, is it
retired (end-of-life), has it been renamed? Flathub renamed Thunderbird under
Steel OS's feet once (2026-10-19) and the one-click install silently broke.

usage: check-steel-apps.py packages/steel-apps.txt packages/flatpaks-default.txt
Prints one line per app and exits 1 if anything is missing, retired or renamed.
Run by .github/workflows/check-apps.yml (weekly, and on PRs that change the lists).
"""
import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://flathub.org/api/v2"


def app_ids(path):
    """steel-apps.txt: 'id | name | description | category'; flatpaks-default.txt: one id per line."""
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        app = line.split("|", 1)[0].strip()
        if app.count(".") >= 2 and " " not in app:
            out.append(app)
    return out


def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "steel-os-check-apps"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


def value(status, body):
    body = body.strip()
    return body.strip('"') if status == 200 and body not in ("", "null") else ""


def check(app):
    status, body = get(f"{API}/appstream/{app}")
    name = ""
    if status == 200:
        try:
            name = json.loads(body).get("name", "")
        except ValueError:
            pass
    rebase = value(*get(f"{API}/eol/rebase/{app}"))
    eol = value(*get(f"{API}/eol/message/{app}"))
    if rebase:
        return app, f"RENAMED  {app} is now {rebase}: update the list"
    if eol:
        return app, f"RETIRED  {app}: {eol[:120]}"
    if status == 404:
        return app, f"MISSING  {app} is not on Flathub"
    if status != 200:
        return app, f"UNKNOWN  {app}: Flathub did not answer ({status} {body[:80]})"
    return app, f"ok       {app} ({name})"


def main(files):
    apps = sorted({a for f in files for a in app_ids(f)})
    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(check, apps))
    problems = [line for _, line in rows if not line.startswith("ok")]
    for _, line in rows:
        print(line)
    print(f"\n{len(rows)} apps checked, {len(problems)} problem(s)")
    if problems:
        with open("check-steel-apps-problems.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(problems) + "\n")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["packages/steel-apps.txt", "packages/flatpaks-default.txt"]))
