"""Build concise review summaries for the six merged PDF batches."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "shuju" / "cleaned" / "history_book_01"


for n in range(1, 7):
    stem = f"b{n:02}"
    data = json.loads((ROOT / f"{stem}.json").read_text(encoding="utf-8"))
    batch = data["batch"]
    pages = batch["requested_pdf_pages"]
    categories = Counter(issue["category"] for issue in data["review_issues"])
    category_text = "、".join(f"{name} {count}" for name, count in sorted(categories.items()))
    material = [
        f"# {stem} PDF 清洗审阅摘要",
        "",
        f"- PDF 页序：{min(pages)}–{max(pages)}；请求 {len(pages)} 页，完成 {len(batch['completed_pdf_pages'])} 页，部分 {len(batch['partial_pdf_pages'])} 页，未处理 {len(batch['unprocessed_pdf_pages'])} 页。",
        f"- 数据：{len(data['blocks'])} 个原文块、{len(data['assets'])} 个视觉资产、{len(data['knowledge'])} 条待审知识、{len(data['inventory'])} 条覆盖清单、{len(data['map_candidates'])} 个地图候选。",
        f"- 机械结构检查：`{data['validation']['structure_check_status']}`；语义审核：`{data['validation']['semantic_review_status']}`。结构通过不代表史实审核通过。",
        f"- 待核验：{len(data['review_issues'])} 条，其中阻断发布 {sum(issue['blocking'] for issue in data['review_issues'])} 条；类别计数：{category_text}。具体证据和建议见 `review_issues`。",
        "- 图片未导出独立裁剪文件时 `file_path=null`；地图候选的几何未数字化，不可直接作为运行时疆域。",
        "- 四个分段的逐页阅读和特殊续接说明见：" + "、".join(f"[parts/{stem}{letter}.review.md](parts/{stem}{letter}.review.md)" for letter in "abcd") + "。",
        "",
    ]
    (ROOT / f"{stem}.review.md").write_text("\n".join(material), encoding="utf-8")
    print(stem, len(data["review_issues"]), "review issues")
