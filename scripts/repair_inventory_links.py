"""Close already-declared knowledge/inventory links in both directions.

Does not infer a new semantic match: a link must already exist on one side.
"""

import json
import sys
from pathlib import Path


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        path = Path(arg)
        data = json.loads(path.read_text(encoding="utf-8"))
        by_knowledge = {item["id"]: item for item in data["knowledge"]}
        by_inventory = {item["id"]: item for item in data["inventory"]}
        changes = 0
        for inv in data["inventory"]:
            for knowledge_id in inv["knowledge_ids"]:
                knowledge = by_knowledge.get(knowledge_id)
                if knowledge is not None and inv["id"] not in knowledge["source_inventory_ids"]:
                    knowledge["source_inventory_ids"].append(inv["id"])
                    changes += 1
        for knowledge in data["knowledge"]:
            for inventory_id in knowledge["source_inventory_ids"]:
                inv = by_inventory.get(inventory_id)
                if inv is not None and knowledge["id"] not in inv["knowledge_ids"]:
                    inv["knowledge_ids"].append(knowledge["id"])
                    changes += 1
        if changes:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(path.name, changes, "reciprocal links added")
