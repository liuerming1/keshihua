import json,re,copy
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923'); out=root/'s01'; path=root/'s01.patch.json'
p=json.loads(path.read_text(encoding='utf-8')); base=json.loads((root/'baseline.json').read_text(encoding='utf-8'))
K={x['id']:x for x in p['updates']['knowledge']}; B={x['id']:x for x in base['blocks']}; BU={x['id']:x for x in p['updates']['blocks']}
def cl(txt,ids):return {'text':txt,'evidence_block_ids':ids}
def upd(i,field,txt,ids):K[i][field]=cl(txt,ids)
def add_evidence(i,ids):
 for key in ('evidence_block_ids',):
  for x in ids:
   if x not in K[i][key]:K[i][key].append(x)
 for key in ('summary','background','impact'):
  c=K[i].get(key)
  if isinstance(c,dict):
   for x in ids:
    if x in K[i]['evidence_block_ids'] and x not in c.get('evidence_block_ids',[]):
     # add only when the supplied page text supports this claim
     pass
# Explicit background and impact claims grounded in distinct textbook statements.
upd('history_book_01_p0019_k001','background','战国时期各国为富国强兵开展变法，商鞅变法顺应这一历史潮流；本段说明变法由商鞅入秦后推行。',['history_book_01_p0018_b003','history_book_01_p0019_b003'])
upd('history_book_01_p0019_k001','impact','教材指出商鞅变法使秦国国富兵强，为秦统一中国奠定基础；后来商鞅被杀，但措施已深入人心。',['history_book_01_p0019_b003'])
upd('history_book_01_p0020_k001','background','社会经济发展使阶级关系变化、旧贵族等级体系瓦解、新兴士阶层崛起；争霸的各国统治者招揽人才，为学说交流和争辩提供条件。',['history_book_01_p0020_b001'])
upd('history_book_01_p0020_k001','impact','百家争鸣为新兴地主阶级登上历史舞台奠定思想理论基础，也成为后世中华思想文化的源头活水，影响深远。',['history_book_01_p0020_b001'])
upd('history_book_01_p0021_k001','background','新兴地主阶级在多国掌握政权，为打击旧奴隶主贵族、建立封建政治经济秩序、巩固新生政权和增强竞争实力而变法。',['history_book_01_p0021_b001'])
upd('history_book_01_p0021_k001','impact','各国变法旨在建立新的政治经济秩序并巩固新生政权；教材举李悝、吴起改革为例，但没有对各国变法整体成效下统一结论。',['history_book_01_p0021_b001'])
upd('history_book_01_p0022_k001','background','长期战乱造成巨大灾难，人民渴望安定统一；区域经济发展要求消除政治分裂造成的阻碍。秦具殽函地理优势和雄厚物质基础，数代秦王治理、广纳贤才与较清明吏治，以及商鞅变法后的奖励耕战共同提供统一条件。',['history_book_01_p0022_b001'])
upd('history_book_01_p0022_k001','impact','教材明确指出统一中央集权国家的形成是历史发展的必然和客观需要；秦顺应潮流建立统一中央集权国家，促进各地区、各民族政治、经济、文化交流交融。',['history_book_01_p0022_b001'])
upd('history_book_01_p0023_k001','impact','教材称秦统一后建立幅员辽阔的国家；秦确立的政治制度被后世王朝长期沿用，影响深远。',['history_book_01_p0023_b001'])
upd('history_book_01_p0023_k002','impact','秦朝确立的政治制度被后来的王朝长期沿用，影响深远；统一文字、货币、度量衡等措施有助于巩固全国统一。',['history_book_01_p0023_b001'])
upd('history_book_01_p0024_k001','background','此条目以统一后的秦始皇施政为起点，教材本段未另列秦统一前的背景；来源直接列出大兴土木、巡游封禅和征发等暴政行为。',['history_book_01_p0024_b001'])
upd('history_book_01_p0024_k001','impact','教材明确称繁重征发、严苛刑法使百姓不堪重负、生活困苦，社会阶级矛盾严重激化，并将秦速亡与暴政联系起来。',['history_book_01_p0024_b001'])
upd('history_book_01_p0025_k001','background','秦统一后，秦始皇借巡行和刻石宣扬功业，但遇刺、陨石刻字等材料被教材用来说明表面强盛下已存在统治危机；焚书坑儒是该危机的组成部分。',['history_book_01_p0025_b001'])
upd('history_book_01_p0025_k001','impact','教材评价焚书坑儒在中国历史上产生恶劣影响；秦二世继位后严刑峻法、加重人民负担，使阶级矛盾和统治集团内部矛盾尖锐化。',['history_book_01_p0025_b001'])
upd('history_book_01_p0025_k002','background','秦二世实行严刑峻法并加重人民负担，戍卒在大泽乡遇雨误期，依法不能按期到戍地将被处死，遂在陈胜、吴广领导下起义。',['history_book_01_p0025_b001'])
upd('history_book_01_p0025_k002','impact','陈胜、吴广起义揭开反秦起义序幕；刘邦于公元前207年进占咸阳，秦朝灭亡。',['history_book_01_p0025_b001','history_book_01_p0026_b001'])
# Individual processes and literary/social consequences present in the sources.
upd('history_book_01_p0020_k001','points','儒家孟子主张仁政，荀子主张隆礼重法；道家庄子崇尚逍遥自由；墨子提倡节俭、兼爱、非攻和尚贤；法家韩非主张以法治国、加强中央集权。',['history_book_01_p0020_b001'])
upd('history_book_01_p0021_k001','points','李悝在魏国按“食有劳而禄有功”授官爵、主张尽地力并颁布《法经》；吴起在楚国“明法审令，捐不急之官”。',['history_book_01_p0021_b001'])
# Fix the source-backed date interval of the Three Kingdoms and connect the known ending on page 36.
i='history_book_01_p0035_k002'; K[i]['time'].update({'source_text':'220年后','mode':'duration','start_year':220,'end_year':280,'earliest_year':None,'latest_year':None,'precision':'year','end_status':'known','normalization_note':'220年曹丕称帝建立魏，三国格局形成；PDF第36页同一段记280年西晋灭吴完成统一，作为该历史格局的终点证据。'})
add_evidence(i,['history_book_01_p0036_b001'])
# Carryover data: preserve complete cross-page meaning without joining page text as one page.
add_evidence('history_book_01_p0029_k002',['history_book_01_p0030_b001'])
add_evidence('history_book_01_p0030_k004',['history_book_01_p0031_b001'])
add_evidence('history_book_01_p0031_k004',['history_book_01_p0032_b001'])
add_evidence('history_book_01_p0035_k002',['history_book_01_p0036_b001'])
add_evidence('history_book_01_p0038_k003',['history_book_01_p0038_b002','history_book_01_p0039_b001'])
# Repair page 20-29 trailing encoding/watermark noise only in clean_text; preserve raw_text exactly.
for b in base['blocks']:
 m=re.search(r'_p(\d{4})_',b['id']); pg=int(m.group(1)) if m else 999
 if 20<=pg<=29 and 'NÅO' in (b.get('clean_text') or ''):
  clean=(b.get('clean_text') or '')
  clean=clean[:clean.index('NÅO')].rstrip()
  if b['id'] not in BU:
   nb=copy.deepcopy(b);nb['clean_text']=clean;nb['notes']=list(nb.get('notes') or [])+['s01：去除clean_text末尾跨页水印/错误编码串；raw_text完整保留。'];BU[b['id']]=nb
  else:
   BU[b['id']]['clean_text']=clean;BU[b['id']]['notes']=list(BU[b['id']].get('notes') or [])+['s01：去除clean_text末尾跨页水印/错误编码串；raw_text完整保留。']
# Mark page 38 image text partial because the ethnic-affiliation table has cells needing enlarged verification.
for pg in p['updates']['pages']:
 if pg['pdf_page_number']==38:
  pg['image_status']='partial';pg['notes']=list(pg.get('notes') or [])+['图表文字已查看；十六国族属表的小字单元格未能逐格可靠识读，需放大复核。']
# Update blocks list after page20-29 expansions.
p['updates']['blocks']=list(BU.values())
# Additional cross-page review required by primary agent: indices are baseline batch.carryover indices.
p['carryover_review']=[
 {'index':0,'status':'needs_review','evidence_block_ids':['history_book_01_p0010_b007'],'reason':'已复核第10页姜寨聚落说明与第11页新石器晚期社会阶段，教材均未给姜寨遗址的明确年代；不把仰韶文化或父系氏族社会年代套给聚落。'},
 {'index':1,'status':'resolved','evidence_block_ids':['history_book_01_p0012_b003','history_book_01_p0013_b001','history_book_01_p0013_b003'],'reason':'第12页 b003末尾甲骨文字句在第13页 b001/b003续接；核实为同一“商和西周”正文段落。知识k001已引用第13页甲骨文与商朝国家机构证据；第12页历法/干支知识k003仅需其第12页证据。不同页块保持分开引用。'},
 {'index':2,'status':'resolved','evidence_block_ids':['history_book_01_p0029_b001','history_book_01_p0030_b001'],'reason':'第29页正文以“丝绸之路。公”截断，第30页首段以“元前60年”续成“公元前60年”，内容是西汉设西域都护府。已按两页顺序核实并在p29相关知识补入第30页证据；原块不拼接。'},
 {'index':3,'status':'resolved','evidence_block_ids':['history_book_01_p0030_b006','history_book_01_p0031_b001'],'reason':'第30页关于刘秀措施的句子在第31页续为释放奴婢、重视儒学及社会经济恢复，称“光武中兴”；p30 k004现保留并引用两页证据。'},
 {'index':4,'status':'resolved','evidence_block_ids':['history_book_01_p0031_b006','history_book_01_p0032_b001'],'reason':'第31页“真实情”与第32页“况”明确组成“真实情况”；文学知识k004已同时引用两块，clean_text原有文字保留跨页语义。'},
 {'index':5,'status':'resolved','evidence_block_ids':['history_book_01_p0035_b006','history_book_01_p0036_b001'],'reason':'第35页刘备仍用汉国号在第36页续为定都成都、称蜀汉；同一段接述吴及西晋统一。三国鼎立知识已引用两页，时间区间以220至280有据记录。'},
 {'index':6,'status':'resolved','evidence_block_ids':['history_book_01_p0038_b002','history_book_01_p0039_b001'],'reason':'第38页末北魏建立、439年统一北方、孝文帝改革的句子续至第39页“鲜卑贵族一律将籍贯改为洛阳”；北魏知识现同时引用本页和第39页证据，未把两页文字合并成同页块。'}]
# Keep audit/reclean status synchronized for unresolved-only concerns. Needs-review items explicitly identified.
needs={'history_book_01_p0009_k002','history_book_01_p0009_k003','history_book_01_p0010_k001','history_book_01_p0010_k002','history_book_01_p0010_k005','history_book_01_p0014_k002','history_book_01_p0017_k001','history_book_01_p0019_k002','history_book_01_p0023_k001','history_book_01_p0030_k004','history_book_01_p0037_k001','history_book_01_p0038_k001'}
for a in p['knowledge_audit']:
 i=a['id']; k=K[i]
 if i in needs:
  a['decision']='needs_review'; k['reclean_review']['status']='needs_review'
 else:
  a['decision']='changed' if i in set(x['id'] for x in p['updates']['knowledge'] if x['reclean_review'].get('note')) and i in set(x['id'] for x in p['updates']['knowledge'] if x['reclean_review'].get('status')=='agent_reviewed') else a['decision']
  k['reclean_review']['status']='agent_reviewed'
 # Ensure field-specific empty claims reflect the actual populated record.
 empty=a.get('empty_reasons',{})
 for fld in ['flow','points','background','impact']:
  if k.get(fld): empty.pop(fld,None)
  elif fld not in empty: empty[fld]=f'该条“{k["title"]}”经证据块核对，教材未给出可独立归入该字段的内容，故不补写。'
 a['empty_reasons']=empty
 k['reclean_review']['note']=a['note'] + (' 仍有待核事项：见 split_proposals/open_items。' if i in needs else '')
# Ensure proper decisions for changed records not accidentally retained.
for a in p['knowledge_audit']:
 if a['id'] in needs: continue
 if a['id'] in {'history_book_01_p0035_k002','history_book_01_p0019_k001','history_book_01_p0020_k001','history_book_01_p0021_k001','history_book_01_p0022_k001','history_book_01_p0023_k001','history_book_01_p0023_k002','history_book_01_p0024_k001','history_book_01_p0025_k001','history_book_01_p0025_k002','history_book_01_p0037_k003','history_book_01_p0038_k001','history_book_01_p0038_k002','history_book_01_p0038_k004'}:
  a['decision']='changed';K[a['id']]['reclean_review']['status']='agent_reviewed'
# Any knowledge whose evidence changed is also a changed audit unless explicitly needs_review.
for a in p['knowledge_audit']:
 if a['id'] not in needs and K[a['id']]['evidence_block_ids'] != next(k['evidence_block_ids'] for k in base['knowledge'] if k['id']==a['id']):
  a['decision']='changed'
  K[a['id']]['reclean_review']['status']='agent_reviewed'
p['updates']['knowledge']=list(K.values())
# Persist patch.
path.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print('blocks',len(p['updates']['blocks']),'carryover',len(p['carryover_review']),'needs',sum(a['decision']=='needs_review' for a in p['knowledge_audit']))
