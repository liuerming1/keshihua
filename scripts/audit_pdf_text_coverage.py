"""Flag pages whose cleaned evidence omits much of the PDF text layer.

Character overlap is only a triage signal, not proof of page completeness.
"""

import json
import sys
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


def chars(value):
    return Counter(c for c in value if not c.isspace())


if __name__ == "__main__":
    pdf = PdfReader(sys.argv[1])
    for arg in sys.argv[2:]:
        data = json.loads(Path(arg).read_text(encoding="utf-8"))
        pages = {p["id"]: p["pdf_page_number"] for p in data["pages"]}
        texts = {n: [] for n in pages.values()}
        for block in data["blocks"]:
            if block["page_id"] in pages:
                texts[pages[block["page_id"]]].append(block.get("raw_text") or "")
        for asset in data["assets"]:
            if asset["page_id"] in pages:
                texts[pages[asset["page_id"]]].append(asset.get("visible_text") or "")
        print(arg)
        for n in sorted(texts):
            source = chars(pdf.pages[n - 1].extract_text() or "")
            captured = chars("\n".join(texts[n]))
            overlap = sum((source & captured).values())
            ratio = overlap / max(sum(source.values()), 1)
            print(f"  PDF p{n:03}: source={sum(source.values()):4} "
                  f"evidence={sum(captured.values()):4} overlap={ratio:.1%}")
