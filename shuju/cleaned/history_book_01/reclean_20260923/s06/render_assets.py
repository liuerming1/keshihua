import json
from pathlib import Path
import pdfplumber
from PIL import Image
R=Path('shuju/cleaned/history_book_01/reclean_20260923'); D=json.loads((R/'baseline.json').read_text(encoding='utf-8'))
ids=['history_book_01_p0030_a001','history_book_01_p0032_a001','history_book_01_p0038_a002','history_book_01_p0157_a001','history_book_01_p0178_a003','history_book_01_p0182_a001']; A={a['id']:a for a in D['assets']}
pdf=pdfplumber.open('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf'); out=R/'primary'/'ocr'; out.mkdir(parents=True,exist_ok=True)
for aid in ids:
 a=A[aid]; n=a['export']['pdf_page_number']; page=pdf.pages[n-1]
 im=page.to_image(resolution=600).original.convert('RGB')
 x0,y0,x1,y1=a['bbox']; box=(int(x0*im.width),int(y0*im.height),int(x1*im.width),int(y1*im.height))
 crop=im.crop(box); crop.save(out/f'{aid}_pdf600.png')
 print(aid,n,im.size,box,crop.size)
