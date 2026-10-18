# Profile settings

Companion account settings for the profile. Publishing this repository updates
its README; the bio and pins are separate GitHub account settings.

**Name:** Hadi Abdulrahman

**Bio:** Cybersecurity engineering student. Building HoneySentinel, Wolfram, and tools for secure AI systems. Open to internships and entry-level roles.

**Public contact:** haadii2005@gmail.com

**Website:** https://github.com/mandoof1#flagship-work

**Repository pins, in order:**

1. `honeypot-ui` — HoneySentinel AI: protocol emulation, local analysis, and an investigation workspace.
2. `wolfram` — The final evolution of Chimera: a security model integrated into HoneySentinel.
3. `amnis` — Persistent memory, hybrid RAG, and knowledge graphs for AI agents.
4. `aegis` — Attack and defense evaluation for tool-using agents.
5. `abliteration` — Training-free model editing for hybrid-attention architectures.

The main showcase intentionally contains only these five projects. Wolfram
represents the Chimera lineage; the older model versions are not separate
featured projects.

## Maintaining the artwork

Run `python scripts/generate_assets.py` from the repository root. The generator
uses only the Python standard library and writes 22 self-contained SVG assets,
plus `banner.svg` as a stable fallback for earlier links.

- Every panel has light and dark variants.
- The hero, flagship case studies, and contact panel have separate mobile layouts.
- The three research cards wrap naturally at narrower widths.
- GitHub's native Markdown supplies the readable descriptions and links.
- Artwork is original vector geometry; it has no external fonts, scripts, or
  runtime image-service dependencies.

The existing standalone stats card and contribution workflow remain available,
but the profile leads with projects and evidence rather than activity widgets.

## Content sources

- HoneySentinel: repository README, deployment instructions, evaluation notes,
  and `backend/app/ai/llm.py` for the Wolfram integration.
- Wolfram: the local final adapter configuration, fine-tuning and benchmark code,
  HoneySentinel's integration, and the owner's designation as Chimera's final version.
- Amnis, Aegis, and Abliteration: their respective repository READMEs.

Benchmark scores are left in the project reports, where the datasets, methods,
and scope can be explained alongside the results.
