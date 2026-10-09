import json,re
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
d=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
for b in d['blocks']:
 m=re.search(r'_p(\d{4})_b',b['id'])
 if not m or not 187<=int(m.group(1))<=223: continue
 raw=b.get('raw_text') or ''; clean=b.get('clean_text') or ''
 if re.search(r'NÅO|N.A.O|ÅO|AO|N[\s\u00a0]*Å[\s\u00a0]*O',clean,re.I) or ('Å' in clean) or ('NÅ' in clean):
  print(b['id'],'TYPE',b.get('type'),'RAW',raw[:220].replace('\n',' '),'CLEAN',clean[:300].replace('\n',' '))
