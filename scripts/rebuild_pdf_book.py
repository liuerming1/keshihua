"""Rebuild six batch files and the book-level index from 24 checked parts."""

import json
from pathlib import Path

from merge_pdf_cleaning import merge
from validate_pdf_cleaning import check


ROOT = Path(__file__).resolve().parents[1] / "shuju" / "cleaned" / "history_book_01"


def write_merged(output, inputs):
    parts = [json.loads(path.read_text(encoding="utf-8")) for path in inputs]
    data = merge(parts)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _, issues = check(output)
    data["validation"]["structure_check_status"] = "passed" if not issues else "failed"
    data["validation"]["page_coverage_issues"] = [
        {"record_ids": [], "description": issue} for issue in issues if "page" in issue
    ]
    data["validation"]["dangling_references"] = [
        {"record_ids": [], "description": issue} for issue in issues if "->" in issue
    ]
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{output.name}: {len(data['pages'])} pages, "
          f"{len(data['knowledge'])} knowledge, {len(issues)} issues")
    for issue in issues[:15]:
        print(" -", issue)
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    for n in range(1, 7):
        stem = f"b{n:02}"
        inputs = [ROOT / "parts" / f"{stem}{letter}.json" for letter in "abcd"]
        write_merged(ROOT / f"{stem}.json", inputs)
    write_merged(ROOT / "all.json", [ROOT / f"b{n:02}.json" for n in range(1, 7)])
