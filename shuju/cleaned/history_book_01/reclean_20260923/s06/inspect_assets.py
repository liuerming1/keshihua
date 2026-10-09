import json
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923')
D=json.loads((R/'baseline.json').read_text(encoding='utf-8'))
ids=['history_book_01_p0030_a001','history_book_01_p0032_a001','history_book_01_p0038_a002','history_book_01_p0157_a001','history_book_01_p0178_a003','history_book_01_p0182_a001']
assets={a['id']:a for a in D['assets']}
for aid in ids:
 print('\n###',aid,'present',aid in assets)
 if aid in assets: print(json.dumps(assets[aid],ensure_ascii=False,indent=2))
