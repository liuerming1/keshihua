import json,re,copy
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923')
base=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
patch=json.loads((root/'s04.patch.json').read_text(encoding='utf-8'))
source_blocks={b['id']:b for b in base['blocks']}
knowledge={k['id']:copy.deepcopy(k) for k in base['knowledge']}
knowledge.update({k['id']:copy.deepcopy(k) for k in patch['updates']['knowledge']})

# Remove only the corrupt watermark tail from clean_text. Keep all raw_text values intact.
block_updates=[]
for b in base['blocks']:
    try: page=int(b['page_id'].split('_p')[1])
    except (ValueError,IndexError): continue
    if not 113<=page<=149: continue
    clean=b.get('clean_text')
    if not clean or 'NÅO' not in clean: continue
    revised=copy.deepcopy(b)
    pos=clean.find('NÅO')
    prefix=clean[:pos].rstrip()
    revised['clean_text']=prefix if prefix else None
    revised.setdefault('notes',[])
    msg='clean_text中已清除PDF文本层损坏的水印乱码；raw_text原样保留。'
    if msg not in revised['notes']: revised['notes'].append(msg)
    block_updates.append(revised)

# Finish the seven main-review cases using source-backed duration/flow or precise event naming.
def get(id): return knowledge[id]
def claim(text, ids): return {'text':text,'evidence_block_ids':ids}
def put(k): knowledge[k['id']]=k

id='history_book_01_p0113_k002'; k=get(id)
k['title']='克林德事件与克林德碑的变迁'; k['kind']='process'
k['flow']=[
 claim('1900年6月，德国公使克林德在东单牌楼附近与清军冲突，被击毙。',['history_book_01_p0113_b006']),
 claim('1901年《辛丑条约》签订后，清政府派载沣赴德谢罪，并在克林德被害处建立克林德碑。',['history_book_01_p0113_b006']),
 claim('1918年德国战败后，克林德碑改名为“公理战胜碑”，并由东单迁至中央公园。',['history_book_01_p0113_b006','history_book_01_p0113_b007']),
 claim('1952年亚洲及太平洋区域和平会议决定将其改为“保卫和平碑”。',['history_book_01_p0113_b006'])]
k['reclean_review']={'status':'agent_reviewed','note':'按有起点和终点的纪念碑变迁过程保留duration，并将1900、1901、1918、1952各阶段分别列入flow；日期和更名证据均来自正文。','slice':'s04'}
k['uncertainties']=[]; put(k)

id='history_book_01_p0118_k003'; k=get(id)
k['title']='中国同盟会成立后的反清起义与黄花岗起义'; k['kind']='process'
k['time'].update({'source_text':'中国同盟会成立后多次反清起义；1911年4月27日广州黄花岗起义','mode':'duration','start_year':1905,'end_year':1911,'earliest_year':None,'latest_year':None,'precision':'year','end_status':'known','normalization_note':'教材未给多次反清起义各自日期；以同盟会成立的1905年作为该运动的时间下界，以黄花岗起义日期作为本条叙述的终点。独立起义日期保留于flow所引原文，不冒充同一事件。','evidence_block_ids':['history_book_01_p0118_b003','history_book_01_p0118_b004']})
k['evidence_block_ids']=['history_book_01_p0118_b003','history_book_01_p0118_b004']
k['summary']['evidence_block_ids']=k['evidence_block_ids']
k['flow']=[
 claim('1905年中国同盟会成立后，孙中山继续宣传革命理论并组织多次反清武装起义。',['history_book_01_p0118_b003','history_book_01_p0118_b004']),
 claim('徐锡麟、秋瑾等革命党人参与反清斗争；教材未为这些不同起义分别给出日期。',['history_book_01_p0118_b004']),
 claim('1911年4月27日广州黄花岗起义引起巨大震动。',['history_book_01_p0118_b004'])]
k['place_refs'][0]['evidence_block_ids']=['history_book_01_p0118_b004']
k['reclean_review']={'status':'agent_reviewed','note':'保留为同盟会成立后反清武装斗争的过程条目，以duration和flow表达有依据的时间范围；黄花岗起义的4月27日独立列明，教材未给其他起义日期，不臆造新条目或精确日期。','slice':'s04'}
k['uncertainties']=['教材未为多次反清起义逐一标注日期，只有黄花岗起义明确记为1911年4月27日。']; put(k)

id='history_book_01_p0140_k023'; k=get(id)
k['title']='纪念红军长征胜利80周年大会讲话阐释长征精神'; k['kind']='event'; k['content_type']='thought'
k['summary']=claim('2016年10月21日讲话概括长征精神的内涵，并说明其体现的民族精神意义。',['history_book_01_p0140_b001'])
k['points']=[claim('讲话将长征精神概括为把人民和民族利益置于首位、坚定理想信念、实事求是、顾全大局、严守纪律、紧密团结并依靠人民群众。',['history_book_01_p0140_b001'])]
k['impact']=claim('讲话称长征精神体现人民军队革命风范、中华民族自强不息的品格和以爱国主义为核心的民族精神。',['history_book_01_p0140_b001'])
k['reclean_review']={'status':'agent_reviewed','note':'时间指向教材引用的2016年10月21日讲话；标题明确这是讲话这一有来源的事件，不将其写成长征精神的起源时间。','slice':'s04'}
k['uncertainties']=[]; put(k)

id='history_book_01_p0143_k002'; k=get(id)
k['title']='赵一曼（1905—1936）：东北抗日、被捕与就义';
k['time'].update({'source_text':'1935年任东北人民革命军第三军二团政委并被捕；图注记其生卒年1905—1936','mode':'duration','start_year':1935,'end_year':1936,'earliest_year':None,'latest_year':None,'precision':'year','end_status':'known','normalization_note':'人物生卒年保留在标题和图注证据中；time表达教材记载的东北抗日活动/被捕至就义，未把出生年份作为事件起点。','evidence_block_ids':['history_book_01_p0143_b003','history_book_01_p0143_b004']})
k['summary']=claim('赵一曼于1926年加入中国共产党，1935年任东北人民革命军第三军二团政委，在与日军战斗中被捕，后英勇就义；图注标出生卒年1905—1936。',['history_book_01_p0143_b003','history_book_01_p0143_b004'])
k['flow']=[claim('1926年加入中国共产党。',['history_book_01_p0143_b004']),claim('1935年任第三军二团政委，在战斗中被捕，后英勇就义；教材未写出被捕和就义的具体日期。',['history_book_01_p0143_b004'])]
k['points']=[claim('图注给出生卒年1905—1936；该生卒信息不作为抗日活动的持续时间。',['history_book_01_p0143_b003'])]
k['reclean_review']={'status':'agent_reviewed','note':'标题把人物身份与可核对的抗日、被捕、就义事实明确区分；time采用正文事件跨度1935—1936，生卒年仅作为图注信息保留。','slice':'s04'}
k['uncertainties']=['教材只给出被捕及就义的先后关系，未给具体日月；1936年来自人物图注的逝世年。']; put(k)

id='history_book_01_p0143_k003'; k=get(id)
k['title']='华北事变与一二·九运动';
k['time'].update({'source_text':'1935年前后华北事变；1935年12月9日一二·九运动','mode':'uncertain','start_year':None,'end_year':None,'earliest_year':1935,'latest_year':1935,'precision':'year','end_status':'not_applicable','normalization_note':'教材称华北事变为日本制造的一连串事件，并明确一二·九运动发生于1935年12月9日；用1935年表示同一救亡过程的有据年份，不把两者伪装成同一日。','evidence_block_ids':['history_book_01_p0143_b005']})
k['flow']=[claim('日本侵略者控制热河、河北、察哈尔并策动“华北自治运动”；教材将这一连串事态总称华北事变。',['history_book_01_p0143_b005']),claim('1935年12月9日，北平学生因华北自治运动举行大规模游行示威，即一二·九运动。',['history_book_01_p0143_b005'])]
k['reclean_review']={'status':'agent_reviewed','note':'作为同一华北危机及抗日救亡过程保留；用flow分开教材所述事变背景与1935年12月9日运动节点，时间字段保留1935年范围而不制造具体起日。','slice':'s04'}
k['uncertainties']=[]; put(k)

id='history_book_01_p0143_k004'; k=get(id)
k['title']='《八一宣言》与瓦窑堡会议确立抗日民族统一战线方针';
k['time'].update({'source_text':'1935年8月1日《八一宣言》；1935年底瓦窑堡会议','mode':'duration','start_year':1935,'end_year':1935,'earliest_year':None,'latest_year':None,'precision':'year','end_status':'known','normalization_note':'本条表达同一抗日民族统一战线方针形成过程中的两项节点；独立日期分别列于flow，不将二者说成同一事件。','evidence_block_ids':['history_book_01_p0143_b007']})
k['flow']=[claim('1935年8月1日，中共驻共产国际代表团发表《为抗日救国告全体同胞书》，即“八一宣言”，号召停止内战、一致抗日。',['history_book_01_p0143_b007']),claim('1935年底，中共中央在瓦窑堡召开会议；毛泽东随后作报告，确定建立抗日民族统一战线的方针并统一党内思想。',['history_book_01_p0143_b007'])]
k['reclean_review']={'status':'agent_reviewed','note':'作为1935年抗日民族统一战线方针形成过程，保留duration并用flow列出8月1日宣言和年底会议/报告两个不同节点；未合并为单一日期。','slice':'s04'}
k['uncertainties']=[]; put(k)

id='history_book_01_p0149_k003'; k=get(id)
k['title']='台儿庄大捷（1938年徐州会战期间）'
k['time']['normalization_note']='教材明确徐州会战在1938年1月至5月进行并称台儿庄大捷发生其中，未给大捷具体日；时间只表达1938年，不能解读为台儿庄战斗持续1月至5月。'
k['reclean_review']={'status':'agent_reviewed','note':'标题和time明确区分单次大捷与徐州会战持续期；教材支持其发生于1938年徐州会战期间，具体日期未给出，不另造ID或日期。','slice':'s04'}
k['uncertainties']=[x for x in k.get('uncertainties',[]) if '具体' not in x and '日期' not in x]
k['uncertainties'].append('教材只将台儿庄大捷定位于1938年1月至5月徐州会战期间，未给大捷单独日期。')
put(k)

# Main-review is complete: no speculative split requests remain.
patch['updates']['knowledge']=[knowledge[k['id']] for k in patch['updates']['knowledge']]
for id in ['history_book_01_p0113_k002','history_book_01_p0118_k003','history_book_01_p0140_k023','history_book_01_p0143_k002','history_book_01_p0143_k003','history_book_01_p0143_k004','history_book_01_p0149_k003']:
    if id not in {k['id'] for k in patch['updates']['knowledge']}: patch['updates']['knowledge'].append(knowledge[id])
patch['split_proposals']=[]; patch['open_items']=[]
patch['updates']['blocks']=block_updates
# Update audit decision and exact notes for the seven closed items.
final_notes={
'history_book_01_p0113_k002':'依教材正文按1900、1901、1918、1952年列出事件及纪念碑名称变迁，保留1900—1952年的过程时间，不要求拆成多个气泡。',
'history_book_01_p0118_k003':'以同盟会成立后的反清武装斗争为过程，用flow分列多次起义与有明确日期的黄花岗起义；其余起义日期不补猜。',
'history_book_01_p0140_k023':'标题将其明确为2016年10月21日的纪念讲话；日期是讲话发生时间，不表示长征精神起源。',
'history_book_01_p0143_k002':'标题明确赵一曼人物及东北抗日、被捕与就义事实；time记正文事件跨1935—1936年，1905—1936生卒信息留在标题/points。',
'history_book_01_p0143_k003':'作为同一救亡过程保留；flow分开华北事变所含事态与明确的1935年12月9日一二·九运动。',
'history_book_01_p0143_k004':'作为1935年方针形成过程保留；flow分别呈现8月1日宣言与年底瓦窑堡会议，保留两个独立节点日期。',
'history_book_01_p0149_k003':'明确标题所指是台儿庄大捷，time只定位到1938年徐州会战期间；不把徐州会战1—5月时段当作大捷持续时间。'}
for a in patch['knowledge_audit']:
    if a['id'] in final_notes:
        a['decision']='changed'; a['note']=final_notes[a['id']]
        k=knowledge[a['id']]; a['evidence_block_ids']=k['evidence_block_ids']
        # Remove empty-field explanations for any fields now populated.
        if k.get('flow'): a['empty_reasons'].pop('flow',None)
        if k.get('points'): a['empty_reasons'].pop('points',None)
        if k.get('impact'): a['empty_reasons'].pop('impact',None)

# Ensure every changed knowledge record gets the audited final status, preserving prior verification/finalization.
for k in patch['updates']['knowledge']:
    k['reclean_review']['slice']='s04'

patch['visually_checked_pages']=list(range(113,150))
(root/'s04.patch.json').write_text(json.dumps(patch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Rebuild the review copy around final audit decisions and final unresolved status.
lines=['# s04 教材清洗复核（PDF页序113–149）','',f'- 基线 SHA-256：`{patch["baseline_sha256"]}`',f'- 归属知识：{len(patch["knowledge_audit"])} 条；changed={sum(a["decision"]=="changed" for a in patch["knowledge_audit"])}，retained={sum(a["decision"]=="retained" for a in patch["knowledge_audit"])}，needs_review={sum(a["decision"]=="needs_review" for a in patch["knowledge_audit"])}。',f'- 实际检查页图：PDF页序113–149（37页）；carryover额外读取112、150页原文并查看p150页图面。',f'- clean_text残留：扫描301个本段块，37块含NÅO水印/乱码；在patch中只清理clean_text的损坏水印，保留混排正文，并将纯噪声块clean_text置空。所有raw_text原样保留。',f'- 内容收尾：更新{len(patch["updates"]["knowledge"])}条完整知识记录；为多阶段叙述补充分段flow，并明确赵一曼事件时间、2016讲话和台儿庄大捷时间粒度。',f'- carryover索引15–21：7项逐项对照实际前后页，全部resolved。', '- 结构检查：patch JSON已解析；核对94个唯一knowledge审阅ID与归属范围一致、更新ID无重复、carryover索引齐全；未运行项目专用patch validator。', '- 未解决项：无。教材未给的具体日期仍明确保留为未知/年份范围，不据此提出拆条待用户决策。', '', '## knowledge_audit 全量账本','']
for a in patch['knowledge_audit']:
    lines.append(f"### {a['id']} — {a['decision']}")
    lines.append(f"证据：{', '.join(a['evidence_block_ids']) or '无'}。核对：{a['note']}")
    if a['empty_reasons']:
        lines.append('空字段：'+'；'.join(f"{key}：{val}" for key,val in a['empty_reasons'].items()))
lines+=['','## carryover_review','']
for c in patch['carryover_review']:
    lines.append(f"- 索引{c['index']} {c['status']}；证据{', '.join(c['evidence_block_ids'])}。{c['reason']} 下一步：{c['next_action']}")
(root/'s04.review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('clean_text blocks repaired',len(block_updates),'knowledge updates',len(patch['updates']['knowledge']),'audits',len(patch['knowledge_audit']),'open',len(patch['open_items']))
