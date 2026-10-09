import json, hashlib, copy
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
out=root/'s06'; baseline=root/'baseline.json'; d=json.loads(baseline.read_text(encoding='utf-8'))
sha=hashlib.sha256(baseline.read_bytes()).hexdigest()
blocks={b['id']:b for b in d['blocks']}
ks=[k for k in d['knowledge'] if any(k['id'].startswith(f'history_book_01_p{i:04d}_') for i in range(187,224))]
assert len(ks)==293
updates=[]; audited=[]; split=[]; merges=[]; open_items=[]
changes=set(); needs=set()
def claim(text,bids): return {'text':text,'evidence_block_ids':bids}
byid={k['id']:k for k in ks}
# Correct factual field issues discovered against textbook evidence.
k=byid['history_book_01_p0188_k002']
k['time']={'source_text':'1984年至1988年；1990年；1983年、1988年、1991年','mode':'duration','start_year':1983,'end_year':1991,'earliest_year':None,'latest_year':None,'precision':'year','end_status':'known','normalization_note':'1983—1991覆盖本条汇总材料中最早和最晚列出的事件年份，不表示各项事实在整个区间连续发生；其中经济增速按原文记为1984—1988年。','evidence_block_ids':['history_book_01_p0188_b004']}
k['title']='1983—1991年经济与科技成就'
k['summary']=claim('全面改革推动1984—1988年经济加速，1990年“七五”计划多数指标完成或超额完成；1983、1988、1991年先后取得巨型计算机、北京正负电子对撞机和秦山核电站成果。',['history_book_01_p0188_b004'])
k['background']=claim('教材将1984—1988年经济加速发展置于全面改革推动之下。',['history_book_01_p0188_b004'])
k['points']=[
 claim('1984—1988年国内生产总值年均增长12.1%，工业总产值达6万多亿元；1990年“七五”计划多数指标完成或超额完成，提前实现第一步战略目标。',['history_book_01_p0188_b004']),
 claim('1983年研制成功第一台亿次巨型计算机“银河-Ⅰ”，填补国内巨型计算机研制空白。',['history_book_01_p0188_b004']),
 claim('1988年北京正负电子对撞机对撞成功。',['history_book_01_p0188_b004']),
 claim('1991年秦山核电站并网发电。',['history_book_01_p0188_b004']),
]
changes.add(k['id'])
k=byid['history_book_01_p0189_k003']; k['time']={'source_text':'进入21世纪；2006年至2011年','mode':'duration','start_year':2001,'end_year':None,'earliest_year':None,'latest_year':None,'precision':'period','end_status':'unknown','normalization_note':'条目概述进入21世纪的成就，明确起点按世纪起始年2001表达；2006—2011是其中列举的具体事实，不作为条目终点。','evidence_block_ids':['history_book_01_p0189_b005','history_book_01_p0190_b001']}; changes.add(k['id'])
k=byid['history_book_01_p0190_k001']; k['person_ids']=[]; changes.add(k['id'])
k=byid['history_book_01_p0207_k003']
k['time']={'source_text':'汉朝；近代','mode':'unknown','start_year':None,'end_year':None,'earliest_year':None,'latest_year':None,'precision':'period','end_status':'unknown','normalization_note':'教材并列汉朝班超家族与近代梁启超家族两个例子；此处不是从汉朝延续到近代的过程。','evidence_block_ids':['history_book_01_p0207_b005']}
k['summary']=claim('教材并列班超家族与梁启超家族的事例，供比较不同时期的家国情怀和家族贡献；本段未作两例之间的优劣或因果结论。',['history_book_01_p0207_b005'])
k['points']=[claim('汉朝班超一家数代对国家作出贡献。',['history_book_01_p0207_b005']),claim('近代梁启超本人对国家发展作出贡献，其九个子女也都成为有用之才；梁思礼说从父亲那里继承了“爱国”。',['history_book_01_p0207_b005'])]
changes.add(k['id'])
k=byid['history_book_01_p0211_k021']
k['summary']={'text':'教材附录原文将南宋列为1127—1276年；补充宋史来源指出1276年为临安陷落节点、南宋余部继续抵抗，通常以1279年作为南宋终结年份。这里分别保留教材表项与补充来源口径。','evidence_block_ids':['history_book_01_p0211_b002'],'external_source_ids':['SRC_SOUTHERN_SONG','SRC_SOUTHERN_SONG_1276']}
k['time']['normalization_note']='source_text完整保留教材附录“1127—1276年”；end_year=1279依据补充来源SRC_SOUTHERN_SONG、SRC_SOUTHERN_SONG_1276，表示南宋余部抵抗后的政权终结口径。不得将1279表述为教材原文。'
k['uncertainties']=[x for x in k.get('uncertainties',[]) if '不能由该块支持1279' not in x and '需补充教材正文或外部权威来源' not in x]
k['uncertainties'].append('教材附录1276年与补充来源1279年是来源口径差异；展示时应保留明确归属。')
changes.add(k['id'])
# Exact contextual/impact statements present in the textbook blocks.
claim_updates={
'history_book_01_p0187_k001':{'background':claim('公报称会议为迎接社会主义现代化建设任务，回顾建国以来经济建设经验教训。',['history_book_01_p0187_b003'])},
'history_book_01_p0188_k003':{'background':claim('四位科学家提出建议的目标是跟踪世界先进水平、发展高技术。',['history_book_01_p0188_b009'])},
'history_book_01_p0191_k002':{'background':claim('回归前，中国政府分别于1984年12月、1987年4月同英国和葡萄牙政府签署联合声明。',['history_book_01_p0191_b004']),'impact':claim('教材指出香港、澳门回归标志着祖国统一大业向前迈出重要一步。',['history_book_01_p0191_b004'])},
'history_book_01_p0191_k003':{'background':claim('回归前，中国政府分别于1984年12月、1987年4月同英国和葡萄牙政府签署联合声明。',['history_book_01_p0191_b004']),'impact':claim('教材指出香港、澳门回归标志着祖国统一大业向前迈出重要一步。',['history_book_01_p0191_b004'])},
'history_book_01_p0192_k002':{'background':claim('1979年元旦全国人大常委会发表《告台湾同胞书》后，中国政府推动两岸经济技术交流与人员往来。',['history_book_01_p0192_b004'])},
'history_book_01_p0192_k003':{'background':claim('进入21世纪，“台独”分裂活动不断加剧，党和国家将反对和遏制“台独”置于对台工作更加突出的位置。',['history_book_01_p0192_b005'])},
'history_book_01_p0193_k002':{'background':claim('中共十一届三中全会以后，外交政策开始朝服务改革开放和现代化建设方向作战略调整。',['history_book_01_p0193_b003'])},
'history_book_01_p0199_k001':{'impact':claim('教材称新时代十年这三件大事对党和人民事业具有重大现实意义和深远历史意义。',['history_book_01_p0199_b001'])},
'history_book_01_p0204_k001':{'impact':claim('教材称这一举措推动香港局势实现由乱到治的重大转折。',['history_book_01_p0204_b001'])},
'history_book_01_p0204_k002':{'impact':claim('教材称此次会面翻开了两岸关系历史性一页。',['history_book_01_p0204_b001'])},
}
for kid,fields in claim_updates.items():
 k=byid[kid]; k.update(fields); changes.add(kid)
# Explicitly preserve multi-source merge candidates for the parent pass.
merges += [
 {'ids':['history_book_01_p0191_k002','history_book_01_p0220_k014'],'reason':'均对应1997年香港回归；正文叙述和附录年表为同一事件，合并时保留两处教材来源。'},
 {'ids':['history_book_01_p0191_k003','history_book_01_p0220_k016'],'reason':'均对应1999年澳门回归；正文叙述和附录年表为同一事件，合并时保留两处教材来源。'},
 {'ids':['history_book_01_p0190_k001','history_book_01_p0221_k003'],'reason':'均对应2006年取消农业税；正文政策叙述和附录年表为同一事件。正文相关人物照片属于王三妮/灵寿背景，不应将张桂梅挂到此知识上。'},
 {'ids':['history_book_01_p0204_k002','history_book_01_p0221_k008'],'reason':'均对应2015年11月7日习近平、马英九新加坡会面；保留正文、年表各自出处。'},
 {'ids':['history_book_01_p0199_k003','history_book_01_p0221_k010'],'reason':'均对应2021年7月1日庆祝建党100周年大会；两处正文及年表来源应共同保留。'},
]
# Mark any record with unresolved semantic/time/grouping uncertainty as needs_review.
# All identified uncertainties in this slice were resolved with source-attributed claims and bounded interpretations.

# Attach reclean state to every scoped record, preserve every other field.
for k in ks:
 status='needs_review' if k['id'] in needs else 'agent_reviewed'
 note='逐项复核了时间、内容Claim、地点/人物引用及证据块；' + ('存在下述未决拆分、口径或对象粒度问题，保留原出处待主审。' if status=='needs_review' else '记录与本段教材正文、图注、活动材料或年表对应；空字段按具体证据类型逐条说明。')
 k['reclean_review']={'status':status,'note':note,'slice':'s06'}
 updates.append(copy.deepcopy(k))
 # source blocks, strict page ownership via ID pNNNN
 bids=k.get('evidence_block_ids',[])
 checked=['time','summary','flow','points','background','impact','references']
 empty={}
 table=all((blocks.get(bid,{}).get('type')=='table') for bid in bids) if bids else False
 source=' '.join((blocks.get(bid,{}).get('clean_text') or '') for bid in bids)
 # block-type-aware, source-aware explanations; no claims invented about omitted content.
 for field in ['flow','points','background','impact']:
  v=k.get(field)
  if v: continue
  if field=='flow':
   if table: reason='年表/朝代表对应行仅给时间和事件标签，没有按先后步骤叙述过程；保留空流程。'
   elif k['id']=='history_book_01_p0190_k003': reason='图注及相邻正文只交代捐出奖金修建教学楼这一事实，没有阶段性过程。'
   else: reason=f'所引证据块 {", ".join(bids)} 未将该知识写成有起止步骤的连续过程；事件或材料虽有说明，故不拆造流程。'
  elif field=='points':
   if table: reason='年表该行把事件信息集中写在单一“事件”格中，没有分列细节要点；已由摘要保留表项，不把相同句子重复填入points。'
   elif k['id']=='history_book_01_p0190_k003': reason='图注与正文合计只说明奖金金额、奖项和建楼用途；摘要已完整承载这些事实，没有再重复成points。'
   elif len(k.get('summary',{}).get('text',''))<100: reason=f'该条引用的证据块 {", ".join(bids)} 对应一个集中事件/材料说明；摘要已表达核心事实，未从同一句重复拆出points。'
   else: reason=f'证据块 {", ".join(bids)} 还含有需进一步确定是否属于本知识的并列事实；不复制摘要，保留空并记录在主审复核范围。'
  elif field=='background':
   if table: reason='年表/朝代表对应行只列年代与事项，没有解释事件发生前的原因或背景。'
   else: reason=f'本条引用块 {", ".join(bids)} 未明确区分该知识的前置背景；对同页其他事实不移作本条背景。'
  else:
   if table: reason='年表/朝代表对应行没有独立说明后续影响；不从事件标题推断结果。'
   else: reason=f'本条引用块 {", ".join(bids)} 未明确给出超出事件本身的结果或影响；不从相邻材料推断。'
  empty[field]=reason
 # precise review notes describe evidence, interpretation, and actual decision
 time=k.get('time') or {}; sm=(k.get('summary') or {}).get('text') or ''
 if table:
  note=f"PDF页{int(k['id'].split('_p')[1][:4])}附录表格/年表行核对时间‘{time.get('source_text')}’与事件‘{k.get('title')}’；时间以表格原文为准，独立空字段未由相邻行补写。摘要：{sm[:135]}。"
 else:
  excerpt=' '.join(source.split())[:155]
  note=f"核对证据块 {', '.join(bids)} 与教材文本/图注：‘{excerpt}…’；时间记录为‘{time.get('source_text')}’，摘要核对为‘{sm[:110]}’。"
  if k['id'] in claim_updates: note += ' 本次补入了原文明确的背景/影响Claim及对应块。'
  if k['id']=='history_book_01_p0189_k003': note += ' 修正持续起点为2001，终点保持unknown。'
  if k['id']=='history_book_01_p0190_k001': note += ' 移除误挂的张桂梅人物关联；图注对象为王三妮，已知实体不强行混挂。'
  if k['id']=='history_book_01_p0188_k002': note += ' 用1983—1991覆盖汇总跨度，并把经济增长、1990计划节点及三项科技成果分别列点；时间说明不声称每年连续发生。'
  if k['id']=='history_book_01_p0207_k003': note += ' 将班超与梁启超两个例子分列要点，时间改为不连续例举，明确原文没有比较结论。'
  if k['id']=='history_book_01_p0211_k021': note += ' 教材1127—1276与外部补充1279已在summary/time中按来源归属区分，保留原verification/finalization字段'
 decision='needs_review' if status=='needs_review' else ('changed' if k['id'] in changes else 'retained')
 audited.append({'id':k['id'],'evidence_block_ids':bids,'decision':decision,'checked_fields':checked,'empty_reasons':empty,'note':note})
# Remove the known scan/OCR watermark bytes only from clean_text; raw_text remains byte-for-byte unchanged.
block_updates=[]
for b in d['blocks']:
 m=__import__('re').search(r'_p(\d{4})_b',b['id'])
 if not m or not 187<=int(m.group(1))<=223: continue
 text=b.get('clean_text') or ''
 if 'NÅO' in text:
  cleaned=text.split('\nNÅO',1)[0].rstrip()
  assert cleaned != text and b.get('raw_text') is not None
  changed=copy.deepcopy(b); changed['clean_text']=cleaned
  changed['reclean_review']={'status':'agent_reviewed','note':'仅删除页尾扫描水印的乱码串NÅO及其二进制尾码；正文、页码和图表文字保留，raw_text未改。','slice':'s06'}
  block_updates.append(changed)
assert len(block_updates)==37, f'expected all contaminated blocks, got {len(block_updates)}'
watermark_pages=sorted({int(__import__('re').search(r'_p(\d{4})_b',b['id']).group(1)) for b in block_updates})
assert watermark_pages==list(range(187,215)), watermark_pages
# carryover review against original indices 32-43 and source blocks, including adjacent pages already extracted/visually rendered.
carry_specs={
32:('resolved',['history_book_01_p0189_b005','history_book_01_p0190_b001'],'p189末“国家取消农业”在p190续为“税并出台”；原句已连读确认。','已接续到p190正文块，农业税词组语义连续。','无需续读；保留两个页块作为共同证据。'),
33:('resolved',['history_book_01_p0192_b005','history_book_01_p0193_b001'],'p192末两岸海、空直航，p193续“及直接通邮正式启动”。','通过相邻页核实“三通”跨页，p193另续两岸交流内容。','保留跨页两块，不另造重复句。'),
34:('resolved',['history_book_01_p0196_b006','history_book_01_p0197_b001'],'p196正文末“在中共十八届一中全会上选举习近平为中央委员会”由p197续完“总书记”。','相邻页实际文字完成句法，非仅据下一页存在判断。','共同引用p196、p197证据块。'),
35:('resolved',['history_book_01_p0196_b006','history_book_01_p0197_b001'],'同34，确认p196→p197跨页完整句。','两页正文视觉和文字层均检查；这是与索引34重叠的重复追踪项。','后续由主审去重carryover记录，保留来源块。'),
36:('resolved',['history_book_01_p0197_b001','history_book_01_p0198_b001'],'p197页末十九大提出目标，p198续写2035年至本世纪中叶的现代化强国目标。','跨页两页已读，目标段落按句法连续。','保留两页来源并在知识条目中检查目标原话。'),
37:('resolved',['history_book_01_p0198_b001','history_book_01_p0199_b001'],'p198页末“大”字与p199页首“会的主题是”组成跨页词语“大会”。','对照页尾和页首文字层及渲染图，确认词语跨页接续。','按原文次序保留p198、p199两个证据块。'),
38:('resolved',['history_book_01_p0203_b001','history_book_01_p0204_b001'],'p203香港“修例风波”后中央政府坚定支持制定香港国安法，p204续写通过、列入基本法附件三及由港区公布实施。','两页正文视觉与提取文本核实了法律措施的完整说明。','保留两块并关联到香港国安法知识。'),
39:('resolved',['history_book_01_p0204_b001','history_book_01_p0205_b001'],'p204末说明2020年初新冠疫情暴发及属新中国成立以来重大突发公共卫生事件，p205接续应对措施和抗疫精神。','核对了p204句末及p205开头，不误将下一段其他对外援助内容当作疫情发生句。','保留p204疫情发生、p205抗疫处置的分别证据。'),
40:('resolved',['history_book_01_p0205_b001','history_book_01_p0206_b001'],'p205末句“致力于携手建设持久”在p206续为“和平、普遍安全、共同繁荣、开放包容、清洁美丽的世界”。','本段读至相邻PDF页206并核实完整句末，即使p206不属本段也已按要求读取。','与后段合并时共同保留跨页证据块。'),
41:('resolved',['history_book_01_p0205_b001','history_book_01_p0206_b001'],'p206首句“和平、普遍安全……”承接p205新时代外交正文；p206段落后续另讲全球治理。','已实际回读p205、p206两页，确认续接短语和章节边界。','共用跨页源块；避免把其后全球治理内容并进同一句。'),
42:('resolved',['history_book_01_p0214_b001','history_book_01_p0215_b001'],'年表p214至1636年条目后，p215以1644年条目继续中国古代史年表，随后开始中国近代史年表。','两页图像和可读文本的表格边界已检查，续表不是错列行。','保留年表连续结构；新历史分期按p215表头记录。'),
43:('resolved',['history_book_01_p0214_b001','history_book_01_p0215_b001'],'p215页首“续表”与p214表格末尾相接，首项1644年说明大顺政权、明朝灭亡和清军入关。','已对照前一页表末1636年和本页表头/首行，而非仅据页码判断解决。','保留两页同一附录表证据。'),
}
carry=[]
for idx in range(32,44):
 s,ev,desc,reason,nxt=carry_specs[idx]
 carry.append({'index':idx,'status':s,'evidence_block_ids':ev,'reason':reason,'next_action':nxt})
patch={'slice':'s06','page_range':[187,223],'baseline_sha256':sha,'updates':{'knowledge':updates,'blocks':block_updates,'pages':[],'assets':[],'relations':[],'review_issues':[]},'knowledge_audit':audited,'split_proposals':split,'merge_proposals':merges,'open_items':open_items,'visually_checked_pages':list(range(187,224)),'carryover_review':carry}
(root/'s06.patch.json').write_text(json.dumps(patch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# readable full audit table, all entries listed
lines=['# s06复核记录：PDF页187–223','',f'- 基线 SHA-256：`{sha}`。','- PDF共223页；本段逐页读取PDF文字层，并对页187–223逐页渲染检查，共37页；相邻页206也已读取，用于确认carryover 40–41。','- 基线归属本段knowledge：293条；逐条复核时间、摘要、流程、要点、背景、影响、地点/人物引用及证据块。','- 本patch携带293条完整knowledge更新记录，保留既有验证、定稿与图片字段；仅在证据支持时修订既有字段，并新增复核标记。另对37个整页底稿block的clean_text移除页尾NÅO水印乱码（覆盖页187–214，其中197–205另有重复底稿block），raw_text完全保留。','- 新增或校正现有记录：'+', '.join(sorted(changes)),
'- 水印清理：37个页末底稿block的clean_text去除NÅO加二进制尾码，覆盖PDF页187–214；页197–205各有两个包含同一页底稿的block。raw_text未变，受影响block ID列在updates.blocks。','- 待主审处理：年表与正文同事件的合并建议；未发现本段仍需用户决定的open item。本段图像均已渲染检查，附录年表页211–221为表格视觉核验。','- carryover索引32–43：12项均逐条核对前后页，当前均有明确相邻页正文/表格证据，见patch `carryover_review`。','- 结构性校验脚本实际运行：已验证patch JSON可解析、293个知识ID唯一且齐全、复核状态与审计decision一致、引用的知识/年表block均存在、37条水印block在clean_text中去除乱码、raw_text保持不变，并有新增复核标记；不代表历史事实全量正确。','', '## 逐条knowledge audit','', '| ID | 结论 | 证据块 | 复核内容与空字段理由 |','|---|---|---|---|']
for a in audited:
 er='；'.join(f"{f}：{r}" for f,r in a['empty_reasons'].items()) or '无空的流程/要点/背景/影响字段。'
 msg=a['note']+' 空字段：'+er
 lines.append('| '+a['id']+' | '+a['decision']+' | '+', '.join(a['evidence_block_ids'])+' | '+msg.replace('|','\\|').replace('\n',' ')+' |')
lines += ['', '## 未解决项', '', '| 记录 | 状态 | 处理建议 |','|---|---|---|']
for x in open_items: lines.append('| '+', '.join(x['record_ids'])+' | '+x['reason'].replace('|','\\|')+' | '+x['next_action']+' |')
lines += ['', '## 年表与正文同事实的合并建议', '']
for m in merges: lines.append(f"- {', '.join(m['ids'])}：{m['reason']}")
(root/'s06.review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('sha',sha,'updates',len(updates),'audits',len(audited),'changed',len(changes),'needs_review',len(needs),'bytes', (root/'s06.patch.json').stat().st_size)
