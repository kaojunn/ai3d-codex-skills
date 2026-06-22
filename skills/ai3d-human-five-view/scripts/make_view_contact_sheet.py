#!/usr/bin/env python3
"""Create a contact sheet for AI3D human or character five-view reference images."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
VIEWS = [
    ("Front", "front"),
    ("Back", "back"),
    ("Left Side", "left_side"),
    ("Right Side", "right_side"),
    ("Top", "top"),
]


def image_candidates(views_dir: Path, prefix: str | None, view: str) -> list[Path]:
    suffix = f"_{view}_view"
    candidates: list[Path] = []
    if prefix:
        candidates.extend(sorted(views_dir.glob(f"{prefix}{suffix}.*")))
    candidates.extend(sorted(views_dir.glob(f"*{suffix}.*")))

    if view == "left_side":
        if prefix:
            candidates.extend(sorted(views_dir.glob(f"{prefix}_left_view.*")))
        candidates.extend(sorted(views_dir.glob("*_left_view.*")))
    elif view == "right_side":
        if prefix:
            candidates.extend(sorted(views_dir.glob(f"{prefix}_right_view.*")))
        candidates.extend(sorted(views_dir.glob("*_right_view.*")))

    seen: set[Path] = set()
    filtered: list[Path] = []
    for path in candidates:
        if path in seen or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        seen.add(path)
        filtered.append(path)
    return filtered


def resolve_view_file(views_dir: Path, prefix: str | None, view: str) -> Path:
    candidates = image_candidates(views_dir, prefix, view)
    if not candidates:
        raise FileNotFoundError(f"Missing image for view '{view}' in {views_dir}")
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--views-dir", required=True, type=Path, help="Directory containing five view images.")
    parser.add_argument("--out", required=True, type=Path, help="Output contact sheet path.")
    parser.add_argument("--prefix", default=None, help="Optional filename prefix, e.g. hero.")
    parser.add_argument("--thumb-width", type=int, default=360)
    parser.add_argument("--thumb-height", type=int, default=500)
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
    save_kwargs = {}
    if args.out.suffix.lower() in {".jpg", ".jpeg"}:
        save_kwargs.update({"quality": 92, "optimize": True})
    sheet.save(args.out, **save_kwargs)
    print(args.out)


if __name__ == "__main__":
    main()
