import copy, json
from pathlib import Path
W=Path('shuju/cleaned/history_book_01/reclean_20260923')
patch_path=W/'s02.patch.json'
base=json.loads((W/'baseline.json').read_text(encoding='utf-8'))
p=json.loads(patch_path.read_text(encoding='utf-8'))
base_knowledge={k['id']:k for k in base['knowledge']}
base_blocks={b['id']:b for b in base['blocks']}
updates={k['id']:k for k in p['updates']['knowledge']}
audits={a['id']:a for a in p['knowledge_audit']}

# Restore the painting/lifestyle record to its own PDF p.71 source. It had been
# accidentally overwritten with page 72 population statistics in the first s02 patch.
p71='history_book_01_p0071_k005'
k=copy.deepcopy(base_knowledge[p71])
k['time']={
 'source_text':'宋墓壁画', 'mode':'uncertain', 'start_year':None, 'end_year':None,
 'earliest_year':None, 'latest_year':None, 'precision':'period', 'end_status':'unknown',
 'normalization_note':'教材只称其为宋墓壁画，未提供壁画或墓葬的具体年代。',
 'evidence_block_ids':['history_book_01_p0071_b004']}
k['summary']={
 'text':'教材以宋墓壁画《夫妻对坐宴饮图》呈现墓主人生前家居生活，并引沈括对唐宋生活消费的比较。',
 'evidence_block_ids':['history_book_01_p0071_b003','history_book_01_p0071_b004']}
k['background']={
 'text':'教材指出，沈括所见宋人生活和消费水平高于唐朝，其背景是经济发展水平提高。',
 'evidence_block_ids':['history_book_01_p0071_b004']}
k['impact']={
 'text':'沈括对“富贵诗”的评论间接反映宋人生活和消费水准明显超过唐朝；教材将这一变化联系到经济发展水平提高。',
 'evidence_block_ids':['history_book_01_p0071_b004']}
k['evidence_block_ids']=['history_book_01_p0071_b003','history_book_01_p0071_b004']
k['reclean_review']={
 'status':'agent_reviewed',
 'note':'回读页71 b003图注和b004正文：图为宋墓壁画但无具体公历年代；b004明确区分沈括的唐宋消费比较与其背景“经济发展水平提高”。',
 'slice':'s02'}
updates[p71]=k
a=audits[p71]
a.update({
 'evidence_block_ids':['history_book_01_p0071_b003','history_book_01_p0071_b004'],
 'decision':'changed',
 'empty_reasons':{
  'flow':'p0071_b003是静态壁画图注，p0071_b004是沈括的唐宋消费比较，没有按先后展开的连续步骤，flow留空。',
  'points':'p0071_b003只标识图像，p0071_b004提供一段比较及其背景；没有另外并列的具体生活物品或消费指标，points留空。'
 },
 'note':k['reclean_review']['note']})

# The population time series belongs to p.72 k005. Keep both explicit snapshot years
# as a range of dates, not a continuous event, and retain the estimate's qualification.
p72='history_book_01_p0072_k005'
k=updates[p72]
k['time']={
 'source_text':'989年、1110年', 'mode':'uncertain', 'start_year':None, 'end_year':None,
 'earliest_year':989, 'latest_year':1110, 'precision':'year', 'end_status':'unknown',
 'normalization_note':'教材列出989年和1110年两个离散人口统计截面，不表示连续持续；“实际人口超过1亿”是按户口比例推算。',
 'evidence_block_ids':['history_book_01_p0072_b003']}
k['summary']={
 'text':'教材列出北宋初期989年全国户数650万、北宋末1110年户数2088万及登记口数4673万；多数研究者认为“口数”可能只计成年男子，按汉唐户均约5口估算，北宋末实际人口可能超过1亿。后两项是学者判断和推算，不是直接统计值。',
 'evidence_block_ids':['history_book_01_p0072_b003']}
k['points']=[
 {'text':'989年全国户数为650万；1110年户数为2088万，记载口数4673万、户均口数2.24。','evidence_block_ids':['history_book_01_p0072_b003']},
 {'text':'多数研究者认为北宋统计口数可能仅含成年男子；若按汉唐户均约5口推算，实际人口可能超过1亿，属于估算而非直接统计。','evidence_block_ids':['history_book_01_p0072_b003']}
]
k['background']={
 'text':'教材指出户口增长是观察农业发展的一个重要指标。',
 'evidence_block_ids':['history_book_01_p0072_b003']}
k['impact']={
 'text':'教材将按户口比例推算出的北宋末人口规模评价为中国古代人口史的一个划时代标志；该评价针对估算值，不是实测口数。',
 'evidence_block_ids':['history_book_01_p0072_b003']}
k['evidence_block_ids']=['history_book_01_p0072_b003']
k['reclean_review']={
 'status':'agent_reviewed',
 'note':'回读页72 b003：989年户数、1110年户数与登记口数均为原文明载；超过1亿是多数研究者按户均比例作的估算，已和统计数分列。',
 'slice':'s02'}
a=audits[p72]
a.update({
 'evidence_block_ids':['history_book_01_p0072_b003'],
 'decision':'changed',
 'empty_reasons':{
  'flow':'页72 b003并列989、1110两个统计截面及人口估算，没有叙述一个持续行动或按步骤发生的事件，flow留空。'
 },
 'note':k['reclean_review']['note']})

p['updates']['knowledge']=sorted(updates.values(),key=lambda x:x['id'])
p['knowledge_audit']=sorted(audits.values(),key=lambda x:x['id'])
# If an earlier split/open item mistakenly referenced the restored painting ID, remove it.
p['split_proposals']=[x for x in p.get('split_proposals',[]) if x.get('id')!=p71]
p['open_items']=[x for x in p.get('open_items',[]) if p71 not in x.get('record_ids',[])]
patch_path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Regenerate the exhaustive review, preserving its per-record evidence and decisions.
lines=['# s02 逐条语义复核（PDF页序39–75）','',
 f"基线 SHA-256：`{p['baseline_sha256']}`；knowledge审计{len(p['knowledge_audit'])}条，知识更新{len(p['updates']['knowledge'])}条，源块更新{len(p['updates']['blocks'])}条。页39—75逐页联系表目视检查；页39、40、47、50、55、72、75及相邻页38、76使用高分辨率图像复核。原始raw_text未改。",
 '', '更正记录：原补丁曾将页72人口统计误归到页71_k005。本版已恢复页71图像条目，并将人口统计及相应时间证据放回页72_k005。']
for item in p['knowledge_audit']:
 lines += [f"\n## {item['id']} — {item['decision']}",f"证据块：{', '.join(item['evidence_block_ids']) or '无'}",f"逐条核对：{item['note']}"]
 for field,reason in item.get('empty_reasons',{}).items(): lines.append(f"- {field}留空：{reason}")
lines += ['', '## 未决事项','','- p0042_k002、p0065_k001仍有拆分建议，待主审决定是否创建新ID并迁移原证据。','- p0072_k005中“实际人口超过1亿”是按户口比例推算，保留“可能”限定；不能作为登记人口数。','- 页段51项图片资产本轮未重新裁剪、导出或重新哈希；页面图像逐页目视检查。']
(W/'s02.review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('repaired p71/p72 scope collision; audits',len(p['knowledge_audit']))
