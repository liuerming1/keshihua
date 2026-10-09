"""Merge four disjoint page-range part files into one batch JSON.

Usage: python scripts/merge_pdf_cleaning.py OUTPUT.json PART1.json ... PART4.json
The merged file stays pending review even if the mechanical check passes.
"""

import json
import sys
from copy import deepcopy
from pathlib import Path

from validate_pdf_cleaning import COLLECTIONS, check


def replace_strings(value, mapping):
    if isinstance(value, str):
        return mapping.get(value, value)
    if isinstance(value, list):
        return [replace_strings(item, mapping) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item, mapping) for key, item in value.items()}
    return value


def merge(parts):
    first = parts[0]
    # Four slices become b01; six already-merged batches become one book index.
    first_id = first["batch"]["id"]
    target_id = (first_id[:-1] if first_id[-1:] in "abcd"
                 else f"{first['batch']['document_id']}_all")
    result = {
        "schema_version": "history-pdf-ingest/1.0",
        "batch": {
            "id": target_id,
            "document_id": first["batch"]["document_id"],
            "requested_pdf_pages": [], "completed_pdf_pages": [],
            "partial_pdf_pages": [], "unprocessed_pdf_pages": [],
            "complete": False, "next_pdf_page": None, "carryover": [],
        },
        **{name: [] for name in COLLECTIONS},
        "validation": {
            "structure_check_status": "not_run", "duplicate_ids": [],
            "dangling_references": [], "page_coverage_issues": [], "time_issues": [],
            "source_issues": [], "unreadable_blocks": [], "unprocessed_assets": [],
            "semantic_review_status": "not_performed",
        },
    }
    seen_documents = set()
    seen_ids = set()
    for original_part in parts:
        part = deepcopy(original_part)
        part_ids = {item["id"] for name in COLLECTIONS if name != "documents"
                    for item in part.get(name, [])}
        collided = sorted(part_ids & seen_ids)
        if collided:
            suffix = part["batch"]["id"].rsplit("_", 1)[-1]
            mapping = {old: f"{old}_{suffix}" for old in collided}
            part = replace_strings(part, mapping)
            result["validation"]["source_issues"].append({
                "record_ids": [],
                "description": f"Namespaced {len(mapping)} colliding IDs from {original_part['batch']['id']}; semantic entity deduplication remains pending",
            })
            part_ids = {item["id"] for name in COLLECTIONS if name != "documents"
                        for item in part.get(name, [])}
        seen_ids.update(part_ids)
        if part["batch"]["document_id"] != result["batch"]["document_id"]:
            raise ValueError("Different document IDs")
        for field in ("requested_pdf_pages", "completed_pdf_pages", "partial_pdf_pages", "unprocessed_pdf_pages", "carryover"):
            result["batch"][field].extend(part["batch"].get(field, []))
        for name in COLLECTIONS:
            for item in part.get(name, []):
                if name == "documents":
                    if item["id"] in seen_documents:
                        canonical = next(doc for doc in result[name] if doc["id"] == item["id"])
                        differing = [key for key in canonical if canonical.get(key) != item.get(key)]
                        if differing:
                            result["validation"]["source_issues"].append({
                                "record_ids": [item["id"]],
                                "description": "Part document metadata differs; canonical first part retained: "
                                               + ", ".join(differing),
                            })
                        continue
                    seen_documents.add(item["id"])
                result[name].append(item)
    for field in ("requested_pdf_pages", "completed_pdf_pages", "partial_pdf_pages", "unprocessed_pdf_pages"):
        result["batch"][field].sort()
    incomplete = result["batch"]["partial_pdf_pages"] + result["batch"]["unprocessed_pdf_pages"]
    result["batch"]["complete"] = not incomplete
    result["batch"]["next_pdf_page"] = min(incomplete) if incomplete else None
    return result


if __name__ == "__main__":
    output = Path(sys.argv[1])
    parts = [json.loads(Path(path).read_text(encoding="utf-8")) for path in sys.argv[2:]]
    result = merge(parts)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _, issues = check(output)
    result["validation"]["structure_check_status"] = "failed" if issues else "passed"
    result["validation"]["page_coverage_issues"] = [
        {"record_ids": [], "description": issue} for issue in issues if "page" in issue
    ]
    result["validation"]["dangling_references"] = [
        {"record_ids": [], "description": issue} for issue in issues if "->" in issue
    ]
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{output}: {len(result['pages'])} pages; {len(issues)} mechanical issues")
    for issue in issues[:30]:
        print(" -", issue)
