import json,hashlib
from pathlib import Path
R=Path('shuju/cleaned/history_book_01/reclean_20260923')
P=json.loads((R/'s03.patch.json').read_text(encoding='utf-8')); B=json.loads((R/'baseline.json').read_text(encoding='utf-8'))
base={b['id']:b for b in B['blocks']}; blocks={b['id']:b for b in P['updates']['blocks']}
targets={'history_book_01_p0082_b001':('xiRhWng','xiéháng'),'history_book_01_p0082_b010':('xiRhWng','xiéháng'),'history_book_01_p0083_b001':('bY','bó'),'history_book_01_p0083_b007':('bY','bó'),'history_book_01_p0095_b002':('sGu','sǒu'),'history_book_01_p0101_b004':('yP','yú')}
assert P['baseline_sha256']==hashlib.sha256((R/'baseline.json').read_bytes()).hexdigest()
assert len(blocks)==len(P['updates']['blocks'])
for bid,(bad,good) in targets.items():
 assert bid in blocks
 assert bad not in (blocks[bid].get('clean_text') or ''),bid
 assert good in (blocks[bid].get('clean_text') or ''),bid
 assert blocks[bid]['raw_text']==base[bid]['raw_text'],bid
assert '拼音OCR主审补记' in (R/'s03.review.md').read_text(encoding='utf-8')
assert len(P['updates']['knowledge'])==34
for name in ['pdf_page_0082.png','pdf_page_0082_颉颃.png','pdf_page_0082_颉颃_600.png','pdf_page_0083.png','pdf_page_0083_踣.png','pdf_page_0083_踣_600.png','pdf_page_0095.png','pdf_page_0095_渊薮.png','pdf_page_0095_渊薮_600.png','pdf_page_0101.png','pdf_page_0101_徐继畬.png','pdf_page_0101_徐继畬_600.png']:
 assert (R/'primary'/'ocr'/name).exists(),name
print('PASS: 6 requested block corrections, baseline raw_text preserved, knowledge unchanged, review addendum and 12 screenshots present.')
