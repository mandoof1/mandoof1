#!/usr/bin/env python3
"""Generate banner.svg — a clean terminal-style header card for the GitHub profile.

Self-contained animated SVG (CSS keyframes only). Renders when embedded via <img>.
GitHub-native dark palette, no external dependencies.
"""
from html import escape

W = 1200
FONT = "'SFMono-Regular', 'Cascadia Code', 'Fira Code', Consolas, 'Courier New', monospace"
FS = 16
CH = 9.62  # approx monospace advance at FS=16

BG = "#0d1117"
SURFACE = "#161b22"
BORDER = "#30363d"
FG = "#e6edf3"
DIM = "#8b949e"
BLUE = "#58a6ff"
GREEN = "#3fb950"
PURPLE = "#bc8cff"

# (prompt, text, text_color) — None text = blank spacer line
LINES = [
    ("$ ", "whoami", FG),
    (None, "Hadi Abdulrahman — Security Researcher & Software Engineer", FG),
    (None, None, None),
    ("$ ", "cat focus.txt", FG),
    (None, "offensive security · detection engineering · applied ML · systems", DIM),
    (None, None, None),
    ("$ ", "cat status.txt", FG),
    (None, "open to new opportunities", GREEN),
]

LX = 44
TOP = 92
LINE_H = 27
SPACER_H = 14

body = []
y = TOP
last_end_x = LX
delay = 0.4
for prompt, txt, tcol in LINES:
    if txt is None:
        y += SPACER_H
        continue
    seg = (f'<text x="{LX}" y="{y}" xml:space="preserve" font-family="{FONT}" '
           f'font-size="{FS}" style="animation: fadein 0.35s ease {delay:.2f}s both">')
    n = 0
    if prompt:
        seg += f'<tspan fill="{BLUE}">{escape(prompt)}</tspan>'
        n += len(prompt)
    seg += f'<tspan fill="{tcol}">{escape(txt)}</tspan></text>'
    n += len(txt)
    body.append(seg)
    last_end_x = LX + n * CH
    y += LINE_H
    delay += 0.28

cursor_y = y - LINE_H
body.append(
    f'<rect x="{last_end_x + 4:.0f}" y="{cursor_y - 13}" width="9" height="17" fill="{GREEN}" '
    f'style="animation: blink 1.1s steps(1) 2.6s infinite"/>'
)
body = "\n  ".join(body)

H = cursor_y + 58

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Hadi Abdulrahman - Security Researcher and Software Engineer">
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BLUE}"/>
      <stop offset="0.5" stop-color="{PURPLE}"/>
      <stop offset="1" stop-color="{GREEN}"/>
    </linearGradient>
    <style>
      @keyframes fadein {{
        from {{ opacity: 0; transform: translateY(4px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes blink {{
        0%, 49%   {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" rx="12" fill="{BG}"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{BORDER}"/>

  <rect x="1" y="1" width="{W-2}" height="44" rx="12" fill="{SURFACE}"/>
  <rect x="1" y="30" width="{W-2}" height="15" fill="{SURFACE}"/>
  <circle cx="30" cy="23" r="6" fill="#ff5f57"/>
  <circle cx="52" cy="23" r="6" fill="#febc2e"/>
  <circle cx="74" cy="23" r="6" fill="#28c840"/>
  <text x="{W//2}" y="28" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{DIM}">hadi@github: ~/profile</text>
  <rect x="1" y="44" width="{W-2}" height="2" fill="url(#accent)" opacity="0.9"/>

  {body}

  <rect x="{LX}" y="{H-42}" width="{W-2*LX}" height="1" fill="{BORDER}"/>
  <text x="{LX}" y="{H-20}" font-family="{FONT}" font-size="12" fill="{DIM}">github.com/mandoof1</text>
  <text x="{W-LX}" y="{H-20}" text-anchor="end" font-family="{FONT}" font-size="12" fill="{DIM}">building things that hold up</text>
</svg>
"""

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)

import os
print(f"banner.svg: {os.path.getsize('banner.svg') / 1024:.1f} KB  ({W}x{H})")
