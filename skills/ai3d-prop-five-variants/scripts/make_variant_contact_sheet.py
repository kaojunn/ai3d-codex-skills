#!/usr/bin/env python3
"""Create a numeric-order contact sheet for five prop front-view variants."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
VARIANT_IDS = [f"{index:02d}" for index in range(1, 6)]


def resolve_variant(final_dir: Path, prefix: str | None, variant_id: str) -> Path:
    patterns = []
    if prefix:
        patterns.append(f"{prefix}_variant_{variant_id}_front.*")
    patterns.extend(
        [
            f"*_variant_{variant_id}_front.*",
            f"*_variant_{variant_id}.*",
            f"*variant{int(variant_id)}*.*",
        ]
    )
    candidates: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for path in sorted(final_dir.glob(pattern)):
            if path.suffix.lower() in IMAGE_SUFFIXES and path not in seen:
                seen.add(path)
                candidates.append(path)
    if not candidates:
        raise FileNotFoundError(f"Missing variant {variant_id} in {final_dir}")
    if len(candidates) > 1:
        raise RuntimeError(
            f"Multiple files match variant {variant_id}: {', '.join(path.name for path in candidates)}"
        )
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--prefix")
    parser.add_argument("--thumb-width", type=int, default=320)
    parser.add_argument("--thumb-height", type=int, default=420)
    args = parser.parse_args()

    label_h = 42
    sheet = Image.new(
        "RGB",
        (len(VARIANT_IDS) * args.thumb_width, args.thumb_height + label_h),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    for index, variant_id in enumerate(VARIANT_IDS):
        path = resolve_variant(args.final_dir, args.prefix, variant_id)
        image = Image.open(path).convert("RGB")
        image.thumbnail(
            (args.thumb_width - 24, args.thumb_height - 24),
            Image.Resampling.LANCZOS,
        )
        x0 = index * args.thumb_width
        x = x0 + (args.thumb_width - image.width) // 2
        y = label_h + (args.thumb_height - image.height) // 2
        draw.text((x0 + 12, 12), f"Variant {variant_id}", fill=(20, 20, 20))
        sheet.paste(image, (x, y))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {"quality": 92, "optimize": True} if args.out.suffix.lower() in {".jpg", ".jpeg"} else {}
    sheet.save(args.out, **save_kwargs)
    print(args.out)


if __name__ == "__main__":
    main()
