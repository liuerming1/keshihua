import json
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923')
for fn in ['s03.patch.json','baseline.json']:
 p=R/fn; d=json.loads(p.read_text(encoding='utf-8')); print(fn,'keys',list(d.keys()),'updates',len(d.get('updates',{}).get('blocks',[])))
 if fn=='s03.patch.json':
  for b in d['updates']['blocks']:
   if b['id'] in ['history_book_01_p0082_b001','history_book_01_p0082_b010','history_book_01_p0083_b001','history_book_01_p0083_b007','history_book_01_p0095_b002','history_book_01_p0101_b004']:
    print('PATCH BLOCK',b['id'],'raw',repr((b.get('raw_text') or '')[:1000]),'clean',repr((b.get('clean_text') or '')[:1000]))
