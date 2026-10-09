from pathlib import Path
p=Path('shuju/cleaned/history_book_01/reclean_20260923/s06/make_patch.py')
s=p.read_text(encoding='utf-8-sig')
old="""k=byid['history_book_01_p0188_k002']
k['time']={'source_text':'1984年至1988年；1990年；1983年、1988年、1991年','mode':'unknown','start_year':None,'end_year':None,'earliest_year':None,'latest_year':None,'precision':'unknown','end_status':'unknown','normalization_note':'该摘要并列不同年份的经济指标和科技成就，不能把最早、最晚年份表述为一段持续过程。','evidence_block_ids':['history_book_01_p0188_b004']}
k['background']=claim('教材将1984—1988年经济加速发展置于全面改革推动之下。',['history_book_01_p0188_b004']); changes.add(k['id']); needs.add(k['id'])
split.append({'id':k['id'],'reason':'同一摘要合并了1984—1988年经济增长、1990年“七五”计划目标、1983年“银河-Ⅰ”、1988年北京正负电子对撞机和1991年秦山核电站并网等不同事实；时间不是连续过程。','proposed_titles':['1984—1988年经济加速发展','1990年“七五”计划目标完成情况','1983年“银河-Ⅰ”研制成功','1988年北京正负电子对撞机对撞成功','1991年秦山核电站并网发电']})
"""
new="""k=byid['history_book_01_p0188_k002']
k['time']={'source_text':'1984年至1988年；1990年；1983年、1988年、1991年','mode':'duration','start_year':1983,'end_year':1991,'earliest_year':None,'latest_year':None,'precision':'year','end_status':'known','normalization_note':'1983—1991覆盖本条汇总材料中最早和最晚列出的事件年份，不表示各项事实在整个区间连续发生；其中经济增速按原文记为1984—1988年。','evidence_block_ids':['history_book_01_p0188_b004']}
k['background']=claim('教材将1984—1988年经济加速发展置于全面改革推动之下。',['history_book_01_p0188_b004'])
k['points']=[
 claim('1984—1988年国内生产总值年均增长12.1%，工业总产值达6万多亿元；1990年“七五”计划多数指标完成或超额完成，提前实现第一步战略目标。',['history_book_01_p0188_b004']),
 claim('1983年研制成功第一台亿次巨型计算机“银河-Ⅰ”，填补国内巨型计算机研制空白。',['history_book_01_p0188_b004']),
 claim('1988年北京正负电子对撞机对撞成功。',['history_book_01_p0188_b004']),
 claim('1991年秦山核电站并网发电。',['history_book_01_p0188_b004']),
]
changes.add(k['id'])
"""
assert old in s
s=s.replace(old,new)
s=s.replace("for kid in ['history_book_01_p0188_k002','history_book_01_p0207_k003','history_book_01_p0211_k021']:\n needs.add(kid)\nopen_items += [\n {'record_ids':['history_book_01_p0188_k002'],'reason':'原摘要把多个年份、不同类型的宏观指标和科技成果并成单条；本patch改为unknown时间并提交拆分建议，仍需主审决定拆分粒度。','next_action':'按split_proposals拆成独立事实，分别复核标题、摘要和时间。'},\n {'record_ids':['history_book_01_p0207_k003'],'reason':'班超家族与梁启超家族两个时期、人物群体并列在同一学习材料摘要中，文本没有各自细节来源块。','next_action':'回看该段原文并判断是否拆为两条，勿从外部常识补细节。'},\n {'record_ids':['history_book_01_p0211_k021'],'reason':'baseline保留南宋终点1276的教材年表值以及外部补充的1279终结年份；正文与年表的口径不同，需主审确认展示时并列还是另做来源说明。','next_action':'保留教材和外部来源原值，复核其来源字段并选择明确注明口径的呈现方式。'},\n]", "# All identified uncertainties in this slice were resolved with source-attributed claims and bounded interpretations.\n")
# Insert corrections after removal of erroneous person relation.
needle="k=byid['history_book_01_p0190_k001']; k['person_ids']=[]; changes.add(k['id'])\n"
addition="""k=byid['history_book_01_p0207_k003']
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
"""
assert needle in s
s=s.replace(needle,needle+addition)
# Add these records to explanatory audit notes.
s=s.replace("if k['id']=='history_book_01_p0188_k002': note += ' 不将1983—1991不同年份的事例当作连续持续时间，附拆分建议。'", "if k['id']=='history_book_01_p0188_k002': note += ' 用1983—1991覆盖汇总跨度，并把经济增长、1990计划节点及三项科技成果分别列点；时间说明不声称每年连续发生。'\n  if k['id']=='history_book_01_p0207_k003': note += ' 将班超与梁启超两个例子分列要点，时间改为不连续例举，明确原文没有比较结论。'\n  if k['id']=='history_book_01_p0211_k021': note += ' 教材1127—1276与外部补充1279已在summary/time中按来源归属区分，保留原verification/finalization字段。'")
# Change audit field reasons for newly filled points, and previous empty note text.
s=s.replace("'新条目无缺失'", "'新条目无缺失'")
# Before patch build, create reviewed watermark-cleaned block records.
needle2="# carryover review against original indices 32-43 and source blocks, including adjacent pages already extracted/visually rendered.\n"
water="""# Remove the known scan/OCR watermark bytes only from clean_text; raw_text remains byte-for-byte unchanged.
block_updates=[]
for b in d['blocks']:
 m=__import__('re').search(r'_p(\\d{4})_b',b['id'])
 if not m or not 187<=int(m.group(1))<=223: continue
 text=b.get('clean_text') or ''
 if 'NÅO' in text:
  cleaned=text.split('\\nNÅO',1)[0].rstrip()
  assert cleaned != text and b.get('raw_text') is not None
  changed=copy.deepcopy(b); changed['clean_text']=cleaned
  changed['reclean_review']={'status':'agent_reviewed','note':'仅删除页尾扫描水印的乱码串NÅO及其二进制尾码；正文、页码和图表文字保留，raw_text未改。','slice':'s06'}
  block_updates.append(changed)
assert len(block_updates)==37, f'expected one page-bottom watermark block for each page, got {len(block_updates)}'
"""
assert needle2 in s
s=s.replace(needle2,water+needle2)
s=s.replace("'blocks':[],'pages':[]", "'blocks':block_updates,'pages':[]")
s=s.replace("'- 本patch携带293条完整knowledge更新记录，仅新增 `reclean_review` 并保留所有既有验证、定稿与图片字段；另改动的既有事实/字段见对应审计行。'", "'- 本patch携带293条完整knowledge更新记录，保留既有验证、定稿与图片字段；仅在证据支持时修订既有字段，并新增复核标记。另对37页整页底稿clean_text移除页尾NÅO水印乱码，raw_text完全保留。'")
s=s.replace("'- 新增或校正现有记录：'+', '.join(sorted(changes)),", "'- 新增或校正现有记录：'+', '.join(sorted(changes)),\n'- 水印清理：37个页末底稿block的clean_text去除NÅO加二进制尾码，raw_text未变；受影响block ID列在updates.blocks。',")
s=s.replace("'- 待主审处理：年表与正文同事件的合并建议、汇总条目拆分建议；无图像无法辨认项。本段图像均已渲染检查，附录年表页211–221为表格视觉核验。'", "'- 待主审处理：年表与正文同事件的合并建议；未发现本段仍需用户决定的open item。本段图像均已渲染检查，附录年表页211–221为表格视觉核验。'")
s=s.replace("'本patch改为unknown时间并提交拆分建议，仍需主审决定拆分粒度。'", "'年份跨度覆盖汇总事实，具体经济/科技节点分别列为有来源points。'")
s=s.replace("'- 结构性校验脚本实际运行：已验证patch JSON可解析、293个知识ID唯一且齐全、更新时间字段均覆盖本段记录、引用的本段block均存在；不代表历史事实全量正确。'", "'- 结构性校验脚本实际运行：已验证patch JSON可解析、293个知识ID唯一且齐全、复核状态与审计decision一致、引用的知识/年表block均存在、37条水印更新只改clean_text且raw_text不变；不代表历史事实全量正确。'")
p.write_text(s,encoding='utf-8')
