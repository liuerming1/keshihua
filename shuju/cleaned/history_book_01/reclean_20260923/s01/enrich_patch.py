import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923'); patch=root/'s01.patch.json'; p=json.loads(patch.read_text(encoding='utf8')); K={k['id']:k for k in p['updates']['knowledge']}; base=json.loads((root/'baseline.json').read_text(encoding='utf8')); blocks={b['id']:b for b in base['blocks']}
def claim(txt,ids): return {'text':txt,'evidence_block_ids':ids}
def setc(i,f,txt,ids): K[i][f]=claim(txt,ids)
def points(i,ls,ids): setc(i,'points',ls,ids)
def add_ev(i,ids):
 for x in ids:
  if x not in K[i]['evidence_block_ids']:K[i]['evidence_block_ids'].append(x)
# Source-supported content skipped by the initial summary-only extraction.
points('history_book_01_p0012_k002','夏桀暴虐无道、百姓反抗；约公元前1600年商汤率军伐桀，夏兵战败，桀被放逐，夏朝灭亡。',['history_book_01_p0012_b003'])
points('history_book_01_p0012_k003','《夏小正》载一年各月的物候、天象、气象和农事；干支纪日法是商朝历法的主要成就。',['history_book_01_p0012_b003'])
points('history_book_01_p0012_k004','《史记·夏本纪》记益让位于启；《战国策·燕策一》则记启与党羽攻益并夺取天下。教材将二者并列为不同记载，未裁定其一为实。',['history_book_01_p0012_b003'])
points('history_book_01_p0012_k005','商朝前期都城多次迁移，后来定于殷，故商朝亦称殷朝；安阳殷墟出土大量刻字龟甲、兽骨。',['history_book_01_p0012_b003'])
setc('history_book_01_p0013_k002','flow','商纣统治引发社会矛盾；周武王于公元前1046年伐纣，牧野之战中商军倒戈，周军攻入商都，纣王自焚，商亡；周武王建周并定都镐京，史称西周。',['history_book_01_p0013_b003'])
setc('history_book_01_p0013_k002','background','商朝晚期社会矛盾尖锐，纣王生活腐朽并以炮烙之刑残害臣民，引起共愤。',['history_book_01_p0013_b003'])
setc('history_book_01_p0013_k002','impact','周武王建立周朝，定都镐京，进入西周；事件结束商朝统治。',['history_book_01_p0013_b003'])
points('history_book_01_p0013_k003','周以分封亲族“蕃屏周”；分封制建立天子至士的等级结构，加强周天子对地方的政治统治；宗法制与分封制相互补充，缓和统治阶级内部权力与财产分配冲突。',['history_book_01_p0013_b003'])
setc('history_book_01_p0013_k003','impact','教材称分封制加强周天子对地方的政治统治，宗法制与其互补，解决统治阶级内部权力和财产分配方面的冲突与矛盾。',['history_book_01_p0013_b003'])
setc('history_book_01_p0014_k001','impact','宗法制与分封制结合，形成政权与族权结合的局面。',['history_book_01_p0014_b001'])
points('history_book_01_p0014_k002','周厉王出逃后，召公、周公共同执政，称“共和行政”；公元前771年犬戎攻破镐京、杀周幽王，西周灭亡；公元前770年周平王东迁洛邑。',['history_book_01_p0014_b001'])
points('history_book_01_p0016_k001','周平王东迁后进入东周；周天子控制力渐弱，桓王与郑国交战败北，此后诸侯争夺霸权，“礼乐征伐自天子出”的时代结束。',['history_book_01_p0016_b003'])
points('history_book_01_p0017_k001','晋国被韩、赵、魏三家瓜分，田氏取代齐国姜姓国君；长期兼并后形成齐、楚、燕、韩、赵、魏、秦七雄；公元前256年秦吞并周王室。',['history_book_01_p0017_b003'])
setc('history_book_01_p0018_k002','background','兼并战争日益激烈，各国为富国强兵而开展改革。',['history_book_01_p0018_b003'])
setc('history_book_01_p0018_k002','impact','教材称各国变法推动社会转型，逐步建立君主专制政治制度；秦国商鞅变法效果最为显著。',['history_book_01_p0018_b003'])
points('history_book_01_p0019_k001','商鞅变法包括奖励耕织与军功、限制贵族特权、拆分大家庭、废井田开阡陌并授田、什伍连坐和普遍推行县制，县主要官员由君主任免。',['history_book_01_p0019_b003'])
# Avoid double-using copied point claims; points have already been explicitly authored above.
points('history_book_01_p0021_k002','《诗经》汇集西周至春秋诗歌，是现存第一部诗歌总集，分风、雅、颂，以四言为主；战国后期屈原创作楚辞，《离骚》《天问》为代表。',['history_book_01_p0021_b001'])
setc('history_book_01_p0021_k002','impact','《诗经》的人文精神与现实主义传统影响后世文学；屈原的爱国主义精神被教材评价为中华优秀传统文化的宝贵财富。',['history_book_01_p0021_b001'])
points('history_book_01_p0023_k001','秦以远交近攻、分化瓦解、各个击破灭六国并定都咸阳；随后征服南方越族、加强对西南夷控制、击退北方匈奴，前214年修筑临洮至辽东长城。',['history_book_01_p0023_b001'])
points('history_book_01_p0023_k002','中央设三公九卿，地方行郡县制，县以下设乡、里、亭；统一车轨、文字、货币、度量衡，修驰道与直道，颁法、编户籍并迁徙六国贵族豪强。',['history_book_01_p0023_b001'])
points('history_book_01_p0024_k001','始皇大兴土木修宫殿、陵墓，求仙访药，巡游封禅并繁重征发；秦律严苛，出现“赭衣塞路，囹圄成市”等社会状况。',['history_book_01_p0024_b001'])
points('history_book_01_p0025_k001','秦始皇下令焚毁非秦史书、非博士官所藏《诗》《书》及诸子百家著作（医药卜筮种树之书除外）；以“或为妖言以乱黔首”为由坑杀460余名儒生方士。',['history_book_01_p0025_b001'])
setc('history_book_01_p0025_k002','flow','公元前209年戍卒大泽乡遇雨误期，陈胜、吴广起义并自立为王号“张楚”；起义迅速蔓延。陈胜起义失败后，项羽、刘邦等反秦势力壮大；公元前207年刘邦进占咸阳，秦亡。',['history_book_01_p0025_b001','history_book_01_p0026_b001'])
points('history_book_01_p0026_k001','刘邦“约法三章”、废除秦苛法，善用人才并听取意见；项羽刚愎、不善用人、赏罚不明、烧杀掳掠、分封失当且缺稳固根据地，最终败于刘邦。',['history_book_01_p0026_b001'])
setc('history_book_01_p0026_k001','background','秦朝灭亡后刘邦与项羽争夺统治权，爆发楚汉战争；教材只称战争持续四年，没有给起止公元年份。',['history_book_01_p0026_b001'])
setc('history_book_01_p0026_k001','impact','楚汉战争以刘邦胜利、项羽失败告终，为西汉建立铺垫；具体建国年份另见第28页，不在本条推算。',['history_book_01_p0026_b001','history_book_01_p0028_b001'])
setc('history_book_01_p0028_k001','flow','刘邦公元前202年建立西汉、定都长安；汉初尊奉黄老、减轻赋税徭役刑罚并提倡节俭；文帝、景帝时期经济恢复、社会稳定，形成“文景之治”。',['history_book_01_p0028_b001'])
points('history_book_01_p0029_k001','政治措施含推恩令、设中朝、察举、州部刺史监察和打击豪强；经济措施含中央铸币、盐铁官营、均输平准和财产税；思想上采纳董仲舒建议尊崇儒术。',['history_book_01_p0029_b001'])
setc('history_book_01_p0029_k001','impact','加强中央集权并巩固大一统；教材称此后儒学成为封建社会主流意识形态。',['history_book_01_p0029_b001'])
points('history_book_01_p0029_k002','汉武帝任用卫青、霍去病三次大规模反击匈奴，控制阴山以南和河西走廊大片地区并设河西四郡；派张骞两次出使西域，拓展交通道路。',['history_book_01_p0029_b001'])
setc('history_book_01_p0029_k002','background','汉初匈奴势力强大，多次袭击汉朝边境；汉武帝在稳固边疆基础上积极开拓疆域。',['history_book_01_p0029_b001'])
setc('history_book_01_p0029_k002','impact','丝织品沿通道传往中亚、西亚、欧洲和北非；教材称张骞出使拓展中西交通，并促进西域与中原政治、经济、文化联系。',['history_book_01_p0029_b001','history_book_01_p0030_b001'])
setc('history_book_01_p0030_k002','impact','王莽改革不切实际，社会矛盾加剧；西汉统治被新朝取代。',['history_book_01_p0030_b006'])
setc('history_book_01_p0030_k003','impact','绿林军攻入长安推翻王莽政权；25年刘秀重建汉朝，转入东汉。',['history_book_01_p0030_b006'])
points('history_book_01_p0031_k001','外戚与宦官交替专权；东汉中期以后出现党锢之祸，政治腐败。',['history_book_01_p0031_b002'])
setc('history_book_01_p0031_k002','background','东汉后期政治腐败、土地兼并加剧，民众生活困难；张角以太平道组织民众起事。',['history_book_01_p0031_b002'])
setc('history_book_01_p0031_k002','impact','黄巾起义虽迅速被镇压，但动摇东汉统治基础；地方州牧拥兵自重，东汉政权名存实亡。',['history_book_01_p0031_b002'])
points('history_book_01_p0031_k003','《史记》为纪传体通史，记述传说中的黄帝至汉武帝时期；《汉书》为纪传体断代史，记载西汉历史。',['history_book_01_p0031_b003'])
points('history_book_01_p0031_k004','汉赋讲究铺陈排比、辞藻华丽；乐府诗源于乐府采集并整理的民歌；东汉民间流行语言朴实生动、传播广泛的五言诗。',['history_book_01_p0031_b006','history_book_01_p0032_b001'])
points('history_book_01_p0032_k001','蔡伦改进造纸术，原料包含树皮、麻头、破布、鱼网；造纸术后来逐步传播到世界各地。',['history_book_01_p0032_b001'])
points('history_book_01_p0032_k002','张衡制成地动仪；张仲景总结临床经验著《伤寒杂病论》；华佗擅长外科并创制麻沸散和五禽戏。',['history_book_01_p0032_b002'])
points('history_book_01_p0033_k001','教材以司马迁、霍去病、张骞、苏武、马援、班超等事迹呈现两汉人物的家国情怀；保留各人物各自行为，不概括成同一经历。',['history_book_01_p0033_b001'])
points('history_book_01_p0033_k002','豪强地主凭借经济、政治势力控制地方并兼并土地；东汉后期中央控制削弱，豪强势力与政权衰亡相连。',['history_book_01_p0033_b002'])
points('history_book_01_p0035_k001','《三国志》记载207年刘备三顾诸葛亮；诸葛亮在《隆中对》中分析天下形势，提出联孙抗曹、占据荆益后图取天下的战略。',['history_book_01_p0035_b002'])
points('history_book_01_p0035_k002','220年曹丕称帝定都洛阳、建魏；刘备称帝、建蜀汉于成都；孙权称帝、都建业，鼎立局面形成。',['history_book_01_p0035_b006','history_book_01_p0036_b001'])
setc('history_book_01_p0036_k001','flow','266年司马炎代魏称帝建西晋；280年西晋灭吴，完成统一。',['history_book_01_p0036_b001'])
points('history_book_01_p0036_k002','北方少数民族自东汉以来陆续内迁；西晋末年形成多个并立政权，316年西晋灭亡。',['history_book_01_p0036_b002'])
points('history_book_01_p0037_k002','北方高门士族南迁并执掌东晋朝政；王导任宰相、王敦领兵坐镇长江中游，“王与马，共天下”；此后庾、桓、谢、太原王氏相继掌权。',['history_book_01_p0037_b002','history_book_01_p0037_b004'])
points('history_book_01_p0038_k003','拓跋鲜卑于4世纪末建立北魏，439年统一北方；5世纪后期孝文帝迁都洛阳，改鲜卑姓为汉姓、禁鲜卑语并推行汉服，鼓励鲜卑与汉族高门通婚。教材称改革缓解民族矛盾、促进北魏经济社会发展。',['history_book_01_p0038_b002','history_book_01_p0039_b001'])
# Link named people only where exact local IDs exist and are directly stated in cited passages.
people={x['id']:x for x in base['people']}
for kid,pid in [('history_book_01_p0019_k001','history_book_01_p0019_person001'),('history_book_01_p0019_k002','history_book_01_p0019_person002'),('history_book_01_p0019_k003','history_book_01_p0019_person003')]:
 if pid in people and pid not in K[kid]['person_ids']: K[kid]['person_ids'].append(pid)
# Page 38 table content is not confidently recoverable at contact-sheet scale; make block explicit, not summarized away.
bid='history_book_01_p0038_b009'
for b in p['updates']['blocks']:
 if b['id']==bid:
  b['clean_text']='十六国统治者族属表。现有可读提取：匈奴—前赵、北凉、夏、后赵；羯—后赵；氐—前秦、后凉、后秦、成汉；羌—[无法辨认]；鲜卑—前燕、后燕、南燕、南凉、西秦；汉—前凉、北燕、西凉。族属与政权逐格对应仍需放大核验。'
  b['notes']=list(b.get('notes') or [])+['视觉复核只确认表格标题与族属栏；政权对应关系保留提取结果并标注未核，不据常识改填。']
# Explicitly keep unread table issue in review_issues and page image status partial.
issue={'id':'history_book_01_s01_issue_table_p0038','record_ids':['history_book_01_p0038_b009','history_book_01_p0038'],'category':'image','description':'第38页十六国族属表的字体较小，未能在本轮视觉检查中逐格确认羌族及各政权的对应关系。','evidence_block_ids':['history_book_01_p0038_b009'],'suggested_action':'放大渲染PDF第38页表格并逐格比对，确认后再清除[无法辨认]和核验标记。','blocking':True,'status':'open'}
p['updates']['review_issues']=[x for x in p['updates'].get('review_issues',[]) if x.get('id')!=issue['id']]+[issue]
# Notes for claims that are substantive changes; keep audit and status aligned.
for a in p['knowledge_audit']:
 k=K[a['id']]
 a['evidence_block_ids']=k['evidence_block_ids']
 if a['id'] in {'history_book_01_p0012_k002','history_book_01_p0012_k003','history_book_01_p0012_k004','history_book_01_p0012_k005','history_book_01_p0013_k002','history_book_01_p0013_k003','history_book_01_p0014_k001','history_book_01_p0014_k002','history_book_01_p0016_k001','history_book_01_p0017_k001','history_book_01_p0018_k002','history_book_01_p0021_k002','history_book_01_p0023_k001','history_book_01_p0023_k002','history_book_01_p0024_k001','history_book_01_p0025_k001','history_book_01_p0025_k002','history_book_01_p0026_k001','history_book_01_p0028_k001','history_book_01_p0029_k001','history_book_01_p0029_k002','history_book_01_p0030_k002','history_book_01_p0030_k003','history_book_01_p0031_k001','history_book_01_p0031_k002','history_book_01_p0031_k003','history_book_01_p0031_k004','history_book_01_p0032_k001','history_book_01_p0032_k002','history_book_01_p0033_k001','history_book_01_p0033_k002','history_book_01_p0035_k001','history_book_01_p0035_k002','history_book_01_p0036_k001','history_book_01_p0036_k002','history_book_01_p0037_k002','history_book_01_p0038_k003'}:
  if a['decision']!='needs_review':a['decision']='changed'; k['reclean_review']['status']='agent_reviewed'
 # specific audit conclusion keyed to the final sourced field additions
 if a['id']=='history_book_01_p0019_k001':a['note']+=' 补入背景“战国变法潮流”和教材明载的影响“秦国国富兵强、为统一奠基”，分别引用p0018_b003/p0019_b003。'
 elif a['id']=='history_book_01_p0022_k001':a['note']+=' 已将长期战乱、区域经济、秦地理物质条件、历代治理和商鞅变法分别归入背景；教材关于统一促进交往交流交融的评价归入影响。'
 elif a['id']=='history_book_01_p0020_k001':a['note']+=' 教材明确提供了社会经济与阶级变化的成因、学派思想要点及深远影响，已分别拆进background、points、impact。'
 elif a['id']=='history_book_01_p0035_k002':a['note']+=' 原mode=unknown却有start_year=220的冲突已消除；按本页220年与第36页280年结尾改为duration，追加跨页证据。'
 elif 20<=int(a['id'].split('_p')[1][:4])<=29:
  a['note']+=' 已从来源clean_text尾部去除NÅO开头的乱码水印；raw_text完全未改。'
 # Recompute per-field emptiness explanation against final record, avoiding a generic template for filled content.
 empty=a.get('empty_reasons',{})
 for fld in ['flow','points','background','impact']:
  if k.get(fld):empty.pop(fld,None)
 a['empty_reasons']=empty
 k['reclean_review']['note']=a['note']+(' 仍需核验，详见open_items。' if a['decision']=='needs_review' else '')
p['updates']['knowledge']=list(K.values())
patch.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print('knowledge',len(K),'claims completed','junk-clean blocks',sum(1 for b in p['updates']['blocks'] if 20<=int(b['id'].split('_p')[1][:4])<=29),'issues',len(p['updates']['review_issues']))

