import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923');f=root/'s01.patch.json';p=json.loads(f.read_text(encoding='utf8'))
b=next(b for b in p['updates']['blocks'] if b['id']=='history_book_01_p0038_b009')
b['clean_text']='十六国统治者族属表：匈奴—前赵、北凉、夏；羯—后赵；氐—前秦、后凉；羌—后秦；賨（cóng）—成汉；鲜卑—前燕、后燕、南燕、南凉、西秦；汉—前凉、北燕、西凉。'
b['table_data']={'columns':['族属','政权'],'rows':[
 ['匈奴','前赵'],['匈奴','北凉'],['匈奴','夏'],['羯','后赵'],['氐','前秦'],['氐','后凉'],['羌','后秦'],['賨（cóng）','成汉'],
 ['鲜卑','前燕'],['鲜卑','后燕'],['鲜卑','南燕'],['鲜卑','南凉'],['鲜卑','西秦'],['汉','前凉'],['汉','北燕'],['汉','西凉']],
 'notes':['按PDF表格合并表头还原族属分组；“羌”栏为后秦，“賨（cóng）”栏为成汉，不合并两栏。']}
b['notes']=[
 '据PDF第38页240dpi渲染图并单独放大表格逐格核对。合并表头对应：匈奴栏前赵、北凉、夏；羯栏后赵；氐栏前秦、后凉；羌栏后秦；賨（cóng）栏成汉；鲜卑栏前燕、后燕、南燕、南凉、西秦；汉栏前凉、北燕、西凉。',
 '原raw_text保留baseline初次提取值；本次修正clean_text和table_data，区分羌与賨两组。'
]
# Correct accurate audit prose and prior erroneous review statements.
g=root/'s01'/'review_final.py';s=g.read_text(encoding='utf8')
s=s.replace('羌对应后秦、成汉','羌对应后秦、賨（cóng）对应成汉')
s=s.replace('羌—后秦、成汉','羌—后秦、賨（cóng）—成汉')
g.write_text(s,encoding='utf8')
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print(b['clean_text'])
