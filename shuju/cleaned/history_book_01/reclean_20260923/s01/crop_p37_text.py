from PIL import Image
from pathlib import Path
im=Image.open('shuju/cleaned/history_book_01/reclean_20260923/s01/page_37_240dpi.png')
box=(350,2200,1850,2670); x=im.crop(box); x.resize((x.width*2,x.height*2)).save(Path('shuju/cleaned/history_book_01/reclean_20260923/s01/page_37_border_paragraph.png'))
