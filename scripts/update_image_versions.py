"""Publish SVGs at content-specific paths so caches cannot serve older art."""
import hashlib
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
assets = root / "assets"
assets.mkdir(exist_ok=True)
readme = root / "README.md"
text = readme.read_text(encoding="utf-8")
for name in ("contrib-heatmap.svg", "stats.svg", "avi-ascii.svg"):
    content = (root / name).read_bytes().replace(b"\r\n", b"\n")
    digest = hashlib.sha256(content).hexdigest()[:16]
    stem = Path(name).stem
    target = assets / f"{stem}-{digest}.svg"
    target.write_bytes(content)
    pattern = rf'src="[^"]*/{re.escape(stem)}(?:-[a-f0-9]{{16}})?\.svg(?:\?[^" ]*)?"'
    text, count = re.subn(pattern, f'src="./assets/{target.name}"', text)
    if count != 1:
        raise ValueError(f"Expected one README image for {name}, found {count}")
    for previous in assets.glob(f"{stem}-*.svg"):
        if previous != target:
            previous.unlink()
readme.write_text(text, encoding="utf-8")
print("Published images with content-specific filenames")
