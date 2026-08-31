#!/usr/bin/env python3
"""Generate stats.svg — a self-hosted GitHub stats card for the profile README.

Fetches public profile data from the GitHub REST API and renders a static SVG in
the GitHub-native dark palette. No third-party widget services.

Run locally or inside a GitHub Action (uses GITHUB_TOKEN when present).
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

USER = "mandoof1"
FONT = "'SFMono-Regular', 'Cascadia Code', 'Fira Code', Consolas, 'Courier New', monospace"

GREEN = "#3fb950"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"
DIM = "#8b949e"
FG = "#e6edf3"
DARK = "#0d1117"
BAR_BG = "#21262d"
BORDER = "#30363d"
FOOTER = "#484f58"


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
    owned = [r for r in repos if not r["fork"]]

    stars = sum(r["stargazers_count"] for r in owned)
    followers = user["followers"]
    since = user["created_at"][:4]

    # language share by bytes — owned (non-fork) repos only
    lang_bytes: dict[str, int] = {}
    for r in owned:
        try:
            langs = gh(f"/repos/{USER}/{r['name']}/languages")
            for lang, n in langs.items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + n
        except Exception:
            continue
    total = sum(lang_bytes.values()) or 1
    top = sorted(lang_bytes.items(), key=lambda kv: kv[1], reverse=True)[:5]

    sync = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # ---------- layout ----------
    W, H = 880, 350
    MX = 44
    cells = [
        ("REPOS", str(len(owned))),
        ("STARS", str(stars)),
        ("FOLLOWERS", str(followers)),
        ("SINCE", since),
    ]
    n = len(cells)
    span = W - 2 * MX
    step = span / n

    p: list[str] = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub stats for {USER}">')
    p.append("<defs>")
    p.append('<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{BLUE}"/>'
             "</linearGradient>")
    p.append("</defs>")

    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="{DARK}"/>')
    p.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{BORDER}"/>')

    # header
    p.append(f'<text x="{MX}" y="46" xml:space="preserve" font-family="{FONT}" font-size="16" fill="{FG}">'
             f'<tspan fill="{BLUE}">$ </tspan>gh api /users/{USER}</text>')
    p.append(f'<rect x="{MX}" y="60" width="{W-2*MX}" height="1" fill="{BORDER}"/>')

    # stat cells
    for i, (label, value) in enumerate(cells):
        cx = MX + step * i + step / 2
        p.append(f'<text x="{cx:.0f}" y="112" text-anchor="middle" font-family="{FONT}" '
                 f'font-size="34" font-weight="bold" fill="{GREEN}">{value}</text>')
        p.append(f'<text x="{cx:.0f}" y="136" text-anchor="middle" font-family="{FONT}" '
                 f'font-size="12" letter-spacing="2" fill="{DIM}">{label}</text>')

    # languages
    p.append(f'<text x="{MX}" y="186" font-family="{FONT}" font-size="12" letter-spacing="3" '
             f'fill="{BLUE}">LANGUAGES · owned repositories</text>')
    bar_x, bar_w = MX + 130, W - MX - 130 - 60
    for i, (lang, nbytes) in enumerate(top):
        y = 212 + i * 22
        pct = nbytes / total * 100
        w = max(bar_w * pct / 100, 4)
        p.append(f'<text x="{MX}" y="{y}" font-family="{FONT}" font-size="13" fill="{FG}">{lang}</text>')
        p.append(f'<rect x="{bar_x}" y="{y-10}" width="{bar_w}" height="8" rx="4" fill="{BAR_BG}"/>')
        p.append(f'<rect x="{bar_x}" y="{y-10}" width="{w:.0f}" height="8" rx="4" fill="url(#bar)"/>')
        p.append(f'<text x="{W-MX}" y="{y}" text-anchor="end" font-family="{FONT}" '
                 f'font-size="12" fill="{DIM}">{pct:.1f}%</text>')

    # footer
    p.append(f'<rect x="{MX}" y="{H-34}" width="{W-2*MX}" height="1" fill="{BORDER}"/>')
    p.append(f'<text x="{MX}" y="{H-14}" font-family="{FONT}" font-size="11" fill="{FOOTER}">'
             f'updated {sync} · self-hosted render, no third-party widgets</text>')
    p.append("</svg>")

    with open("stats.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"stats.svg written — owned={len(owned)} stars={stars} langs={len(top)}")


if __name__ == "__main__":
    sys.exit(main())
