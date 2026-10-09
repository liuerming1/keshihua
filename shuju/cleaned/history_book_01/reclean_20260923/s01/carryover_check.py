import json
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf8'))
for bid in ['history_book_01_p0012_b003','history_book_01_p0013_b003','history_book_01_p0029_b001','history_book_01_p0030_b001','history_book_01_p0031_b001','history_book_01_p0031_b006','history_book_01_p0032_b001','history_book_01_p0035_b006','history_book_01_p0036_b001','history_book_01_p0038_b008','history_book_01_p0039_b001']:
 b=next((x for x in D['blocks'] if x['id']==bid),None)
 print('\n',bid,'\nRAW',repr((b or {}).get('raw_text')),'\nCLEAN',repr((b or {}).get('clean_text')))
for k in D['knowledge']:
 if k['id'] in ['history_book_01_p0012_k003','history_book_01_p0013_k001','history_book_01_p0029_k002','history_book_01_p0030_k004','history_book_01_p0031_k004','history_book_01_p0035_k002','history_book_01_p0036_k001','history_book_01_p0038_k003']:
  print('\nK',k['id'],k['title'],k['evidence_block_ids'],k['summary'])
