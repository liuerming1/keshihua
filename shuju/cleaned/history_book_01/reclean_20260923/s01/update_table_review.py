import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923');f=root/'s01.patch.json';p=json.loads(f.read_text(encoding='utf8'))
b=next(b for b in p['updates']['blocks'] if b['id']=='history_book_01_p0038_b009')
b['table_data']={'columns':['族属','政权'],'rows':[
 ['匈奴','前赵'],['匈奴','北凉'],['匈奴','夏'],['羯','后赵'],
 ['氐','前秦'],['氐','后凉'],['羌','后秦'],['羌','成汉'],
 ['鲜卑','前燕'],['鲜卑','后燕'],['鲜卑','南燕'],['鲜卑','南凉'],['鲜卑','西秦'],
 ['汉','前凉'],['汉','北燕'],['汉','西凉']
 ],'notes':['据PDF第38页放大表格恢复合并表头的逐行对应关系；原图依族属分组，规范化为族属/政权两列。']}
p['updates']['blocks']=[b if x['id']==b['id'] else x for x in p['updates']['blocks']]
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
# Fix the review generator so a future regeneration keeps the corrected visual evidence and status.
g= root/'s01'/'review_final.py';s=g.read_text(encoding='utf8')
s=s.replace('所有raw_text保留原值。','既有源块raw_text未改；新增p0037_b009的raw_text为PDF文字层原行序文本。')
s=s.replace('第38页十六国族属表字较小，格内对应关系未逐格确认，page.image_status设为partial，并保留待核issue。','第38页族属表以240dpi单页渲染并单独放大，逐格核对“羌—后秦、成汉”等对应，page.image_status为complete；图像文件page_38_table.png保留复核证据。')
s=s.replace("'- 第38页十六国族属表的羌族和政权对应需放大原页逐格确认。',", "'- 第38页十六国族属表已放大逐格核对：羌对应后秦、成汉；clean_text及table_data已修正。',")
s=s.replace('第37页补录缺失的页末疆域正文，第38页补充地图/表格说明。','第37页按PDF逐字补录缺失的页末疆域正文，第38页复核地图及族属表格。')
g.write_text(s,encoding='utf8')
