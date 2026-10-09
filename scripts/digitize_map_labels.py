"""Extract map-label pixel positions from the PDF text layer.

Coordinates are normalized within each separately cropped image. They are
*not* longitude/latitude or a georeferencing transform. Exact text matches
only; unmatched names remain explicit for manual review.
"""

import argparse
import json
import re
from pathlib import Path

import pdfplumber


def candidate_names(values):
    names = []
    for value in values:
        for part in re.split(r"[、，,；;／/]", value):
            part = part.strip()
            if part and part not in names:
                names.append(part)
    return names


def spatial_char_match(chars, name):
    """Match one label only when adjacent PDF glyph boxes form its text."""
    matches = []
    for first in chars:
        if first["text"] != name[0]:
            continue
        chains = [([first], None)]
        for letter in name[1:]:
            next_chains = []
            for chain, direction in chains:
                previous = chain[-1]
                px = (previous["x0"] + previous["x1"]) / 2
                py = (previous["top"] + previous["bottom"]) / 2
                size = max(previous["x1"] - previous["x0"], previous["bottom"] - previous["top"], 1)
                for candidate in chars:
                    if candidate["text"] != letter or candidate in chain:
                        continue
                    cx = (candidate["x0"] + candidate["x1"]) / 2
                    cy = (candidate["top"] + candidate["bottom"]) / 2
                    dx, dy = cx - px, cy - py
                    horizontal = 0.45 * size <= dx <= 1.75 * size and abs(dy) <= 0.55 * size
                    vertical = 0.45 * size <= dy <= 1.75 * size and abs(dx) <= 0.55 * size
                    if horizontal and direction in (None, "horizontal"):
                        next_chains.append((chain + [candidate], "horizontal"))
                    if vertical and direction in (None, "vertical"):
                        next_chains.append((chain + [candidate], "vertical"))
            chains = next_chains
            if not chains:
                break
        matches.extend(chain for chain, _ in chains)
    return matches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--reports-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.data.read_text(encoding="utf-8"))
    assets = {item["id"]: item for item in data["assets"]}
    pages = {item["id"]: item["pdf_page_number"] for item in data["pages"]}
    crops = {}
    for report_path in sorted(args.reports_dir.glob("b???.json")):
        for record in json.loads(report_path.read_text(encoding="utf-8"))["asset_crops"]:
            crops[record["asset_id"]] = record["bbox"]
    results = []
    with pdfplumber.open(args.pdf) as pdf:
        for candidate in data["map_candidates"]:
            asset_id = candidate["asset_id"]
            if asset_id not in crops:
                continue
            page_number = pages[assets[asset_id]["page_id"]]
            page = pdf.pages[page_number - 1]
            left, top, right, bottom = crops[asset_id]
            rect = (left * page.width, top * page.height, right * page.width, bottom * page.height)
            words = page.crop(rect).extract_words()
            chars = page.crop(rect).chars
            labels = []
            unmatched = []
            for name in candidate_names(candidate["historical_names"]):
                exact = [word for word in words if word["text"] == name]
                regions = [(word["x0"], word["top"], word["x1"], word["bottom"], "exact_pdf_text_layer_match")
                           for word in exact]
                if not regions:
                    regions = [(min(char["x0"] for char in chain), min(char["top"] for char in chain),
                                max(char["x1"] for char in chain), max(char["bottom"] for char in chain),
                                "exact_pdf_chars_spatial_sequence") for chain in spatial_char_match(chars, name)]
                if not regions:
                    unmatched.append(name)
                    continue
                for x0, y0, x1, y1, method in regions:
                    x = ((x0 + x1) / 2 - rect[0]) / (rect[2] - rect[0])
                    y = ((y0 + y1) / 2 - rect[1]) / (rect[3] - rect[1])
                    if 0 <= x <= 1 and 0 <= y <= 1:
                        labels.append({"text": name, "image_position": [round(x, 6), round(y, 6)],
                                       "method": method, "spatial_precision": "image_pixel_only"})
            results.append({"map_candidate_id": candidate["id"], "asset_id": asset_id,
                            "pdf_page_number": page_number, "labels": labels, "unmatched_names": unmatched,
                            "coordinate_system": "normalized_cropped_image", "georeferenced": False})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"maps": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Digitized {sum(len(x['labels']) for x in results)} exact text labels in {len(results)} maps; "
          f"{sum(len(x['unmatched_names']) for x in results)} names unmatched")


if __name__ == "__main__":
    main()
