import json,hashlib,re
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923'); B=json.loads((R/'baseline.json').read_text(encoding='utf-8')); P=json.loads((R/'s06.patch.json').read_text(encoding='utf-8'))
assert P['baseline_sha256']==hashlib.sha256((R/'baseline.json').read_bytes()).hexdigest()
origk={x['id']:x for x in B['knowledge']}; upd={x['id']:x for x in P['updates']['knowledge']}; audits={a['id']:a for a in P['knowledge_audit']}
scoped={k['id'] for k in B['knowledge'] if any(k['id'].startswith(f'history_book_01_p{i:04d}_') for i in range(187,224))}
assert len(scoped)==293 and set(upd)==scoped==set(audits) and len(P['updates']['knowledge'])==293
blocks={x['id']:x for x in B['blocks']}; ub={x['id']:x for x in P['updates']['blocks']}
assert len(ub)==37 and {int(re.search(r'_p(\d{4})_b',bid).group(1)) for bid in ub}==set(range(187,215))
for bid,b in ub.items():
 orig=blocks[bid]; assert orig['raw_text']==b['raw_text'],bid
 assert 'NÅO' not in (b.get('clean_text') or ''),bid
 assert b['reclean_review']['status']=='agent_reviewed'
 for key,val in orig.items():
  if key not in ['clean_text','reclean_review']: assert b[key]==val,(bid,key)
for kid,k in upd.items():
 assert k['reclean_review']['status']==('needs_review' if audits[kid]['decision']=='needs_review' else 'agent_reviewed')
 for eid in k.get('evidence_block_ids',[]): assert eid in blocks,(kid,eid)
 for f in ['flow','points','background','impact']:
  if not k.get(f): assert f in audits[kid]['empty_reasons'],(kid,f)
for a in audits.values(): assert all(e in blocks for e in a['evidence_block_ids'])
assert all(bid in blocks for x in P['carryover_review'] for bid in x['evidence_block_ids'])
assert [x['index'] for x in P['carryover_review']]==list(range(32,44))
assert not P['open_items'] and not P['split_proposals']
assert sum(k['reclean_review']['status']=='needs_review' for k in upd.values())==0
k=upd['history_book_01_p0188_k002']; assert k['time']['mode']=='duration' and k['time']['start_year']==1983 and k['time']['end_year']==1991 and len(k['points'])==4 and k['title'].startswith('1983—1991')
k=upd['history_book_01_p0207_k003']; assert k['time']['mode']=='unknown' and len(k['points'])==2 and '未作' in k['summary']['text']
k=upd['history_book_01_p0211_k021']; assert '教材附录原文' in k['summary']['text'] and k['time']['source_text']=='1127—1276年' and k['time']['end_year']==1279 and 'SRC_SOUTHERN_SONG' in k['time']['external_source_ids']
print('PASS: patch JSON/hash; 293 complete knowledge/audits; audit-state consistency; references; 37 contaminated blocks on 28 pages, clean_text watermark removal and raw_text/other-field preservation; carryover 32–43; resolved requested items.')
print('changed',sum(a['decision']=='changed' for a in audits.values()),'needs_review',sum(a['decision']=='needs_review' for a in audits.values()),'open_items',len(P['open_items']),'watermark blocks',len(ub),'watermark pages',len({int(re.search(r'_p(\d{4})_b',bid).group(1)) for bid in ub}))

