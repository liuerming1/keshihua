import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923');f=root/'s01.patch.json';p=json.loads(f.read_text(encoding='utf8'));K={k['id']:k for k in p['updates']['knowledge']}
def c(txt,ids):return {'text':txt,'evidence_block_ids':ids}
def set_claim(i,field,txt,ids):
 if field in ('flow','points'):K[i][field]=[c(txt,ids)]
 else:K[i][field]=c(txt,ids)
# Additional substantive content directly stated in the remaining source blocks.
set_claim('history_book_01_p0011_k001','points','龙山文化以黑陶为代表，蛋壳陶胎壁极薄；红山、良渚文化有玉器，并出现较大祭坛、神庙。',['history_book_01_p0011_b003'])
set_claim('history_book_01_p0011_k001','impact','大汶口、良渚考古发现显示私有制产生、阶级分化明显，部落出现权贵阶层；教材据此称中国即将迈入阶级社会门槛。',['history_book_01_p0011_b003'])
set_claim('history_book_01_p0011_k002','background','母系氏族社会生产力低下，氏族成员共同劳动、成果共享；新石器时代晚期生产和社会关系变化中，贫富分化、不平等开始出现。',['history_book_01_p0011_b003'])
set_claim('history_book_01_p0011_k002','impact','私有制、阶级分化和部落权贵出现，氏族联系趋紧并形成更大部落或部落联盟，社会向阶级社会发展。',['history_book_01_p0011_b003'])
set_claim('history_book_01_p0011_k003','points','传说五帝时期有炎黄部落联盟、尧舜禅让；相当于五帝后期的龙山文化时代已出现邦国林立的“万邦”局面，陶寺遗址有宫殿、天文建筑和礼器。',['history_book_01_p0011_b003'])
set_claim('history_book_01_p0011_k003','impact','陶寺都城规模、建筑与阶级分化特征使部分专家认为其具备国家初始形态；这是考古学判断，保留教材限定。',['history_book_01_p0011_b003'])
set_claim('history_book_01_p0011_k004','points','传说黄帝与炎帝结成部落联盟，被后世共尊为华夏始祖；尧年老后经推举和考察，由舜继位，这种做法称禅让。',['history_book_01_p0011_b003'])
set_claim('history_book_01_p0012_k001','flow','禹因治水有功而受舜禅让，成为联盟首领；约公元前2070年建立夏朝；禹死后启继位，世袭制取代禅让制。',['history_book_01_p0012_b003'])
set_claim('history_book_01_p0012_k001','points','夏王为最高统治者，中央设行政、军事、司法、宗教机构和职官；夏部族生活地区直接统治，其他地区主要通过控制部族间接统治。',['history_book_01_p0012_b003'])
set_claim('history_book_01_p0012_k002','background','夏桀暴虐无道，百姓不断反抗夏朝统治。',['history_book_01_p0012_b003'])
set_claim('history_book_01_p0012_k002','flow','约公元前1600年商汤率军伐桀，夏兵大败，桀被放逐到南方，夏朝灭亡；汤建立商朝。',['history_book_01_p0012_b003'])
set_claim('history_book_01_p0012_k005','flow','商朝前期都城多次迁移，后来定于殷，因此商朝也称殷朝；河南安阳殷墟遗址出土大量刻字龟甲、兽骨。',['history_book_01_p0012_b003'])
set_claim('history_book_01_p0014_k003','impact','教材称商和西周时期农业、手工业发展并走向繁荣，青铜器种类繁多，形成灿烂青铜文化。',['history_book_01_p0014_b001'])
set_claim('history_book_01_p0017_k002','impact','华夏族吸收周边民族成员后更加稳定、分布更广；民族交融与共同祖先观念得到发展。',['history_book_01_p0017_b003'])
set_claim('history_book_01_p0018_k001','impact','农业进步推动社会分工，促进工商业繁荣；各阶级关系变化，推动上层建筑变革并成为战国变法潮流的重要背景。',['history_book_01_p0018_b003'])
set_claim('history_book_01_p0027_k001','background','秦朝重视法制建设，制定名目繁多、分类细密的法律，但传世文献保存下来的秦律很少。',['history_book_01_p0027_b001'])
set_claim('history_book_01_p0027_k001','impact','睡虎地秦简丰富对秦律的认识；教材指出出土文献常能印证、纠正或补充传世文献。',['history_book_01_p0027_b001'])
set_claim('history_book_01_p0031_k001','background','东汉中期后皇帝多幼年继位且年寿不长，太后临朝使外戚掌权；皇帝长大后借宦官清除外戚，宦官继而掌政。',['history_book_01_p0031_b002'])
set_claim('history_book_01_p0031_k001','impact','外戚、宦官各谋私利、相互争斗，导致东汉后期政治腐朽黑暗；士人清议遭镇压，形成党锢之祸。',['history_book_01_p0031_b002'])
set_claim('history_book_01_p0032_k001','impact','教材称造纸术逐步传播到世界各地，促进人类文明发展；不将传播时间和路线在此页没有的内容补入。',['history_book_01_p0032_b001'])
set_claim('history_book_01_p0032_k002','impact','《伤寒杂病论》奠定中医临床学基础；麻沸散被教材称为世界最早的麻醉药；五禽戏是强身健体方法。',['history_book_01_p0032_b002'])
set_claim('history_book_01_p0033_k002','background','东汉时期豪强地主势力迅速发展，土地兼并严重，阶级矛盾日益尖锐。',['history_book_01_p0033_b002'])
set_claim('history_book_01_p0033_k002','impact','豪强地主势力扩张与中央政权控制削弱、东汉政权走向衰亡相连；教材讨论其关系，但不把单一因素写作唯一原因。',['history_book_01_p0033_b002'])
set_claim('history_book_01_p0038_k002','impact','前秦迅速崩溃后，曾稍显缓和的民族矛盾又加剧。',['history_book_01_p0038_b002'])
set_claim('history_book_01_p0038_k003','impact','孝文帝改革缓解民族矛盾，促进北魏经济发展和社会繁荣，并为以后北方统一南方及隋唐盛世打下基础。',['history_book_01_p0039_b001'])
# The page-37 territorial detail is a point, not a chronology claim; retain its event-level time ambiguity for review.
# Append specific audit notes, so the review records the findings rather than a blank-field template.
notes={
'history_book_01_p0011_k001':'第11页同一段包含龙山黑陶、红山/良渚祭坛神庙与私有制/阶级分化；分别补points与impact，未把考古解释提升为无条件事实。',
'history_book_01_p0011_k002':'母系社会的生产力及共同劳动是教材给出的背景，父系氏族下分化与权贵出现是发展结果，已分开归类。',
'history_book_01_p0011_k003':'龙山“万邦”及陶寺建筑有原文证据；“具备国家初始形态”明确保留为专家判断。',
'history_book_01_p0012_k001':'补出禹治水、舜禅让、夏朝建立、启继位和夏朝管理层次，均来自p0012_b003。',
'history_book_01_p0012_k002':'桀的暴政列为起因，汤伐桀、夏亡、商建按源文顺序写成流程。',
'history_book_01_p0012_k005':'迁都最终定于殷的顺序与称殷缘由依据本页原文，作为流程保存。',
'history_book_01_p0014_k003':'把农业/手工业繁荣和青铜文化作为教材明言的影响/结果，不补地理或年代。',
'history_book_01_p0017_k002':'原文明确叙述华夏族吸收新成员后更加稳定、分布更广，补入impact。',
'history_book_01_p0018_k001':'原文明确写农业推动分工、工商业繁荣，并带动阶级关系和上层建筑变化，补入impact。',
'history_book_01_p0027_k001':'“传世秦律少”作为出土睡虎地竹简的背景，“丰富认识/补充传世文献”作为影响。',
'history_book_01_p0031_k001':'按原文拆开外戚/宦官交替的制度原因与其导致的政治黑暗、党锢后果。',
'history_book_01_p0032_k001':'仅填教材直接概括的世界传播影响，不补具体传播年代。',
'history_book_01_p0032_k002':'分别照教材描述三种科技/医学成果的应用或意义，不追加页外史实。',
'history_book_01_p0033_k002':'土地兼并、阶级矛盾作为背景；豪强扩张与政权衰亡的关系按教材讨论限定表达。',
'history_book_01_p0038_k002':'前秦战败、崩溃后的民族矛盾再度加剧是源文明确后果，补入impact。',
'history_book_01_p0038_k003':'孝文帝改革的民族、经济、社会和后世影响源自第39页跨页块，作为影响写入并保留外部页块ID。'}
for a in p['knowledge_audit']:
 if a['id'] in notes:a['note']+=' '+notes[a['id']]
 k=K[a['id']]
 for fld in ('flow','points','background','impact'):
  if k.get(fld):a.get('empty_reasons',{}).pop(fld,None)
 k['reclean_review']['note']=a['note']+(' 仍有待核事项，见open_items/split_proposals。' if a['decision']=='needs_review' else '')
p['updates']['knowledge']=list(K.values())
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
