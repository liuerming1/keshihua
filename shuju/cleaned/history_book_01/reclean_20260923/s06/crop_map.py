from pathlib import Path
from PIL import Image
p=Path('shuju/cleaned/history_book_01/reclean_20260923/primary/ocr/history_book_01_p0030_a001_pdf600.png')
im=Image.open(p); w,h=im.size
for name,box in [('tl',(0,0,w//2,h//2)),('tr',(w//2,0,w,h//2)),('bl',(0,h//2,w//2,h)),('br',(w//2,h//2,w,h))]: im.crop(box).save(p.parent/f'p0030_map_{name}.png')
