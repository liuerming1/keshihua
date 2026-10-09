import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923'); f=root/'s01.patch.json';p=json.loads(f.read_text(encoding='utf8'))
for k in p['updates']['knowledge']:
 for fld in ('flow','points'):
  if isinstance(k.get(fld),dict):k[fld]=[k[fld]]
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
