import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923');f=root/'s01.patch.json';p=json.loads(f.read_text(encoding='utf8'))
block_id='history_book_01_p0037_b009'
text='东晋北边疆域大致至淮水；东晋南朝之交一度将势力范围扩至黄河南岸附近，后因军事上转弱又退至淮水一线。到陈朝，仅保有长江以南，上游失去四川和荆襄，在南北对峙中处于明显劣势，覆亡大局已定。'
if not any(b['id']==block_id for b in p['updates']['blocks']):
 p['updates']['blocks'].append({'id':block_id,'page_id':'history_book_01_p0037','order':9,'type':'paragraph','bbox':None,'raw_text':text,'clean_text':text,'asset_ids':[],'table_data':None,'notes':['s01复核PDF页序37，补录baseline遗漏的页面末段正文；按独立源块记录，不拼入相邻页或exercise块。']})
k=next(k for k in p['updates']['knowledge'] if k['id']=='history_book_01_p0037_k001')
claim={'text':'东晋北边大致至淮水；东晋南朝之交曾扩至黄河南岸后退回淮水。至陈朝仅保有长江以南，且失去四川和荆襄，在对峙中明显处于劣势。','evidence_block_ids':[block_id]}
k['points']=[c for c in k.get('points',[]) if not (isinstance(c,dict) and c.get('evidence_block_ids')==[block_id])]+[claim]
if block_id not in k['evidence_block_ids']:k['evidence_block_ids'].append(block_id)
a=next(a for a in p['knowledge_audit'] if a['id']==k['id']);a['evidence_block_ids']=k['evidence_block_ids'];a['decision']='needs_review'
a['note']+=' 第37页原知识块缺失页末“东晋北边疆域…陈朝仅保有长江以南”段，现依PDF增补独立源块p0037_b009，并将范围变化列为points；条目时间仍不推算南朝结束年。'
k['reclean_review']['status']='needs_review';k['reclean_review']['note']=a['note']+' 仍有待核事项，见open_items/split_proposals。'
# Correct the carryover record locator: baseline attached the continuation to the archaeology paragraph b008.
for c in p['carryover_review']:
 if c['index']==6:
  c['reason']='第38页有关北魏孝文帝改革的正文在“鲜”字处续到第39页“卑贵族一律将籍贯改为洛阳”。基线把该carryover误指p0038_b008（嘎仙洞考古段，该段在38页已完整结束）；实际续接证据是p0038_b002与p0039_b001。北魏知识已引用这两块，原页块不合并。'
# Record the supplementation and unresolved split in detailed notes.
p['open_items'].append({'record_ids':['history_book_01_p0037_k001'],'reason':'页末疆域变化已补入独立源块及知识要点，但本条同时含317年东晋建立与420年刘裕改国号宋，建议拆分；教材以“此后170年间”概述南朝而未给结束年。','next_action':'若执行拆分，分别迁移两条事件摘要/地点/人物；保留p0037_b009只支撑南北疆域变化，不推算终年。'})
p['updates']['knowledge']=[k if x['id']==k['id'] else x for x in p['updates']['knowledge']]
p['updates']['blocks'].sort(key=lambda b:(int(b['id'].split('_p')[1][:4]), b.get('order',0)))
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print('added page 37 omitted source paragraph')
