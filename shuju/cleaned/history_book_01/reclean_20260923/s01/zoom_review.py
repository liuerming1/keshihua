from PIL import Image
from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s01/page_38_240dpi.png'); im=Image.open(p)
# Crop the table from the rendered page and enlarge it for character-level verification.
box=(1260,680,1820,1110); crop=im.crop(box)
crop.resize((crop.width*3,crop.height*3)).save(p.with_name('page_38_table_crop.png'))
from pypdf import PdfReader
pdf=PdfReader('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf')
t=pdf.pages[36].extract_text() or ''
print('PAGE37_EXTRACT_TAIL:\n'+t[-1600:])
