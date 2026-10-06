import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep_photo(input_path):
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    # Output path
    output_path = input_path.parent / f"{input_path.stem}-prepped.png"

    # --------------------------------------------------
    # 1. Remove background using rembg
    # --------------------------------------------------
    print("Removing background...")

    with open(input_path, "rb") as f:
        input_data = f.read()

    output_data = remove(input_data)

    # Load the result as RGBA
    foreground = Image.open(
        __import__("io").BytesIO(output_data)
    ).convert("RGBA")

    # --------------------------------------------------
    # 2. Composite subject onto pure white background
    # --------------------------------------------------
    print("Compositing onto white background...")

    white = Image.new(
        "RGBA",
        foreground.size,
        (255, 255, 255, 255)
    )

    composited = Image.alpha_composite(white, foreground)

    # --------------------------------------------------
    # 3. Convert to grayscale
    # --------------------------------------------------
    gray = composited.convert("L")

    # Convert PIL image -> OpenCV image
    img = np.array(gray)

    # --------------------------------------------------
    # 4. Boost local contrast using CLAHE
    # --------------------------------------------------
    print("Applying CLAHE...")

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(img)

    # --------------------------------------------------
    # 5. Save result
    # --------------------------------------------------
    cv2.imwrite(str(output_path), enhanced)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)

    prep_photo(sys.argv[1])