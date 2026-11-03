"""Change README image URLs whenever their contents change, bypassing stale caches."""
import hashlib
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
readme = root / "README.md"
text = readme.read_text(encoding="utf-8")
for name in ("contrib-heatmap.svg", "stats.svg", "avi-ascii.svg"):
    digest = hashlib.sha256((root / name).read_bytes()).hexdigest()[:16]
    text, count = re.subn(
        rf'src="\./{re.escape(name)}(?:\?v=[^"\s]*)?"',
        f'src="./{name}?v={digest}"', text,
    )
    if count != 1:
        raise ValueError(f"Expected one README image for {name}, found {count}")
readme.write_text(text, encoding="utf-8")
print("Updated README image versions from SVG contents")
