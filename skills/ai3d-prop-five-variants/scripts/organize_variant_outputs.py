#!/usr/bin/env python3
"""Organize five AI3D prop front-view variants and support artifacts."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
VARIANT_IDS = [f"{index:02d}" for index in range(1, 6)]


def normalized_stem(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_")


def detect_variant(path: Path) -> str | None:
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        return None
    match = re.search(r"(?:^|_)variant_?0?([1-5])(?:_|$)", normalized_stem(path))
    return f"{int(match.group(1)):02d}" if match else None


def parse_explicit(values: list[str], source_dir: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--variant must use ID=PATH, for example --variant 01=image.png")
        raw_id, raw_path = value.split("=", 1)
        variant_id = f"{int(raw_id):02d}"
        if variant_id not in VARIANT_IDS:
            raise ValueError(f"Variant ID must be 01-05, got {raw_id}")
        if variant_id in result:
            raise ValueError(f"Duplicate explicit mapping for variant {variant_id}")
        path = Path(raw_path)
        if not path.is_absolute():
            path = source_dir / path
        path = path.resolve()
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            raise FileNotFoundError(f"Invalid variant image: {path}")
        result[variant_id] = path
    return result


def is_inside(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


def unique_target(path: Path, overwrite: bool) -> Path:
    if overwrite or not path.exists():
        return path
    for index in range(2, 1000):
        candidate = path.with_name(f"{path.stem}_v{index:02d}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not create a unique target for {path}")


def transfer(src: Path, dst: Path, mode: str, overwrite: bool, dry_run: bool) -> Path:
    destination = unique_target(dst, overwrite)
    if dry_run or src.resolve() == destination.resolve():
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "copy":
        shutil.copy2(src, destination)
    else:
        shutil.move(str(src), str(destination))
    return destination


def load_variation_plan(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    with path.open("r", encoding="utf-8") as handle:
        plan = json.load(handle)
    ids = [str(item.get("id", "")).zfill(2) for item in plan.get("variants", [])]
    if ids != VARIANT_IDS:
        raise ValueError("Variation plan must contain variants 01-05 exactly once in numeric order.")
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--final-dir", required=True, type=Path)
    parser.add_argument("--support-dir", required=True, type=Path)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--variation-plan", type=Path)
    parser.add_argument("--variant", action="append", default=[], help="Explicit ID=PATH mapping.")
    parser.add_argument("--mode", choices=["copy", "move"], default="copy")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    final_dir = args.final_dir.resolve()
    support_dir = args.support_dir.resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"Missing source directory: {source_dir}")

    explicit = parse_explicit(args.variant, source_dir)
    iterator = source_dir.rglob("*") if args.recursive else source_dir.iterdir()
    source_files = sorted(
        path.resolve()
        for path in iterator
        if path.is_file()
        and not is_inside(path, final_dir)
        and not is_inside(path, support_dir)
    )

    detected: dict[str, list[Path]] = {variant_id: [] for variant_id in VARIANT_IDS}
    explicit_paths = set(explicit.values())
    for path in source_files:
        if path in explicit_paths:
            continue
        variant_id = detect_variant(path)
        if variant_id and variant_id not in explicit:
            detected[variant_id].append(path)

    duplicates = {variant_id: paths for variant_id, paths in detected.items() if len(paths) > 1}
    if duplicates:
        details = "; ".join(
            f"{variant_id}: {', '.join(path.name for path in paths)}"
            for variant_id, paths in duplicates.items()
        )
        raise SystemExit(f"Duplicate variant candidates found. Resolve with --variant: {details}")

    selected = {
        variant_id: explicit.get(variant_id) or (detected[variant_id][0] if detected[variant_id] else None)
        for variant_id in VARIANT_IDS
    }
    missing = [variant_id for variant_id, path in selected.items() if path is None]
    if missing:
        raise SystemExit(f"Missing required variants: {', '.join(missing)}")

    plan_path = args.variation_plan.resolve() if args.variation_plan else None
    plan = load_variation_plan(plan_path)
    plan_by_id = {
        str(item["id"]).zfill(2): item for item in (plan or {}).get("variants", [])
    }

    manifest: dict[str, Any] = {
        "source_dir": str(source_dir),
        "final_dir": str(final_dir),
        "support_dir": str(support_dir),
        "prefix": args.prefix,
        "mode": args.mode,
        "variants": {},
        "support_files": [],
    }
    used = {path for path in selected.values() if path is not None}
    if plan_path:
        used.add(plan_path)

    for variant_id in VARIANT_IDS:
        src = selected[variant_id]
        assert src is not None
        target = final_dir / f"{args.prefix}_variant_{variant_id}_front{src.suffix.lower()}"
        destination = transfer(src, target, args.mode, args.overwrite, args.dry_run)
        manifest["variants"][variant_id] = {
            "source": str(src),
            "output": str(destination),
            "plan": plan_by_id.get(variant_id),
        }

    if plan_path:
        plan_target = support_dir / f"{args.prefix}_variation_plan.json"
        manifest["variation_plan"] = str(
            transfer(plan_path, plan_target, "copy", args.overwrite, args.dry_run)
        )

    for src in source_files:
        if src in used:
            continue
        destination = transfer(src, support_dir / src.name, args.mode, args.overwrite, args.dry_run)
        manifest["support_files"].append(str(destination))

    manifest_path = unique_target(
        support_dir / f"{args.prefix}_organization_manifest.json", args.overwrite
    )
    manifest["manifest"] = str(manifest_path)
    if not args.dry_run:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
