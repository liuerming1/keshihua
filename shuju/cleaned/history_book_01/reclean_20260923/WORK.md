# 本轮清洗子任务约定（2026-09-23）

输入只读：本目录baseline.json，是public/data/history_book_01.json修改前快照。原PDF：shuju/普通高中教科书·历史必修_中外历史纲要（上）.pdf。依据docs/PDF图文清洗提示词.md、docs/PDF教材清洗与数据设计.md与Agent.md。所有任务用gpt-6-luna/high。只写被分配的 sNN.patch.json、sNN.review.md及本目录sNN/内部临时脚本/截图，不能改共享数据、代码或脚本。

你的职责：对指定页段的全部knowledge逐条检查其time/summary/flow/points/background/impact/place_refs/person_ids/evidence与实际源块；源块不可靠时回原PDF读文字/渲染。修复内容而非仅重命名状态或机械复制summary填points。原文有事实、步骤、背景、影响应提取对应Claim及准确证据；确实没有则保持空并逐条记录原因。不要给所有知识按关键词自动生成同样的模板。可以程序读写数据，但事实和字段角色的判断必须按条核对。

clean_text是保留内容的排版清理：去水印乱码和错误串栏，目录不能变成“已整理”的一句话。raw_text不改。整页底稿可保留但clean_text需可读；边栏混排不能用一刀切删除含正文的行。所需图片文字未读全必须partial/unreadable；已导出图片并不证明字识读完成。保留实际无法确认项，不凭空补经纬度或历史地图几何。

时间：point必须单一明确start_year，uncertain保存约数/范围，多个年份独立事件提出split建议；原话source_text不能放推算年月；未知终点不能ongoing。将已知开始但未知终点的过程标duration + end_status=unknown，不把已知年份塞unknown。可读所有其他页源块作跨页证据，但只修改自己归属段的记录。knowledge归属页为其id内pNNNN，否则最小evidence页。

输出patch结构：
{
 "slice":"sNN", "page_range":[1,38], "baseline_sha256":"真实计算",
 "updates": {"knowledge":[],"blocks":[],"pages":[],"assets":[],"relations":[],"review_issues":[]},
 "knowledge_audit":[{"id":"每个归属knowledge都必须出现一次","evidence_block_ids":[],"decision":"changed或retained或needs_review","checked_fields":["time","summary","flow","points","background","impact","references"],"empty_reasons":{"flow":"为空时针对该条目的理由","background":"同理","impact":"同理","points":"同理"},"note":"具体核对结论"}],
 "split_proposals":[{"id":"原条目","reason":"为什么拆","proposed_titles":[]}],
 "merge_proposals":[{"ids":[],"reason":"必须同一事实，保留多出处"}],
 "open_items":[{"record_ids":[],"reason":"实际不能解决的问题","next_action":"具体动作"}],
 "visually_checked_pages":[]
}
updates中的对象是完整记录，保留此前verification/finalization、图片export等字段，不擅自删除。但你的新内容不能继续冒充原先verified，新增reclean_review={status:'agent_reviewed'或'needs_review',note:'...',slice:'sNN'}供主代理最终决定发布状态。
review.md说明实际逐条数、修改数、视觉检查哪些页、仍缺什么。完整列出本段knowledge_audit，不能用一句“全部检查”代替。页段末尾跨页需读相邻页或明确待核验，不能说以后从已读取页继续。

Python路径C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe，使用-B -X utf8。可用pypdf/pdfplumber、PIL、pdftoppm；阅读PDF时先读PDF技能。如需要截图可用pdfplumber page.to_image或Poppler，再view_image，不输出base64文本。不联网推断新史实；本轮专注已有教材证据的清洗，不扩展产品范围。
