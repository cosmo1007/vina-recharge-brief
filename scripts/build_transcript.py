#!/usr/bin/env python3
"""
Build a styled transcript.html page from the raw .txt transcript.

Input: transcript.txt
Output: transcript.html (writes next to input)

The .txt format alternates between speaker headers and content:
  HH:MM:SS Speaker Name
  content...

Run from the repo root:
  python3 scripts/build_transcript.py
"""

from html import escape
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT = REPO_ROOT / "transcript.txt"
OUTPUT = REPO_ROOT / "transcript.html"

# Match a line that starts with a timestamp like "00:00:02 Speaker Name"
HEADER_RE = re.compile(r"^(\d{2}:\d{2}:\d{2})\s+(.+?)\s*$")


def normalize_speaker(name: str) -> str:
    """Map speaker variants to a canonical name and CSS class."""
    raw = name.strip()
    lower = raw.lower()
    if "valerie kincaid" in lower or "valerie" == lower:
        return ("Valerie Kincaid, GSA General Counsel", "speaker-counsel")
    if "christina buck" in lower or lower == "christina":
        return ("Christina Buck, Butte County DWRC", "speaker-staff")
    if "susan" in lower:
        return ("Susan Schraeder", "speaker-public")
    if "cheetah" in lower:
        return ("Cheetah Tchudi", "speaker-public")
    if "jim graydon" in lower or lower.startswith("jim"):
        return ("Jim Graydon", "speaker-public")
    if "tod" in lower or "todd" in lower:
        return ("Tod Kimmelshue", "speaker-public")
    if "patrizia" in lower or "patricia" in lower:
        return ("Patrizia Hironimus", "speaker-public")
    if "ronald" in lower:
        return ("Ronald", "speaker-public")
    return (raw, "speaker-public")


def parse(text: str):
    """Yield (timestamp, speaker_name, speaker_class, content) tuples."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        m = HEADER_RE.match(line)
        if m:
            timestamp, raw_speaker = m.group(1), m.group(2)
            speaker_name, speaker_class = normalize_speaker(raw_speaker)
            content_lines = []
            j = i + 1
            while j < len(lines):
                nxt = lines[j].strip()
                if not nxt:
                    j += 1
                    continue
                if HEADER_RE.match(nxt):
                    break
                content_lines.append(nxt)
                j += 1
            content = " ".join(content_lines).strip()
            if content:
                yield timestamp, speaker_name, speaker_class, content
            i = j
        else:
            i += 1


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Transcript — Vina GSA Recharge Legal Framework Webinar, May 8, 2026</title>
<meta name="description" content="Verbatim transcript of the May 8, 2026 Vina GSA webinar on the legal framework for groundwater recharge projects.">

<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Vina Recharge Rules — Landowner Brief">
<meta property="og:title" content="Transcript · Vina GSA Recharge Webinar, May 8, 2026">
<meta property="og:description" content="Verbatim transcript of GSA General Counsel Valerie Kincaid's framework for groundwater recharge in the Vina Subbasin.">
<meta property="og:url" content="https://cosmo1007.github.io/vina-recharge-brief/transcript.html">
<meta property="og:image" content="https://cosmo1007.github.io/vina-recharge-brief/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Transcript · Vina GSA Recharge Webinar, May 8, 2026">
<meta name="twitter:description" content="Verbatim transcript of GSA General Counsel Valerie Kincaid's framework for groundwater recharge in the Vina Subbasin.">
<meta name="twitter:image" content="https://cosmo1007.github.io/vina-recharge-brief/og-image.png">
<style>
  :root {{
    --navy: #1a2b4a;
    --teal: #2d6e8c;
    --sage: #3a6b4a;
    --gray-line: #d0d0c8;
    --gray-mute: #8a8a82;
    --bg: #fafaf6;
    --ink: #1f2330;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{
    margin: 0;
    padding: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.5;
  }}
  .page {{
    max-width: 42em;
    margin: 0 auto;
    padding: 2rem 1.25rem 4rem 1.25rem;
  }}
  .nav {{
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1.5rem;
  }}
  .nav a {{
    color: var(--teal);
    text-decoration: none;
    border-bottom: 1px solid var(--gray-line);
    padding-bottom: 1px;
  }}
  .nav a:hover {{ color: var(--navy); border-color: var(--navy); }}
  header.doc {{
    border-bottom: 3px solid var(--navy);
    padding-bottom: 0.75rem;
    margin-bottom: 1.5rem;
  }}
  .eyebrow {{
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 9pt;
    color: var(--teal);
    font-weight: 600;
  }}
  h1 {{
    font-size: 22pt;
    color: var(--navy);
    margin: 4px 0 6px 0;
    line-height: 1.18;
    letter-spacing: -0.01em;
  }}
  .doc-meta {{
    font-size: 10.5pt;
    color: var(--gray-mute);
  }}
  .preamble {{
    background: white;
    border: 1px solid var(--gray-line);
    border-left: 4px solid var(--teal);
    padding: 0.9rem 1rem;
    margin-bottom: 2rem;
    font-size: 10pt;
    color: #2a2f3d;
    border-radius: 3px;
  }}
  .turn {{
    margin: 0 0 1.1rem 0;
    padding-left: 0.75rem;
    border-left: 3px solid var(--gray-line);
  }}
  .turn .meta {{
    font-size: 9pt;
    margin-bottom: 0.15rem;
  }}
  .turn .timestamp {{
    color: var(--gray-mute);
    font-variant-numeric: tabular-nums;
    margin-right: 0.5rem;
  }}
  .turn .speaker {{
    font-weight: 700;
    color: var(--navy);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 9pt;
  }}
  .turn.speaker-counsel {{ border-left-color: var(--navy); }}
  .turn.speaker-counsel .speaker {{ color: var(--navy); }}
  .turn.speaker-staff {{ border-left-color: var(--teal); }}
  .turn.speaker-staff .speaker {{ color: var(--teal); }}
  .turn.speaker-public {{ border-left-color: var(--sage); }}
  .turn.speaker-public .speaker {{ color: var(--sage); }}
  .turn p {{
    margin: 0;
    font-size: 10.5pt;
    color: #1f2330;
  }}
  footer {{
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--gray-line);
    font-size: 9pt;
    color: var(--gray-mute);
  }}
</style>
</head>
<body>
<div class="page">
  <div class="nav"><a href="index.html">&larr; Back to Landowner Brief</a></div>

  <header class="doc">
    <div class="eyebrow">Verbatim Transcript · Vina Subbasin</div>
    <h1>Vina GSA Recharge Legal Framework Webinar</h1>
    <div class="doc-meta">May 8, 2026 · GSA General Counsel Valerie Kincaid · Facilitator: Christina Buck, Butte County DWRC</div>
  </header>

  <div class="preamble">
    Auto-generated transcript from the public webinar Zoom recording. Light cleanup of speaker labels; spoken language preserved as captured. Obvious transcription artifacts (e.g., &ldquo;Sigma&rdquo; for &ldquo;SGMA&rdquo;, &ldquo;service water&rdquo; for &ldquo;surface water&rdquo;) have not been corrected here &mdash; for cleaned, citable excerpts, see the Landowner Brief.
  </div>

  <div class="turns">
{turns}
  </div>

  <footer>
    Source: Vina GSA public webinar, May 8, 2026 &middot; Transcript captured via Zoom auto-caption
  </footer>
</div>
</body>
</html>
"""


def render(turns):
    blocks = []
    for ts, speaker, klass, content in turns:
        blocks.append(
            f'    <div class="turn {klass}">\n'
            f'      <div class="meta"><span class="timestamp">{escape(ts)}</span><span class="speaker">{escape(speaker)}</span></div>\n'
            f'      <p>{escape(content)}</p>\n'
            f'    </div>'
        )
    return "\n".join(blocks)


def main():
    text = INPUT.read_text(encoding="utf-8")
    turns = list(parse(text))
    html = HTML_TEMPLATE.format(turns=render(turns))
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(turns)} turns)")


if __name__ == "__main__":
    main()
