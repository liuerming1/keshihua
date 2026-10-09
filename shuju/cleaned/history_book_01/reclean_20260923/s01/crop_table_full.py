from PIL import Image
from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s01/page_38_240dpi.png'); im=Image.open(p)
for name,box in [('table_full',(1250,650,1830,1500)),('table_lower',(1250,930,1830,1500))]:
 crop=im.crop(box); crop.resize((crop.width*3,crop.height*3)).save(p.with_name(name+'.png'))
