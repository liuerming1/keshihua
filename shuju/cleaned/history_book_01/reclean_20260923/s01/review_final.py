import json
from pathlib import Path
root=Path('shuju/cleaned/history_book_01/reclean_20260923'); f=root/'s01.patch.json';p=json.loads(f.read_text(encoding='utf8'))
base=json.loads((root/'baseline.json').read_text(encoding='utf8')); old={k['id']:k for k in base['knowledge']}; now={k['id']:k for k in p['updates']['knowledge']}
needs={a['id'] for a in p['knowledge_audit'] if a['decision']=='needs_review'}
counts={'changed':0,'retained':0,'needs_review':0}
for a in p['knowledge_audit']:
 i=a['id']; a0=dict(old[i]); a1=dict(now[i]); a0.pop('verification',None);a0.pop('finalization',None);a1.pop('verification',None);a1.pop('finalization',None);a1.pop('reclean_review',None)
 # Baseline did not contain the reclean_review review metadata; all content/claim fields compare directly.
 actual_changed=a0!=a1
 if i in needs:a['decision']='needs_review';now[i]['reclean_review']['status']='needs_review'
 elif actual_changed:a['decision']='changed';now[i]['reclean_review']['status']='agent_reviewed'
 else:a['decision']='retained';now[i]['reclean_review']['status']='agent_reviewed'
 counts[a['decision']]+=1
 a['evidence_block_ids']=now[i]['evidence_block_ids']
 now[i]['reclean_review']['note']=a['note']+(' 仍有待核事项见open_items。' if a['decision']=='needs_review' else '')
p['updates']['knowledge']=list(now.values());f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# s01 审阅记录：PDF 页序 1–38','','- 输入：`baseline.json`（只读）；PDF：`普通高中教科书·历史必修_中外历史纲要（上）.pdf`。','- baseline SHA-256：`'+p['baseline_sha256']+'`。','- 本段归属知识：80 条；changed '+str(counts['changed'])+'、retained '+str(counts['retained'])+'、needs_review '+str(counts['needs_review'])+'。','- 源块清洗：26 个完整 block 更新，其中目录页4–6恢复全目录课目和印刷页码；第30页补回视觉可核的“公”；第20–29页各清除clean_text尾部乱码；第37页按PDF逐字补录缺失的页末疆域正文，第38页复核地图及族属表格。既有源块raw_text未改；新增p0037_b009的raw_text为PDF文字层原行序文本。','- 视觉检查：PDF页序1–38逐页渲染并查看8张联系图；正文版面、目录、插图与地图均核对。第38页族属表以240dpi单页渲染并单独放大，逐格核对“羌—后秦、賨（cóng）—成汉”等对应，page.image_status为complete；图像证据保存在s01/page_37_border_paragraph.png和s01/page_38_table_crop.png。地图像素不作历史疆域几何。','- 拼音OCR逐页视觉复核（raw_text均未修改）：页序12 luG→luǒ、bSng→bàng；14 cuU→cuī、hO→hū；16 guY→guó；17 shFng→shèng、tQo→tāo；18 QuFbEi→Quèbēi、gL→gǔ；22 chAn→chǎn；27 kL→kǔ、tK→tì。声调逐字依据480dpi PDF裁剪图核读，逐项核对证据在s01/p12_luG_bSng.png、p14_cuU.png、p14_hO.png、p16_guY.png、p17_shFng_tQo.png、p18_QuFbEi.png、p18_gL.png、p22_chAn.png、p27_kL_tK.png；原页300dpi渲染亦保留。',
'- 跨页续接：carryover_review 0–6逐项回读相邻页；6项已解决、1项（姜寨无明确年代）保留needs_review。知识证据使用分开的页块ID，没有合并不同页原文。','- 时间修复：距今考古时间及约公元前2070/1600均只保留source_text，start/end/earliest/latest全部留空；复合历程按明确起止证据记duration并在flow逐项保留节点：前841—前770、春秋后期/战国前期至前256（起始公元年未给）、秦前230—前214、25年起东汉初年（终点未知）、317年起东晋至南朝（终点未知）；孔子条目保留“春秋后期”不确定时间，不以生卒年冒充思想起止；第35页三国时间与第36页280年终点核对；第37页删除推算的“约589年”。','- 重点字段补全：商鞅变法补背景（战国变法潮流）和影响（秦国国富兵强、为统一奠基）；秦统一条件拆列长期战乱、区域经济、秦地理物质基础与治理，并录入教材所述统一影响；百家争鸣、战国变法、秦暴政与秦末起义按教材分开补背景/影响。','- 本补丁不修改共享数据、程序、baseline或原PDF；不把来源未给出的地点坐标、终年或疆域几何补入。','', '## 仍需核对或裁决的事项','', '- 考古学“距今”时间没有教材给出的公历换算基准；4条知识已保留原话和uncertain，不给虚假公元前年份。若时间轴必须公历化，需先统一约定年代参照。','- 六条曾列为拆分候选的复合记录已逐项裁定并留在原知识ID内，按教材原话给出的时间性质、可定位区间和事件flow表达；patch不再保留这六条split_proposals。起始年或结束年未给出的记录保持null/unknown，不以推算填值。','- 第38页十六国族属表已放大逐格核对：羌对应后秦、賨（cóng）对应成汉；clean_text及table_data已修正。','- 姜寨聚落证据没有明确年代，不从仰韶文化时期或氏族社会阶段推断具体年份；考古‘距今’换算和姜寨定年是现存open_items。','', '## 全量知识审计','', '以下逐条列出 `knowledge_audit` 全字段。`empty_reasons`仅针对仍为空的详情字段；needs_review与对应reclean_review.status保持一致。','', '```json',json.dumps(p['knowledge_audit'],ensure_ascii=False,indent=2),'```','']
(root/'s01.review.md').write_text('\n'.join(lines),encoding='utf8')
print(json.dumps({'counts':counts,'audit_rows':len(p['knowledge_audit'])},ensure_ascii=False))

