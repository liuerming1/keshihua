"""Check the import artifact, exported files and source-attribution links."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--public-dir", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.package.read_text(encoding="utf-8"))
    assets = {item["id"]: item for item in data["assets"]}
    blocks = {item["id"] for item in data["blocks"]}
    sources = data["verification_report"]["external_source_registry"]
    assert len(data["pages"]) == 223
    reclean = data.get('reclean_report')
    if reclean:
        original_path = Path(__file__).resolve().parents[1] / 'shuju/cleaned/history_book_01/reclean_20260923/baseline.json'
        assert hashlib.sha256(original_path.read_bytes()).hexdigest() == reclean['source_sha256']
        original = json.loads(original_path.read_text(encoding='utf8'))
        live_ids = {k['id'] for k in data['knowledge']}
        archived_ids = {k['id'] for k in data['archived_knowledge_candidates']}
        assert not live_ids & archived_ids
        assert live_ids | archived_ids == {k['id'] for k in original['knowledge']}
        assert len(live_ids) == len(data['knowledge']) == reclean['canonical_knowledge_count']
        assert len(archived_ids) == len(data['archived_knowledge_candidates']) == reclean['archived_candidate_count']
        assert len(live_ids) + len(archived_ids) == reclean['reviewed_candidate_count'] == 819
        assert set(data['knowledge_aliases']) == archived_ids
        assert all(targets and set(targets) <= live_ids for targets in data['knowledge_aliases'].values())
        new_blocks = {b['id']: b for b in data['blocks']}
        assert all(new_blocks[b['id']]['raw_text'] == b['raw_text'] for b in original['blocks'])
        assert {x['id'] for x in data['inventory']} == {x['id'] for x in original['inventory']}
        assert len(reclean['carryover_review']) == len(original['batch']['carryover'])
        assert sources == original['verification_report']['external_source_registry']
    else:
        assert len(data["knowledge"]) == 819
    assert len(assets) == 256
    assert len(data["map_layers"]) == 45
    assert len(data["map_reference_points"]["features"]) == 4
    assert {item["id"] for item in data["map_candidates"]} == {item["id"] for item in data["map_layers"]}

    for item in data["assets"]:
        box = item["bbox"]
        assert len(box) == 4 and 0 <= box[0] < box[2] <= 1 and 0 <= box[1] < box[3] <= 1, item["id"]
        file_path = item["file_path"]
        assert file_path.startswith("/textbook-assets/") and file_path.endswith(".png"), item["id"]
        local_file = args.public_dir / file_path.lstrip("/")
        assert local_file.is_file(), local_file
        assert hashlib.sha256(local_file.read_bytes()).hexdigest() == item["export"]["sha256"], item["id"]

    statuses = Counter()
    for item in data["knowledge"]:
        assert item["verification"]["review_completed"] is True, item["id"]
        status = item["finalization"]["status"]
        assert status in ({"ready", "qualified", "needs_review"} if reclean else {"ready", "qualified"}), item["id"]
        if reclean:
            assert (status == 'needs_review') == (item['reclean_review']['status'] == 'needs_review'), item['id']
        statuses[status] += 1
        for field in ("summary", "background", "impact", "flow", "points"):
            value = item[field]
            claims = value if isinstance(value, list) else [value] if value else []
            for claim in claims:
                assert claim['text'].strip(), (item['id'],field)
                assert claim.get('evidence_block_ids') or claim.get('external_source_ids'), (item['id'],field)
                assert set(claim["evidence_block_ids"]) <= blocks, (item["id"], field)
                assert set(claim.get("external_source_ids", [])) <= sources.keys(), (item["id"], field)
        assert set(item["finalization"].get("supplemental_source_ids", [])) <= sources.keys(), item["id"]

    for layer in data["map_layers"]:
        assert layer["raster_asset_id"] in assets, layer["id"]
        assert layer["raster_file_path"] == assets[layer["raster_asset_id"]]["file_path"], layer["id"]
        assert layer["geometry"] is None and layer["georeferenced"] is False, layer["id"]
        assert layer["geometry_status"] == "not_digitized", layer["id"]
        for label in layer["image_labels"]:
            x, y = label["image_position"]
            assert 0 <= x <= 1 and 0 <= y <= 1, layer["id"]
    for point in data["map_reference_points"]["features"]:
        lon, lat = point["geometry"]["coordinates"]
        assert -180 <= lon <= 180 and -90 <= lat <= 90
        assert point["properties"]["historical_geometry"] is False
        assert point["properties"]["map_candidate_id"] in {layer["id"] for layer in data["map_layers"]}

    assert {status: count for status, count in data["finalization_report"]["fact_status_counts"].items()
            if count} == dict(statuses)
    assert data["finalization_report"]["image_export_count"] == 256
    assert data["finalization_report"]["source_xobject_image_count"] == sum(
        item["export"]["method"] == "pdf_xobject" for item in data["assets"])
    assert data["finalization_report"]["map_raster_count"] == 45
    assert data["finalization_report"]["map_image_label_count"] == sum(len(x["image_labels"]) for x in data["map_layers"])
    assert data["finalization_report"]["map_geometry_count"] == 4
    print(f"Validated {len(data['knowledge'])} knowledge, {len(assets)} image files, "
          f"{len(data['map_layers'])} raster maps, {data['finalization_report']['map_image_label_count']} image labels")


if __name__ == "__main__":
    main()
