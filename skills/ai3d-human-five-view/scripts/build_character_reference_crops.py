#!/usr/bin/env python3
"""Build local character feature crops and a contact sheet from a JSON crop spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def load_spec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        spec = json.load(f)
    if not isinstance(spec.get("crops"), list) or not spec["crops"]:
        raise SystemExit("Spec must contain a non-empty 'crops' list.")
    return spec


def clamp_box(box: list[int], width: int, height: int) -> tuple[int, int, int, int]:
    if len(box) != 4:
        raise ValueError("Crop box must have four integers: [left, top, right, bottom].")
    left, top, right, bottom = [int(v) for v in box]
    left = max(0, min(left, width))
    top = max(0, min(top, height))
    right = max(0, min(right, width))
    bottom = max(0, min(bottom, height))
    if right <= left or bottom <= top:
        raise ValueError(f"Invalid crop box after clamping: {[left, top, right, bottom]}")
    return left, top, right, bottom


def resolve_source(photo_dir: Path, source: str) -> Path:
    src_path = photo_dir / source
    if src_path.exists():
        return src_path

    source_path = Path(source)
    stem = source_path.stem
    for candidate in sorted(photo_dir.glob(f"{stem}.*")):
        if candidate.suffix.lower() in IMAGE_SUFFIXES:
            return candidate
    raise FileNotFoundError(f"Missing source image: {src_path}")


def save_crop(photo_dir: Path, out_dir: Path, item: dict[str, Any], max_side: int) -> Path:
    source = item.get("source")
    output = item.get("output")
    box = item.get("box")
    if not source or not output or box is None:
        raise ValueError("Each crop needs 'source', 'output', and 'box'.")

    img = ImageOps.exif_transpose(Image.open(resolve_source(photo_dir, str(source))).convert("RGB"))
    crop = img.crop(clamp_box(box, img.width, img.height))
    if max(crop.size) > max_side:
        crop.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)

    out_path = out_dir / str(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs: dict[str, Any] = {}
    if out_path.suffix.lower() in {".jpg", ".jpeg"}:
        save_kwargs.update({"quality": 92, "optimize": True})
    crop.save(out_path, **save_kwargs)
    return out_path


def make_contact_sheet(out_dir: Path, items: list[dict[str, Any]], sheet_spec: dict[str, Any]) -> Path:
    filename = str(sheet_spec.get("filename", "contact_sheet.jpg"))
    columns = max(1, int(sheet_spec.get("columns", 3)))
    thumb_width = max(120, int(sheet_spec.get("thumb_width", 320)))
    thumb_height = max(120, int(sheet_spec.get("thumb_height", 360)))
    label_height = 50
    rows = (len(items) + columns - 1) // columns

    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "white")
    draw = ImageDraw.Draw(sheet)

    for index, item in enumerate(items):
        out_path = out_dir / str(item["output"])
        img = Image.open(out_path).convert("RGB")
        img.thumbnail((thumb_width - 24, thumb_height - 24), Image.Resampling.LANCZOS)

        col = index % columns
        row = index // columns
        x0 = col * thumb_width
        y0 = row * (thumb_height + label_height)
        x = x0 + (thumb_width - img.width) // 2
        y = y0 + 8 + (thumb_height - img.height) // 2
        sheet.paste(img, (x, y))

        label = str(item.get("label") or out_path.stem)
        source = str(item.get("source") or "")
        draw.text((x0 + 8, y0 + thumb_height + 6), label[:46], fill=(20, 20, 20))
        draw.text((x0 + 8, y0 + thumb_height + 24), source[:46], fill=(80, 80, 80))

    sheet_path = out_dir / filename
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs: dict[str, Any] = {}
    if sheet_path.suffix.lower() in {".jpg", ".jpeg"}:
        save_kwargs.update({"quality": 90, "optimize": True})
    sheet.save(sheet_path, **save_kwargs)
    return sheet_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path, help="JSON crop spec path.")
    parser.add_argument("--photo-dir", required=True, type=Path, help="Directory containing source images.")
    parser.add_argument("--out-dir", required=True, type=Path, help="Directory for generated crops.")
    parser.add_argument("--max-side", type=int, default=900, help="Maximum output crop edge in pixels.")
    args = parser.parse_args()

    spec = load_spec(args.spec)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    crop_items = spec["crops"]
    for item in crop_items:
        save_crop(args.photo_dir, args.out_dir, item, args.max_side)

    sheet = make_contact_sheet(args.out_dir, crop_items, spec.get("contact_sheet", {}))
    print(f"Created {len(crop_items)} crops in {args.out_dir}")
    print(f"Contact sheet: {sheet}")


if __name__ == "__main__":
    main()
