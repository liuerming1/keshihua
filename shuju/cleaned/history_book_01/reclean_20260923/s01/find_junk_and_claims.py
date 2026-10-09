import json,re
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf8'))
for b in D['blocks']:
 m=re.search(r'_p(\d{4})_',b['id']); pg=int(m.group(1)) if m else 999
 if 20<=pg<=29 and any(x in (b.get('raw_text') or '')+(b.get('clean_text') or '') for x in ['NÅO','\\x9b','\x9b','\x7f','º[f','ÿ']):
  print('\n',b['id'],'type',b['type'],'\nRAW tail=',repr((b.get('raw_text') or '')[-130:]),'\nCLEAN tail=',repr((b.get('clean_text') or '')[-130:]))
print('\nSELECTED CLAIMS')
for k in D['knowledge']:
 if k['id'] in ['history_book_01_p0019_k001','history_book_01_p0020_k001','history_book_01_p0021_k001','history_book_01_p0022_k001','history_book_01_p0023_k001','history_book_01_p0023_k002','history_book_01_p0024_k001','history_book_01_p0025_k001','history_book_01_p0025_k002']:
  print('\n',k['id'],k['title'],'\nsummary',k['summary'],'\nflow',k['flow'],'\npts',k['points'],'\nbg',k['background'],'\nimpact',k['impact'])
  for x in k['evidence_block_ids']:
   b=next(xb for xb in D['blocks'] if xb['id']==x);print(x,repr(b.get('clean_text') or b.get('raw_text'))[:2200])
