# Vina Recharge Rules — Landowner Brief

A one-page interactive brief for Vina Subbasin landowners on the legal framework
the Vina GSA is building for groundwater recharge projects. Based on the May 8,
2026 public webinar with GSA General Counsel Valerie Kincaid (facilitated by
Christina Buck, Butte County DWRC).

**Live site:** <https://cosmo1007.github.io/vina-recharge-brief/>

## What's here

- `index.html` — the brief. Click any path or term box to read counsel's
  verbatim comments from the webinar.
- `transcript.html` — full styled transcript of the webinar, generated from
  `transcript.txt`.
- `transcript.txt` — raw transcript captured via Zoom auto-caption.
- `scripts/build_transcript.py` — regenerates `transcript.html` from
  `transcript.txt`. Run from the repo root: `python3 scripts/build_transcript.py`

## Quoting conventions in the brief

Quotes pulled from the transcript are verbatim, with two exceptions noted in
the text:

- `[bracketed]` — single-word substitution where the auto-transcript was
  garbled (e.g., `[role]` for &ldquo;rule for buy-in&rdquo;).
- `[...]` — material omitted between kept sentences.

Obvious transcription artifacts (&ldquo;Sigma&rdquo; &rarr; SGMA, &ldquo;service water&rdquo; &rarr;
surface water, &ldquo;researcher&rdquo; &rarr; recharger) are silently corrected in the
brief but preserved in `transcript.html`.

## Updating the brief

Edit `index.html` directly. The page is a single self-contained file
(HTML + CSS + a small vanilla-JS expand/collapse script) — no build step.

To regenerate the transcript page after editing `transcript.txt`:

```bash
python3 scripts/build_transcript.py
```

## Author

Tovey Giezentanner &middot; AGUBC representative and Vina GSA advisor &middot;
[tovey@giezentanner.com](mailto:tovey@giezentanner.com)
