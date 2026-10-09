from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s06/validate_final.py')
s=p.read_text(encoding='utf-8-sig').replace("==set(range(187,224))", "==set(range(187,215))").replace("'37 watermark clean_text updates/raw_text preservation'", "'37 watermark block clean_text updates across 28 pages/raw_text preservation'")
p.write_text(s,encoding='utf-8')
