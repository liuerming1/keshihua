from PIL import Image
from pathlib import Path
im=Image.open('shuju/cleaned/history_book_01/reclean_20260923/s01/page_38_240dpi.png')
for name,box in [('upper_groups',(1260,740,1820,920)),('lower_groups',(1260,900,1820,1120))]:
 x=im.crop(box);x.resize((x.width*5,x.height*5)).save(Path('shuju/cleaned/history_book_01/reclean_20260923/s01')/(name+'.png'))
