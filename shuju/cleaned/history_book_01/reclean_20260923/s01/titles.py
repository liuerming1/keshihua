import json,re
from pathlib import Path
D=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf8'))
for p in range(8,39):
 xs=[k for k in D['knowledge'] if re.search(fr'_p{p:04d}_',k['id'])]
 if xs: print(f'P{p:04d}: '+ ' || '.join(k['id'].split('_')[-1]+':'+k['title'] for k in xs))
