#!/usr/bin/env python3
"""
Image-to-WebP converter.

Usage:
    python scripts/convert-images.py <file-or-dir> [options]

Examples:
    python scripts/convert-images.py static/img/logo.png --lossless
    python scripts/convert-images.py assets/img/hero.jpg --quality 85 --width 1920
    python scripts/convert-images.py static/img/ --lossless
    python scripts/convert-images.py static/img/ --quality 80 --dry-run
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("ERROR: Pillow not installed — run: pip install Pillow")

SUPPORTED = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif"}


def convert(src: Path, lossless: bool, quality: int, width: int | None, dry_run: bool) -> None:
    dst = src.with_suffix(".webp")

    img = Image.open(src)

    if width and img.width > width:
        ratio = width / img.width
        new_height = round(img.height * ratio)
        img = img.resize((width, new_height), Image.LANCZOS)

    # Preserve transparency for RGBA/P images
    if img.mode in ("RGBA", "LA", "PA"):
        # lossless is always preferred for images with transparency
        effective_lossless = True
    else:
        effective_lossless = lossless
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

    src_kb = src.stat().st_size // 1024

    if dry_run:
        mode_label = "lossless" if effective_lossless else f"q{quality}"
        resize_label = f" → {width}px wide" if width and img.width != width else ""
        print(f"  [dry-run] {src}  ({src_kb} KB){resize_label}  → {dst.name}  [{mode_label}]")
        return

    save_kwargs: dict = {"format": "WEBP", "lossless": effective_lossless}
    if not effective_lossless:
        save_kwargs["quality"] = quality

    img.save(dst, **save_kwargs)
    dst_kb = dst.stat().st_size // 1024
    saving = src_kb - dst_kb
    pct = round(saving / src_kb * 100) if src_kb else 0
    mode_label = "lossless" if effective_lossless else f"q{quality}"
    print(f"  ✅ {src.name:<40} {src_kb:>5} KB  →  {dst.name:<44} {dst_kb:>4} KB  (-{saving} KB, -{pct}%)  [{mode_label}]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert images to WebP")
    parser.add_argument("target", help="File or directory to convert")
    parser.add_argument("--lossless", action="store_true", help="Lossless compression (best for logos/icons)")
    parser.add_argument("--quality", type=int, default=85, metavar="N", help="Lossy quality 1-100 (default 85)")
    parser.add_argument("--width", type=int, default=None, metavar="PX", help="Resize to this width (aspect ratio preserved)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be converted without writing files")
    args = parser.parse_args()

    target = Path(args.target)

    if not target.exists():
        sys.exit(f"ERROR: {target} does not exist")

    sources: list[Path] = []
    if target.is_dir():
        for ext in SUPPORTED:
            sources.extend(sorted(target.glob(f"*{ext}")))
            sources.extend(sorted(target.glob(f"*{ext.upper()}")))
        sources = sorted(set(sources))
    elif target.suffix.lower() in SUPPORTED:
        sources = [target]
    else:
        sys.exit(f"ERROR: unsupported format '{target.suffix}' — supported: {', '.join(SUPPORTED)}")

    if not sources:
        print(f"No convertible images found in {target}")
        return

    print(f"\nConverting {len(sources)} image(s):\n")
    errors = 0
    for src in sources:
        try:
            convert(src, args.lossless, args.quality, args.width, args.dry_run)
        except Exception as e:
            print(f"  ❌ {src.name}: {e}")
            errors += 1

    print()
    if errors:
        sys.exit(f"{errors} error(s) — see above")


if __name__ == "__main__":
    main()
