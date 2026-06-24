#!/usr/bin/env python3
"""Build local prop feature crops and a contact sheet from a JSON crop spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


def load_spec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    if not isinstance(spec.get("crops"), list) or not spec["crops"]:
        raise SystemExit("Spec must contain a non-empty 'crops' list.")
    return spec


def clamp_box(box: list[int], width: int, height: int) -> tuple[int, int, int, int]:
    if len(box) != 4:
        raise ValueError("Crop box must be [left, top, right, bottom].")
    left, top, right, bottom = [int(value) for value in box]
    left, top = max(0, min(left, width)), max(0, min(top, height))
    right, bottom = max(0, min(right, width)), max(0, min(bottom, height))
    if right <= left or bottom <= top:
        raise ValueError(f"Invalid crop box after clamping: {[left, top, right, bottom]}")
    return left, top, right, bottom


def save_crop(photo_dir: Path, out_dir: Path, item: dict[str, Any], max_side: int) -> Path:
    source = photo_dir / str(item["source"])
    if not source.is_file():
        raise FileNotFoundError(f"Missing source image: {source}")
    image = ImageOps.exif_transpose(Image.open(source).convert("RGB"))
    crop = image.crop(clamp_box(item["box"], image.width, image.height))
    if max(crop.size) > max_side:
        crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    output = out_dir / str(item["output"])
    output.parent.mkdir(parents=True, exist_ok=True)
    crop.save(output, quality=92 if output.suffix.lower() in {".jpg", ".jpeg"} else None)
    return output


def make_contact_sheet(out_dir: Path, items: list[dict[str, Any]], spec: dict[str, Any]) -> Path:
    columns = max(1, int(spec.get("columns", 3)))
    thumb_w = max(120, int(spec.get("thumb_width", 320)))
    thumb_h = max(120, int(spec.get("thumb_height", 320)))
    label_h = 54
    rows = (len(items) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, item in enumerate(items):
        image = Image.open(out_dir / str(item["output"])).convert("RGB")
        image.thumbnail((thumb_w - 24, thumb_h - 24), Image.Resampling.LANCZOS)
        col, row = index % columns, index // columns
        x0, y0 = col * thumb_w, row * (thumb_h + label_h)
        x = x0 + (thumb_w - image.width) // 2
        y = y0 + (thumb_h - image.height) // 2
        sheet.paste(image, (x, y))
        draw.text((x0 + 8, y0 + thumb_h + 7), str(item.get("label", ""))[:48], fill=(20, 20, 20))
        draw.text((x0 + 8, y0 + thumb_h + 27), str(item.get("source", ""))[:48], fill=(80, 80, 80))
    output = out_dir / str(spec.get("filename", "contact_sheet.jpg"))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=90 if output.suffix.lower() in {".jpg", ".jpeg"} else None)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--photo-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--max-side", type=int, default=900)
    args = parser.parse_args()

    spec = load_spec(args.spec)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for item in spec["crops"]:
        save_crop(args.photo_dir, args.out_dir, item, args.max_side)
    sheet = make_contact_sheet(args.out_dir, spec["crops"], spec.get("contact_sheet", {}))
    print(f"Created {len(spec['crops'])} crops in {args.out_dir}")
    print(f"Contact sheet: {sheet}")


if __name__ == "__main__":
    main()
