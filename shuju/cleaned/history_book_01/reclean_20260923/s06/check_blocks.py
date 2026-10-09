import json
from pathlib import Path
P=json.loads(Path('shuju/cleaned/history_book_01/reclean_20260923/s06.patch.json').read_text(encoding='utf-8'))
print(sorted({int(b['id'].split('_p')[1][:4]) for b in P['updates']['blocks']}))
print([(b['id'],b.get('clean_text','')[-40:]) for b in P['updates']['blocks'] if 'NÅO' in b.get('clean_text','')])
