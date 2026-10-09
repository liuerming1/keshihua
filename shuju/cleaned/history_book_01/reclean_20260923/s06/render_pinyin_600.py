from pathlib import Path
import pdfplumber
root=Path('shuju/cleaned/history_book_01/reclean_20260923/primary/ocr')
pdf=pdfplumber.open('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf')
for n,w in [(82,'颉颃'),(83,'踣'),(95,'渊薮'),(101,'徐继畬')]:
 page=pdf.pages[n-1]; im=page.to_image(resolution=600).original.convert('RGB'); h=page.search(w)[0]; sc=600/72
 x0=max(0,int((h['x0']-20)*sc)); x1=min(im.width,int((h['x1']+105)*sc)); y0=max(0,int((h['top']-5)*sc)); y1=min(im.height,int((h['bottom']+25)*sc))
 im.crop((x0,y0,x1,y1)).save(root/f'pdf_page_{n:04d}_{w}_600.png')
