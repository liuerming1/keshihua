from PIL import Image
from pathlib import Path
s=Path('shuju/cleaned/history_book_01/reclean_20260923/s01')
Image.open(s/'table_full.png').save(s/'page_38_table_crop.png')
