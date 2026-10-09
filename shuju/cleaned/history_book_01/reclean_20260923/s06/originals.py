import json
from pathlib import Path
d=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8'))
for i in ['history_book_01_p0188_k002','history_book_01_p0189_k003','history_book_01_p0190_k001','history_book_01_p0211_k021']:
 k=next(x for x in d['knowledge'] if x['id']==i)
 print('\n',i); print(json.dumps(k,ensure_ascii=False,indent=2))
