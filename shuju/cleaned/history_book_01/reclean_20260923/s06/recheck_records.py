import json
from pathlib import Path
d=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8'))
for kid in ['history_book_01_p0207_k003','history_book_01_p0211_k021']:
 k=next(x for x in d['knowledge'] if x['id']==kid); print(kid,k['evidence_block_ids'],k.get('summary'),k.get('points'),k['time'])
 for bid in k['evidence_block_ids']:
  b=next(x for x in d['blocks'] if x['id']==bid); print(bid,b.get('clean_text','')[:1100])
