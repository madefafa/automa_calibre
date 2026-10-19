# Validation v3

workflow_file: "workflow-v3-calibre-ebook-content-render.automa.json"
workflow_version: "v3"
automa_version: "1.30.02"
source_asset: "workflow-v2-calibre-file-probe-url-normalized.automa.json"
source_asset_version: "1.30.02"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "pass"
status: testing

## 变更范围

- 保留 v1/v2，不覆盖已验证资产。
- 从 v2 完整深拷贝顶层结构、Trigger、Active Tab、edges 和 JavaScript Block 结构。
- 仅替换工作流名称/说明、JavaScript 节点 ID/说明/代码及对应 edge target handle/id/class。
- 新脚本保留 v2 URL 解码比较和 `.calibreMain` 检查；增加唯一 `.calibreEbookContent` 检查和幂等 style 注入。
- 样式目标：body 只保留含正文的祖先链；`.calibreEbookContent` 白底、`width: 80vw`、水平居中、最小高度 100vh、内边距；不改磁盘文件。

## 静态检查

| 检查 | 结果 |
|---|---|
| JSON parse | pass |
| Automa 1.30.02 metadata | pass |
| `drawflow.nodes` + `drawflow.edges` | pass |
| no legacy `drawflow.Home.data` | pass |
| manual Trigger no empty `triggers` | pass |
| unique node IDs | pass |
| edge endpoints / handles / ids / classes | pass |
| reachability from Trigger | pass；3/3 nodes |
| non-negative geometry | pass |
| URL normalization retained | pass |
| `.calibreEbookContent` selector | pass |
| idempotent style ID | pass；`automa-calibre-reader-style-v3` |
| 80vw and white background | pass |
| external network/dependency | pass；none |
| import recognition | not-run |
| render runtime | not-run；等待用户运行 |

## 字段记录

- copied_fields: v2 顶层/Settings/globalData/drawflow family、Trigger、Active Tab、edge 原生字段及 JavaScript 参数字段。
- request_specific_fields: v3 workflow name/description、JavaScript node ID/description/code、对应 edge target handle/id/class。
- schema-risk: none observed。
- unresolved_conflicts: none。

## 运行前提

1. 导入 `workflow-v3-calibre-ebook-content-render.automa.json`，不要继续运行 v1/v2。
2. 保持 Automa 的 `Allow access to file URLs` 开启。
3. 打开目标 Calibre `file://` 页面并保持活动标签页。
4. 手动运行 v3；关闭 alert 后观察页面。
5. 记录：正文是否唯一可见、背景/宽度/居中、导航和目录是否隐藏、重复运行是否稳定、重载是否恢复原样。

## 证据边界

静态 pass 不代表 Automa 导入识别成功，也不代表 CSS `:has()` 与页面现有样式在实际浏览器中达到预期。v2 的 URL/DOM 检测有用户截图成功证据；v3 渲染效果仍为 testing。
