#!/usr/bin/env python3
"""Organize AI3D five-view generation outputs into views and support folders."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
VIEW_ORDER = ["front", "back", "left_side", "right_side", "top"]
VIEW_ALIASES = {
    "front": "front",
    "back": "back",
    "rear": "back",
    "left": "left_side",
    "left_side": "left_side",
    "right": "right_side",
    "right_side": "right_side",
    "top": "top",
    "top_down": "top",
}


def normalized_stem(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_")


def detect_view(path: Path) -> tuple[str, int] | None:
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        return None

    stem = normalized_stem(path)
    tokens = stem.split("_")

    checks = [
        ("left_side", "left_side_view", 120),
        ("right_side", "right_side_view", 120),
        ("front", "front_view", 110),
        ("back", "back_view", 110),
        ("top", "top_view", 110),
        ("back", "rear_view", 105),
        ("left_side", "left_view", 100),
        ("right_side", "right_view", 100),
        ("top", "top_down", 95),
        ("top", "topdown", 95),
    ]
    for view, marker, score in checks:
        if marker in stem:
            return view, score

    if "front" in tokens:
        return "front", 70
    if "back" in tokens or "rear" in tokens:
        return "back", 70
    if "left" in tokens and "right" not in tokens:
        return "left_side", 65
    if "right" in tokens and "left" not in tokens:
        return "right_side", 65
    if "top" in tokens:
        return "top", 65
    return None


def normalize_view_name(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    if normalized not in VIEW_ALIASES:
        raise ValueError(f"Unknown view '{name}'. Expected one of: {', '.join(sorted(VIEW_ALIASES))}")
    return VIEW_ALIASES[normalized]


def parse_view_mapping(values: list[str], source_dir: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--view must use VIEW=PATH, for example --view front=front.png")
        raw_view, raw_path = value.split("=", 1)
        view = normalize_view_name(raw_view)
        path = Path(raw_path)
        if not path.is_absolute():
            path = source_dir / path
        path = path.resolve()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"Explicit {view} view file does not exist: {path}")
        result[view] = path
    return result


def iter_source_files(source_dir: Path, recursive: bool) -> list[Path]:
    iterator = source_dir.rglob("*") if recursive else source_dir.iterdir()
    return sorted(path.resolve() for path in iterator if path.is_file())


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
    dst = unique_target(dst, overwrite)
    if src.resolve() == dst.resolve():
        return dst
    if dry_run:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    if mode == "copy":
        shutil.copy2(src, dst)
    else:
        shutil.move(str(src), str(dst))
    return dst


def canonical_view_name(prefix: str, view: str, suffix: str) -> str:
    return f"{prefix}_{view}_view{suffix.lower()}"


def choose_auto_views(files: list[Path], explicit: dict[str, Path]) -> dict[str, Path]:
    candidates: dict[str, list[tuple[int, str, Path]]] = {view: [] for view in VIEW_ORDER}
    explicit_paths = set(explicit.values())

    for path in files:
        if path in explicit_paths:
            continue
        detected = detect_view(path)
        if detected is None:
            continue
        view, score = detected
        if view in explicit:
            continue
        candidates[view].append((-score, path.name.lower(), path))

    chosen: dict[str, Path] = {}
    for view in VIEW_ORDER:
        if candidates[view]:
            chosen[view] = sorted(candidates[view])[0][2]
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path, help="Folder containing mixed generated files.")
    parser.add_argument("--views-dir", required=True, type=Path, help="Destination folder for final five view images.")
    parser.add_argument("--support-dir", required=True, type=Path, help="Destination folder for prompts, previews, drafts, contact sheets, and manifests.")
    parser.add_argument("--prefix", required=True, help="Output filename prefix, e.g. cat or hero.")
    parser.add_argument("--view", action="append", default=[], help="Explicit final view mapping: front=path. Can be repeated.")
    parser.add_argument("--mode", choices=["copy", "move"], default="copy", help="Copy by default; use move to clean an already cluttered project folder.")
    parser.add_argument("--recursive", action="store_true", help="Scan source-dir recursively.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite destination files instead of creating versioned names.")
    parser.add_argument("--dry-run", action="store_true", help="Print the manifest without copying or moving files.")
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    views_dir = args.views_dir.resolve()
    support_dir = args.support_dir.resolve()
    if not source_dir.exists() or not source_dir.is_dir():
        raise SystemExit(f"Missing source directory: {source_dir}")

    explicit = parse_view_mapping(args.view, source_dir)
    source_files = [
        path for path in iter_source_files(source_dir, args.recursive)
        if not is_inside(path, views_dir) and not is_inside(path, support_dir)
    ]
    auto_views = choose_auto_views(source_files, explicit)
    final_views = {**auto_views, **explicit}

    used: set[Path] = set()
    manifest: dict[str, Any] = {
        "source_dir": str(source_dir),
        "views_dir": str(views_dir),
        "support_dir": str(support_dir),
        "mode": args.mode,
        "views": {},
        "support_files": [],
        "missing_views": [],
    }

    for view in VIEW_ORDER:
        src = final_views.get(view)
        if src is None:
            manifest["views"][view] = None
            manifest["missing_views"].append(view)
            continue
        target = views_dir / canonical_view_name(args.prefix, view, src.suffix)
        dst = transfer(src, target, args.mode, args.overwrite, args.dry_run)
        used.add(src)
        manifest["views"][view] = str(dst)

    for src in source_files:
        if src in used:
            continue
        dst = transfer(src, support_dir / src.name, args.mode, args.overwrite, args.dry_run)
        manifest["support_files"].append(str(dst))

    manifest_path = support_dir / f"{args.prefix}_organization_manifest.json"
    manifest_path = unique_target(manifest_path, args.overwrite)
    manifest["manifest"] = str(manifest_path)
    if not args.dry_run:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
