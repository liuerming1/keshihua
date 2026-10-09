import json,re
from pathlib import Path
d=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8'))
for b in d['blocks']:
 s=(b.get('clean_text') or '')
 if any(x in s for x in ['xiRhWng','bY','sGu','yP']): print(b['id'],repr(s[:500]))
