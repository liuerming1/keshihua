# 首版任务索引

父规格：[中国高中历史知识可视化：首版规格](spec.md)

用户于 2026-09-18 批准此拆分。现已发布 12 个独立任务文件，共 50 条验收条件；本页只导航，不替代每项任务正文。

## 任务与直接依赖

| 任务 | 标题 | Blocked by | 外部资料说明 |
| --- | --- | --- | --- |
| [01](issues/01-local-globe-learning-path.md) | 本机打开地球并阅读一条示例知识 | 无 | 可用明确标注的测试数据 |
| [02](issues/02-region-time-navigation.md) | 在百年、十年和一年视图间下钻与返回 | [01](issues/01-local-globe-learning-path.md) | 可用明确标注的测试数据 |
| [03](issues/03-temporal-event-selection.md) | 按时间显示单点事件与持续过程 | [02](issues/02-region-time-navigation.md) | 可用明确标注的测试数据 |
| [04](issues/04-historical-map-snapshots.md) | 切换年代时呈现起点版图与历史名称 | [02](issues/02-region-time-navigation.md) | 可用明确标注的测试数据 |
| [05](issues/05-knowledge-details-and-sources.md) | 侧边阅读完整知识与可追溯教材出处 | [01](issues/01-local-globe-learning-path.md) | 可用明确标注的测试数据 |
| [06](issues/06-marker-clustering-and-list.md) | 通过聚合气泡和列表访问密集知识 | [03](issues/03-temporal-event-selection.md) | 可用明确标注的测试数据 |
| [07](issues/07-theme-colors-and-filtering.md) | 按发展主题切换地图颜色和知识筛选 | [04](issues/04-historical-map-snapshots.md)、[06](issues/06-marker-clustering-and-list.md) | 可用明确标注的测试数据 |
| [08](issues/08-knowledge-relationships.md) | 从知识详情理解多地人物与后续影响 | [03](issues/03-temporal-event-selection.md)、[05](issues/05-knowledge-details-and-sources.md) | 可用明确标注的测试数据 |
| [09](issues/09-data-availability-states.md) | 区分无匹配知识、缺资料和示意内容 | [04](issues/04-historical-map-snapshots.md)、[05](issues/05-knowledge-details-and-sources.md)、[06](issues/06-marker-clustering-and-list.md) | 可用明确标注的测试数据 |
| [10](issues/10-first-textbook-batch.md) | 把一个小批真实教材知识接入学习路径 | [03](issues/03-temporal-event-selection.md)、[04](issues/04-historical-map-snapshots.md)、[05](issues/05-knowledge-details-and-sources.md) | 真实教材与必要地图／地名来源尚缺 |
| [11](issues/11-content-coverage-report.md) | 生成能核对页面入口的内容覆盖与缺项报告 | [10](issues/10-first-textbook-batch.md) | 依赖首批真实内容 |
| [12](issues/12-continuous-browsing-and-local-handoff.md) | 跨功能连续浏览与本机阶段交付 | [07](issues/07-theme-colors-and-filtering.md)、[08](issues/08-knowledge-relationships.md)、[09](issues/09-data-availability-states.md)、[11](issues/11-content-coverage-report.md) | 依赖首批真实内容 |

## 从哪里开始

发布时全部任务为 `ready-for-agent`，均未实施。执行必须同时满足任务前置与外部资料条件；这个标签不代表所有任务都能立即开始。

当前只有任务 01 无任务前置。01 完成后，02 与 05 在依赖关系上可分别推进；继续根据每项任务的直接依赖选择可执行项，不能把发布顺序当作必须串行执行的顺序。

任务 10 还等待真实教材及必要可核验来源；即使 03、04、05 已完成，资料不到位也不能开始真实批次。11、12 会通过依赖关系受到影响。实施时以各任务最新记录为准，不将本页的发布时快照当作永远不变的进度。

## 全量内容与最终验收

这 12 项交付功能及代表性内容闭环，不取代全教材范围。教材到位后，按实际版本与连续小单元追加内容和地图批次任务；每批贯通资料、页面入口、详情、出处与内容核验。已知首批上限为 20 条知识及两个地图参考状态，超过则继续拆分。

批次依赖按真实复用关系建立，不强制所有批次串行。具体批次清单齐备后，另建全量首版验收任务，列明任务 12 及所有必要批次作为阻塞项。样例跑通、缺项提示可用或阶段验收通过，均不等于中国通史全量内容已完成。

本次仅发布任务。父规格保持原内容和状态，未启动代码实现、认领任务或生成未经确认的全量批次。

