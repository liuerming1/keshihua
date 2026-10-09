import json,re
from pathlib import Path
from pypdf import PdfReader
root=Path('shuju/cleaned/history_book_01/reclean_20260923'); sf=root/'s01'; f=root/'s01.patch.json'
p=json.loads(f.read_text(encoding='utf-8'))
# Capture the exact PDF text-layer span, retaining the extracted line wraps.
pdf=PdfReader('shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf')
page_text=pdf.pages[36].extract_text() or ''
start='东晋北边的疆域，大致到淮水为止。'
end='覆亡大局已定。'
a=page_text.index(start); z=page_text.index(end,a)+len(end)
raw=page_text[a:z]
expected='东晋北边的疆域，大致到淮水为止。东晋南朝之交，一度将势力范围扩展到黄河南岸附近，但随后在军事上渐处下风，又退回到淮水一线。到陈朝，只能保有长江以南，上游又丢掉了四川和荆襄，在南北对峙中处于明显劣势，覆亡大局已定。'
assert re.sub(r'\s+','',raw)==expected,repr(raw)
# Correct the new block to raw PDF text, with a layout-cleaned but lexically faithful clean_text.
b=next(b for b in p['updates']['blocks'] if b['id']=='history_book_01_p0037_b009')
b['raw_text']=raw
b['clean_text']=expected
b['notes']=[
 'raw_text为PDF第37页文字层按原行序截取，原标点、字词及换行保留；已与240dpi页面渲染图逐字核对。',
 'clean_text仅合并版面换行，不改写“在军事上渐处下风”等原文措辞。'
]
# Read the enlarged page-38 table by row groups.
table=next(b for b in p['updates']['blocks'] if b['id']=='history_book_01_p0038_b009')
table['clean_text']='十六国统治者族属表：匈奴—前赵、北凉、夏；羯—后赵；氐—前秦、后凉；羌—后秦、成汉；鲜卑—前燕、后燕、南燕、南凉、西秦；汉—前凉、北燕、西凉。'
table['notes']=[
 '据PDF第38页240dpi渲染图并单独放大表格逐格核对。表头/合并单元格对应为：匈奴栏含前赵、北凉、夏；羯栏含后赵；氐栏含前秦、后凉；羌栏含后秦、成汉；鲜卑栏含前燕、后燕、南燕、南凉、西秦；汉栏含前凉、北燕、西凉。',
 '原raw_text保留baseline的初次提取值；本次更正仅写入clean_text，并记录羌、氐分组与初次提取不同。'
]
# Table reading is resolved; restore page image status and remove its blocking issue/open item.
for page in p['updates']['pages']:
 if page['pdf_page_number']==38:
  page['image_status']='complete'
  page['notes']=[n for n in page.get('notes',[]) if '十六国族属表的小字单元格未能逐格可靠识读' not in n and '族属表的字体较小' not in n]
  page['notes'].append('第38页十六国族属表已240dpi放大逐格识读并核对，族属对应写入p0038_b009.clean_text。')
p['updates']['review_issues']=[x for x in p['updates']['review_issues'] if x['id']!='history_book_01_s01_issue_table_p0038']
p['open_items']=[x for x in p['open_items'] if 'history_book_01_p0038_b009' not in x.get('record_ids',[])]
# Update human audit note with exact provenance and the corrected table interpretation.
audit=next(x for x in p['knowledge_audit'] if x['id']=='history_book_01_p0037_k001')
audit['note']+=' 新增p0037_b009现以PDF文字层原文及换行保存，并经240dpi原页逐字核对；此前把“在军事上渐处下风”概括为“军事转弱”已纠正为原句。'
for k in p['updates']['knowledge']:
 if k['id']=='history_book_01_p0037_k001':
  for c in k['points']:
   if '淮水' in c['text']:
    c['text']=expected
  k['reclean_review']['note']=audit['note']+' 仍有待核事项，见open_items/split_proposals。'
p['updates']['knowledge']=[next(k for k in p['updates']['knowledge'] if k['id']==a['id']) for a in p['knowledge_audit']]
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'p37_raw_text':raw,'table_clean_text':table['clean_text'],'image_status':next(x['image_status'] for x in p['updates']['pages'] if x['pdf_page_number']==38),'open_items':len(p['open_items']),'issues':len(p['updates']['review_issues'])},ensure_ascii=False,indent=2))
