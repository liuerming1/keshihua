import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923'); f=root/'s01.patch.json';p=json.loads(f.read_text(encoding='utf8'))
for page in p['updates']['pages']:
 if page['pdf_page_number']==38:
  page['notes']=[n for n in page['notes'] if '低分辨率地图小字或表格单元格未作几何/逐字推断' not in n]
  page['notes'].append('地图像素不作疆域几何数字化；十六国族属表已放大至240dpi并逐格核对。')
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
g=root/'s01'/'review_final.py';s=g.read_text(encoding='utf8')
s=s.replace('图像文件page_38_table.png保留复核证据。','图像证据保存在s01/page_37_border_paragraph.png和s01/page_38_table_crop.png。')
g.write_text(s,encoding='utf8')
