#!/usr/bin/env python3
"""Self-hosted public GitHub stats. Use --offline to redraw the cached snapshot."""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

from scripts.generate_assets import BG, BORDER, CYAN, LIME, MUTED, WHITE, svg, text

ROOT = Path(__file__).resolve().parent
USER = "mandoof1"
CACHE = ROOT / "assets" / "stats.json"


def gh(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "mandoof1-profile"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def collect():
    user = gh(f"/users/{USER}")
    repos = []
    page = 1
    while True:
        batch = gh(f"/users/{USER}/repos?type=owner&per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    owned = [repo for repo in repos if not repo["fork"] and not repo["private"]]
    languages = {}
    for repo in owned:
        # Fail the refresh rather than publishing language shares from partial data.
        for language, count in gh(f"/repos/{USER}/{repo['name']}/languages").items():
            languages[language] = languages.get(language, 0) + count
    total = sum(languages.values()) or 1
    return {
        "user": USER,
        "repos": len(owned),
        "stars": sum(repo["stargazers_count"] for repo in owned),
        "followers": user["followers"],
        "since": user["created_at"][:4],
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "languages": [
            {"name": language, "percent": round(count / total * 100, 1)}
            for language, count in sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5]
        ],
    }


def render(data):
    metrics = [("PUBLIC REPOS", data["repos"]), ("STARS", data["stars"]),
               ("FOLLOWERS", data["followers"]), ("BUILDING SINCE", data["since"])]
    parts = [f'<rect width="1200" height="420" rx="20" fill="{BG}"/>',
             f'<rect x="1" y="1" width="1198" height="418" rx="19" stroke="{BORDER}" fill="none"/>',
             text(36, 46, "OPEN-SOURCE SNAPSHOT", 18, LIME, mono=True, letter_spacing="1.5")]
    for index, (label, value) in enumerate(metrics):
        x = 36 + index * 292
        parts.extend([text(x, 115, str(value), 48, WHITE, 700),
                      text(x, 147, label, 15, MUTED, mono=True)])
    parts.extend([f'<path d="M 36 178 H 1164" stroke="{BORDER}"/>',
                  text(36, 213, "LANGUAGES / SOURCE BYTES", 15, MUTED, mono=True)])
    colors = [LIME, CYAN, "#a9baf7", "#e8c88d", "#c5a5da"]
    for index, language in enumerate(data["languages"][:5]):
        y = 245 + index * 26
        width = max(0, min(100, language["percent"])) / 100 * 790
        parts.extend([
            text(36, y, language["name"], 17, WHITE),
            f'<rect x="265" y="{y - 11}" width="790" height="7" rx="3.5" fill="{BORDER}"/>',
            f'<rect x="265" y="{y - 11}" width="{width:.1f}" height="7" rx="3.5" fill="{colors[index]}"/>',
            text(1164, y, f'{language["percent"]:.1f}%', 16, MUTED, mono=True, text_anchor="end"),
        ])
    parts.extend([f'<path d="M 36 374 H 1164" stroke="{BORDER}"/>',
                  text(36, 401, f'PUBLIC, NON-FORK REPOS / UPDATED {data["updated"]}', 14, MUTED, mono=True)])
    return svg(1200, 420, f'GitHub stats for {USER}, collected {data["updated"]}',
               "Public, owned, non-fork repository statistics. Language shares measure source bytes, not proficiency.",
               "\n".join(parts))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="redraw cached data without a network request")
    args = parser.parse_args()
    data = json.loads(CACHE.read_text(encoding="utf-8")) if args.offline else collect()
    artwork = render(data)
    if not args.offline:
        CACHE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    (ROOT / "stats.svg").write_text(artwork, encoding="utf-8")
    print(f'stats.svg rendered using data from {data["updated"]}')


if __name__ == "__main__":
    main()
