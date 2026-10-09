import json,unicodedata,re
from pathlib import Path
d=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/baseline.json').read_text(encoding='utf-8'))
for b in d['blocks']:
 m=re.search(r'_p(\d{4})_b',b['id'])
 if not m or not 187<=int(m.group(1))<=223:continue
 for key in ['raw_text','clean_text']:
  s=b.get(key) or ''
  if 'Å' in s or 'Ã' in s or 'NÃO' in s or 'NÅO' in s or 'N A O' in s or 'NAO' in s:
   print(b['id'],key,repr(s[-400:]))
