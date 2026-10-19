# Decision v10

workflow_file: "workflow-v10-calibre-reader-floating-ball-fixed.automa.json"
workflow_version: "v10"
automa_version: "1.30.02"
source_asset: "workflow-v9-calibre-reader-responsive-fix.automa.json"
status: testing

- 用户批准 v10 悬浮球修复；并追加宽屏正文居中修复。
- v10 保留 v9，修正 toggle ID/CSS 绑定，强制正文块级居中。
- JSON/JS/schema/edge/reachability 静态校验通过。
- 当前进入 testing；悬浮球视觉、宽屏居中、面板交互与 file:// 自动触发均待用户运行反馈。
