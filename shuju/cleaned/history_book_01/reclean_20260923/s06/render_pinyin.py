from pathlib import Path
import pdfplumber
from PIL import Image,ImageOps,ImageDraw
root=Path('shuju/cleaned/history_book_01/reclean_20260923/primary/ocr')
pdf=pdfplumber.open('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf')
terms={82:['颉颃'],83:['踣'],95:['渊薮'],101:['徐继畬']}
for n, words in terms.items():
 page=pdf.pages[n-1]
 im=page.to_image(resolution=300).original.convert('RGB')
 im.save(root/f'pdf_page_{n:04d}.png')
 # Find the exact printed term + nearby pinyin, then save a large contextual crop.
 for w in words:
  hits=page.search(w, regex=False)
  print('page',n,'word',w,'hits',[(h['x0'],h['top'],h['x1'],h['bottom']) for h in hits])
  if not hits: continue
  h=hits[0]; scale=300/72
  # crop about two lines around matched word, preserving enough context to see diacritics
  x0=max(0,int((h['x0']-30)*scale)); x1=min(im.width,int((h['x1']+160)*scale))
  y0=max(0,int((h['top']-20)*scale)); y1=min(im.height,int((h['bottom']+65)*scale))
  crop=im.crop((x0,y0,x1,y1))
  crop.save(root/f'pdf_page_{n:04d}_{w}.png')
