# Profile settings

Companion settings for the GitHub profile. These are suggested values; account
settings and repository pins are managed separately from the profile README.

**Name:** Hadi Abdulrahman

**Bio:** Cybersecurity engineering student building security tools, AI agents, and fine-tuned models. Open to internships & entry-level roles. Open source. Self-hosted.

**Public contact:** haadii2005@gmail.com

**Website:** https://github.com/mandoof1#selected-work

**Availability:** Open to cybersecurity internships and entry-level roles.

**Additional research:** `aegis` (agent security benchmarking) and `abliteration` (refusal-ablation research).

**Suggested repository pins, in order:**

1. `honeypot-ui` — HoneySentinel AI: honeypots, local ML, and an investigation workspace.
2. `amnis` — Persistent memory, hybrid RAG, and knowledge graphs for AI agents.
3. `wisp` — Lightweight encrypted C2 with a Go implant and Python server.
4. `chimera-14b-v2` — ATT&CK-aware security reasoning LoRA for Ministral 3 14B.
5. `aether` — A local-first desktop AI agent.
6. `browseye` — Firefox automation and browser control over WebSocket.

## Maintaining the design

- Run `python scripts/generate_assets.py` to regenerate the banner, project cards,
  and contact panel. The generator uses only Python's standard library.
- Run `python gen_stats.py` to refresh the public statistics when connected to
  GitHub. `GITHUB_TOKEN` is optional locally and provided by the scheduled Action.
- Run `python gen_stats.py --offline` to redraw the last recorded snapshot in
  `assets/stats.json` without changing its collection date.
- The stats card states the date of the data and counts public, owned,
  non-fork repositories. Language shares are by source bytes, not proficiency.
- The stats and contribution animation refresh through the existing workflows.
- All main artwork is served from this repository. The main profile has no
  dependency on badge servers, externally rendered cards, or custom CSS.
