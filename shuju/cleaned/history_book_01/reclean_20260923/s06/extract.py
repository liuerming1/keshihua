import json, pdfplumber, hashlib
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
d=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
pdf=pdfplumber.open('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf')
print('PDF pages',len(pdf.pages))
for i in range(180,223):
    t=pdf.pages[i].extract_text() or ''
    (root/'s06'/f'p{i+1:03}.txt').write_text(t,encoding='utf-8')
    print(f'\n### PDF {i+1} ###\n{t}')
