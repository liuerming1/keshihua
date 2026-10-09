import json,re
from pathlib import Path
d=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8'))
for b in d['blocks']:
 m=re.search(r'_p(\d{4})_b',b['id'])
 if m and 187<=int(m.group(1))<=223 and 'NÅO' in (b.get('clean_text') or ''):
  print(m.group(1),b['id'],len(b['clean_text']),repr(b['clean_text'][-50:]))
