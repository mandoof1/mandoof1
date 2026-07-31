#!/usr/bin/env python3
"""Generate animated matrix/CRT terminal banner.svg for GitHub profile README.
Self-contained SVG, CSS keyframes inside — animates when rendered via <img>.
"""
import random
from html import escape

random.seed(1337)

W, H = 1200, 520
FONT = "Consolas, 'Cascadia Code', 'Fira Code', 'Courier New', monospace"

# ---------------- matrix rain chars ----------------
CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ｱｲｳｴｵｶｷｸｹｺ$#%&*<>/\\"
COLS = 30
COL_W = 38
START_X = 14
rain = []
for c in range(COLS):
    x = START_X + c * COL_W
    n = random.randint(12, 16)
    for i in range(n):
        y0 = -random.randint(10, 140) - i * 24
        dur = round(random.uniform(2.4, 5.2), 2)
        delay = round(random.uniform(0, 6.0), 2)
        ch = random.choice(CHARS)
        bright = random.random() < 0.12
        fill = "#d8ffe8" if bright else "#00ff41"
        op = "0.95" if bright else "0.55"
        rain.append(
            f'<text x="{x}" y="{y0}" font-family="{FONT}" font-size="20" fill="{fill}" '
            f'opacity="{op}" style="animation: fall {dur}s linear -{delay}s infinite">{escape(ch)}</text>'
        )
rain_svg = "\n    ".join(rain)

# ---------------- terminal boot lines ----------------
boot = [
    ("$ ./init.sh --stealth", "#e6edf3"),
    ("[ ok ] kernel modules ................ ok", "#00ff41"),
    ("[ ok ] c2 payloads ................... 3/3", "#00ff41"),
    ("[ ok ] honeypots ..................... 7 traps", "#00ff41"),
    ("[ ok ] media pipeline ................ up", "#00ff41"),
    ("[ ok ] uplink encrypted ............. x25519", "#00ff41"),
    ("[ ok ] memory daemon ................ online", "#00ff41"),
    ("$ whoami", "#e6edf3"),
    ("hadi — security researcher & novelist", "#00d4ff"),
    ("mandoof@matrix:~$", "#00ff41"),
]
LX, LY0, STEP = 206, 322, 20
boot_svg = []
for i, (txt, col) in enumerate(boot):
    delay = round(0.6 + i * 0.55, 2)
    boot_svg.append(
        f'<text x="{LX}" y="{LY0 + i * STEP}" font-family="{FONT}" font-size="15" fill="{col}" '
        f'style="animation: fadein 0.3s ease {delay}s both">{escape(txt)}</text>'
    )
# blinking cursor after the last line
last_y = LY0 + (len(boot) - 1) * STEP
boot_svg.append(
    f'<rect x="{LX + 150}" y="{last_y - 12}" width="9" height="15" fill="#00ff41" '
    f'style="animation: blink 1s steps(1) 5.5s infinite" opacity="0"/>'
)
boot_svg = "\n    ".join(boot_svg)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="1200" height="520">
  <defs>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="2" fill="#000000" opacity="0.22"/>
      <rect y="2" width="4" height="2" fill="#00ff41" opacity="0.035"/>
    </pattern>
    <radialGradient id="vig" cx="50%" cy="42%" r="75%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.55"/>
    </radialGradient>
    <linearGradient id="termbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d1117" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#050a07" stop-opacity="0.95"/>
    </linearGradient>
    <style>
      @keyframes fall {{
        0%   {{ transform: translateY(-70px); opacity: 0; }}
        8%   {{ opacity: 1; }}
        85%  {{ opacity: 0.9; }}
        100% {{ transform: translateY(560px); opacity: 0; }}
      }}
      @keyframes fadein {{
        from {{ opacity: 0; transform: translateY(5px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes blink {{
        0%, 49%   {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes flick {{
        0%, 91.5%  {{ opacity: 1; transform: none; }}
        92%        {{ opacity: 0.15; transform: translateX(3px) skewX(2deg); }}
        93%        {{ opacity: 1; transform: none; }}
        95.5%      {{ opacity: 0.4; transform: translateX(-2px); }}
        96%        {{ opacity: 1; transform: none; }}
      }}
      @keyframes rshift {{
        0%, 90%   {{ opacity: 0; }}
        91%       {{ opacity: 0.75; }}
        92%       {{ opacity: 0; }}
        96%       {{ opacity: 0.5; }}
        97%       {{ opacity: 0; }}
      }}
      @keyframes cshift {{
        0%, 92%   {{ opacity: 0; }}
        93%       {{ opacity: 0.7; }}
        94%       {{ opacity: 0; }}
        97.5%     {{ opacity: 0.45; }}
        98.5%     {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- bg -->
  <rect width="{W}" height="{H}" fill="#040a06"/>

  <!-- matrix rain -->
  {rain_svg}

  <!-- scanlines + vignette -->
  <rect width="{W}" height="{H}" fill="url(#scan)"/>
  <rect width="{W}" height="{H}" fill="url(#vig)"/>

  <!-- glitch title -->
  <g text-anchor="middle">
    <text x="600" y="152" font-family="{FONT}" font-size="110" font-weight="bold" letter-spacing="12"
          fill="#00ff41" filter="url(#glow)" opacity="0.3">MANDOOF</text>
    <text x="597" y="152" font-family="{FONT}" font-size="110" font-weight="bold" letter-spacing="12"
          fill="#ff0055" style="animation: rshift 3.4s linear infinite">MANDOOF</text>
    <text x="603" y="152" font-family="{FONT}" font-size="110" font-weight="bold" letter-spacing="12"
          fill="#00d4ff" style="animation: cshift 3.4s linear infinite">MANDOOF</text>
    <text x="600" y="152" font-family="{FONT}" font-size="110" font-weight="bold" letter-spacing="12"
          fill="#00ff41" style="animation: flick 3.4s linear infinite">MANDOOF</text>
    <text x="600" y="206" font-family="{FONT}" font-size="21" letter-spacing="7" fill="#00d4ff"
          style="animation: fadein 0.8s ease 0.3s both">SECURITY RESEARCHER · NOVELIST · ENCRYPTED EVERYTHING</text>
  </g>

  <!-- terminal window -->
  <g>
    <rect x="180" y="262" width="840" height="226" rx="10" fill="url(#termbg)" stroke="#00ff41" stroke-opacity="0.25"/>
    <rect x="180" y="262" width="840" height="34" rx="10" fill="#0d1117" stroke="#00ff41" stroke-opacity="0.15"/>
    <circle cx="206" cy="279" r="5.5" fill="#ff5f57"/>
    <circle cx="228" cy="279" r="5.5" fill="#febc2e"/>
    <circle cx="250" cy="279" r="5.5" fill="#28c840"/>
    <text x="600" y="284" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#8b949e">root@matrix: ~/profile</text>
    {boot_svg}
  </g>

  <text x="180" y="508" font-family="{FONT}" font-size="12" fill="#3d4f46">gh: mandoof1 · uptime: ∞ · stay paranoid</text>
</svg>
"""

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)

import os
print(f"banner.svg written: {os.path.getsize('banner.svg') / 1024:.1f} KB")
