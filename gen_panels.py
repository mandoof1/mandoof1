#!/usr/bin/env python3
"""Generate status.svg (radar sweep + service LED panel) and badges.svg
(medallion wall) for the GitHub profile. Self-contained animated SVGs."""
from html import escape

FONT = "Consolas, 'Cascadia Code', 'Fira Code', 'Courier New', monospace"
GREEN, CYAN, RED, AMBER, MAGENTA = "#00ff41", "#00d4ff", "#ff0055", "#febc2e", "#ff00aa"
FG, DIM, DARK, FOOTER = "#e6edf3", "#8b949e", "#0d1117", "#3d4f46"


def frame(w, h):
    return (f'<rect width="{w}" height="{h}" rx="10" fill="{DARK}"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="9" fill="none" stroke="{GREEN}" stroke-opacity="0.28"/>')


# ================= status.svg =================
W, H = 846, 250
services = [
    ("wisp", "ONLINE", GREEN, "1.1s"),
    ("amnis", "ONLINE", GREEN, "1.7s"),
    ("honeypots", "ARMED", GREEN, "0.9s"),
    ("browseye", "STANDBY", AMBER, "2.3s"),
    ("media pipeline", "STREAMING", CYAN, "1.4s"),
    ("uplink", "X25519", GREEN, "2.1s"),
    ("novelist", "WRITING", MAGENTA, "3.1s"),
]
svc_svg = []
for i, (name, state, color, speed) in enumerate(services):
    y = 58 + i * 26
    svc_svg.append(
        f'<circle cx="262" cy="{y - 4}" r="4" fill="{color}" style="animation: led {speed} ease-in-out infinite"/>'
    )
    svc_svg.append(f'<text x="278" y="{y}" font-family="{FONT}" font-size="14" fill="{FG}">{name}</text>')
    svc_svg.append(
        f'<text x="810" y="{y}" text-anchor="end" font-family="{FONT}" font-size="13" '
        f'letter-spacing="1" fill="{color}">[{state}]</text>'
    )
svc_svg = "\n    ".join(svc_svg)

blips = [
    (90, 100, "0s"), (182, 168, "1.4s"), (150, 78, "2.6s"), (105, 172, "3.8s"),
]
blip_svg = []
for bx, by, delay in blips:
    blip_svg.append(
        f'<circle cx="{bx}" cy="{by}" r="3.5" fill="{RED}" style="animation: blip 6s linear {delay} infinite"/>'
    )
    blip_svg.append(
        f'<circle cx="{bx}" cy="{by}" r="7" fill="none" stroke="{RED}" stroke-opacity="0.6" '
        f'style="animation: ping 6s linear {delay} infinite; transform-box: fill-box; transform-origin: center"/>'
    )
blip_svg = "\n    ".join(blip_svg)

status_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="846" height="250">
  <defs>
    <linearGradient id="sweep" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0.5"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <style>
      @keyframes led {{
        0%, 100% {{ opacity: 1; }}
        50%      {{ opacity: 0.12; }}
      }}
      @keyframes rec {{
        0%, 55%  {{ opacity: 1; }}
        56%, 100% {{ opacity: 0.1; }}
      }}
      @keyframes blip {{
        0%, 100% {{ opacity: 0; }}
        8%       {{ opacity: 1; }}
        30%      {{ opacity: 1; }}
        42%      {{ opacity: 0; }}
      }}
      @keyframes ping {{
        0%   {{ opacity: 0.8; transform: scale(0.6); }}
        30%  {{ opacity: 0; transform: scale(1.6); }}
        100% {{ opacity: 0; transform: scale(1.6); }}
      }}
    </style>
  </defs>
  {frame(W, H)}
  <text x="24" y="32" font-family="{FONT}" font-size="15" fill="{FG}">$ ./status --monitor</text>
  <text x="822" y="32" text-anchor="end" font-family="{FONT}" font-size="13" fill="{RED}"
        style="animation: rec 1.4s steps(1) infinite">● REC</text>
  <rect x="24" y="44" width="{W - 48}" height="1" fill="{GREEN}" opacity="0.35"/>

  <!-- radar -->
  <g>
    <circle cx="130" cy="130" r="85" fill="none" stroke="{GREEN}" stroke-opacity="0.3"/>
    <circle cx="130" cy="130" r="57" fill="none" stroke="{GREEN}" stroke-opacity="0.2"/>
    <circle cx="130" cy="130" r="28" fill="none" stroke="{GREEN}" stroke-opacity="0.15"/>
    <line x1="45" y1="130" x2="215" y2="130" stroke="{GREEN}" stroke-opacity="0.15"/>
    <line x1="130" y1="45" x2="130" y2="215" stroke="{GREEN}" stroke-opacity="0.15"/>
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 130 130" to="360 130 130"
                        dur="3.2s" repeatCount="indefinite"/>
      <path d="M130,130 L130,45 A85,85 0 0 1 203.6,87.5 Z" fill="url(#sweep)"/>
      <line x1="130" y1="130" x2="130" y2="45" stroke="{GREEN}" stroke-opacity="0.95"/>
    </g>
    {blip_svg}
    <text x="130" y="243" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{DIM}">scanning: 4 contacts</text>
  </g>

  <!-- services -->
  {svc_svg}
  <rect x="24" y="228" width="{W - 48}" height="1" fill="{GREEN}" opacity="0.2"/>
  <text x="24" y="242" font-family="{FONT}" font-size="11" fill="{FOOTER}">signal integrity 99.9% · no third-party trackers · stay paranoid</text>
</svg>
"""
with open("status.svg", "w", encoding="utf-8") as f:
    f.write(status_svg)

# ================= badges.svg =================
BW, BH = 846, 132
medals = [
    ("★", "C2 ARCHITECT", "wisp", "1.2s"),
    ("☠", "EXPLOIT ENGINEER", "exim rce", "1.9s"),
    ("◈", "MEMORY WIZARD", "amnis", "0.8s"),
    ("⬡", "BROWSER GHOST", "browseye", "2.7s"),
    ("◆", "HONEYPOT HERDER", "deception", "1.5s"),
    ("✎", "NOVELIST", "fiction", "2.1s"),
]
card_w, card_h, gap = 120, 100, 12
x0 = (BW - (6 * card_w + 5 * gap)) // 2
cards = []
for i, (glyph, name, sub, speed) in enumerate(medals):
    x = x0 + i * (card_w + gap)
    cards.append(
        f'<rect x="{x}" y="16" width="{card_w}" height="{card_h}" rx="8" fill="{DARK}" '
        f'stroke="{GREEN}" stroke-opacity="0.3"/>'
    )
    cards.append(
        f'<circle cx="{x + card_w - 12}" cy="28" r="3" fill="{GREEN}" '
        f'style="animation: led {speed} ease-in-out infinite"/>'
    )
    cards.append(
        f'<text x="{x + card_w // 2}" y="58" text-anchor="middle" '
        f'font-family="DejaVu Sans, Arial, sans-serif" font-size="30" fill="{CYAN}">{glyph}</text>'
    )
    cards.append(
        f'<text x="{x + card_w // 2}" y="80" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" font-weight="bold" letter-spacing="1" fill="{GREEN}">{escape(name)}</text>'
    )
    cards.append(
        f'<text x="{x + card_w // 2}" y="98" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10" fill="{DIM}">{escape(sub)}</text>'
    )
cards = "\n    ".join(cards)

badges_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BW} {BH}" width="846" height="132">
  <defs>
    <style>
      @keyframes led {{
        0%, 100% {{ opacity: 1; }}
        50%      {{ opacity: 0.1; }}
      }}
    </style>
  </defs>
  {frame(BW, BH)}
  {cards}
</svg>
"""
with open("badges.svg", "w", encoding="utf-8") as f:
    f.write(badges_svg)

import os
print(f"status.svg: {os.path.getsize('status.svg') / 1024:.1f} KB")
print(f"badges.svg: {os.path.getsize('badges.svg') / 1024:.1f} KB")
