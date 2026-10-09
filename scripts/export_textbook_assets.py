"""Export reviewed PDF image regions without inventing their page positions.

Input manifest has {"asset_crops": [{"asset_id": ..., "bbox": [l,t,r,b]}]}.
Bboxes are normalized against the visible, unrotated PDF page. Source pages
and asset IDs are checked against the cleaning JSON before any crop is run.
"""

import argparse
import hashlib
import json
import re
import struct
import subprocess
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader
from PIL import Image


def png_size(path: Path):
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG: {path}")
    return struct.unpack(">II", header[16:24])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--xobject-overrides", type=Path)
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()
    if args.dpi < 100 or args.dpi > 400:
        raise ValueError("DPI must be between 100 and 400")
    source = PdfReader(str(args.pdf))
    data = json.loads(args.data.read_text(encoding="utf-8"))
    crops = json.loads(args.manifest.read_text(encoding="utf-8"))["asset_crops"]
    overrides = json.loads(args.xobject_overrides.read_text(encoding="utf-8")) if args.xobject_overrides else {}
    assets = {asset["id"]: asset for asset in data["assets"]}
    pages = {page["id"]: page["pdf_page_number"] for page in data["pages"]}
    if len(crops) != len({entry["asset_id"] for entry in crops}):
        raise ValueError("Duplicate asset ID in crop manifest")
    poppler = Path(r"C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe")
    if not poppler.is_file():
        raise FileNotFoundError(poppler)
    for entry in crops:
        asset_id = entry["asset_id"]
        if asset_id not in assets or not re.fullmatch(r"[A-Za-z0-9_-]+", asset_id):
            raise ValueError(f"Unknown or unsafe asset ID: {asset_id}")
        box = entry["bbox"]
        if not isinstance(box, list) or len(box) != 4 or not all(isinstance(v, (int, float)) for v in box):
            raise ValueError(f"Invalid bbox for {asset_id}")
        left, top, right, bottom = box
        if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
            raise ValueError(f"Out-of-page bbox for {asset_id}: {box}")
        if pages[assets[asset_id]["page_id"]] < 1:
            raise ValueError(f"Invalid page for {asset_id}")
    if set(overrides) - set(assets):
        raise ValueError("Unknown XObject override asset")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for entry in crops:
        asset_id = entry["asset_id"]
        page_number = pages[assets[asset_id]["page_id"]]
        page = source.pages[page_number - 1]
        if int(page.get("/Rotate", 0)) % 360:
            raise ValueError(f"Rotated PDF page {page_number} requires explicit handling")
        page_width = float(page.mediabox.width) * args.dpi / 72
        page_height = float(page.mediabox.height) * args.dpi / 72
        left, top, right, bottom = entry["bbox"]
        x = round(left * page_width)
        y = round(top * page_height)
        width = max(1, round(right * page_width) - x)
        height = max(1, round(bottom * page_height) - y)
        prefix = args.out_dir / asset_id
        output = prefix.with_suffix(".png")
        override = overrides.get(asset_id)
        if override:
            if override["pdf_page_number"] != page_number:
                raise ValueError(f"XObject page mismatch for {asset_id}")
            image_index = override["image_index"]
            if not isinstance(image_index, int) or image_index < 0 or image_index >= len(page.images):
                raise ValueError(f"Invalid XObject image index for {asset_id}")
            source_image = page.images[image_index]
            with Image.open(BytesIO(source_image.data)) as image:
                image.convert("RGB").save(output, format="PNG")
            export_method = "pdf_xobject"
            source_image_name = source_image.name
        else:
            command = [str(poppler), "-f", str(page_number), "-l", str(page_number),
                       "-r", str(args.dpi), "-x", str(x), "-y", str(y),
                       "-W", str(width), "-H", str(height), "-singlefile", "-png",
                       str(args.pdf), str(prefix)]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(f"Crop failed for {asset_id}: {result.stderr[-500:]}")
            export_method = "page_crop"
            source_image_name = None
        size = png_size(output)
        if min(size) < 24:
            raise ValueError(f"Suspiciously small crop for {asset_id}: {size}")
        records.append({"asset_id": asset_id, "pdf_page_number": page_number,
                        "bbox": entry["bbox"], "file_path": f"/textbook-assets/{output.name}",
                        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                        "pixel_size": list(size), "notes": entry.get("notes", []),
                        "export_method": export_method, "source_image_name": source_image_name,
                        "export_reason": override.get("reason") if override else None})
    payload = {"source_pdf_sha256": hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
               "dpi": args.dpi, "asset_crops": records,
               "missing_asset_ids": sorted(set(assets) - {record["asset_id"] for record in records})}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(records)}/{len(assets)} assets; {len(payload['missing_asset_ids'])} missing")


if __name__ == "__main__":
    main()
