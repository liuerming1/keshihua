import json,hashlib
from pathlib import Path
W=Path('shuju/cleaned/history_book_01/reclean_20260923');base=json.loads((W/'baseline.json').read_text(encoding='utf-8')); idx={k['id']:k for k in base['knowledge']}; bidx={x['id']:x for x in base['blocks']}
for sl in ('s04','s05'):
 p=json.loads((W/f'{sl}.patch.json').read_text(encoding='utf-8'));print('\n##',sl,'range',p['page_range'],'audit',len(p['knowledge_audit']),'updated knowledge',len(p['updates']['knowledge']),'blocks',len(p['updates']['blocks']))
 for k in p['updates']['knowledge']:
  old=idx[k['id']]; dif=[f for f in k if k.get(f)!=old.get(f)]
  substantive=[f for f in dif if f!='reclean_review']
  if substantive:
   print(k['id'],'FIELDS',','.join(substantive));
   for f in substantive:
    if f in ('title','time','summary','flow','points','background','impact','place_refs','person_ids','evidence_block_ids','uncertainties'): print(' ',f,':',repr(old.get(f)),'=>',repr(k.get(f)))
 print('block modifications:')
 for x in p['updates']['blocks']:
  old=bidx[x['id']]
  if old.get('clean_text')!=x.get('clean_text'):
   print(x['id'],'rawunchanged=',old.get('raw_text')==x.get('raw_text'),'OLD',repr(old.get('clean_text')),'NEW',repr(x.get('clean_text')))
