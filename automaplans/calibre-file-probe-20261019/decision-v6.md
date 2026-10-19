# Decision v6

workflow_file: "workflow-v6-calibre-reader-overlay-fullwidth.automa.json"
workflow_version: "v6"
automa_version: "1.30.02"
source_asset: "workflow-v5-calibre-reader-panel-url-trigger.automa.json"
status: testing

- 用户批准原文：“批准 v6，生成 workflow-v6-calibre-reader-overlay-fullwidth.automa.json 并静态校验。”
- 审批时间：2026-10-19T02:42:54Z（会话环境提供）。
- v6 保留 v1-v5；修改 parsererror 隐藏、正文全宽/图片约束、默认折叠 overlay 面板。
- 静态检查通过：schema、节点/边/可达性、目标规则均通过。
- 运行状态：testing。file:// URL 自动触发以及页面视觉与交互效果未验证。
