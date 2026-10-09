import json
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923'); p=json.loads((R/'s03.patch.json').read_text(encoding='utf-8')); b=json.loads((R/'baseline.json').read_text(encoding='utf-8'))
print('updates blocks ids:')
for x in p['updates']['blocks']: print(x['id'])
want=['history_book_01_p0082_b001','history_book_01_p0082_b010','history_book_01_p0083_b001','history_book_01_p0083_b007','history_book_01_p0095_b002','history_book_01_p0101_b004']
base={x['id']:x for x in b['blocks']}; patch={x['id']:x for x in p['updates']['blocks']}
for id in want:
 x=patch.get(id,base.get(id)); print('\n',id,'in patch',id in patch,'raw',repr((x.get('raw_text') or '')[:800]),'clean',repr((x.get('clean_text') or '')[:800]))
