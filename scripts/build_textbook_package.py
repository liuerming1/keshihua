"""Assemble the reviewed fact data and independently cropped textbook images.

The output is a single JSON import artifact. Raster map references are
machine-readable, but no coordinate geometry is inferred from page pixels.
"""

import argparse
import json
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--reports-dir", type=Path, required=True)
    parser.add_argument("--crops-dir", type=Path, required=True)
    parser.add_argument("--map-labels", type=Path, required=True)
    parser.add_argument("--map-points", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    data = json.loads(args.data.read_text(encoding="utf-8"))
    assets = {record["id"]: record for record in data["assets"]}
    reports = sorted(args.reports_dir.glob("b???.json"))
    if len(reports) != 24:
        raise ValueError(f"Expected 24 image export reports, found {len(reports)}")
    manifests = sorted(args.crops_dir.glob("b???.json"))
    if len(manifests) != 24:
        raise ValueError(f"Expected 24 crop manifests, found {len(manifests)}")
    manifest_crops = {}
    covered_pages = set()
    asset_page_numbers = {asset["id"]: int(asset["page_id"].rsplit("_p", 1)[1]) for asset in data["assets"]}
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        first, last = manifest["range"]
        if first < 1 or last > 223 or first > last or covered_pages.intersection(range(first, last + 1)):
            raise ValueError(f"Overlapping/invalid page slice: {manifest_path.name}")
        covered_pages.update(range(first, last + 1))
        if manifest.get("unresolved"):
            raise ValueError(f"Unresolved crop review: {manifest_path.name}")
        for crop in manifest["asset_crops"]:
            if crop["asset_id"] in manifest_crops:
                raise ValueError(f"Duplicate crop manifest asset: {crop['asset_id']}")
            if crop["asset_id"] not in asset_page_numbers or not first <= asset_page_numbers[crop["asset_id"]] <= last:
                raise ValueError(f"Wrong-page asset in {manifest_path.name}: {crop['asset_id']}")
            manifest_crops[crop["asset_id"]] = crop
    if covered_pages != set(range(1, 224)):
        raise ValueError("Crop manifests do not cover PDF pages 1-223")
    crops = {}
    pdf_hashes = set()
    for report_path in reports:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        pdf_hashes.add(report["source_pdf_sha256"])
        for crop in report["asset_crops"]:
            record_id = crop["asset_id"]
            if record_id in crops or record_id not in assets:
                raise ValueError(f"Duplicate/unknown exported asset: {record_id}")
            crops[record_id] = crop
    if len(pdf_hashes) != 1 or pdf_hashes.pop() != data["documents"][0]["sha256"].lower():
        raise ValueError("Image reports do not match textbook PDF")
    missing = sorted(set(assets) - set(crops))
    if missing:
        raise ValueError(f"Unexported assets: {missing}")
    if set(manifest_crops) != set(crops):
        raise ValueError("Crop manifests and export reports differ")
    if any(manifest_crops[record_id]["bbox"] != crop["bbox"] for record_id, crop in crops.items()):
        raise ValueError("An export report does not match the reviewed crop")

    for record_id, asset in assets.items():
        crop = crops[record_id]
        asset["bbox"] = crop["bbox"]
        asset["file_path"] = crop["file_path"]
        asset["export"] = {
            "sha256": crop["sha256"], "pixel_size": crop["pixel_size"],
            "pdf_page_number": crop["pdf_page_number"], "dpi": 180,
            "crop_review_notes": crop["notes"],
            "method": crop.get("export_method", "page_crop"),
            "source_image_name": crop.get("source_image_name"),
            "export_reason": crop.get("export_reason"),
        }
        asset["notes"] = [note for note in asset["notes"] if note != "未导出独立图片文件。"]

    label_index = {item["map_candidate_id"]: item for item in
                   json.loads(args.map_labels.read_text(encoding="utf-8"))["maps"]}
    if set(label_index) != {item["id"] for item in data["map_candidates"]}:
        raise ValueError("Map-label inventory does not cover all candidates")
    map_points = json.loads(args.map_points.read_text(encoding="utf-8"))
    if map_points["type"] != "FeatureCollection" or map_points["coordinate_reference_system"] != "EPSG:4326":
        raise ValueError("Invalid point geometry catalog")
    data["map_reference_points"] = map_points
    data["map_layers"] = []
    for candidate in data["map_candidates"]:
        asset = assets[candidate["asset_id"]]
        label_data = label_index[candidate["id"]]
        data["map_layers"].append({
            "id": candidate["id"], "candidate_id": candidate["id"],
            "raster_asset_id": asset["id"], "raster_file_path": asset["file_path"],
            "raster_sha256": asset["export"]["sha256"],
            "reference_time_text": candidate["reference_time_text"],
            "reference_year": candidate["reference_year"],
            "date_precision": candidate["date_precision"],
            "historical_names": candidate["historical_names"],
            "legend_text": candidate["legend_text"],
            "evidence_block_ids": candidate["evidence_block_ids"],
            "image_labels": label_data["labels"],
            "unmatched_historical_names": label_data["unmatched_names"],
            "render_kind": "textbook_raster_reference",
            "georeferenced": False, "geometry": None,
            "geometry_status": "not_digitized",
            "spatial_precision": "unknown",
            "review_status": "raster_extracted_geometry_pending",
            "review_note": "教材原图已独立导出并索引；未经地理配准，不能作为准确历史边界或坐标点。",
            "reference_point_ids": [point["id"] for point in map_points["features"]
                                    if point["properties"]["map_candidate_id"] == candidate["id"]],
        })

    statuses = Counter(item["finalization"]["status"] for item in data["knowledge"])
    if statuses.get("needs_source", 0):
        raise ValueError("Unresolved fact corrections in import package")
    data["finalization_report"]["image_export_count"] = len(crops)
    data["finalization_report"]["source_xobject_image_count"] = sum(
        crop.get("export_method") == "pdf_xobject" for crop in crops.values())
    data["finalization_report"]["map_raster_count"] = len(data["map_layers"])
    data["finalization_report"]["map_image_label_count"] = sum(len(layer["image_labels"]) for layer in data["map_layers"])
    data["finalization_report"]["map_georeferenced_count"] = 0
    data["finalization_report"]["map_geometry_count"] = len(map_points["features"])
    data["finalization_report"]["import_status"] = "content_and_raster_ready_geometry_pending"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Assembled {len(data['knowledge'])} knowledge, {len(crops)} images, {len(data['map_layers'])} raster maps")


if __name__ == "__main__":
    main()
