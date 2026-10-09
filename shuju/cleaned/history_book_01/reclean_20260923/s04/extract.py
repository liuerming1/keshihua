import json,re
from pathlib import Path
src=Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json')
d=json.loads(src.read_text(encoding='utf-8'))
out=Path('shuju/cleaned/history_book_01/reclean_20260923/s04')
ks=[k for k in d['knowledge'] if 113<=int(k['id'].split('_p')[1][:4])<=149]
blocks={b['id']:b for b in d['blocks']}
with (out/'knowledge_evidence.txt').open('w',encoding='utf-8') as f:
 for k in ks:
  print('\n'+'='*100+'\n'+k['id']+' | '+k['title'],file=f)
  print(json.dumps({x:k.get(x) for x in ['kind','content_type','time','themes','place_refs','person_ids','summary','flow','points','background','impact','evidence_block_ids','uncertainties']},ensure_ascii=False),file=f)
  ids=set(k.get('evidence_block_ids',[]))
  for key in ['summary','flow','points','background','impact']:
   v=k.get(key)
   if isinstance(v,dict): ids.update(v.get('evidence_block_ids',[]))
   elif isinstance(v,list):
    for c in v: ids.update(c.get('evidence_block_ids',[]))
  for bid in sorted(ids):
   b=blocks.get(bid)
   print('BLOCK',bid,('type='+str(b.get('type'))+' text='+str(b.get('clean_text'))) if b else 'MISSING',file=f)
# page block extraction text for relevant and neighbor pages
with (out/'page_blocks.txt').open('w',encoding='utf-8') as f:
 for p in d['pages']:
  n=p['pdf_page_number']
  if 112<=n<=150:
   print('\n### PAGE',n,p['id'],p.get('printed_page_label'),p.get('chapter_path'),file=f)
   for b in sorted((x for x in d['blocks'] if x.get('page_id')==p['id']),key=lambda x:x.get('order',0)):
    print(b['id'],b.get('type'),repr(b.get('clean_text')),file=f)
