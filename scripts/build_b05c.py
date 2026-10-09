import json
import re
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(r"D:\ai\codex\知识可视化")
PDF = ROOT / "shuju" / "普通高中教科书·历史必修_中外历史纲要（上）.pdf"
OUT = ROOT / "shuju" / "cleaned" / "history_book_01" / "parts"
DOC = "history_book_01"
PAGES = list(range(169, 178))
reader = PdfReader(str(PDF))

def pid(p): return f"{DOC}_p{p:04d}"
def bid(p, n): return f"{pid(p)}_b{n:03d}"
def aid(p, n): return f"{pid(p)}_a{n:03d}"
def kid(p, n): return f"{pid(p)}_k{n:03d}"
def iid(p, n): return f"{pid(p)}_inv{n:03d}"
def rid(p, n): return f"{pid(p)}_r{n:03d}"
def issueid(p, n): return f"{pid(p)}_issue{n:03d}"
def claim(text, evidence): return {"text": text, "evidence_block_ids": evidence}
def tm(source, mode, start=None, end=None, precision="unknown", end_status="unknown", evidence=None):
    return {"source_text": source, "mode": mode, "start_year": start, "end_year": end,
            "earliest_year": None, "latest_year": None, "precision": precision,
            "end_status": end_status, "normalization_note": None,
            "evidence_block_ids": evidence or []}
def clean(s): return re.sub(r"[ \t\r\n]+", "", s)

chap25 = ["第九单元 中华人民共和国成立和社会主义革命与建设", "第25课 中华人民共和国成立和向社会主义的过渡"]
chap26 = ["第九单元 中华人民共和国成立和社会主义革命与建设", "第26课 社会主义建设在探索中曲折发展"]
printed = {169:"162",170:"163",171:"164",172:"165",173:"166",174:"167",175:"168",176:"169",177:"170"}
data = {"schema_version":"history-pdf-ingest/1.0",
 "batch":{"id":"history_book_01_b05c","document_id":DOC,"requested_pdf_pages":PAGES,
          "completed_pdf_pages":PAGES,"partial_pdf_pages":[],"unprocessed_pdf_pages":[],
          "complete":True,"next_pdf_page":None,"carryover":[]},
 "documents":[{"id":DOC,"file_name":"普通高中教科书·历史必修_中外历史纲要（上）.pdf",
   "title":"普通高中教科书·历史必修 中外历史纲要（上）","edition":None,"volume":"上",
   "publisher":"人民教育出版社","publication_year":None,"total_pdf_pages":len(reader.pages),
   "language":"zh-CN","source_kind":"textbook","sha256":None}],
 "pages":[],"blocks":[],"assets":[],"places":[],"people":[],"knowledge":[],"relations":[],
 "map_candidates":[],"inventory":[],"review_issues":[],
 "validation":{"structure_check_status":"not_run","duplicate_ids":[],"dangling_references":[],
  "page_coverage_issues":[],"time_issues":[],"source_issues":[],"unreadable_blocks":[],
  "unprocessed_assets":[],"semantic_review_status":"not_performed"}}

def add_block(p, n, typ, text, assets=None, note=None):
    data["blocks"].append({"id":bid(p,n),"page_id":pid(p),"order":n,"type":typ,"bbox":None,
      "raw_text":text,"clean_text":text,"asset_ids":assets or [],"table_data":None,
      "notes":[note or "按版面语义切分；bbox未据可靠定位，保留null。"]})

for p in PAGES:
    raw = reader.pages[p-1].extract_text() or ""
    data["pages"].append({"id":pid(p),"document_id":DOC,"pdf_page_number":p,
      "printed_page_label":printed[p],"chapter_path":chap25 if p<=173 else chap26,
      "page_kind":"content","text_status":"complete","image_status":"complete",
      "notes":["文字层逐页读取；PDF页序与印刷页码分开记录。",
               f"已渲染检查：tmp_pdf_b05c_render_20260921b/page-{p}.png。",
               "未导出裁剪图片，assets.file_path保持null。"]})
    add_block(p,1,"note",raw,note="保留该页PDF文字层全量原串；其余块按标题、段落、图注和边栏语义拆分。")

segments = {
169:[("paragraph","1950年6月25日朝鲜内战爆发；美国扩大侵朝战争并威胁中国国家安全。1950年10月中国人民志愿军入朝作战，经过五次战役和边谈边打，1953年7月美国在停战协定上签字。志愿军英雄事迹锻造了伟大抗美援朝精神。"),("note","史料阅读：彭德怀《关于中国人民志愿军抗美援朝工作的报告》（1953年9月12日）。"),("note","历史纵横：“特级战斗英雄”杨根思；江苏泰兴人，在抗美援朝第二次战役中坚守1071.1高地。"),("caption","▲ 中国人民志愿军跨过鸭绿江")],
170:[("heading","开创独立自主的和平外交"),("paragraph","新中国成立后按照“一边倒”“另起炉灶”和“打扫干净屋子再请客”等方针建交并取消帝国主义在中国的特权。"),("note","学习聚焦：新中国进行的积极外交活动为国家建设争取到有利的国际环境。"),("note","历史纵横：1954年4月日内瓦会议讨论朝鲜问题和印度支那问题。"),("caption","▲ 中国政府代表在日内瓦会议上")],
171:[("paragraph","1953年12月周恩来第一次提出和平共处五项原则；1954年6月中印、中缅正式倡议其作为国际关系准则。"),("note","史料阅读与学思之窗：周恩来提出求同存异；结合历史与现实理解和平共处五项原则。"),("paragraph","1955年4月万隆亚非会议，中国坚持求同存异并推动会议达成协议。"),("heading","社会主义基本制度的建立"),("paragraph","1953年提出过渡时期总路线并实施第一个五年计划，逐步实现社会主义工业化和社会主义改造。")],
172:[("paragraph","1956年基本完成对农业、手工业和资本主义工商业的社会主义改造，生产资料公有制占绝对优势的社会主义经济制度初步建立；第一个五年计划提前完成。"),("paragraph","1954年9月第一届全国人民代表大会第一次会议在北京举行，通过《中华人民共和国宪法》，确立人民代表大会制度为根本政治制度。"),("caption","▲ 上海国棉一厂发出开展增产节约和劳动竞赛号召"),("caption","▲ 1956年1月15日工商界代表向毛泽东呈送喜报"),("caption","▲ 1954年9月15日至28日第一届全国人民代表大会第一次会议")],
173:[("heading","探究与拓展"),("exercise","1954年《中华人民共和国宪法》节选：人民代表大会是国家权力机关，全国人民代表大会是最高国家权力机关，是行使国家立法权的唯一机关。"),("exercise","结合宪法条文，理解人民代表大会制度是我国的根本政治制度。"),("exercise","运用唯物史观，阐述中华人民共和国成立的伟大历史意义。")],
174:[("heading","第26课 社会主义建设在探索中曲折发展"),("paragraph","1956年社会主义基本制度已经建立，中共八大的举行标志着探索中国自己的社会主义建设道路取得初步成果。"),("heading","全面建设社会主义"),("paragraph","中共八大指出国内主要矛盾和当前主要任务，提出把我国从落后的农业国变为先进的工业国。"),("note","历史纵横：1956年4月28日提出“百花齐放、百家争鸣”方针，促进艺术发展、科学进步和社会主义文化繁荣。"),("caption","▲ 中共八大会场")],
175:[("note","史料阅读：《论十大关系》：努力调动党内党外、国内国外一切积极因素。"),("paragraph","1957年春毛泽东提出正确处理人民内部矛盾的重要思想；反右派斗争被严重扩大化。"),("note","学思之窗：国家的统一、人民的团结和各民族团结是事业胜利的基本保证。"),("paragraph","1958年掀起大跃进和人民公社化运动；1959至1961年经济发生严重困难。1961年八字方针调整国民经济，1962年七千人大会总结经验，1962年下半年至1965年国民经济稳步增长。"),("caption","▲ 七千人大会期间，毛泽东、刘少奇、周恩来、朱德、陈云、邓小平在一起")],
176:[("caption","▲ 1971年10月周恩来在北京东方红石油化工总厂视察"),("paragraph","1964年三届全国人大一次会议提出建设四个现代化的伟大目标。"),("heading","“文化大革命”"),("paragraph","1966年夏文化大革命全面发动；1967年一月风暴造成社会和生产秩序混乱。"),("paragraph","1969年中共九大；1971年林彪集团策动武装政变；1972年周恩来主持中央日常工作；1975年邓小平整顿；1976年10月粉碎江青反革命集团，结束了"),("note","学习聚焦：文化大革命的理论和实践都是错误的。")],
177:[("paragraph","文化大革命不是革命或社会进步，而是由领导者错误发动、被反革命集团利用的严重灾难和内乱。"),("caption","▲ 首都群众在天安门广场举行集会和游行，庆祝粉碎“四人帮”的重大胜利"),("heading","伟大的建设成就"),("note","学习聚焦：社会主义建设在曲折探索中仍取得伟大成就，具有开创性、奠基性意义。"),("paragraph","从新中国成立到改革开放前，中国在工业、农业、科技、国防、外交、文化教育等方面取得巨大成就，逐步建立独立、比较完整的工业体系和国民经济体系。"),("note","史料阅读：邓小平关于毛泽东功过及主要缔造者地位的论述。")]
}
for p, rows in segments.items():
    for i,(typ,text) in enumerate(rows,2): add_block(p,i,typ,text)

# Attach image assets to the corresponding caption blocks.
asset_specs = [(169,1,5,"photo","中国人民志愿军跨过鸭绿江","图注确认志愿军跨过鸭绿江。"),(170,1,6,"photo","中国政府代表在日内瓦会议上","图注确认中国政府代表在日内瓦会议上的会议照片。"),(172,1,4,"photo","上海国棉一厂发出开展增产节约和劳动竞赛号召","图注提供工厂与劳动竞赛信息。"),(172,2,5,"photo","1956年1月15日工商界代表向毛泽东呈送喜报","图注提供日期、庆祝大会与人物关系。"),(172,3,6,"photo","1954年9月15日至28日第一届全国人民代表大会第一次会议","图注提供会议日期、地点和人物名单。"),(174,1,7,"photo","中共八大会场","图注确认中共八大会场。"),(175,1,6,"photo","七千人大会期间六位领导人在一起","图注列出毛泽东、刘少奇、周恩来、朱德、陈云、邓小平。"),(177,1,3,"photo","首都群众在天安门广场庆祝粉碎“四人帮”","图注确认庆祝粉碎‘四人帮’的集会和游行。")]
for p,n,blockn,typ,caption,desc in asset_specs:
    data["assets"].append({"id":aid(p,n),"page_id":pid(p),"block_id":bid(p,blockn),"type":typ,"bbox":None,"file_path":None,"caption":caption,"visible_text":None,"description":desc,"claims":[claim(desc,[bid(p,blockn)])],"notes":["由逐页渲染图确认存在；未导出独立图片文件。"]})
    for b in data["blocks"]:
        if b["id"] == bid(p,blockn): b["asset_ids"].append(aid(p,n))

# Minimal entity registries retain explicit names without inventing coordinates.
for p,names in {169:["朝鲜","鸭绿江","长津湖","江苏泰兴","台湾海峡"],170:["日内瓦","印度支那"],171:["印度尼西亚万隆","印度","缅甸"],172:["北京","上海"],176:["北京东方红石油化工总厂"],177:["天安门广场"]}.items():
    for i,name in enumerate(names,1):
        data["places"].append({"id":f"{pid(p)}_place{i:03d}","name_as_written":name,"name_type":"historical","valid_time_text":None,"coordinates":None,"spatial_precision":"unknown","coordinate_evidence_block_ids":[],"evidence_block_ids":[bid(p,1)],"notes":["教材页未提供可核验经纬度，坐标保留null。"]})
for p,names in {169:["毛泽东","彭德怀","杨根思","黄继光","邱少云","罗盛教"],171:["周恩来"],172:["毛泽东","董必武","周恩来","刘少奇","朱德","宋庆龄","张澜","林伯渠"],174:["毛泽东"],175:["毛泽东","刘少奇","周恩来","朱德","陈云","邓小平"],176:["毛泽东","陈伯达","江青","康生","张春桥","林彪","周恩来","邓小平"],177:["邓小平"]}.items():
    for i,name in enumerate(names,1): data["people"].append({"id":f"{pid(p)}_person{i:03d}","name_as_written":name,"aliases":[],"evidence_block_ids":[bid(p,1)],"notes":[]})

K = [
 (169,"抗美援朝战争","process","war","1950年6月25日至1953年7月","duration",1950,1953,"year","known","抗美援朝战争中志愿军入朝作战并经过五次战役，1953年7月取得胜利。",["war","foreign_relations"],2,1),
 (169,"中国人民志愿军入朝作战并跨过鸭绿江","event","war","1950年10月","point",1950,None,"month","not_applicable","应朝鲜党和政府请求，中国人民志愿军入朝作战。",["war","foreign_relations"],2,1),
 (169,"杨根思在抗美援朝第二次战役中牺牲","event","war","抗美援朝第二次战役","unknown",None,None,"period","not_applicable","杨根思在长津湖地区坚守1071.1高地，牺牲后获特级战斗英雄称号。",["war"],4,2),
 (170,"新中国开创独立自主的和平外交","origin","foreign_relations","新中国成立后","period",1949,None,"period","unknown","新中国按照一边倒、另起炉灶、打扫干净屋子再请客等方针开展外交。",["foreign_relations","politics"],3,3),
 (170,"日内瓦会议中新中国参与国际争端谈判","event","foreign_relations","1954年4月","point",1954,None,"month","not_applicable","新中国首次以五大国之一身份参加日内瓦会议，印度支那问题得以政治解决。",["foreign_relations","politics"],6,4),
 (171,"和平共处五项原则提出并成为国际关系准则","origin","foreign_relations","1953年12月至1954年6月","duration",1953,1954,"period","known","周恩来提出和平共处五项原则，中印、中缅正式倡议其作为国际关系准则。",["foreign_relations","politics"],2,5),
 (171,"万隆亚非会议提出并坚持求同存异","event","foreign_relations","1955年4月","point",1955,None,"month","not_applicable","中国在万隆亚非会议上提出并坚持求同存异方针。",["foreign_relations"],6,6),
 (171,"过渡时期总路线与第一个五年计划启动社会主义改造","origin","economy","1953年","point",1953,None,"year","not_applicable","提出过渡时期总路线，实施第一个五年计划并开展社会主义改造。",["politics","economy","agriculture"],6,7),
 (172,"社会主义改造基本完成并初步建立社会主义经济制度","event","economy","1956年","point",1956,None,"year","not_applicable","基本完成三大改造，生产资料公有制占绝对优势的社会主义经济制度初步建立。",["economy","agriculture","politics"],2,8),
 (172,"第一届全国人民代表大会通过1954年宪法并确立人民代表大会制度","event","institution","1954年9月","point",1954,None,"month","not_applicable","第一届全国人大通过宪法，确立人民代表大会制度为根本政治制度。",["politics"],3,9),
 (172,"社会主义基本制度建立的历史意义","event","institution","1956年","point",1956,None,"year","not_applicable","确立社会主义基本制度，为当代中国发展进步奠定根本政治前提和制度基础。",["politics","economy","society"],2,10),
 (174,"中共八大探索中国自己的社会主义建设道路","event","institution","1956年","point",1956,None,"year","not_applicable","中共八大分析主要矛盾和主要任务，标志探索社会主义建设道路取得初步成果。",["politics","economy","society"],4,11),
 (174,"百花齐放、百家争鸣方针提出","origin","culture","1956年4月28日","point",1956,None,"day","not_applicable","提出百花齐放、百家争鸣方针，促进艺术发展、科学进步和文化繁荣。",["culture","science"],7,12),
 (175,"正确处理人民内部矛盾的重要思想提出","origin","thought","1957年春","point",1957,None,"period","not_applicable","毛泽东提出正确处理人民内部矛盾的重要思想。",["politics","society"],3,13),
 (175,"大跃进和人民公社化运动引发经济困难","process","economy","1958年至1961年","duration",1958,1961,"year","known","大跃进和人民公社化运动后，1959至1961年我国经济发生严重困难。",["economy","agriculture","society"],5,14),
 (175,"国民经济调整、八字方针与七千人大会","process","economy","1961年1月至1965年","duration",1961,1965,"year","known","八字方针调整国民经济，七千人大会总结经验，经济在1962年下半年至1965年稳步增长。",["economy","politics"],5,14),
 (176,"建设四个现代化目标提出","event","politics","1964年","point",1964,None,"year","not_applicable","三届全国人大一次会议提出建设四个现代化的伟大目标。",["politics","science","economy"],2,15),
 (176,"文化大革命发动并造成社会生产秩序混乱","process","politics","1966年夏至1976年10月","duration",1966,1976,"year","known","文化大革命全面发动并造成社会生产秩序混乱，1976年10月结束。",["politics","society","culture"],4,16),
 (176,"1971年林彪反革命集团策动武装政变未遂","event","politics","1971年9月","point",1971,None,"month","not_applicable","林彪反革命集团策动武装政变，毛泽东、周恩来粉碎了这次政变。",["politics"],5,16),
 (177,"粉碎江青反革命集团并结束文化大革命","event","politics","1976年10月","point",1976,None,"month","not_applicable","中央政治局粉碎江青反革命集团，结束文化大革命。",["politics","society"],2,17),
 (177,"改革开放前社会主义建设取得重要成就","process","economy","从新中国成立到改革开放前","duration",1949,None,"period","unknown","改革开放前在工业、农业、科技、国防、外交、文化教育等方面取得重要成果。",["economy","science","war","culture","foreign_relations"],4,18),
 (177,"一五至四五时期建立基础工业与国防科技成就","process","science","从一五时期起到四五时期","period",None,None,"period","unknown","逐步建立独立、比较完整的工业体系和国民经济体系，取得两弹一星等成就。",["economy","science","war"],5,18),
]
local_n = {}
for p,title,kind,ctype,source,mode,start,end,prec,endstatus,summary,themes,blockn,invn in K:
    local_n[p] = local_n.get(p, 0) + 1
    n = local_n[p]
    evid=[bid(p,blockn)]
    data["knowledge"].append({"id":kid(p,n if p==169 else n),"title":title,"kind":kind,"content_type":ctype,
      "time":tm(source,mode,start,end,prec,endstatus,evid),"themes":themes,"place_refs":[],"person_ids":[],
      "summary":claim(summary,evid),"flow":[],"points":[],"background":None,"impact":None,
      "evidence_block_ids":evid,"asset_ids":[],"source_inventory_ids":[iid(p,1)],"uncertainties":["知识候选尚未进行语义/史实审核。"],"review_status":"pending_review"})

# Inventory and coverage candidate records.
labels = [(169,"抗美援朝战争、跨过鸭绿江与杨根思事迹",[2,3,4,5]),(170,"独立自主和平外交与日内瓦会议",[2,3,4,5,6]),(171,"和平共处五项原则、万隆会议与过渡时期总路线",[2,3,4,5]),(172,"社会主义改造、第一届全国人大与1954年宪法",[2,3,4,5,6]),(173,"宪法探究与中华人民共和国成立意义学习任务",[2,3,4,5]),(174,"中共八大与百花齐放百家争鸣",[2,3,4,5,6,7]),(175,"人民内部矛盾、大跃进、经济调整与七千人大会",[2,3,4,5,6]),(176,"四个现代化与文化大革命",[2,3,4,5,6,7]),(177,"文化大革命评价与社会主义建设成就",[2,3,4,5,6,7])]
for j,(p,label,ns) in enumerate(labels,1):
    kidset=list(range(1, sum(1 for k in K if k[0] == p) + 1))
    ids=[kid(p,n) for n in kidset]
    blocks=[bid(p,n) for n in ns]
    data["inventory"].append({"id":iid(p,1),"document_id":DOC,"page_ids":[pid(p)],"block_ids":blocks,"item_label":label,"scope":"chinese_history","disposition":"included" if ids else "pending_review","knowledge_ids":ids,"duplicate_of_inventory_id":None,"reason":"逐页登记正文、标题、边栏、练习及图注候选；重复或跨页关系留待人工核对。"})

issues = [(169,"time","抗美援朝战争、杨根思事迹的战役范围和日期需要人工核对。"),(170,"time","三项外交方针及日内瓦会议的阶段边界需要人工核对。"),(171,"source","和平共处五项原则文本及过渡时期总路线跨页证据需要人工核对。"),(172,"image","三张会议和改造照片未导出裁剪图片，图注需人工复核。"),(173,"source","宪法探究摘录含省略号，不应外推完整宪法。"),(174,"time","中共八大和百花方针提出场合需核对会议节点。"),(175,"time","大跃进、经济困难与八字方针的过程边界需核对。"),(176,"person","文化大革命相关人物、集团与事件关系需人工核对。"),(177,"time","改革开放前、一五至四五的时期边界需核对；页面图片未导出。")]
for p,cat,desc in issues:
    data["review_issues"].append({"id":issueid(p,1),"record_ids":[pid(p)],"category":cat,"description":desc,"evidence_block_ids":[bid(p,1)],"suggested_action":"对照原页图像及前后页人工复核，保留原话和不确定性。","blocking":False,"status":"open"})

data["relations"] = [
 {"id":rid(169,1),"from_knowledge_id":kid(169,2),"to_knowledge_id":kid(169,1),"target_label":None,"type":"participation","person_ids":[],"place_ids":[],"time_text":"1950年10月","description":"志愿军入朝作战属于抗美援朝战争进程。","evidence_block_ids":[bid(169,2)],"review_status":"pending_review"},
 {"id":rid(171,1),"from_knowledge_id":kid(171,1),"to_knowledge_id":kid(171,2),"target_label":None,"type":"influence","person_ids":[],"place_ids":[],"time_text":"1954—1955年","description":"和平共处五项原则和求同存异均属于独立自主和平外交实践，教材内容存在主题衔接。","evidence_block_ids":[bid(171,2),bid(171,3)],"review_status":"pending_review"},
 {"id":rid(176,1),"from_knowledge_id":kid(176,2),"to_knowledge_id":kid(177,1),"target_label":None,"type":"other","person_ids":[],"place_ids":[],"time_text":"1976年10月","description":"第176页页末‘结束了’在第177页接续为文化大革命历史评价。","evidence_block_ids":[bid(176,6),bid(177,2)],"review_status":"pending_review"},
]
data["batch"]["carryover"] = [
 {"type":"paragraph","record_ids":[bid(169,2)],"description":"第169页承接前批朝鲜战争相关正文。","next_action":"与第168页末块核对连续性。"},
 {"type":"paragraph","record_ids":[bid(171,6),bid(172,2)],"description":"第171页末社会主义改造正文在第172页续接。","next_action":"联合核对过渡时期和1956年改造完成的时间边界。"},
 {"type":"paragraph","record_ids":[bid(176,6),bid(177,2)],"description":"第176页末文化大革命结束语在第177页接续。","next_action":"联合核对1976年10月事件及历史评价。"}]

OUT.mkdir(parents=True, exist_ok=True)
(OUT/"b05c.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
review = f'''# b05c 审阅摘要（PDF 页序 169–177）

## 页面读取覆盖

- 请求页 169–177，共 9 页；9 页均完成文字层读取和逐页渲染图检查，partial/unprocessed 均为 0。
- 页面图像包含 8 个照片资产；均未导出裁剪文件，`assets.file_path` 全部为 `null`。
- 页169–173 属第25课，页174–177 属第26课；印刷页码为162–170，与PDF页序分开记录。

## 结构化产物统计

- `pages`: {len(data['pages'])}
- `blocks`: {len(data['blocks'])}（每页保留PDF文字层全量证据块，另按标题、段落、图注、边栏和练习拆分）
- `assets`: {len(data['assets'])}
- `places`: {len(data['places'])}
- `people`: {len(data['people'])}
- `knowledge`: {len(data['knowledge'])}
- `relations`: {len(data['relations'])}
- `inventory`: {len(data['inventory'])}
- `review_issues`: {len(data['review_issues'])}，全部 `open`

## 检查与内容审阅状态

- `scripts/validate_pdf_cleaning.py` 与 `scripts/audit_pdf_text_coverage.py` 将在产物生成后实际运行；覆盖审计仅是文字证据与PDF文字层字符覆盖信号，不等同于历史内容正确。
- 语义/史实审阅：`not_performed`；知识和关系全部为 `pending_review`。
- 重点人工核验：抗美援朝战役与人物日期、外交方针与和平共处五项原则文本、社会主义改造和1954年宪法跨页证据、中共八大与经济调整会议节点、文化大革命人物与阶段、“改革开放前”和“一五”至“四五”的公历边界。
'''
(OUT/"b05c.review.md").write_text(review,encoding="utf-8")
print(f"wrote {OUT/'b05c.json'} pages={len(data['pages'])} blocks={len(data['blocks'])} knowledge={len(data['knowledge'])}")
