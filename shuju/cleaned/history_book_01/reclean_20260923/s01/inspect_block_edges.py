import json
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf8'))
for pg in list(range(1,8))+[37,38]:
 print('\nPAGE',pg)
 for b in D['blocks']:
  if b['page_id'].endswith(f'p{pg:04d}'):
   print(b['id'],b['type'],'raw=',repr(b.get('raw_text')),'\nclean=',repr(b.get('clean_text')))
for k in D['knowledge']:
 if k['id'].startswith('history_book_01_p0037'):
  print('\nKNOWLEDGE',json.dumps(k,ensure_ascii=False,indent=2))
