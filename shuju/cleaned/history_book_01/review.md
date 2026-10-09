# 《中外历史纲要（上）》PDF 图文清洗审阅摘要

日期：2026-09-21。状态：六批、24 个页段的待审中间数据已生成；尚未做全量历史事实审核、图片裁剪导出、地图数字化或前端导入。

## 原件与范围

- 原件：`shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf`，PDF 共 223 页。SHA-256：`833DFC015A6E1DB90A744A9B2E94424043149995AE796330A461A922ACB18E27`。
- 文档标识：`history_book_01`。书名与出版社依据封面、版权页；出版年和版次未从可见页证实，保留 `null`。
- 六个批次按 PDF 页序连续划分，每批四个子代理页段；分段原文件和审阅摘要在 `parts/`，六批汇总为 `b01.json`—`b06.json` 及同名 `.review.md`，全书合并为 `all.json`。

| 批次 | PDF 页序 | 页 | 原文块 | 图片资产 | 知识候选 | 覆盖清单 | 待核验问题 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| b01 | 1–38 | 38 | 181 | 47 | 80 | 93 | 29 |
| b02 | 39–75 | 37 | 350 | 51 | 136 | 143 | 61 |
| b03 | 76–112 | 37 | 1184 | 44 | 102 | 105 | 56 |
| b04 | 113–149 | 37 | 301 | 46 | 94 | 109 | 45 |
| b05 | 150–186 | 37 | 271 | 46 | 114 | 130 | 55 |
| b06 | 187–223 | 37 | 334 | 22 | 293 | 314 | 43 |
| 合计 | 1–223 | 223 | 2621 | 256 | 819 | 894 | 289 |

第六批知识数量较高，主要因为附录朝代表和年表逐项登记。这些是待审候选，不是 819 条已去重、已发布知识。不同页段的块粒度有差异：部分同时保留整页文字层底稿和细分块，因此块数量不能直接衡量知识覆盖率。

## 实际检查

- `all.json` 的 `requested_pdf_pages`、`completed_pdf_pages` 均为 1–223；`partial_pdf_pages` 和 `unprocessed_pdf_pages` 均为空。203 页文字与图像状态均为 `complete`，19 页的图像检查后标为 `not_applicable`，1 页空白页两项均为 `not_applicable`。这些状态依据分段逐页检查报告；主代理没有独立重看全部 223 页图像。
- 运行 `scripts/validate_pdf_cleaning.py` 对 24 个分段、六个批次和全书文件检查字段、枚举、全局 ID、页分区、引用、知识—清单双向关系及时间基础约束；最终全书报告 0 个机械错误。`validation.structure_check_status=passed`；`semantic_review_status=not_performed`。
- 各页段运行 `scripts/audit_pdf_text_coverage.py` 比对 PDF 文字层和证据文本。低覆盖信号已由分段代理复核；字符重叠是遗漏线索，不证明图中文字或史实正确。
- 主代理抽查 PDF 页序 9、55、90、140、170、211 的源文本与对应知识摘要；所抽样条目的概括与原文大体对应。抽样不等于全书事实核验。
- 修复过并行 ID 碰撞、错误证据指针、整页大块证据粒度及知识—覆盖清单反向引用。随后按提示词枚举规范化原代理误填的 `content_type`、时间 `mode/precision` 等字段；不支持的政治、社会、对外交往标签保留在 `themes`，原值与变更写入记录的 `uncertainties` 或 `normalization_note`。未据此补造年代。

## 发布前仍需处理

- 819 条知识及 88 条关系均为 `pending_review`；289 条 `review_issues` 均为 `open`，其中 38 条标记阻断发布。时间、人物、地点、史料观点、因果关系和跨页重复尚未逐条人工核验；157 条知识的时间模式为 `unknown`。
- 256 个资产未导出独立裁剪图片，`file_path=null`；图中文字较小或文字层异常的记录见 `review_issues`。45 个地图候选的 `geometry=null`、`geometry_status=not_digitized`；363 个地点均未填写无来源坐标。不能据此生成精确气泡或历史疆域。
- 并行页段及批次出现过同名地点／人物 ID，合并时已命名空间化并保留差异记录；这只是消除技术冲突，不是语义去重。导语与正文均有“百家争鸣”等同名候选，须按事实范围和多处出处核对后再合并。
- 两条后记／封底覆盖记录按现有枚举以 `scope=uncertain`、`disposition=out_of_scope` 保存，原因中明确为非历史教材内容；不是历史知识待判定。
- 清洗产物是较现有前端模型更丰富的中间格式，不能直接替换 `demoKnowledge`。正式接入前需完成事实审阅、时间与缺坐标适配、图片出处核验和地图空间数据另行数字化。
- 本轮生成的部分渲染 PNG、文字转储及 `__pycache__` 留在项目的 `tmp*` 和缓存目录：已确认这些是临时文件，但终端删除操作被执行策略拒绝，未删除。它们不参与 `all.json` 或重建流程。

## 复现

使用 Codex bundled Python 从 24 个 `parts/b???.json` 重建并验证：

```powershell
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 scripts\rebuild_pdf_book.py
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 scripts\validate_pdf_cleaning.py shuju\cleaned\history_book_01\all.json
```

结构检查通过与页数齐全只说明清洗中间数据可继续审阅，不说明整本教材内容已经正确或已在应用中发布。
