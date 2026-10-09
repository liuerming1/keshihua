import json
from pathlib import Path
d=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8'))
want={'history_book_01_p0082_b001','history_book_01_p0082_b010','history_book_01_p0083_b001','history_book_01_p0083_b007','history_book_01_p0095_b002','history_book_01_p0101_b004'}
for b in d['blocks']:
 if b['id'] in want: print(b['id'],'type',b.get('type'),'bbox',b.get('bbox'),'page',b.get('page_id'),'text',repr(b.get('clean_text')))
