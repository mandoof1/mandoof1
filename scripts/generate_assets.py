#!/usr/bin/env python3
"""Render the profile's original SVG artwork. Standard library only; no network.

Run from any directory: python scripts/generate_assets.py
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BG = "#0b1118"
SURFACE = "#101a24"
BORDER = "#253440"
WHITE = "#f1f5ec"
MUTED = "#a8b7c4"
LIME = "#c5f277"
CYAN = "#78dce8"
SANS = "Arial, Helvetica, sans-serif"
MONO = "'Courier New', monospace"


def text(x, y, value, size=20, color=WHITE, weight=400, mono=False, **attrs):
    attrs = " ".join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in attrs.items())
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO if mono else SANS}" '
            f'font-size="{size}" font-weight="{weight}" {attrs}>{escape(value)}</text>')


def svg(width, height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
{body}
</svg>
'''


def hero():
    parts = [f'''
<defs>
  <radialGradient id="glow" cx="78%" cy="38%" r="65%">
    <stop offset="0" stop-color="#1c3540"/><stop offset="1" stop-color="{BG}"/>
  </radialGradient>
  <pattern id="grid" width="38" height="38" patternUnits="userSpaceOnUse">
    <path d="M 38 0 L 0 0 0 38" fill="none" stroke="#91b9be" stroke-opacity=".07"/>
  </pattern>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
    <stop stop-color="{LIME}"/><stop offset="1" stop-color="{CYAN}"/>
  </linearGradient>
</defs>
<rect width="1280" height="480" rx="24" fill="url(#glow)"/>
<rect x="1" y="1" width="1278" height="478" rx="23" fill="none" stroke="{BORDER}"/>
<path d="M 780 1 H 1256 Q 1279 1 1279 24 V 456 Q 1279 479 1256 479 H 780 Z" fill="url(#grid)"/>
<path d="M 48 45 H 76" stroke="{LIME}" stroke-width="3"/>
''', text(90, 51, "MANDOOF1  /  ENGINEERING & RESEARCH", 16, LIME, mono=True, letter_spacing="1.6"),
        text(48, 153, "Hadi", 82, WHITE, 700, letter_spacing="-4"),
        text(44, 242, "Abdulrahman.", 82, WHITE, 700, letter_spacing="-4"),
        text(48, 300, "Security research. Intelligent systems.", 28, WHITE),
        text(48, 339, "From adversarial thinking to working software.", 21, MUTED),
        f'<path d="M 48 390 H 1232" stroke="{BORDER}"/>',
        text(48, 435, "01 / SECURITY", 16, LIME, mono=True),
        text(290, 435, "02 / APPLIED AI", 16, CYAN, mono=True),
        text(550, 435, "03 / SYSTEMS", 16, MUTED, mono=True),
        text(1232, 435, "BUILD · BREAK · UNDERSTAND", 14, MUTED, mono=True, text_anchor="end"),
        f'''
<g transform="translate(1000 204)">
  <circle r="153" fill="none" stroke="{BORDER}"/>
  <circle r="122" fill="none" stroke="{BORDER}" stroke-dasharray="2 12"/>
  <path d="M -153 0 H -174 M 153 0 H 174 M 0 -153 V -174 M 0 153 V 174" stroke="#4a626e"/>
  <path d="M 0 -153 A 153 153 0 0 1 153 0" fill="none" stroke="{CYAN}" stroke-width="2"/>
  <path d="M 0 -92 L 82 -46 V 46 L 0 92 L -82 46 V -46 Z" fill="#12252c" stroke="url(#edge)" stroke-width="2.5"/>
  <path d="M 0 0 L -82 -46 M 0 0 L 82 -46 M 0 0 V 92 M 0 -92 V 0" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
  <path d="M -82 46 L 0 0 L 82 46" fill="none" stroke="{CYAN}" stroke-opacity=".3" stroke-dasharray="4 6"/>
  <circle r="7" fill="{LIME}"/>
  <circle cx="-82" cy="-46" r="4" fill="{LIME}"/>
  <circle cx="82" cy="46" r="4" fill="{CYAN}"/>
  <circle cy="-153" r="5" fill="{CYAN}"/>
  <circle cx="-132.5" cy="76.5" r="5" fill="{LIME}"/>
</g>''']
    (ROOT / "banner.svg").write_text(svg(1280, 480, "Hadi Abdulrahman — cybersecurity engineering student",
        "Security research. Intelligent systems. From adversarial thinking to working software. Security, applied AI, and systems.", "\n".join(parts)), encoding="utf-8")


PROJECTS = [
    ("honeysentinel", "01", "DETECTION & DEFENSE", "HoneySentinel AI", LIME,
     ["Capture the interaction.", "Investigate the behavior."], "HONEYPOTS  /  LOCAL ML  /  ATT&CK", "shield"),
    ("amnis", "02", "AGENT INFRASTRUCTURE", "Amnis", CYAN,
     ["Long-term memory for agents.", "Knowledge that survives the session."], "MCP  /  HYBRID RAG  /  KNOWLEDGE GRAPH", "nodes"),
    ("wisp", "03", "OFFENSIVE SECURITY", "Wisp", CYAN,
     ["A lightweight encrypted C2.", "Go implant. Python control plane."], "GO  /  PYTHON  /  X25519", "signal"),
    ("chimera", "04", "SECURITY × MACHINE LEARNING", "Chimera 14B v2", LIME,
     ["Fine-tuned for security reasoning.", "ATT&CK-aware blue-team analysis."], "MINISTRAL 3 14B  /  LORA  /  REASONING", "model"),
]


def icon(kind, color):
    shapes = {
        "shield": '<path d="M 0 -25 L 22 -16 V 3 Q 22 20 0 31 Q -22 20 -22 3 V -16 Z"/><path d="M -10 2 L -2 10 L 13 -7"/>',
        "nodes": '<path d="M -22 13 L 0 -19 L 24 13 Z M 0 -19 V 27 M -22 13 L 0 27 L 24 13"/><circle cy="-19" r="5"/><circle cx="-22" cy="13" r="5"/><circle cx="24" cy="13" r="5"/><circle cy="27" r="5"/>',
        "signal": '<path d="M -27 10 Q 0 -24 27 10 M -19 18 Q 0 -7 19 18 M -10 26 Q 0 13 10 26"/><circle cy="32" r="2"/>',
        "model": '<path d="M 0 -25 L 25 -11 V 17 L 0 31 L -25 17 V -11 Z M -25 -11 L 0 3 L 25 -11 M 0 3 V 31 M -13 -18 L 13 -4 V 24 M 13 -18 L -13 -4 V 24"/>',
    }
    return f'<g transform="translate(526 92)" stroke="{color}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">{shapes[kind]}</g>'


def cards():
    for slug, number, category, title, accent, lines, tags, kind in PROJECTS:
        body = [f'''
<rect x="1" y="1" width="598" height="286" rx="18" fill="{SURFACE}" stroke="{BORDER}"/>
<path d="M 32 1 H 100" stroke="{accent}" stroke-width="3"/>
<circle cx="526" cy="92" r="45" fill="{accent}" fill-opacity=".045"/>
''', text(32, 43, f"{number} / {category}", 14, accent, mono=True, letter_spacing=".6"),
            text(30, 108, title, 37, WHITE, 700, letter_spacing="-1"),
            text(32, 155, lines[0], 21, MUTED),
            text(32, 185, lines[1], 21, MUTED),
            f'<path d="M 32 216 H 568" stroke="{BORDER}"/>',
            text(32, 252, tags, 13, accent, mono=True),
            f'<path d="M 547 247 H 566 M 559 240 L 566 247 L 559 254" stroke="{accent}" stroke-width="2" fill="none"/>',
            icon(kind, accent)]
        (ROOT / "assets" / f"{slug}.svg").write_text(svg(600, 288, title, "; ".join([category, *lines, tags]), "\n".join(body)), encoding="utf-8")


def footer():
    body = f'''
<rect width="1280" height="152" rx="18" fill="{BG}"/>
<rect x="1" y="1" width="1278" height="150" rx="17" fill="none" stroke="{BORDER}"/>
<path d="M 42 50 V 103" stroke="{LIME}" stroke-width="3"/>
{text(65, 64, "HAVE SOMETHING INTERESTING IN MIND?", 16, LIME, mono=True, letter_spacing="1.5")}
{text(63, 108, "Let's build it.", 32, WHITE, 700)}
{text(1205, 89, "haadii2005@gmail.com", 25, WHITE, text_anchor="end")}
<path d="M 1223 79 H 1242 M 1235 72 L 1242 79 L 1235 86" stroke="{LIME}" stroke-width="2" fill="none"/>
'''
    (ROOT / "assets" / "contact.svg").write_text(svg(1280, 152, "Let's build it — haadii2005@gmail.com", "Contact Hadi Abdulrahman to discuss engineering, security research, or collaboration.", body), encoding="utf-8")


def mobile():
    body = f'''
<rect width="640" height="510" rx="20" fill="{BG}"/>
<rect x="1" y="1" width="638" height="508" rx="19" fill="none" stroke="{BORDER}"/>
<circle cx="552" cy="62" r="20" fill="none" stroke="{CYAN}"/>
<path d="M 540 62 H 564 M 552 50 V 74" stroke="{LIME}"/>
{text(32, 68, "MANDOOF1 / ENGINEERING", 19, LIME, mono=True, letter_spacing="1")}
{text(30, 178, "Hadi", 76, WHITE, 700, letter_spacing="-3")}
{text(28, 257, "Abdulrahman.", 68, WHITE, 700, letter_spacing="-3")}
{text(32, 327, "Security research.", 32, WHITE)}
{text(32, 371, "Intelligent systems.", 32, WHITE)}
<path d="M 32 420 H 608" stroke="{BORDER}"/>
{text(32, 464, "SECURITY / APPLIED AI / SYSTEMS", 20, MUTED, mono=True)}
'''
    (ROOT / "assets" / "banner-mobile.svg").write_text(svg(640, 510, "Hadi Abdulrahman", "Security research. Intelligent systems.", body), encoding="utf-8")
    body = f'''
<rect width="640" height="230" rx="20" fill="{BG}"/>
<rect x="1" y="1" width="638" height="228" rx="19" fill="none" stroke="{BORDER}"/>
{text(32, 53, "SOMETHING INTERESTING IN MIND?", 19, LIME, mono=True)}
{text(30, 119, "Let's build it.", 44, WHITE, 700)}
{text(32, 180, "haadii2005@gmail.com", 29, WHITE)}
<path d="M 550 170 H 590 M 577 157 L 590 170 L 577 183" stroke="{LIME}" stroke-width="3" fill="none"/>
'''
    (ROOT / "assets" / "contact-mobile.svg").write_text(svg(640, 230, "Let's build it", "Email haadii2005@gmail.com", body), encoding="utf-8")


if __name__ == "__main__":
    (ROOT / "assets").mkdir(exist_ok=True)
    hero()
    cards()
    footer()
    mobile()
    print("Generated banner.svg and seven assets/*.svg files.")
