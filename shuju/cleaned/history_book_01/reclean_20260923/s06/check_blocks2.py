import json,re
from pathlib import Path
P=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/s06.patch.json').read_text(encoding='utf-8'))
ids=[b['id'] for b in P['updates']['blocks']]
print(len(ids)); print([(x, bool(re.search(r'_p(\d{4})_b',x))) for x in ids[-12:]])
print(sorted({int(re.search(r'_p(\d{4})_b',x).group(1)) for x in ids}))
