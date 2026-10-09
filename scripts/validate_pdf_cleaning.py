"""Mechanical checks for history-pdf-ingest/1.0 part or batch JSON files.

This does not perform historical/semantic review.
"""

import json
import sys
from collections import Counter
from pathlib import Path


COLLECTIONS = (
    "documents", "pages", "blocks", "assets", "places", "people", "knowledge",
    "relations", "map_candidates", "inventory", "review_issues",
)
REQUIRED = {
    "documents": "id file_name title edition volume publisher publication_year total_pdf_pages language source_kind sha256",
    "pages": "id document_id pdf_page_number printed_page_label chapter_path page_kind text_status image_status notes",
    "blocks": "id page_id order type bbox raw_text clean_text asset_ids table_data notes",
    "assets": "id page_id block_id type bbox file_path caption visible_text description claims notes",
    "places": "id name_as_written name_type valid_time_text coordinates spatial_precision coordinate_evidence_block_ids evidence_block_ids notes",
    "people": "id name_as_written aliases evidence_block_ids notes",
    "knowledge": "id title kind content_type time themes place_refs person_ids summary flow points background impact evidence_block_ids asset_ids source_inventory_ids uncertainties review_status",
    "relations": "id from_knowledge_id to_knowledge_id target_label type person_ids place_ids time_text description evidence_block_ids review_status",
    "map_candidates": "id asset_id reference_time_text reference_year date_precision historical_names legend_text evidence_block_ids geometry geometry_status notes",
    "inventory": "id document_id page_ids block_ids item_label scope disposition knowledge_ids duplicate_of_inventory_id reason",
    "review_issues": "id record_ids category description evidence_block_ids suggested_action blocking status",
}
ALLOWED = {
    "documents": {"source_kind": {"textbook", "supplement"}},
    "pages": {"page_kind": {"content", "front_matter", "blank", "other"},
              "text_status": {"complete", "partial", "unreadable", "unread", "not_applicable"},
              "image_status": {"complete", "partial", "unreadable", "unread", "not_applicable"}},
    "blocks": {"type": {"heading", "paragraph", "caption", "table", "note", "exercise", "image"}},
    "assets": {"type": {"map", "timeline", "chart", "table", "photo", "illustration", "other"}},
    "places": {"name_type": {"historical", "modern", "unknown"},
               "spatial_precision": {"exact", "approximate", "unknown"}},
    "knowledge": {"kind": {"event", "process", "origin", None},
                  "content_type": {"event", "institution", "thought", "economy", "culture", "science", "war", "other"},
                  "review_status": {"pending_review"}},
    "relations": {"type": {"participation", "origin", "spread", "reform", "influence", "causes", "other"},
                  "review_status": {"pending_review"}},
    "map_candidates": {"date_precision": {"year", "month", "day", "period", "unknown"},
                       "geometry_status": {"not_digitized"}},
    "inventory": {"scope": {"chinese_history", "world_history", "mixed", "uncertain"},
                  "disposition": {"included", "pending_review", "out_of_scope", "duplicate"}},
    "review_issues": {"category": {"ocr", "time", "place", "person", "relation", "source", "image", "scope", "duplicate", "other"},
                      "status": {"open"}},
}


def check(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    issues = []
    if data.get("schema_version") != "history-pdf-ingest/1.0":
        issues.append("wrong schema_version")
    records = {key: data.get(key, []) for key in COLLECTIONS}
    for key, items in records.items():
        if not isinstance(items, list):
            issues.append(f"{key} is not a list")
            records[key] = []
        for item in records[key]:
            missing = set(REQUIRED[key].split()) - set(item)
            if missing:
                issues.append(f"{key}.{item.get('id')} missing keys: {sorted(missing)}")
            for field, allowed in ALLOWED.get(key, {}).items():
                if item.get(field) not in allowed:
                    issues.append(f"{key}.{item.get('id')}.{field} invalid: {item.get(field)!r}")
    ids = [item.get("id") for items in records.values() for item in items]
    counts = Counter(ids)
    issues += [f"duplicate id: {key}" for key, count in counts.items() if count > 1]
    if any(not isinstance(key, str) or not key for key in ids):
        issues.append("missing/empty id")
    indexed = {key: {item.get("id") for item in items} for key, items in records.items()}
    inventories_by_id = {item["id"]: item for item in records["inventory"]}
    knowledge_by_id = {item["id"]: item for item in records["knowledge"]}
    def ref(obj, key, collection, label):
        value = obj.get(key)
        if value is not None and value not in indexed[collection]:
            issues.append(f"{label}.{key} -> missing {collection}: {value}")
    for p in records["pages"]:
        ref(p, "document_id", "documents", p.get("id"))
    for b in records["blocks"]:
        ref(b, "page_id", "pages", b.get("id"))
        for a in b.get("asset_ids", []):
            if a not in indexed["assets"]:
                issues.append(f"{b.get('id')}.asset_ids -> {a}")
    for a in records["assets"]:
        ref(a, "page_id", "pages", a.get("id"))
        ref(a, "block_id", "blocks", a.get("id"))
        for claim in a.get("claims", []):
            for value in claim.get("evidence_block_ids", []):
                if value not in indexed["blocks"]:
                    issues.append(f"{a.get('id')}.claims -> {value}")
    for k in records["knowledge"]:
        allowed_themes = {"culture", "science", "agriculture", "war", "politics", "economy", "society", "foreign_relations", "other"}
        for theme in k.get("themes", []):
            if theme not in allowed_themes:
                issues.append(f"{k.get('id')}.themes invalid: {theme!r}")
        for field in ("evidence_block_ids",):
            for value in k.get(field, []):
                if value not in indexed["blocks"]:
                    issues.append(f"{k.get('id')}.{field} -> {value}")
        for field in ("summary", "background", "impact"):
            claim = k.get(field)
            if claim:
                for value in claim.get("evidence_block_ids", []):
                    if value not in indexed["blocks"]:
                        issues.append(f"{k.get('id')}.{field} -> {value}")
        for field in ("flow", "points"):
            for claim in k.get(field, []):
                for value in claim.get("evidence_block_ids", []):
                    if value not in indexed["blocks"]:
                        issues.append(f"{k.get('id')}.{field} -> {value}")
        for value in k.get("asset_ids", []):
            if value not in indexed["assets"]:
                issues.append(f"{k.get('id')}.asset_ids -> {value}")
        for value in k.get("source_inventory_ids", []):
            if value not in indexed["inventory"]:
                issues.append(f"{k.get('id')}.source_inventory_ids -> {value}")
            elif k.get("id") not in inventories_by_id[value].get("knowledge_ids", []):
                issues.append(f"{k.get('id')}.source_inventory_ids not reciprocal: {value}")
        if not k.get("source_inventory_ids"):
            issues.append(f"{k.get('id')} has no source_inventory_ids")
        for value in k.get("person_ids", []):
            if value not in indexed["people"]:
                issues.append(f"{k.get('id')}.person_ids -> {value}")
        for place in k.get("place_refs", []):
            if place.get("place_id") not in indexed["places"]:
                issues.append(f"{k.get('id')}.place_refs -> {place.get('place_id')}")
            for value in place.get("evidence_block_ids", []):
                if value not in indexed["blocks"]:
                    issues.append(f"{k.get('id')}.place_refs.evidence -> {value}")
        t = k.get("time", {})
        missing_time = set("source_text mode start_year end_year earliest_year latest_year precision end_status normalization_note evidence_block_ids".split()) - set(t)
        if missing_time:
            issues.append(f"{k.get('id')}.time missing keys: {sorted(missing_time)}")
        for field, allowed in {
            "mode": {"point", "duration", "uncertain", "unknown"},
            "precision": {"day", "month", "year", "decade", "century", "period", "unknown"},
            "end_status": {"known", "ongoing", "unknown", "not_applicable"},
        }.items():
            if t.get(field) not in allowed:
                issues.append(f"{k.get('id')}.time.{field} invalid: {t.get(field)!r}")
        for field in ("start_year", "end_year", "earliest_year", "latest_year"):
            if t.get(field) == 0:
                issues.append(f"{k.get('id')}.time.{field} is year zero")
        for value in t.get("evidence_block_ids", []):
            if value not in indexed["blocks"]:
                issues.append(f"{k.get('id')}.time.evidence -> {value}")
        if t.get("mode") == "point" and (t.get("end_year") is not None or t.get("end_status") != "not_applicable"):
            issues.append(f"{k.get('id')}.time point/end conflict")
        if k.get("review_status") != "pending_review":
            issues.append(f"{k.get('id')} review_status must be pending_review")
        for place in k.get("place_refs", []):
            if place.get("role") not in {"occurrence", "origin", "spread", "influence", "related"}:
                issues.append(f"{k.get('id')}.place_refs.role invalid: {place.get('role')!r}")
    for inv in records["inventory"]:
        ref(inv, "document_id", "documents", inv.get("id"))
        for field, collection in (("page_ids", "pages"), ("block_ids", "blocks"), ("knowledge_ids", "knowledge")):
            for value in inv.get(field, []):
                if value not in indexed[collection]:
                    issues.append(f"{inv.get('id')}.{field} -> {value}")
        for value in inv.get("knowledge_ids", []):
            if value in knowledge_by_id and inv.get("id") not in knowledge_by_id[value].get("source_inventory_ids", []):
                issues.append(f"{inv.get('id')}.knowledge_ids not reciprocal: {value}")
    for rel in records["relations"]:
        ref(rel, "from_knowledge_id", "knowledge", rel.get("id"))
        ref(rel, "to_knowledge_id", "knowledge", rel.get("id"))
        if rel.get("review_status") != "pending_review":
            issues.append(f"{rel.get('id')} review_status must be pending_review")
        for field, collection in (("person_ids", "people"), ("place_ids", "places"), ("evidence_block_ids", "blocks")):
            for value in rel.get(field, []):
                if value not in indexed[collection]:
                    issues.append(f"{rel.get('id')}.{field} -> {value}")
    for m in records["map_candidates"]:
        ref(m, "asset_id", "assets", m.get("id"))
        if m.get("geometry") is not None or m.get("geometry_status") != "not_digitized":
            issues.append(f"{m.get('id')} map geometry must remain not_digitized")
        for value in m.get("evidence_block_ids", []):
            if value not in indexed["blocks"]:
                issues.append(f"{m.get('id')}.evidence_block_ids -> {value}")
    for name in ("places", "people", "review_issues"):
        for item in records[name]:
            for value in item.get("evidence_block_ids", []):
                if value not in indexed["blocks"]:
                    issues.append(f"{item.get('id')}.evidence_block_ids -> {value}")
    requested = data.get("batch", {}).get("requested_pdf_pages", [])
    buckets = [data.get("batch", {}).get(field, []) for field in
               ("completed_pdf_pages", "partial_pdf_pages", "unprocessed_pdf_pages")]
    if Counter(requested) != Counter(page for bucket in buckets for page in bucket):
        issues.append("requested/completed/partial/unprocessed page partition mismatch")
    if set(requested) != {p.get("pdf_page_number") for p in records["pages"]}:
        issues.append("pages records do not cover requested PDF pages")
    if any(issue.get("status") != "open" for issue in records["review_issues"]):
        issues.append("review_issues.status must be open")
    return data, issues


if __name__ == "__main__":
    result = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        data, issues = check(path)
        print(f"{path}: {len(data.get('pages', []))} pages, "
              f"{len(data.get('blocks', []))} blocks, "
              f"{len(data.get('knowledge', []))} knowledge, "
              f"{len(data.get('inventory', []))} inventory; {len(issues)} issues")
        for issue in issues[:30]:
            print("  -", issue)
        result |= bool(issues)
    sys.exit(result)
