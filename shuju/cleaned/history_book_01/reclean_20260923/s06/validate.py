import json,hashlib
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923')
B=json.loads((R/'baseline.json').read_text(encoding='utf-8'))
P=json.loads((R/'s06.patch.json').read_text(encoding='utf-8'))
basehash=hashlib.sha256((R/'baseline.json').read_bytes()).hexdigest()
assert P['baseline_sha256']==basehash
orig={x['id']:x for x in B['knowledge']}; upd=P['updates']['knowledge']; u={x['id']:x for x in upd}
assert len(upd)==293==len(u)==len(P['knowledge_audit'])
assert set(u)=={k['id'] for k in B['knowledge'] if any(k['id'].startswith(f'history_book_01_p{i:04d}_') for i in range(187,224))}
assert len({a['id'] for a in P['knowledge_audit']})==293
bl={b['id'] for b in B['blocks']}
assert all(bid in bl for x in upd for bid in x.get('evidence_block_ids',[]))
assert all(bid in bl for a in P['knowledge_audit'] for bid in a['evidence_block_ids'])
assert all(bid in bl for x in P['carryover_review'] for bid in x['evidence_block_ids'])
assert [x['index'] for x in P['carryover_review']]==list(range(32,44))
for a in P['knowledge_audit']:
 x=u[a['id']]
 assert a['decision']==('needs_review' if x['reclean_review']['status']=='needs_review' else a['decision'])
 for f in ['flow','points','background','impact']:
  if not x.get(f): assert f in a['empty_reasons'],(a['id'],f)
assert all(set(x['reclean_review'])=={'status','note','slice'} for x in upd)
print('JSON/hash/ID/reference/field checks passed')
print('visually checked',len(P['visually_checked_pages']),'pages; changes',len([a for a in P['knowledge_audit'] if a['decision']=='changed']),'needs_review',len([a for a in P['knowledge_audit'] if a['decision']=='needs_review']),'open items',len(P['open_items']))
