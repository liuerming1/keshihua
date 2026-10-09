import pdfplumber
p='shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf'
with pdfplumber.open(p) as d:
 pg=d.pages[37]
 for w in pg.extract_words(x_tolerance=1,y_tolerance=2,keep_blank_chars=False):
  if any(x in w['text'] for x in ['族属','匈奴','羯','氐','羌','前赵','北凉','后赵','前秦','后凉','后秦','成汉','鲜卑','前燕','汉','前凉']):print(w['text'],round(w['x0'],1),round(w['x1'],1),round(w['top'],1),round(w['bottom'],1))
