import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923'); f=root/'s01.patch.json';p=json.loads(f.read_text(encoding='utf8'))
valid={b['id'] for b in json.loads((root/'baseline.json').read_text(encoding='utf8'))['blocks']} | {b['id'] for b in p['updates']['blocks']}
K={k['id']:k for k in p['updates']['knowledge']}
for k in p['updates']['knowledge']:
 refs=[]
 for field in ('summary','background','impact'):
  c=k.get(field)
  if isinstance(c,dict):refs.extend(c.get('evidence_block_ids',[]))
 for field in ('flow','points'):
  for c in k.get(field) or []:refs.extend(c.get('evidence_block_ids',[]))
 for bid in refs:
  if bid not in valid:raise ValueError(f'unknown evidence {k["id"]} {bid}')
  if bid not in k['evidence_block_ids']:k['evidence_block_ids'].append(bid)
for a in p['knowledge_audit']:a['evidence_block_ids']=K[a['id']]['evidence_block_ids']
p['updates']['knowledge']=list(K.values())
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
# Slice-only fixture for the project read-only content contract checker.
(root/'s01'/'contract_fixture.json').write_text(json.dumps({'knowledge':p['updates']['knowledge'],'blocks':p['updates']['blocks'],'batch':{'complete':False,'carryover':[]}},ensure_ascii=False),encoding='utf8')
print('claim evidence reconciled')

