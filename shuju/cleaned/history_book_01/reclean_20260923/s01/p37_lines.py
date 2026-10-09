import pdfplumber
p='shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf'
with pdfplumber.open(p) as d:
 pg=d.pages[36]
 for line in pg.extract_text_lines():
  if any(x in line['text'] for x in ['东晋北边','一度将势力','处下风','覆亡大局']):print(line)
