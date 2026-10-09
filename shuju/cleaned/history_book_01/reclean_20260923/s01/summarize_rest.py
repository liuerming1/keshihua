import json,re
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf8'));B={b['id']:b for b in D['blocks']}
def pg(k):
 m=re.search(r'_p(\d{4})_',k['id']);
 if m:return int(m.group(1))
 return min([int(re.search(r'_p(\d{4})_',B[x]['page_id']).group(1)) for x in k.get('evidence_block_ids',[]) if x in B] or [999])
for k in D['knowledge']:
 p=pg(k)
 if 16<=p<=38:
  print(f"\n{p:02} {k['id']} | {k['title']} | {k['kind']}/{k['content_type']} | TIME {k['time'].get('source_text')} => {k['time'].get('mode')},{k['time'].get('start_year')},{k['time'].get('end_year')},{k['time'].get('end_status')} ")
  for key in ['summary','flow','points','background','impact']:
   val=k.get(key);print(' '+key+'='+json.dumps(val,ensure_ascii=False))
  print(' refs=',json.dumps(k.get('place_refs'),ensure_ascii=False),'persons=',k.get('person_ids'))
  for bid in k.get('evidence_block_ids',[]):
   b=B.get(bid);print(' src',bid,repr(b.get('clean_text') if b else 'MISSING'))
