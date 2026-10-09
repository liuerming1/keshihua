from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s06/make_patch.py')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("(out/'s06.patch.json')", "(root/'s06.patch.json')")
s=s.replace("(out/'s06.review.md')", "(root/'s06.review.md')")
p.write_text(s,encoding='utf-8')
