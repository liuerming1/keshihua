import json
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/s01.patch.json').read_text(encoding='utf8'));B={b['id']:b for b in json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf8'))['blocks']}
for k in D['updates']['knowledge']:
 if k.get('background') is None or k.get('impact') is None:
  print('\n',k['id'],k['title'],'BG',bool(k.get('background')),'IM',bool(k.get('impact')),'SUMMARY',k.get('summary',{}).get('text'))
  for bid in k['evidence_block_ids']:
   b=B.get(bid)
   if b: print(bid,repr((b.get('clean_text') or '')[:800]))
