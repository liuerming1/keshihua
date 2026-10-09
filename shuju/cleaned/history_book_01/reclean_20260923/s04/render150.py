from pathlib import Path
import pdfplumber
p='shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf'; o=Path('shuju/cleaned/history_book_01/reclean_20260923/s04/p150.png')
with pdfplumber.open(p) as d: d.pages[149].to_image(resolution=100).save(o,format='PNG')
print(o)
