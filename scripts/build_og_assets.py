#!/usr/bin/env python3
"""
Generate static branding assets:
  - og-image.png  (1200 x 630)  for link previews on Slack/iMessage/Twitter
  - favicon.png   (32 x 32)     for browser tabs
  - apple-touch-icon.png (180 x 180) for iOS home-screen / link previews

Run from the repo root:
  python3 scripts/build_og_assets.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent

# Brand
NAVY = (26, 43, 74)
TEAL = (45, 110, 140)
SAGE = (58, 107, 74)
GRAY_OUT = (138, 138, 130)
WHITE = (250, 250, 246)
WHITE_DIM = (200, 205, 215)

HELVETICA = "/System/Library/Fonts/HelveticaNeue.ttc"


def font(size, weight="bold"):
    # Verified HelveticaNeue.ttc indices on macOS:
    # 0=Regular, 1=Bold, 2=Italic, 3=Bold Italic, 4=Condensed Bold,
    # 5=UltraLight, 7=Light, 9=Condensed Black, 10=Medium, 12=Thin
    idx = {"bold": 1, "medium": 10, "regular": 0}.get(weight, 0)
    return ImageFont.truetype(HELVETICA, size, index=idx)


def build_og_image() -> Path:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Top horizontal accent band
    d.rectangle([(0, 0), (W, 6)], fill=TEAL)

    # Eyebrow
    eyebrow = "LANDOWNER BRIEF  ·  VINA SUBBASIN"
    d.text((80, 100), eyebrow, fill=TEAL, font=font(22, "bold"))

    # Title (two lines)
    d.text((80, 150), "Recharge Rules:", fill=WHITE, font=font(78, "bold"))
    d.text((80, 240), "What's Coming", fill=WHITE, font=font(78, "bold"))

    # Subtitle (two lines, kept clear of the bars on the right)
    d.text((80, 360), "May 8, 2026 Vina GSA webinar", fill=WHITE_DIM, font=font(24, "medium"))
    d.text((80, 396), "GSA General Counsel Valerie Kincaid", fill=WHITE_DIM, font=font(24, "regular"))

    # Right-side visual: four-path ladder mark
    # Bars: 1 (out), 2 (in), 3 (in), 4 (out)
    bar_x = 820
    bar_y = 130
    bar_w = 64
    bar_gap = 28
    bar_h_out = 200
    bar_h_in = 280

    layout = [
        (GRAY_OUT, bar_h_out, "1"),
        (SAGE, bar_h_in, "2"),
        (SAGE, bar_h_in, "3"),
        (GRAY_OUT, bar_h_out, "4"),
    ]

    for i, (color, h, label) in enumerate(layout):
        x0 = bar_x + i * (bar_w + bar_gap)
        y0 = bar_y + (bar_h_in - h)
        x1 = x0 + bar_w
        y1 = y0 + h
        d.rounded_rectangle([(x0, y0), (x1, y1)], radius=6, fill=color)
        # Path number
        label_font = font(28, "bold")
        # measure for centering
        bbox = d.textbbox((0, 0), label, font=label_font)
        tw = bbox[2] - bbox[0]
        d.text(
            (x0 + (bar_w - tw) / 2, y1 + 12),
            label,
            fill=WHITE if color == SAGE else WHITE_DIM,
            font=label_font,
        )

    # Caption under bars
    cap = "4 PATHS  ·  2 LIKELY"
    d.text((bar_x, bar_y + bar_h_in + 80), cap, fill=WHITE_DIM, font=font(18, "bold"))

    # Footer URL
    d.text((80, 540), "cosmo1007.github.io/vina-recharge-brief", fill=TEAL, font=font(20, "medium"))

    out = REPO_ROOT / "og-image.png"
    img.save(out, "PNG", optimize=True)
    return out


def build_favicon(size: int, filename: str) -> Path:
    img = Image.new("RGB", (size, size), NAVY)
    d = ImageDraw.Draw(img)

    # Four small vertical bars echoing the path ladder
    # Total width budget ~ 60% of size, centered
    pad = size * 0.18
    inner_w = size - 2 * pad
    bar_count = 4
    gap = inner_w * 0.12
    bar_w = (inner_w - 3 * gap) / bar_count
    base_y = size - pad
    h_out = inner_w * 0.45
    h_in = inner_w * 0.65

    heights = [h_out, h_in, h_in, h_out]
    colors = [GRAY_OUT, SAGE, SAGE, GRAY_OUT]

    for i in range(bar_count):
        x0 = pad + i * (bar_w + gap)
        x1 = x0 + bar_w
        y0 = base_y - heights[i]
        y1 = base_y
        radius = max(1, int(bar_w * 0.18))
        d.rounded_rectangle([(x0, y0), (x1, y1)], radius=radius, fill=colors[i])

    out = REPO_ROOT / filename
    img.save(out, "PNG", optimize=True)
    return out


def main():
    paths = [
        build_og_image(),
        build_favicon(32, "favicon.png"),
        build_favicon(180, "apple-touch-icon.png"),
    ]
    for p in paths:
        print(f"Wrote {p.name}  ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
