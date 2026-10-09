import pdfplumber
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
root=Path('shuju/cleaned/history_book_01/reclean_20260923/s06')
pdf=pdfplumber.open('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf')
thumbs=[]
for n in range(187,224):
 im=pdf.pages[n-1].to_image(resolution=55).original.convert('RGB')
 im.thumbnail((250,330))
 tile=Image.new('RGB',(270,365),'white'); tile.paste(im,((270-im.width)//2,25)); ImageDraw.Draw(tile).text((8,5),f'PDF {n}',fill='black')
 thumbs.append(tile)
for j in range(0,len(thumbs),8):
 group=thumbs[j:j+8]; sheet=Image.new('RGB',(270*4,365*2),'#ddd')
 for i,im in enumerate(group): sheet.paste(im,((i%4)*270,(i//4)*365))
 sheet.save(root/f'contact_{j//8+1}.png')
