# Triage Labels

本项目使用默认五种分诊角色及同名标签。本地规格或实施任务以 `Status: <标签>` 保存当前分诊状态。

| 技能中的角色 | 本项目标签 | 含义 |
| --- | --- | --- |
| needs-triage | needs-triage | 维护者需要评估 |
| needs-info | needs-info | 需要补充信息 |
| ready-for-agent | ready-for-agent | 规格足够明确，可交给代理执行 |
| ready-for-human | ready-for-human | 需要人工处理 |
| wontfix | wontfix | 不予实施 |

技能提及分诊角色时使用本表映射。改变状态时保留相应原因；设置标签本身不启动实现任务。

wayfinder 探索子任务的 open／claimed／resolved 另按 issue-tracker.md 中的工作流约定处理。
