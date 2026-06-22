#!/usr/bin/env python3
"""Create a contact sheet for AI3D cat five-view reference images."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


VIEWS = [
    ("Front", "front"),
    ("Back", "back"),
    ("Left Side", "left_side"),
    ("Right Side", "right_side"),
    ("Top", "top"),
]


def resolve_view_file(views_dir: Path, prefix: str | None, view: str) -> Path:
    suffix = f"_{view}_view"
    candidates: list[Path] = []
    if prefix:
        candidates.extend(sorted(views_dir.glob(f"{prefix}{suffix}.*")))
    candidates.extend(sorted(views_dir.glob(f"*{suffix}.*")))
    candidates = [p for p in candidates if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
    if not candidates:
        raise FileNotFoundError(f"Missing image for view '{view}' in {views_dir}")
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--views-dir", required=True, type=Path, help="Directory containing five view images.")
    parser.add_argument("--out", required=True, type=Path, help="Output contact sheet path.")
    parser.add_argument("--prefix", default=None, help="Optional filename prefix, e.g. targetcat.")
    parser.add_argument("--thumb-width", type=int, default=340)
    parser.add_argument("--thumb-height", type=int, default=390)
    args = parser.parse_args()

    cols = 3
    rows = 2
    label_h = 34
    sheet = Image.new("RGB", (cols * args.thumb_width, rows * (args.thumb_height + label_h)), "white")
    draw = ImageDraw.Draw(sheet)

    for i, (label, view) in enumerate(VIEWS):
        path = resolve_view_file(args.views_dir, args.prefix, view)
        img = Image.open(path).convert("RGB")
        img.thumbnail((args.thumb_width - 24, args.thumb_height - 24), Image.Resampling.LANCZOS)
        col = i % cols
        row = i // cols
        x0 = col * args.thumb_width
        y0 = row * (args.thumb_height + label_h)
        x = x0 + (args.thumb_width - img.width) // 2
        y = y0 + label_h + (args.thumb_height - img.height) // 2
        draw.text((x0 + 12, y0 + 10), label, fill=(20, 20, 20))
        sheet.paste(img, (x, y))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out, quality=92, optimize=True)
    print(args.out)


if __name__ == "__main__":
    main()
