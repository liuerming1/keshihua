import pdfplumber
from pathlib import Path
from PIL import Image
p=Path('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf'); out=Path('shuju/cleaned/history_book_01/reclean_20260923/s01')
with pdfplumber.open(p) as d:
 for n in (37,38):
  im=d.pages[n-1].to_image(resolution=240).original
  im.save(out/f'page_{n}_240dpi.png')
  print('saved',n,im.size)
