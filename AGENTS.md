# 项目代理入口

开始项目工作时读取根目录的 `Agent.md`，遵循其中的产品范围、工作流程、会话日志和问题记录规则。追溯需求依据时读取 `项目讨论总稿.md`，规划首版实现或验收时读取 `项目规格说明.md` 并核对其确认状态。

## Agent skills

### Issue tracker

规格和任务采用 `.scratch/<feature-slug>/` 下的本地 Markdown 管理。约定见 `docs/agents/issue-tracker.md`。

### Triage labels

采用默认五种分诊标签，存储在本地文件的 `Status:` 字段中。映射见 `docs/agents/triage-labels.md`。

### Domain docs

采用 single-context：根目录 `CONTEXT.md` 与 `docs/adr/`。读取规则见 `docs/agents/domain.md`，文档按需建立。
