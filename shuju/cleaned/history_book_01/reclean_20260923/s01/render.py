import pdfplumber
from PIL import Image, ImageDraw
from pathlib import Path
pdf=Path('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf')
out=Path('shuju/cleaned/history_book_01/reclean_20260923/s01')
with pdfplumber.open(pdf) as doc:
    for start in range(1,39,5):
        imgs=[]
        for n in range(start,min(start+5,39)):
            im=doc.pages[n-1].to_image(resolution=68).original.convert('RGB')
            im.thumbnail((520,740))
            tile=Image.new('RGB',(540,780),'white');tile.paste(im,((540-im.width)//2,28))
            ImageDraw.Draw(tile).text((10,5),f'PDF page {n}',fill='black')
            imgs.append(tile)
        sheet=Image.new('RGB',(540*2,780*3),'#d8d8d8')
        for i,im in enumerate(imgs):sheet.paste(im,((i%2)*540,(i//2)*780))
        sheet.save(out/f'visual_{start:02}_{min(start+4,38):02}.png')
print('rendered contact sheets 1-38')
