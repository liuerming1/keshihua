import json, hashlib
from pathlib import Path
from pypdf import PdfReader
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
d=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
pdf=Path('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf')
reader=PdfReader(str(pdf))
blocks={b['id']:b for b in d['blocks']}
pages={p['id']:p for p in d['pages']}
def own_page(k):
    ident=k['id']
    import re
    m=re.search(r'_p(\d{4})_',ident)
    if m:return int(m.group(1))
    nums=[]
    for bid in k.get('evidence_block_ids',[]):
        b=blocks.get(bid)
        if b:
            m=re.search(r'_p(\d{4})_',b['page_id'])
            if m: nums.append(int(m.group(1)))
    return min(nums) if nums else None
ks=[k for k in d['knowledge'] if own_page(k) and 1<=own_page(k)<=38]
lines=[]
for pg in range(1,39):
    p=pages[f'history_book_01_p{pg:04d}']
    lines.append(f'\n===== PDF PAGE {pg} | printed={p.get("printed_page_label")} | kind={p.get("page_kind")} | text={p.get("text_status")} image={p.get("image_status")} =====')
    lines.append('PDF_TEXT:\n'+(reader.pages[pg-1].extract_text() or ''))
    lines.append('BASELINE_BLOCKS:')
    for b in d['blocks']:
        if b['page_id']==p['id']:
            lines.append(f"[{b['id']}|{b['type']}] raw={b.get('raw_text')}\n clean={b.get('clean_text')}")
    lines.append('KNOWLEDGE:')
    for k in ks:
        if own_page(k)==pg:
            lines.append(json.dumps(k,ensure_ascii=False,indent=2))
(root/'s01'/'source_audit.txt').write_text('\n'.join(lines),encoding='utf-8')
meta={'pdf':str(pdf.resolve()),'pdf_pages':len(reader.pages),'baseline_sha256':hashlib.sha256((root/'baseline.json').read_bytes()).hexdigest(),'knowledge_count':len(ks),'knowledge_by_page':{},'ids':[k['id'] for k in ks]}
for k in ks: meta['knowledge_by_page'].setdefault(own_page(k),[]).append(k['id'])
(root/'s01'/'scope.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print('pdf pages',len(reader.pages),'knowledge',len(ks),'sha256',meta['baseline_sha256'])
print('by page',[(p,len(ids)) for p,ids in meta['knowledge_by_page'].items()])
