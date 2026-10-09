import pdfplumber
p='shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf'
with pdfplumber.open(p) as pdf:
 print('total pages',len(pdf.pages))
 for n in [112,113,116,117,118,121,122,123,128,129,130,131,132,133,136,137,138,140,141,142,149,150]:
  pg=pdf.pages[n-1]
  print('\n--- PDF PAGE',n,'size',pg.width,pg.height,'---\n', (pg.extract_text(layout=False) or '')[:5000])
