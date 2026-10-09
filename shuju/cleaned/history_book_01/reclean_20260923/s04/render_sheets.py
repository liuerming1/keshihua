from pathlib import Path
import pdfplumber
from PIL import Image,ImageOps,ImageDraw
pdf='shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf'
out=Path('shuju/cleaned/history_book_01/reclean_20260923/s04')
with pdfplumber.open(pdf) as doc:
 pages=list(range(113,150))
 for i in range(0,len(pages),6):
  nums=pages[i:i+6]
  imgs=[]
  for n in nums:
   im=doc.pages[n-1].to_image(resolution=72).original.convert('RGB')
   im.thumbnail((500,710))
   canvas=Image.new('RGB',(520,750),'white'); canvas.paste(im,((520-im.width)//2,30))
   ImageDraw.Draw(canvas).text((12,8),f'PDF page {n}',fill='black')
   imgs.append(canvas)
  sheet=Image.new('RGB',(520*3,750*2),(210,210,210))
  for j,im in enumerate(imgs): sheet.paste(im,((j%3)*520,(j//3)*750))
  sheet.save(out/f'visual_{nums[0]}_{nums[-1]}.jpg',quality=88)
 print('rendered sheets',len(list(out.glob('visual_*.jpg'))))
