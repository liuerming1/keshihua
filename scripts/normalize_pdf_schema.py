"""Normalize known out-of-schema values while preserving their original meaning.

Only changes the explicitly listed enum mismatches. Historical facts remain pending review.
"""

import json
import sys
from collections import Counter
from pathlib import Path


def normalize(data):
    changed = Counter()
    for block in data["blocks"]:
        if block["type"] == "asset":
            block["type"] = "image"
            changed["block asset -> image"] += 1
    for asset in data["assets"]:
        if asset["type"] == "portrait":
            asset["type"] = "photo"
            changed["asset portrait -> photo"] += 1
    for item in data["inventory"]:
        if item["scope"] == "out_of_scope":
            item["scope"] = "uncertain"
            changed["inventory scope out_of_scope -> uncertain"] += 1
    for knowledge in data["knowledge"]:
        if knowledge["kind"] == "period":
            knowledge["kind"] = None
            knowledge["uncertainties"].append(
                "原提取将 kind 标为 period；该值不属于事件性质枚举，已留空待判断。"
            )
            changed["knowledge kind period -> null"] += 1
        original_type = knowledge["content_type"]
        if original_type in {"politics", "foreign_relations", "society", "agriculture"}:
            knowledge["content_type"] = "economy" if original_type == "agriculture" else "other"
            if original_type not in knowledge["themes"]:
                knowledge["themes"].append(original_type)
            knowledge["uncertainties"].append(
                f"原提取 content_type={original_type} 不属该字段枚举；已规范化为 {knowledge['content_type']}，原标签保留在 themes。"
            )
            changed[f"content_type {original_type} -> {knowledge['content_type']}"] += 1
        if "thought" in knowledge["themes"]:
            knowledge["themes"] = ["culture" if theme == "thought" else theme
                                   for theme in knowledge["themes"]]
            knowledge["themes"] = list(dict.fromkeys(knowledge["themes"]))
            knowledge["uncertainties"].append(
                "原提取筛选主题 thought 不属 themes 枚举；改为 culture，思想类别仍以 content_type 保留。"
            )
            changed["theme thought -> culture"] += 1
        time = knowledge["time"]
        notes = []
        if time["mode"] == "period":
            time["mode"] = "unknown"
            notes.append("原提取 mode=period 不属时间性质枚举；保留 source_text/precision，不推断持续区间。")
            changed["time mode period -> unknown"] += 1
        if time["precision"] == "season":
            time["precision"] = "period"
            notes.append("原提取精度为 season，约定枚举无季节级；原话保留，精度降为 period。")
            changed["time precision season -> period"] += 1
        if time["end_status"] == "known" and time["end_year"] is None:
            time["end_status"] = "unknown"
            notes.append("原提取标记已知结束年，但未提供 end_year；改为 unknown 待核验。")
            changed["end_status known without end_year -> unknown"] += 1
        if notes:
            prior = time["normalization_note"]
            time["normalization_note"] = (prior + "；" if prior else "") + "；".join(notes)
    return changed


if __name__ == "__main__":
    total = Counter()
    for arg in sys.argv[1:]:
        path = Path(arg)
        data = json.loads(path.read_text(encoding="utf-8"))
        changes = normalize(data)
        if changes:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        total.update(changes)
        print(path.name, sum(changes.values()), "normalizations")
    print("Total:", dict(total))
