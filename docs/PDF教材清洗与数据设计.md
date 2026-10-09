# PDF 教材清洗与系统数据设计

日期：2026-09-21。状态：清洗与正式资料接入设计；尚未修改应用模型、创建数据库、实现导入器或处理 PDF。本文依据本轮重新读取的现有代码。用户已说明资料为含图片的 PDF，但尚未指定文件路径，工作区未发现 PDF。

配套：[可独立复制的 PDF 清洗提示词](PDF图文清洗提示词.md)。使用时复制该文件的提示词正文并附上 PDF；不必另附本文。

## 1. 当前数据库实际是什么

当前没有 SQL 数据库、数据库服务器或独立后端。数据以 TypeScript 对象保存在 `src/modules/history/index.ts`，经 `createKnowledgeRepository({items, coverage})` 提供 query/get/getRelated，应用使用 queryKnowledge/getKnowledge/getRelatedKnowledge。

这是一套本地数据仓库接口，已经把页面与具体存储隔开，但目前数据仍是虚构演示集。地图测试状态单独在 `src/modules/map/snapshots.ts`。

| 已实现对象 | 已实现字段 |
| --- | --- |
| Knowledge | id、title、year、endYear?、location、regionIds、summary、theme、kind、flow、points、background?、impact?、sources、relations、uncertain? |
| Source | id、kind(textbook/supplement/demo)、title、chapter?、pages?、quote? |
| Relation | id、label、location、placeName?、sourceId、targetId? |
| KnowledgeCoverage | startYear、endYear、regionIds |
| MapSnapshot | id、name、from、to、ring、subdivision? |

主要字段的使用方式：

- `year/endYear` 用于时间筛选；公元前为负数、无 0 年，区间两端包含。
- `location` 为 [经度, 纬度]，用于气泡；`regionIds` 用于区域过滤。
- `theme` 当前单值，字典为 culture/science/agriculture/war。
- `kind` 为 event/process/origin，分别表示单点事件、持续过程、起源知识。
- `summary/flow/points/background/impact` 构成阅读详情。
- `sources` 可有多个出处；关系的 `sourceId` 指 Source.id，不是知识ID，`targetId` 才是关联知识ID。
- 地图 from/to 是有效时段；ring 为单个测试多边形，不是已建成的完整历史GIS数据库。

## 2. 为什么正式教材不能直接照演示字段清洗

现有模型尚不能完整表达以下情况：未知年代、约数年代、未知结束年、缺少坐标、多主题、图片证据、PDF页序与印刷页码的区别。

尤其是现有 `process` 未给 endYear 时会显示“持续中”，而教材未写结束年份常常只是“不知道”。不能让提取模型为了适配旧接口，把缺值编成年代或经纬度。

采用四层数据流：

**原始 PDF／图片 → 页级证据 → 规范化知识 → 审核与页面适配。**

清洗输出先作为待审 JSON 文件包，保留全部内容及缺项；只有核验后、满足相应显示条件的数据才进入页面。暂时不需要为此更换技术栈或引入数据库。以后采用数据库时，各集合可映射为表，引用字段对应外键；知识与出处、知识与地点等多对多关系可映射为关联表。

## 3. 正式资料分成哪些数据块

下面是建议新增的清洗格式，不是现有代码已支持的格式。完整字段类型与输出要求见配套提示词。

| 数据块 | 关键数据标签 | 作用 |
| --- | --- | --- |
| documents 教材 | 文件名、书名、版次、册名、出版社、出版年、总页数、来源类型、文件哈希 | 区分版本，定位原文件 |
| pages 页面 | 文档ID、PDF页序、印刷页码、章节路径、页面类型、文本／图像读取状态 | 判断哪些页读过、哪些未读 |
| blocks 原文块 | 页ID、阅读顺序、类型、页面位置、原始文本、清洗文本、表格、关联图片 | 保留原文、图注、脚注和OCR纠错证据 |
| assets 图片 | 页ID、类型、位置、实际文件路径、图注、可见文字、客观描述、有依据的结论 | 保存地图、时间轴、照片、图表，不遗漏图片知识 |
| places 地点 | 原文地名、历史／现代名称类型、有效时期、坐标、空间精度、定位依据 | 区分古今地名，为地图气泡提供依据 |
| people 人物 | 原文姓名、别名、证据、备注 | 统一人物引用，避免同名误合并 |
| knowledge 知识 | 标题、事件性质、内容类别、时间、主题、人物、地点、摘要、流程、要点、背景、影响、证据、图片、审核状态 | 形成可学习知识单元 |
| relations 关系 | 起止知识ID、类型、人物地点、时间原话、关系解释、出处 | 表达参与、起源、传播、改革、影响、因果 |
| map_candidates 地图候选 | 原图ID、对应年代、精度、历史名称、图例、来源、几何、数字化状态 | 记录可以进一步制作地图的数据，不伪造精确疆域 |
| inventory 覆盖清单 | 原文块、知识候选标题、内容范围、处理结果、知识ID、重复映射、原因 | 核对教材知识是否遗漏，不能从已有结果反推“已全覆盖” |
| review_issues 待核验 | 对象、问题类别、依据、建议处理、是否阻断发布、状态 | 单列OCR不清、年代冲突、来源或坐标缺失 |
| batch/validation 批次与检查 | 请求页、完成页、部分页、未读页、续接位置、引用错误、覆盖缺项 | 支持长PDF分批、断点继续和机械校验 |

### 知识的标签分三类

- 时间性质 `kind`：event / process / origin。它决定怎样筛选时间，不等于教材主题。
- 内容类别 `content_type`：event / institution / thought / economy / culture / science / war / other。
- 筛选主题 `themes`：数组，允许 culture / science / agriculture / war / politics / economy / society / foreign_relations / other。一条知识可以有多个主题；后五项和多主题需要页面适配。

不强制每条知识都有准确时间、人物或坐标；缺少依据留 null 或空数组并登记问题。清洗层保留完整性，发布层决定可展示能力。

### 每一块整理内容都要有证据

摘要、流程步骤、知识要点、背景和影响分别采用 `{text, evidence_block_ids}`。例如某条影响结论引用到具体原文块，再通过块查到页和教材。只给整条知识挂一个教材名，不足以核对某个结论。

重复内容可以合并，但保留多条出处。只因标题相近不能合并；不同年代的起源、传播或改革通常应是独立知识，通过关系关联。

## 4. 时间和图片的清洗规则

时间同时保存原话和机器字段：source_text、mode、start_year、end_year、earliest_year、latest_year、precision、end_status、normalization_note、evidence_block_ids。

- 明确单点：mode=point；明确持续：mode=duration；约数、某世纪发生：mode=uncertain；无法归年：unknown。
- end_status=known/ongoing/unknown/not_applicable。只在资料明确持续时写ongoing；缺结束年用unknown。
- “发生于某世纪”是发生时间不确定，不意味着事件持续整个世纪。没有依据不补世纪起止、朝代公历对应或精确日期。
- 公元前用负数，无0年；跨公元按历史年数计算，不能让模型使用包含0年的直线整数计数。

PDF必须同时处理文字与页面图像，避免丢失图注、地图图例和图片中文字。raw_text保留提取原串，clean_text保存排版清理；无法识别写“[无法辨认]”。实质字词修正单列原值、改值和视觉依据。

图片仅描述可见内容；人物身份、年代、地点不能凭画面风格猜。没有真实导出图片就不编file_path；没有工具计算哈希就不编sha256。

**历史地图截图不是可直接渲染的疆域数据。**地图候选先保留图名、年代、图例和历史地名，geometry=null，另行数字化与核验。不能用像素位置当经纬度、用现代省界替代古代边界、用一个时期的综合地图冒充区间起点版图。

## 5. 与现有页面的对应及后续改动

| 清洗数据 | 页面字段或处理 |
| --- | --- |
| knowledge.id/title/kind | 基本直接对应；不确定kind可在清洗层保留null，待判定 |
| time | 精确年可映射year/endYear；模糊年、未知结束、日期精度须先扩展模型及筛选逻辑 |
| places | 核验后选定气泡定位和相关历史区域；place_id不等于regionId，缺坐标保留清单入口，需扩展页面处理 |
| themes | 保留全部主题；升级筛选或显式确定主主题映射，不能静默丢弃其余主题 |
| 内容分块 | text映射现有详情，证据原样保留在中间层，必要时扩展页面引用 |
| documents/pages/blocks | 生成多个Source，保留原文；扩展PDF页序、印刷页码及块定位，不把两个页码混成一个值 |
| assets | 先保留证据；详情显示图片和查看原页是后续接入改动，不声称当前页面已实现 |
| relations | sourceId映射实际Source.id，targetId映射知识ID；关联地点经核验才可画线 |
| map_candidates | 只有已核验的空间几何及有效时点才生成运行时地图快照；多政权、多面、孔洞需要扩展当前单ring模型 |
| inventory | 用来计算教材内容覆盖；与query用的年代资料窗口分开维护，某年有一条知识不代表该年或整个时期完整 |

清洗中间层故意比现有运行时更丰富。它的产物不能直接替换 demoKnowledge，必须经过校验、历史内容审核和导入适配。所有暂不能上图的知识仍保留在清单，避免丢失教材覆盖。

## 6. 执行与验收

先取得PDF路径，盘点版本、页数、扫描质量及中国史范围；以一个连续小单元试清洗。任务10首批发布范围最多20条知识、两个地图参考状态；超过则追加批次，不为了凑上限省略知识。大文件可以按连续页段提取，跨页段落与跨批次关系用carryover和ID索引续接。

每批分别检查：

1. 页面覆盖：请求页逐一有读取状态，未读图像和模糊内容不能标完整。
2. 结构：JSON有效、ID唯一、引用可解析、枚举和时间合法。
3. 知识覆盖：逐项对照正文、图注、脚注、表格等原文候选清单；重复和范围外都有理由。
4. 内容：人工或独立复核时间、人物、地名、关系与结论对应证据；结构通过不等于内容正确。
5. 发布：确定坐标和时间适配，检查页面入口、详情和出处一致。未满足项留待核验。

本轮仅交付设计与提示词，未创建数据表、未修改程序代码、未运行PDF提取，也未完成任务10的真实内容验收。
