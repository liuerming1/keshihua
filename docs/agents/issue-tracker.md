# Issue tracker: Local Markdown

本项目的规格与任务使用本地 Markdown，不要求 Git 远程仓库或外部平台。

## 存放约定

- 每项功能一个目录：`.scratch/<feature-slug>/`。
- 正式规格：`.scratch/<feature-slug>/spec.md`。
- 实施任务：`.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 编号，每个任务单独一个文件，不合并成一份任务清单。
- 规格与任务顶部使用 `Status:` 行记录分诊状态；标签映射见 `docs/agents/triage-labels.md`，路径均相对项目根目录。
- 讨论与评论追加在对应文件底部的 `## Comments` 下。

## 技能操作对应方式

- “发布到议题跟踪器”：在上述目录新建或更新对应 Markdown；已经存在时先读取，避免重复创建。
- “应用标签”：将对应标签写入 `Status:` 行；技能要求 `ready-for-agent` 时按该映射记录。
- “读取相关任务”：读取用户提供路径或明确任务编号对应的文件；编号不唯一时依据功能目录定位。
- “更新任务”：保留既有内容、评论及有用历史，修改正文或状态并记录原因。
- 未来将根目录规格草案正式发布后，应明确正式正文的位置，根目录可保留入口说明，避免维护两份不同的有效规格。本次设置不自动完成发布。

## Wayfinding operations

以下仅供使用 wayfinder 时采用，本次不创建探索任务。

- Map：`.scratch/<effort>/map.md`，保存 Notes、Decisions-so-far 和 Fog。
- 子任务：`.scratch/<effort>/issues/NN-<slug>.md`，正文保存待解问题。
- `Type:` 表示 `research`、`prototype`、`grilling` 或 `task`。
- 此类探索子任务使用 `Status: open`、`Status: claimed`、`Status: resolved` 记录流程状态；它们不是五种分诊标签的别名。
- `Blocked by: NN, NN` 表示依赖；所有依赖都为 `resolved` 时解除阻塞。
- Frontier：按编号选取开放、无阻塞且未认领的子任务。
- Claim：开始前先写入 `Status: claimed` 并保存。
- Resolve：追加 `## Answer`，设置 `Status: resolved`，并向 map 的 Decisions-so-far 追加结论摘要及链接。
