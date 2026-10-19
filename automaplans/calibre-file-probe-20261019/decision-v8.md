# Decision v8

workflow_file: "workflow-v8-calibre-reader-control-split.automa.json"
workflow_version: "v8"
automa_version: "1.30.02"
source_asset: "workflow-v7-calibre-reader-typography-style.automa.json"
status: approved

- 用户批准：生成 v8 并静态校验。
- 用户补充：`pre` / `code` 系统背景强制使用亮色。
- v8 变更：基础阅读布局、v7 字体/语义样式、面板显示三层独立控制；左侧无文字悬浮按钮；代码块亮色背景与深色文字。
- 保留：v1-v7 历史资产、visit-web URL trigger、无 alert、全宽正文、图片防溢出、parsererror 隐藏、面板 overlay。
- file:// URL 自动触发仍需浏览器 runtime 验证，静态校验不得替代实测。
