#!/usr/bin/env python3
"""Generate stats.svg — self-hosted matrix-themed GitHub stats card.

Fetches public profile data from the GitHub REST API and renders an SVG
matching banner.svg's CRT/matrix aesthetic. No third-party widget services.

Run locally or inside a GitHub Action (uses GITHUB_TOKEN when present).
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

USER = "mandoof1"
FONT = "Consolas, 'Cascadia Code', 'Fira Code', 'Courier New', monospace"

GREEN = "#00ff41"
CYAN = "#00d4ff"
RED = "#ff0055"
DIM = "#8b949e"
FG = "#e6edf3"
DARK = "#0d1117"
BAR_BG = "#161b22"
FOOTER = "#3d4f46"


def gh(path: str) -> dict:
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "mandoof-profile-stats")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main() -> None:
    user = gh(f"/users/{USER}")
    repos = gh(f"/users/{USER}/repos?per_page=100&sort=updated")

    stars = sum(r["stargazers_count"] for r in repos)
    forks = sum(r["forks_count"] for r in repos)
    followers = user["followers"]
    following = user["following"]
    gists = user["public_gists"]

    # language share by bytes
    lang_bytes: dict[str, int] = {}
    for r in repos:
        try:
            langs = gh(f"/repos/{USER}/{r['name']}/languages")
            for lang, n in langs.items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + n
        except Exception:
            continue
    total = sum(lang_bytes.values()) or 1
    top = sorted(lang_bytes.items(), key=lambda kv: kv[1], reverse=True)[:6]

    sync = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ---------- layout ----------
    W, H = 880, 360
    cells = [
        ("STARS", str(stars)),
        ("REPOS", str(user["public_repos"])),
        ("FORKS", str(forks)),
        ("FOLLOWERS", str(followers)),
        ("GISTS", str(gists)),
    ]
    cell_x = [40, 216, 392, 568, 744]
    cell_w = 176

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    parts.append("<defs>")
    parts.append('<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">')
    parts.append(f'<stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{CYAN}"/>')
    parts.append("</linearGradient>")
    parts.append('<filter id="glow2" x="-20%" y="-20%" width="140%" height="140%">'
                 '<feGaussianBlur stdDeviation="2.5" result="b"/>'
                 '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    parts.append("</defs>")

    # bg + frame
    parts.append(f'<rect width="{W}" height="{H}" rx="10" fill="{DARK}"/>')
    parts.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="9" fill="none" '
                 f'stroke="{GREEN}" stroke-opacity="0.28"/>')

    # header
    parts.append(f'<text x="40" y="46" font-family="{FONT}" font-size="16" fill="{FG}">'
                 f'$ ./stats --live --user={USER}</text>')
    parts.append(f'<rect x="40" y="58" width="{W-80}" height="1" fill="{GREEN}" opacity="0.35"/>')

    # stat cells
    for (label, value), x in zip(cells, cell_x):
        parts.append(f'<text x="{x + cell_w - 16}" y="104" text-anchor="end" '
                     f'font-family="{FONT}" font-size="30" font-weight="bold" fill="{GREEN}" '
                     f'filter="url(#glow2)">{value}</text>')
        parts.append(f'<text x="{x + cell_w - 16}" y="128" text-anchor="end" '
                     f'font-family="{FONT}" font-size="12" letter-spacing="2" fill="{DIM}">{label}</text>')

    # languages
    parts.append(f'<text x="40" y="176" font-family="{FONT}" font-size="13" letter-spacing="3" '
                 f'fill="{CYAN}">LANGUAGES</text>')
    if top:
        for i, (lang, n) in enumerate(top):
            y = 200 + i * 24
            pct = n / total * 100
            w = int(520 * pct / 100)
            parts.append(f'<text x="40" y="{y}" font-family="{FONT}" font-size="13" fill="{FG}">{lang}</text>')
            parts.append(f'<rect x="180" y="{y - 10}" width="520" height="8" rx="4" fill="{BAR_BG}"/>')
            parts.append(f'<rect x="180" y="{y - 10}" width="{max(w, 6)}" height="8" rx="4" fill="url(#bar)"/>')
            parts.append(f'<text x="720" y="{y}" text-anchor="end" font-family="{FONT}" '
                         f'font-size="12" fill="{DIM}">{pct:.1f}%</text>')
    else:
        parts.append(f'<text x="40" y="200" font-family="{FONT}" font-size="13" fill="{DIM}">/dev/null</text>')

    # footer
    parts.append(f'<rect x="40" y="336" width="{W-80}" height="1" fill="{GREEN}" opacity="0.2"/>')
    parts.append(f'<text x="40" y="352" font-family="{FONT}" font-size="11" fill="{FOOTER}">'
                 f'sync: {sync} · self-hosted · no third-party trackers</text>')
    parts.append("</svg>")

    with open("stats.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"stats.svg written — stars={stars} repos={user['public_repos']} langs={len(top)}")


if __name__ == "__main__":
    sys.exit(main())
