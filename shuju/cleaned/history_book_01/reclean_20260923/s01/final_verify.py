import json,hashlib,re
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923');d=json.loads((root/'baseline.json').read_text(encoding='utf8'));p=json.loads((root/'s01.patch.json').read_text(encoding='utf8'));review=(root/'s01.review.md').read_text(encoding='utf8')
assert p['baseline_sha256']==hashlib.sha256((root/'baseline.json').read_bytes()).hexdigest()
# Regression: explicit None must clear numeric dates for relative '距今' and approximate-only years.
builder=(root/'s01'/'build_patch.py').read_text(encoding='utf8')
assert 'UNSET=object()' in builder and 'if val is not UNSET:t[key]=val' in builder
for tid in ['history_book_01_p0009_k002','history_book_01_p0009_k003','history_book_01_p0010_k001','history_book_01_p0010_k002','history_book_01_p0012_k001','history_book_01_p0012_k002']:
 tk=next(k for k in p['updates']['knowledge'] if k['id']==tid)['time']
 assert all(tk[f] is None for f in ('start_year','end_year','earliest_year','latest_year')), (tid,tk)
basek={x['id']:x for x in d['knowledge']}; ks={x['id']:x for x in p['updates']['knowledge']}; audits={x['id']:x for x in p['knowledge_audit']}
expected={x['id'] for x in d['knowledge'] if re.search(r'_p(?:000[1-9]|00[1-2]\d|003[0-8])_',x['id'])}
assert set(ks)==expected and set(audits)==expected and len(p['knowledge_audit'])==80
blocks={x['id']:x for x in d['blocks']}; bu={x['id']:x for x in p['updates']['blocks']}; valid=set(blocks)|set(bu)
for b in bu.values():
 if b['id'] in blocks: assert b['raw_text']==blocks[b['id']]['raw_text'],b['id']
for i,k in ks.items():
 a=audits[i]; assert a['decision'] in ('changed','retained','needs_review')
 assert (a['decision']=='needs_review')==(k['reclean_review']['status']=='needs_review')
 assert k['reclean_review']['slice']=='s01'
 for fld in ('flow','points'):
  assert isinstance(k.get(fld),list), (i,fld)
 for fld in ('summary','background','impact'):
  val=k.get(fld)
  if val:
   assert val['evidence_block_ids'] and set(val['evidence_block_ids'])<=set(k['evidence_block_ids']),(i,fld)
 for fld in ('flow','points'):
  for c in k[fld]:assert isinstance(c,dict) and c.get('text') and set(c.get('evidence_block_ids',[]))<=set(k['evidence_block_ids']),(i,fld)
 for bid in k['evidence_block_ids']:assert bid in valid,(i,bid)
 for fld in ('flow','points','background','impact'):
  if not k.get(fld):assert fld in a['empty_reasons'],(i,fld)
for b in bu.values():
 if int(re.search(r'_p(\d{4})_',b['id']).group(1)) in range(20,30): assert 'NÅO' not in (b.get('clean_text') or '')
assert [x['index'] for x in p['carryover_review']]==list(range(7))
assert len(re.findall(r'"id": "history_book_01_p\d{4}_k\d{3}"',review))>=80
print(json.dumps({'knowledge':len(ks),'audit_decisions':{x:sum(a['decision']==x for a in audits.values()) for x in ['changed','retained','needs_review']},'blocks':len(bu),'pages':len(p['updates']['pages']),'carryover_review':len(p['carryover_review']),'issues':len(p['updates']['review_issues']),'patch_bytes':(root/'s01.patch.json').stat().st_size,'review_bytes':len(review.encode('utf8'))},ensure_ascii=False))
