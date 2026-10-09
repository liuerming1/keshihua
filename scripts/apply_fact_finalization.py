"""Apply reviewed fact patches to a separate import candidate, preserving sources.

The verified file remains immutable. Unsupported suggestions stay explicitly
blocked rather than being silently published as corrected facts.
"""

import argparse
import json
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--patch", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in data["knowledge"]}
    block_ids = {item["id"] for item in data["blocks"]}
    patches = {}
    issue_resolutions = []
    for path in args.patch:
        part = json.loads(path.read_text(encoding="utf-8"))
        for patch in part["patches"]:
            record_id = patch["id"]
            if record_id in patches or record_id not in by_id:
                raise ValueError(f"Duplicate or unknown knowledge patch: {record_id}")
            if patch["disposition"] not in {"apply", "needs_source"}:
                raise ValueError(f"Unknown disposition for {record_id}")
            evidence = patch.get("evidence_block_ids")
            if evidence is not None and (not isinstance(evidence, list) or any(ref not in block_ids for ref in evidence)):
                raise ValueError(f"Invalid evidence patch for {record_id}")
            patches[record_id] = patch
        issue_resolutions.extend(part.get("issue_resolutions", []))
    statuses = Counter()
    applied = []
    blocked = []
    for item in data["knowledge"]:
        review = item["verification"]
        patch = patches.get(item["id"])
        if patch:
            evidence = patch.get("evidence_block_ids")
            if evidence is not None:
                item["evidence_block_ids"] = list(evidence)
                if item["summary"] is not None:
                    item["summary"]["evidence_block_ids"] = list(evidence)
            for note in patch.get("uncertainties_append", []):
                if note and note not in item["uncertainties"]:
                    item["uncertainties"].append(note)
            if patch["disposition"] == "apply" and patch.get("summary") is not None:
                proposed = patch["summary"]
                if isinstance(proposed, str):
                    refs = evidence or (item["summary"] or {}).get("evidence_block_ids", [])
                    item["summary"] = {"text": proposed, "evidence_block_ids": list(refs)}
                elif isinstance(proposed, dict) and isinstance(proposed.get("text"), str):
                    refs = proposed.get("evidence_block_ids", evidence or [])
                    if any(ref not in block_ids for ref in refs):
                        raise ValueError(f"Invalid summary claim references for {item['id']}")
                    item["summary"] = {"text": proposed["text"], "evidence_block_ids": list(refs)}
                else:
                    raise ValueError(f"Invalid summary patch for {item['id']}")
            if patch["disposition"] == "apply":
                applied.append(item["id"])
        if review["overall_status"] == "verified_with_qualification":
            note = "核验限定：" + review["verification_note"]
            if note not in item["uncertainties"]:
                item["uncertainties"].append(note)
        # The knowledge-level evidence index must contain every claim-level
        # reference. This closes extraction-era omissions without changing a
        # claim or fabricating a new source.
        claim_refs = []
        for field in ("summary", "background", "impact"):
            claim = item.get(field)
            if claim:
                claim_refs.extend(claim["evidence_block_ids"])
        for field in ("flow", "points"):
            for claim in item[field]:
                claim_refs.extend(claim["evidence_block_ids"])
        claim_refs.extend(item["time"]["evidence_block_ids"])
        for place in item["place_refs"]:
            claim_refs.extend(place["evidence_block_ids"])
        item["evidence_block_ids"] = list(dict.fromkeys(item["evidence_block_ids"] + claim_refs))
        needs_fix = review["overall_status"] in {"needs_data_fix", "needs_correction"}
        if patch and patch["disposition"] == "needs_source":
            # An explicitly qualified but factually supported textbook claim
            # can be read with its limitation visible. A verified data-quality
            # relink can also proceed when the proposed block was applied.
            if review["overall_status"] == "verified_with_qualification":
                status = "qualified"
            elif review["overall_status"] == "needs_data_fix" and patch.get("evidence_block_ids"):
                status = "qualified" if review["historical_status"] == "qualified" else "ready"
            else:
                status = "needs_source"
        elif needs_fix and not patch:
            status = "needs_source"
        elif review["historical_status"] == "qualified":
            status = "qualified"
        elif review["historical_status"] == "needs_correction" and not (patch and patch["disposition"] == "apply"):
            status = "needs_source"
        else:
            status = "ready"
        if status == "needs_source":
            blocked.append(item["id"])
        item["finalization"] = {
            "status": status,
            "source_verification_status": review["overall_status"],
            "patch_applied": bool(patch and patch["disposition"] == "apply"),
            "fact_note": patch["reason"] if patch else None,
        }
        statuses[status] += 1
    # These three verifier corrections require an external source. Keep the
    # textbook evidence and the supplementary support separately attributable.
    source_registry = data["verification_report"]["external_source_registry"]
    supplemental = {
        "history_book_01_p0055_k005": {
            "text": "隋朝工匠李春设计并主持建造赵州桥。教材称其为“世界上现存最古老的石拱桥”；按 UNESCO 的桥型限定，它是现存最古老的敞肩式坦弧拱桥之一。",
            "source_ids": ["SRC_ZHAOZHOU"],
        },
        "history_book_01_p0211_k021": {
            "text": "教材附录将南宋列为1127—1276年；1276年是临安陷落的节点，南宋余部仍继续抵抗，通常以1279年作为南宋终结年份。",
            "source_ids": ["SRC_SOUTHERN_SONG", "SRC_SOUTHERN_SONG_1276"],
            "end_year": 1279,
        },
        "history_book_01_p0214_k018": {
            "text": "教材年表以1276年记“南宋灭亡”；这一年元军占领临安，宋室余部继续抵抗，南宋最终终结通常记为1279年。",
            "source_ids": ["SRC_SOUTHERN_SONG", "SRC_SOUTHERN_SONG_1276"],
            "title": "1276年：临安陷落（教材年表作“南宋灭亡”）",
        },
    }
    for record_id, correction in supplemental.items():
        item = by_id[record_id]
        if item["finalization"]["status"] != "needs_source":
            raise ValueError(f"Unexpected correction status: {record_id}")
        if any(ref not in source_registry for ref in correction["source_ids"]):
            raise ValueError(f"Missing supplemental source: {record_id}")
        item["summary"]["text"] = correction["text"]
        item["summary"]["external_source_ids"] = correction["source_ids"]
        if "title" in correction:
            item["title"] = correction["title"]
        if "end_year" in correction:
            item["time"]["end_year"] = correction["end_year"]
            item["time"]["external_source_ids"] = correction["source_ids"]
            item["time"]["normalization_note"] = "教材附录列1276；外部宋史资料以1279为终年，教材原值保存在source_text。"
        item["finalization"]["status"] = "qualified"
        item["finalization"]["patch_applied"] = True
        item["finalization"]["supplemental_source_ids"] = correction["source_ids"]
        statuses["needs_source"] -= 1
        statuses["qualified"] += 1
        blocked.remove(record_id)
        applied.append(record_id)
    # The fourth correction was already source-attributed in the reviewed
    # summary, but its old title still asserted an unqualified endpoint.
    roc_item = by_id["history_book_01_p0219_k001"]
    roc_item["finalization"]["original_title"] = roc_item["title"]
    roc_item["title"] = "1949年4月23日：人民解放军解放南京"
    roc_item["finalization"]["status"] = "qualified"
    roc_item["finalization"]["fact_note"] = "年表的“中华民国时期结束”作为教材分期保留在摘要与原题记录，不作为无范围限定的标题事实。"
    statuses["ready"] -= 1
    statuses["qualified"] += 1
    # Join the page-94 source excerpt to its explicit continuation on page 95.
    # Keep the two original page blocks separate so a reader can inspect each.
    cross_page_item = by_id["history_book_01_p0094_k002"]
    continuation = "history_book_01_p0095_b002"
    if continuation not in block_ids or continuation in cross_page_item["evidence_block_ids"]:
        raise ValueError("Unexpected cross-page source state")
    cross_page_item["evidence_block_ids"].append(continuation)
    cross_page_item["summary"]["evidence_block_ids"].append(continuation)
    cross_page_item["summary"]["text"] = (
        "探究材料跨 PDF 页 94—95，依次引王守仁的“良知”、王畿的解释和李贽《童心说》；"
        "第94页末在“全”字处换页，第95页继续“不复有初矣”及后文，已关联两页原文块。"
    )
    cross_page_item["finalization"]["fact_note"] = "原先跨页截断的史料已连接 PDF 页95续文，保留两页独立证据块。"
    issue_resolutions.append({"id": "history_book_01_b03b_issue015", "status": "resolved",
                              "reason": "p0094_k002 已同时引用第94页材料和第95页续文，未把跨页文本误合为同页。"})
    if len(data["knowledge"]) != 819:
        raise ValueError("Expected 819 knowledge records")
    proposals_by_id = {proposal["id"]: proposal for proposal in issue_resolutions}
    if len(proposals_by_id) != len(issue_resolutions):
        raise ValueError("Duplicate issue resolution proposal")
    issue_statuses = Counter()
    for issue in data["review_issues"]:
        proposal = proposals_by_id.get(issue["id"])
        issue["finalization_status"] = proposal["status"] if proposal else "open"
        issue["finalization_note"] = proposal["reason"] if proposal else None
        issue_statuses[issue["finalization_status"]] += 1
    if set(proposals_by_id) - {issue["id"] for issue in data["review_issues"]}:
        raise ValueError("Unknown issue resolution proposal")
    data["finalization_report"] = {
        "source_file": args.source.name,
        "source_document_sha256": data["documents"][0]["sha256"],
        "knowledge_count": len(data["knowledge"]),
        "fact_status_counts": dict(statuses),
        "applied_patch_ids": applied,
        "needs_source_ids": sorted(set(blocked)),
        "issue_resolution_proposals": issue_resolutions,
        "issue_status_counts": dict(issue_statuses),
        "interpretation": "finalization.status is the import gate; legacy review_status and validation describe the earlier extraction pass and are retained for provenance.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}; statuses={dict(statuses)}, applied={len(applied)}, blocked={len(set(blocked))}")


if __name__ == "__main__":
    main()
