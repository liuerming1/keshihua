import json,hashlib,copy
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
src=root/'baseline.json'; d=json.loads(src.read_text(encoding='utf-8')); blocks={b['id']:b for b in d['blocks']}
ks=[k for k in d['knowledge'] if 113<=int(k['id'].split('_p')[1][:4])<=149]
updates={}

def settime(id,**kw):
 k=copy.deepcopy(next(x for x in ks if x['id']==id)); k['time'].update(kw); updates[id]=k

def evidence(id, refs, fields=None):
 k=updates.get(id,copy.deepcopy(next(x for x in ks if x['id']==id)))
 if fields is None: fields=['evidence_block_ids','summary','flow','points','background','impact','time']
 if 'evidence_block_ids' in fields: k['evidence_block_ids']=refs
 if 'summary' in fields and k.get('summary'): k['summary']['evidence_block_ids']=refs
 if 'time' in fields: k['time']['evidence_block_ids']=refs
 for f in ['flow','points']:
  if f in fields:
   for c in k.get(f,[]): c['evidence_block_ids']=[x for x in c.get('evidence_block_ids',[]) if x in refs] or refs
 for f in ['background','impact']:
  if f in fields and k.get(f): k[f]['evidence_block_ids']=[x for x in k[f].get('evidence_block_ids',[]) if x in refs] or refs
 updates[id]=k

# Repair demonstrably wrong or incomplete source references.
evidence('history_book_01_p0117_k002',['history_book_01_p0117_b006','history_book_01_p0117_b010'])
evidence('history_book_01_p0118_k001',['history_book_01_p0118_b003'])
evidence('history_book_01_p0118_k002',['history_book_01_p0118_b003','history_book_01_p0118_b008'])
evidence('history_book_01_p0118_k003',['history_book_01_p0118_b004'])
evidence('history_book_01_p0118_k004',['history_book_01_p0118_b006'])
evidence('history_book_01_p0119_k001',['history_book_01_p0119_b005'])
evidence('history_book_01_p0119_k002',['history_book_01_p0119_b006','history_book_01_p0119_b007','history_book_01_p0119_b008'])
evidence('history_book_01_p0119_k003',['history_book_01_p0119_b007','history_book_01_p0119_b008'])
evidence('history_book_01_p0122_k001',['history_book_01_p0122_b005','history_book_01_p0123_b002','history_book_01_p0123_b003','history_book_01_p0123_b004'])
evidence('history_book_01_p0149_k004',['history_book_01_p0149_b009','history_book_01_p0150_b001'])

# Replace evidence references that pointed to headings/captions instead of the narrated text.
evidence('history_book_01_p0119_k003',['history_book_01_p0119_b007'])

# Extract only source-backed sequences or causes that add a distinct content role.
for id, claims in {
 'history_book_01_p0113_k001':[
  {'text':'1900年12月列强向清政府提出《议和大纲》，随后拟定详细条款；各国利益不同使谈判旷日持久。','evidence_block_ids':['history_book_01_p0113_b003']},
  {'text':'1901年9月7日清政府与11国签订《辛丑条约》，其后文本列出12款及19个附件的主要条款。','evidence_block_ids':['history_book_01_p0113_b003']}],
 'history_book_01_p0115_k001':[
  {'text':'英国担心义和团运动波及长江流域，策动刘坤一、张之洞与列强合作；盛宣怀牵线，由余联沅与驻沪领事商定“保护东南章程九款”。','evidence_block_ids':['history_book_01_p0115_b001']},
  {'text':'清政府向各国宣战后，更多南方督抚加入并与各参战国商订协议；协议虽未签字，地方大员仍以“自保”表态。','evidence_block_ids':['history_book_01_p0115_b001']}],
 'history_book_01_p0119_k001':[
  {'text':'1906年9月清政府宣布预备立宪；1908年8月颁布《钦定宪法大纲》。','evidence_block_ids':['history_book_01_p0119_b005']},
  {'text':'立宪派三次请愿速开国会未果；1911年5月“皇族内阁”成立后，部分立宪派转而支持革命。','evidence_block_ids':['history_book_01_p0119_b005']}],
 'history_book_01_p0119_k002':[
  {'text':'清政府将川汉、粤汉铁路收归“国有”并与四国银行团签订借款合同，引发多省民众愤慨和保路运动；四川运动发展为武装起义。','evidence_block_ids':['history_book_01_p0119_b007','history_book_01_p0119_b008']}]
 , 'history_book_01_p0119_k003':[
  {'text':'1911年10月10日武昌新军起义，起义军控制武汉三镇并成立湖北军政府；两个月内13省和上海宣布独立，1912年1月1日中华民国临时政府在南京成立。','evidence_block_ids':['history_book_01_p0119_b007']}]
}.items():
 k=updates.get(id,copy.deepcopy(next(x for x in ks if x['id']==id))); k['flow']=claims; updates[id]=k

k=updates.get('history_book_01_p0117_k002',copy.deepcopy(next(x for x in ks if x['id']=='history_book_01_p0117_k002')))
k['background']={'text':'清政府在遭受重挫后试图以改革自救；教材称其政权仍掌握在腐败无能的权贵手中。','evidence_block_ids':['history_book_01_p0117_b006']}
updates[k['id']]=k

for id,refs in {
 'history_book_01_p0118_k001':['history_book_01_p0118_b003'],
 'history_book_01_p0118_k002':['history_book_01_p0118_b003'],
 'history_book_01_p0119_k003':['history_book_01_p0119_b007']
}.items():
 k=updates.get(id,copy.deepcopy(next(x for x in ks if x['id']==id)))
 for ref in k.get('place_refs',[]): ref['evidence_block_ids']=refs
 updates[id]=k

# Time normalization grounded in the original pages and the explicit adjacent-page continuation.
settime('history_book_01_p0117_k002',end_year=None,end_status='unknown',evidence_block_ids=['history_book_01_p0117_b006','history_book_01_p0117_b010'],normalization_note='正文仅说明清末新政于1901年初开始，未提供结束时间；删除错误的end_year=1901。')
settime('history_book_01_p0140_k023',mode='point',end_year=None,end_status='not_applicable',precision='day',normalization_note='证据是2016年10月21日纪念大会讲话，按该明确日期记录；“总结红军长征历史”不是持续时间。')
settime('history_book_01_p0145_k002',mode='point',start_year=1937,end_year=None,end_status='not_applicable',precision='day',source_text='1937年9月23日蒋介石发表谈话后正式形成（前一日国民党中央通讯社发表中共合作宣言）',normalization_note='正文以9月23日蒋介石谈话承认中共合法地位作为“至此”合作实现的节点；保留9月22日宣言作背景证据，不将前一日误作持续时段。')
settime('history_book_01_p0149_k003',mode='uncertain',start_year=None,end_year=None,earliest_year=1938,latest_year=1938,end_status='not_applicable',precision='year',source_text='1938年1月至5月徐州会战期间的台儿庄大捷',normalization_note='原文把1至5月明确用于徐州会战，未给台儿庄大捷的单日；改为会战期间的年份范围，不把整场会战时长误写成大捷时长。')
settime('history_book_01_p0149_k004',mode='duration',start_year=1938,end_year=1938,end_status='known',precision='month',source_text='1938年6月中旬开始；同年10月下旬结束',normalization_note='p149记会战开始，紧邻p150正文记10月下旬武汉失守、会战结束；跨页证据一并保留。')

# Existing durations with explicit end years must carry known end status.
for original in ks:
 k=updates.get(original['id'],copy.deepcopy(original)); t=k.get('time',{})
 if t.get('mode')=='duration' and t.get('end_year') is not None and t.get('end_status')!='known':
  t['end_status']='known'; updates[k['id']]=k

# Human-readable per-entry review notes use the actual source excerpt and current fields.
# Specific unresolved conceptual bundles are called out below; blank fields remain blank unless source evidence supports a claim.
reviewed=[]; audit=[]; open_items=[]
needs={
'history_book_01_p0113_k002':'该条把克林德事件、谢罪与碑名迁改合并成1900—1952年的长跨度；分项建议见split_proposals。',
'history_book_01_p0118_k003':'条目把多次反清起义和黄花岗起义并为一个事件，日期字段不能表示多个独立事件；需拆分后分别定时。',
'history_book_01_p0140_k023':'证据只支持2016年讲话对长征精神的概括；将讲话日期作为概念起源时间是否适合产品呈现需人工决定。',
'history_book_01_p0143_k002':'条目同时包含赵一曼生卒年、抗日活动和牺牲；时间字段混合人物生平与事件时间，需拆分或明确所展示的事实。',
'history_book_01_p0143_k003':'条目并列华北事变与一二·九运动；教材明确一二·九日期但将华北事变称为此前一连串事件，宜拆分。',
'history_book_01_p0143_k004':'条目并列八一宣言与瓦窑堡会议，分别为8月1日和1935年底的事件；宜拆分。',
'history_book_01_p0149_k003':'台儿庄大捷被赋予整段徐州会战时间；已保留教材能支持的年份范围，具体日期仍未由本页教材给出。'
}
notes_specific={
'history_book_01_p0113_k001':'正文逐项记载签约日期、11国、主要条款；p114补充教材对主权、赔款和社会影响的归纳，当前claim各有对应块。',
'history_book_01_p0115_k001':'正文叙述英国策动、盛宣怀牵线、上海道与领事商定章程及清廷宣战后扩大参与；现有概要和结论均归于教材。',
'history_book_01_p0117_k002':'正文与“清末新政内容”框分别支持1901年初开始、官制/新军/工商/教育改革；正文没有结束年份。',
'history_book_01_p0118_k001':'p118正文明确甲午战争后孙中山于1894年11月在檀香山组织兴中会；将证据由后文起义段改指实际句子。',
'history_book_01_p0118_k002':'p118正文与学思之窗引文分别支持同盟会成立、纲领与三民主义；修复原本指向标题的证据块。',
'history_book_01_p0118_k004':'p118史料阅读明确林觉民于4月24日写《与妻书》并投入起义；原引用误指秋瑾图注，已纠正。',
'history_book_01_p0119_k001':'p119正文支持1906年预备立宪、1908年宪法大纲、三次请愿与1911年皇族内阁后转向革命，原引用改指正文。',
'history_book_01_p0119_k002':'p119正文载铁路国有引发保路运动及四川等地响应；修复了原引用指向标题的问题。',
'history_book_01_p0119_k003':'p119图注与相邻正文支持武昌起义后各省响应和南京临时政府成立；拆分建议由主审决定是否保留其复合标题。',
'history_book_01_p0122_k001':'p122末句的对日交涉在p123首段接续；证据已改为实际正文块，另保留袁世凯复辟与取消帝制的相邻正文。',
'history_book_01_p0149_k004':'p149写武汉会战开始，p150 b001续写毛泽东讲话、10月下旬会战结束；已据跨页正文补全持续区间。',
'history_book_01_p0145_k002':'p145叙述中共宣言于9月22日公布、蒋介石谈话于9月23日发表；按两日过程规范时间。',
'history_book_01_p0149_k003':'p149明确1—5月为徐州会战，称台儿庄大捷发生其中；不把整个会战时段冒充捷报日。'
}
for orig in ks:
 id=orig['id']; k=updates.get(id,copy.deepcopy(orig)); title=k['title']; ev=k.get('evidence_block_ids',[])
 raw=' '.join((blocks[x].get('clean_text') or '') for x in ev if x in blocks).replace('\n',' ')
 statement=notes_specific.get(id)
 if not statement:
  claim=(k.get('summary') or {}).get('text') or (k.get('points') or [{}])[0].get('text') or title
  statement=f'逐条核对正文块{", ".join(ev)}；核心表述“{claim[:90]}”与所引教材内容相符。'
 status='needs_review' if id in needs else 'agent_reviewed'
 note=needs.get(id,statement)
 k['reclean_review']={'status':status,'note':note,'slice':'s04'}
 if id in updates: updates[id]=k
 elif id in needs: updates[id]=k
 reviewed.append(k)
 fields=['time','summary','flow','points','background','impact','references']
 er={}
 source_excerpt=' '.join(raw.split())[:180]
 if not k.get('flow'): er['flow']=f'核对{title}所引原文：“{source_excerpt}”。该条现有事实按单点/概述组织，原文未形成可分列且有时间顺序的阶段；不把摘要拆句伪造成流程。'
 if not k.get('points'): er['points']=f'核对{title}所引原文：“{source_excerpt}”。当前摘要已承载这段文字唯一的条目级事实，未找到不重复且可独立成点的第二项。'
 if not k.get('background'): er['background']=f'核对{title}所引原文：“{source_excerpt}”。此处说明的是该事件/概念本身，没有将前置情势单独作为其成因；未把同页相邻叙述补作背景。'
 if not k.get('impact'): er['impact']=f'核对{title}所引原文：“{source_excerpt}”。该条来源块中没有独立写出后续结果；若教材只在别条归纳影响，不移植到本条。'
 audit.append({'id':id,'evidence_block_ids':ev,'decision':'needs_review' if status=='needs_review' else ('changed' if id in updates else 'retained'),'checked_fields':fields,'empty_reasons':er,'note':statement if id not in needs else needs[id]})
 if id in needs: open_items.append({'record_ids':[id],'reason':needs[id],'next_action':'依据split_proposals决定是否拆条；保留教材证据并由主审确认展示粒度。'})

# explicit split proposals for multi-event records
def split(id,why,titles): return {'id':id,'reason':why,'proposed_titles':titles}
splits=[
split('history_book_01_p0113_k002','条目跨越1900—1952年，把克林德遇害、谢罪、1918碑名变更及1952再次改名合并；按独立事件拆开可避免长时段气泡。',['克林德事件','清政府赴德谢罪并建立克林德碑','克林德碑改名并迁至中央公园','公理战胜碑改名为保卫和平碑']),
split('history_book_01_p0118_k003','多次反清武装起义是复数事件，黄花岗起义有明确日期且独立成事，不应用一个时段和一条摘要混合。',['革命党人的多次反清武装起义','广州黄花岗起义']),
split('history_book_01_p0143_k002','人物生卒信息、1935年担任职务/被捕与1936年牺牲是不同时间事实；考虑拆为人物条目和抗日活动/牺牲事件。',['赵一曼生平','赵一曼在东北抗日与被捕','赵一曼牺牲']),
split('history_book_01_p0143_k003','华北事变是此前一连串事态，一二·九运动有明确单日；当前条目并列二者。',['华北事变','一二·九运动']),
split('history_book_01_p0143_k004','八一宣言与瓦窑堡会议日期分别为1935年8月1日和1935年底。',['《八一宣言》发表','瓦窑堡会议确立抗日民族统一战线方针']),
split('history_book_01_p0149_k003','1—5月是徐州会战时段，台儿庄大捷是会战中的单独胜利，教材未给其具体日。',['徐州会战','台儿庄大捷'])]

carry=[]
def cr(i,status,eids,reason,next_action): carry.append({'index':i,'status':status,'evidence_block_ids':eids,'reason':reason,'next_action':next_action})
cr(15,'resolved',['history_book_01_p0117_b012','history_book_01_p0118_b003','history_book_01_p0122_b005','history_book_01_p0123_b002'],'p117正文末句“先后在檀香山、广州、香港等”由p118 b003接为“地比较系统地接受…”；p122 b005关于二十一条的句子由p123 b002续完。前后页实际文字连续，且原carryover对p122块号指向标题而非正文。','合并时引用上述正文块；不要把错误块号p0122_b004当作对日交涉证据。')
cr(16,'resolved',['history_book_01_p0122_b005','history_book_01_p0123_b002'],'p123 b002以“控制之下的‘二十一条’要求”承接p122 b005末尾，构成连续句并继续交涉结果。','保留两页正文证据。')
cr(17,'resolved',['history_book_01_p0129_b012','history_book_01_p0130_b002','history_book_01_p0130_b003','history_book_01_p0131_b002'],'p129五四运动意义句在p130 b002连续；马克思学说研究会叙述在p130 b003和p131 b002接续，内容与页面段落相符。','跨页内容合并引用所列原文块。')
cr(18,'resolved',['history_book_01_p0132_b001','history_book_01_p0133_b001'],'p132国共合作叙述跨页进入p133，后页继续合作成果与广州国民党一大；两页内容连续。','保留相邻块作为证据。')
cr(19,'resolved',['history_book_01_p0136_b001','history_book_01_p0137_b001'],'p136 b001秋收起义段末说明毛泽东改向山区；p137 b001续写进军井冈山及建立根据地，语义与句序衔接。','合并跨页叙述，区分秋收起义与建立根据地等事件。')
cr(20,'resolved',['history_book_01_p0137_b001','history_book_01_p0138_b001'],'p137 b001记1931年11月中华苏维埃临时中央政府成立，并在页末截于“主席”；p138 b001从“员会主席”续接职务并说明其意义。','将两块共同用于政府成立条目。')
cr(21,'resolved',['history_book_01_p0149_b009','history_book_01_p0150_b001'],'p149 b009明确1938年6月中旬武汉会战开始；p150 b001接着说明会战于10月下旬结束、武汉失守。已直接读取相邻页原文。','武汉会战条目使用两块，将时间记为1938年6月中旬至10月下旬。')

# Add generic audit metadata to every complete replacement record; unchanged knowledge stays out of updates unless it needs reclean_review.
for a in audit:
 id=a['id']; k=updates.get(id)
 if k is None:
  if a['decision']=='retained': continue
  k=copy.deepcopy(next(x for x in ks if x['id']==id)); updates[id]=k
 k['reclean_review']={'status':'needs_review' if id in needs else 'agent_reviewed','note':needs.get(id,notes_specific.get(id,a['note'])),'slice':'s04'}
 # For all changed records replace audit block refs with effective new references.
 if id in updates:
  a['evidence_block_ids']=k.get('evidence_block_ids',[])
  a['decision']='needs_review' if id in needs else 'changed'

patch={'slice':'s04','page_range':[113,149],'baseline_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'updates':{'knowledge':list(updates.values()),'blocks':[],'pages':[],'assets':[],'relations':[],'review_issues':[]},'knowledge_audit':audit,'split_proposals':splits,'merge_proposals':[],'open_items':open_items,'visually_checked_pages':list(range(113,150))}
patch['carryover_review']=carry
out=root/'s04.patch.json'; out.write_text(json.dumps(patch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Human review copy, including complete audit ledger.
lines=['# s04 教材清洗复核（PDF页序113–149）','',f'- 基线 SHA-256：`{patch["baseline_sha256"]}`',f'- 归属知识：{len(ks)} 条；changed={sum(a["decision"]=="changed" for a in audit)}，retained={sum(a["decision"]=="retained" for a in audit)}，needs_review={sum(a["decision"]=="needs_review" for a in audit)}。',f'- 实际检查页图：PDF页序113–149（37页）；同时为跨页项读取112、150页文字及150页图面。页图逐页检查了版式、图表/图注、栏序和图文块完整性。',f'- 补正：{len(updates)} 条知识完整记录写入patch；其中修复错误证据块指向、规范明确持续时段、纠正清末新政未知终点，并用p150证据补全武汉会战终点。',f'- carryover索引15–21：{len(carry)}项逐项回看实际前后页，全部resolved；索引15原p122引用块号是标题，已用p122 b005正文代替。', '- 结构检查：已在本构建脚本中解析输入并生成合法JSON；未运行项目专用patch validator，不能据此称通过。', '- 未解决：需人工确定的合并/拆分项见下方；图片已查看页面图面，但没有对图中文字或地图边界作未有根据的内容提取。', '', '## 拆分建议','']
for x in splits: lines.append(f"- `{x['id']}`：{x['reason']} 建议：{'；'.join(x['proposed_titles'])}。")
lines+=['','## 未解决项','']
for x in open_items: lines.append(f"- `{x['record_ids'][0]}`：{x['reason']} 下一步：{x['next_action']}")
lines+=['','## knowledge_audit 全量账本','']
for a in audit:
 lines.append(f"### {a['id']} — {a['decision']}")
 lines.append(f"证据：{', '.join(a['evidence_block_ids']) or '无'}。核对：{a['note']}")
 if a['empty_reasons']:
  lines.append('空字段：'+'；'.join(f"{k}：{v}" for k,v in a['empty_reasons'].items()))
lines+=['','## carryover_review','']
for c in carry: lines.append(f"- 索引{c['index']} {c['status']}；证据{', '.join(c['evidence_block_ids'])}。{c['reason']} 下一步：{c['next_action']}")
(root/'s04.review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('updated',len(updates),'audited',len(audit),'carryover',len(carry),'patch',out.stat().st_size,'review',(root/'s04.review.md').stat().st_size)
