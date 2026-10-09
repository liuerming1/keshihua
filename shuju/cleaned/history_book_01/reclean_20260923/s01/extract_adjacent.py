import pdfplumber
p='shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf'
with pdfplumber.open(p) as d:
 for n in [37,38,39]:
  t=d.pages[n-1].extract_text() or ''
  print('---PAGE',n,'---\n',t[:8000])
