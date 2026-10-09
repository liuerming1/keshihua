"""Apply evidence-reference corrections verified against source page blocks.

This deliberately handles only known, reviewed cases. It is not a fuzzy fixer.
"""

import json
import sys
from pathlib import Path


KNOWN_BLOCK_CORRECTIONS = {
    "history_book_01_p0014_b003": "history_book_01_p0014_b001",
}


def fix(data):
    asset_to_block = {asset["id"]: asset["block_id"] for asset in data["assets"]}
    corrections = {**KNOWN_BLOCK_CORRECTIONS, **asset_to_block}
    changed = []
    for name in ("places", "people", "review_issues"):
        for record in data[name]:
            old = record.get("evidence_block_ids", [])
            new = [corrections.get(value, value) for value in old]
            if new != old:
                changed.append((record["id"], old, new))
                record["evidence_block_ids"] = new
    return changed


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        path = Path(arg)
        data = json.loads(path.read_text(encoding="utf-8"))
        changes = fix(data)
        if changes:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(path, len(changes), "corrected records")
        for change in changes:
            print(" -", change)
