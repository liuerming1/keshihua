import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
d=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
blocks={b['id']:b for b in d['blocks']}
ks=[k for k in d['knowledge'] if any(k['id'].startswith(f'history_book_01_p{i:04d}_') for i in range(187,224))]
for page in range(187,224):
    lines=[]
    for k in ks:
        if not k['id'].startswith(f'history_book_01_p{page:04d}_'): continue
        lines += [f"## {k['id']} {k['title']}", 'TIME '+json.dumps(k.get('time'),ensure_ascii=False), 'SUMMARY '+json.dumps(k.get('summary'),ensure_ascii=False), 'FLOW '+json.dumps(k.get('flow'),ensure_ascii=False), 'POINTS '+json.dumps(k.get('points'),ensure_ascii=False), 'BACKGROUND '+json.dumps(k.get('background'),ensure_ascii=False), 'IMPACT '+json.dumps(k.get('impact'),ensure_ascii=False), 'PLACES '+json.dumps(k.get('place_refs'),ensure_ascii=False), 'PEOPLE '+json.dumps(k.get('person_ids'),ensure_ascii=False), 'EVIDENCE '+json.dumps(k.get('evidence_block_ids'),ensure_ascii=False)]
        for bid in k.get('evidence_block_ids',[]):
            b=blocks.get(bid,{})
            lines.append(f"BLOCK {bid} [{b.get('type')}] {b.get('clean_text')}")
        lines.append('')
    if lines: (root/'s06'/f'audit_p{page}.txt').write_text('\n'.join(lines),encoding='utf-8')
print('dumped',len(ks),'knowledge')
