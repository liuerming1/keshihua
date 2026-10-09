import json,re
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
d=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
B={b['id']:b for b in d['blocks']}
def n(k):
 m=re.search(r'_p(\d{4})_',k['id'])
 if m:return int(m.group(1))
 return min([int(re.search(r'_p(\d{4})_',B[x]['page_id']).group(1)) for x in k['evidence_block_ids'] if x in B] or [999])
for k in d['knowledge']:
 if n(k)<=38:
  print(f"\n### {n(k):02} {k['id']} {k['title']} | time={k['time']} | kind={k['kind']} type={k['content_type']}")
  print(' summary:',k.get('summary'))
  print(' flow:',k.get('flow'))
  print(' points:',k.get('points'))
  print(' bg:',k.get('background'),'impact:',k.get('impact'))
  print(' refs:',k.get('place_refs'),'people:',k.get('person_ids'))
  print(' evidence:')
  for x in k['evidence_block_ids']:
   b=B.get(x);print(' ',x,repr(b.get('clean_text') if b else None))
for p in range(1,39):
 print(f'\n#### PAGE {p}')
 for b in d['blocks']:
  if re.search(fr'_p{p:04d}_',b['id']): print(b['id'],b['type'],repr(b.get('clean_text')))
