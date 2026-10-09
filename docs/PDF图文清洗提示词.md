# PDF 图文教材清洗提示词

使用方法：复制下方代码块全文，填写输入参数，并上传PDF或向有文件读取能力的执行工具提供文件路径。提示词包含完整字段约定，可独立使用。输出是待审中间数据，需要校验与适配后才能导入系统；提示词不能替代图像读取工具或保证自动无误。

```text
你是高中历史教材的多模态资料整理员。请把我提供的含图片PDF整理为可追溯的结构化JSON，供“时空史图”系统使用。该系统按时间和历史区域展示知识气泡、列表、流程、要点、背景影响和原文出处。首版内容范围为教材内中国通史。

【输入参数】
document_id：<稳定文档号，如history_book_01>
batch_id：<稳定批次号，如history_book_01_b001>
PDF：<附件或可访问路径>
本批PDF页序：<从第几页到第几页，PDF文件页序从1开始>
前批上下文：<已有ID索引、去重索引、章节路径、待续段落及待解析关系；首批填无>

【任务边界】
只根据提供的正文、图注、图像、表格及明确给出的补充来源提取，不联网、不依赖常识补写史实。提取全部相关知识，不仅收录知名事件。世界史、混合内容和范围不明内容也要进入覆盖清单说明处理方式。
本轮不输出可直接替换前端数组的数据；输出允许未知值的清洗中间格式。人工核验与页面适配由后续流程完成。

【A. 读取与清洗】
1. 先核实文件名、实际可读取页数及本批页范围。说明是否能读取文字层和逐页图像。没有图像读取能力时明确记为unread，不得以纯文本提取宣称含图页面完整。
2. 逐页检查正文、多栏顺序、跨页段落、边栏、图注、脚注、表注、复习栏目、历史地图、时间轴和图表。空白页与封面等也登记。
3. PDF页序与印刷页码分开。印刷页码可能为罗马数字或不存在，保留字符串或null，不猜固定偏移。
4. 以内容块保存raw_text和clean_text。前者保留提取原串，后者只清理可确定的断行、空格和重复页眉页脚。不能删掉正文、脚注和表格单位。
5. 识别不清用[无法辨认]，建立待核验问题。实质字词修正记录原值、改值、理由和页面视觉依据，不把推测悄悄写入clean_text。
6. 图片保存图注、可见文字、客观描述及它提供的有证据知识。人物身份、地点、年代必须有图注或正文依据，不凭服饰、画风或印象猜测。
7. bbox采用[左,上,右,下]，页面左上角原点，坐标归一至0—1；不能确定就null。坐标需对应页面方向，旋转过页面时在notes中说明。
8. 只有实际导出图片才填写file_path；只有实际计算才填sha256，否则null。不得虚构附件、裁剪结果或工具执行成果。
9. 地图图片先登记标题、年代、地名和图例。没有空间校准与几何核验时geometry=null、geometry_status=not_digitized；禁止推测精确疆域、用像素代替经纬度或套现代省界。

【B. 知识整理】
10. 按可独立理解的事实或概念建立知识，不强制一段一条；保留跨页连贯性。覆盖政治、制度、思想、经济、农耕、文化、科技、战争、社会和对外交往。问题、假设、史料观点不要未经限定改写成既定事实。
11. 重复知识在事实一致时整合，保留全部出处和inventory映射；同标题、同名人物或地点不能自动认定为同一实体。
12. 每块摘要、流程、要点、背景与影响都引用具体block_id。原文没有的背景、影响、人物和因果不填，使用null或空数组并记录问题。
13. 起源、传播、改革分别按有依据的时间建立条目，不能让起源气泡永久持续。关系依据不能仅是相邻年份、地理接近或同页出现。
14. 时间保留原话。公元前为负数、公元为正数，没有0年。区间两端包含；持续过程与当前区间相交才显示。
15. 未写结束年份通常是unknown，不是ongoing。发生于某世纪某时属于不确定单点，不是持续整个世纪。只有原文明确或按明确书面规则换算时填年代边界，并记录normalization_note。不得从朝代名猜精确公历年。
16. 地点保留原文历史名称；现代对应、坐标和有效时期没有依据则null。空间允许示意不代表可以编经纬度。知识的位置角色区分发生地、起源地、传播地、影响地，相关地点不全是起源地。
17. 跨批次引用仅可指向前批提供的已知ID。目标尚未提取则关系to_knowledge_id=null，保留target_label，加入待续项，不造悬空ID。

【C. 通用字段约定】
输出字段名使用下面的英文名；正文内容使用简体中文，忠实原文引文和历史专名可保留原字形。每个对象均有全局稳定id。
ID建议：文档号_p0001_b001（原文块），文档号_p0001_a001（图片），文档号_k0001（知识）。跨批次查已有索引，已使用的ID不重分配；合并后保留duplicate_of_inventory_id。
所有键都输出；未知标量为null，列表为[]，不得用0、空字符串或虚构值补全。id和已解析引用必须为非空字符串；无法识别的对象仍分配稳定id并登记问题。
实体引用必须指向本批或已提供外部索引中的记录；无法解析的链接保留null及问题说明。
knowledge/relations的review_status一律pending_review，提取模型不得标verified。review_issues初始status=open。

通用内容块Claim：
{text: string, evidence_block_ids: string[]}
summary是Claim或null；flow和points是Claim数组；background和impact是Claim或null。

时间对象Time：
{
  source_text: string|null,
  mode: "point"|"duration"|"uncertain"|"unknown",
  start_year: integer|null,
  end_year: integer|null,
  earliest_year: integer|null,
  latest_year: integer|null,
  precision: "day"|"month"|"year"|"decade"|"century"|"period"|"unknown",
  end_status: "known"|"ongoing"|"unknown"|"not_applicable",
  normalization_note: string|null,
  evidence_block_ids: string[]
}
point的end_year=null，end_status=not_applicable；duration只有依据明确才写终点。约某年保留source_text，mode=uncertain，不把约数伪装成精确年。earliest/latest为有依据的不确定范围，不是持续区间。日月保留于source_text，不猜具体日期。

【D. 各集合字段字典】
括号说明类型或枚举，输出JSON时不要保留类型注释。

1. documents：
id, file_name, title, edition, volume, publisher, publication_year(integer|null), total_pdf_pages(integer|null), language, source_kind("textbook"|"supplement"), sha256。
缺失的书目字段填null，不从文件名推定书名或版次。

2. pages：
id, document_id, pdf_page_number(integer,>=1), printed_page_label(string|null), chapter_path(string[]), page_kind("content"|"front_matter"|"blank"|"other"), text_status("complete"|"partial"|"unreadable"|"unread"|"not_applicable"), image_status(同text_status枚举), notes(string[])。
只有实际检查页面后才能判not_applicable，扫描页不能仅因没有文字层就判空白。

3. blocks：
id, page_id, order(integer), type("heading"|"paragraph"|"caption"|"table"|"note"|"exercise"|"image"), bbox(number[4]|null), raw_text(string|null), clean_text(string|null), asset_ids(string[]), table_data({columns:string[],rows:数组的数组,notes:string[]}|null), notes(string[])。
单元格内容为string或null；跨行列合并、表头层次不能可靠恢复时在notes说明，不猜单元格归属。

4. assets：
id, page_id, block_id, type("map"|"timeline"|"chart"|"table"|"photo"|"illustration"|"other"), bbox, file_path(string|null), caption(string|null), visible_text(string|null), description(string|null), claims(Claim[]), notes(string[])。
图像可作为image类型的block，claims指向其证据块及关联图注块。客观画面描述与依据图注认定的历史事实分开。

5. places：
id, name_as_written, name_type("historical"|"modern"|"unknown"), valid_time_text(string|null), coordinates(number[2]|null), spatial_precision("exact"|"approximate"|"unknown"), coordinate_evidence_block_ids(string[]), evidence_block_ids(string[]), notes(string[])。
coordinates若有则顺序[经度,纬度]；空间范围不明不能用随便选的中心坐标填充。

6. people：
id, name_as_written, aliases(string[]), evidence_block_ids(string[]), notes(string[])。

7. knowledge：
id, title, kind("event"|"process"|"origin"|null), content_type("event"|"institution"|"thought"|"economy"|"culture"|"science"|"war"|"other"), time(Time), themes(string[]), place_refs({place_id:string,role:"occurrence"|"origin"|"spread"|"influence"|"related",evidence_block_ids:string[]}[]), person_ids(string[]), summary(Claim|null), flow(Claim[]), points(Claim[]), background(Claim|null), impact(Claim|null), evidence_block_ids(string[]), asset_ids(string[]), source_inventory_ids(string[]), uncertainties(string[]), review_status("pending_review")。
themes允许culture/science/agriculture/war/politics/economy/society/foreign_relations/other，支持多值。kind不清楚填null并建问题，不强制猜分类。

8. relations：
id, from_knowledge_id, to_knowledge_id(string|null), target_label(string|null), type("participation"|"origin"|"spread"|"reform"|"influence"|"causes"|"other"), person_ids(string[]), place_ids(string[]), time_text(string|null), description, evidence_block_ids(string[]), review_status("pending_review")。
关系的文字解释需要依据；causes仅用于原文明确支持的因果。

9. map_candidates：
id, asset_id, reference_time_text(string|null), reference_year(integer|null), date_precision("year"|"month"|"day"|"period"|"unknown"), historical_names(string[]), legend_text(string|null), evidence_block_ids(string[]), geometry(null), geometry_status("not_digitized"), notes(string[])。
本提示词只做图文提取，不做空间数字化；geometry固定null。时期综合图不能填成一个精确起点年。

10. inventory：
id, document_id, page_ids(string[]), block_ids(string[]), item_label, scope("chinese_history"|"world_history"|"mixed"|"uncertain"), disposition("included"|"pending_review"|"out_of_scope"|"duplicate"), knowledge_ids(string[]), duplicate_of_inventory_id(string|null), reason(string|null)。
逐项登记原文知识候选，不能仅根据已生成的knowledge倒造清单；重复和不纳入项必须有理由。

11. review_issues：
id, record_ids(string[]), category("ocr"|"time"|"place"|"person"|"relation"|"source"|"image"|"scope"|"duplicate"|"other"), description, evidence_block_ids(string[]), suggested_action, blocking(boolean), status("open")。
OCR更正的原值、改值及证据写在description。不靠无依据的数值置信度宣称准确。

【E. 最终输出】
输出一个完整合法JSON对象，顶层为：
{
  "schema_version": "history-pdf-ingest/1.0",
  "batch": {
    "id": "输入批次号",
    "document_id": "输入文档号",
    "requested_pdf_pages": [],
    "completed_pdf_pages": [],
    "partial_pdf_pages": [],
    "unprocessed_pdf_pages": [],
    "complete": false,
    "next_pdf_page": null,
    "carryover": []
  },
  "documents": [],
  "pages": [],
  "blocks": [],
  "assets": [],
  "places": [],
  "people": [],
  "knowledge": [],
  "relations": [],
  "map_candidates": [],
  "inventory": [],
  "review_issues": [],
  "validation": {
    "structure_check_status": "not_run",
    "duplicate_ids": [],
    "dangling_references": [],
    "page_coverage_issues": [],
    "time_issues": [],
    "source_issues": [],
    "unreadable_blocks": [],
    "unprocessed_assets": [],
    "semantic_review_status": "not_performed"
  }
}

以上是顶层模板，不是空白交付结果。填入真实提取数据。completed/partial/unprocessed是互斥PDF页序列表，其并集须等于requested；一页的必要文本或图像未读完就不能放completed。complete仅表示本批页面处理完成，不代表史实审核或整本教材完成。
carryover每项为{type:"paragraph"|"relation"|"duplicate"|"other",record_ids:string[],description:string,next_action:string}；next_pdf_page是下一待处理或待重读的页序，没有才null。
validation的问题数组元素为{record_ids:string[],description:string}。实际执行机械校验时structure_check_status=passed/failed；没有工具执行时为not_run，不能把自我检查冒充程序校验。所有待人工内容核验项进入review_issues，semantic_review_status保持not_performed。

输出前检查ID唯一、引用有效、证据齐全、年代合法、页序覆盖及图片是否遗漏。保留自查发现的问题，不删除问题记录来制造“全通过”。
输出长度不足时，交付完整连续页段及合法JSON，保留partial/unprocessed、next_pdf_page与carryover。不要截断JSON，不用“同上”“略”“等若干条”或省略号代替数据，也不要把未读取页面标为完成。

在JSON外附简短Markdown审阅摘要，分别报告：页面读取覆盖、知识清单覆盖、结构检查是否实际运行、需要人工核验的事实、图片未读或未导出情况。不把JSON合法或数量相等写成“全部内容正确”。
如果工具确实能够生成文件，则交付batch.json和review.md；否则直接返回完整JSON和摘要，不宣称已创建附件。
```
