import json
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923')
ids={'history_book_01_p0030_a001','history_book_01_p0032_a001','history_book_01_p0038_a002','history_book_01_p0157_a001','history_book_01_p0178_a003','history_book_01_p0182_a001'}
for fn in sorted(R.glob('s*.patch.json')):
 d=json.loads(fn.read_text(encoding='utf-8'))
 for a in d.get('updates',{}).get('assets',[]):
  if a['id'] in ids: print(fn.name,a['id'],a.get('file_path'),a.get('visible_text'),a.get('notes'))
