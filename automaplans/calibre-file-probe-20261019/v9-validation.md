# Validation v9

workflow_file: "workflow-v9-calibre-reader-responsive-fix.automa.json"
workflow_version: "v9"
automa_version: "1.30.02"
source_asset: "workflow-v8-calibre-reader-control-split.automa.json"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "pass; file URL trigger runtime unverified"
status: testing

## 修订范围

- 保留 v1-v8，不覆盖历史资产。
- 面板默认折叠：`panel.hidden=true`、`panelInput.checked=false`、`aria-expanded=false`。
- 宽屏正文：`width: min(calc(100% - 32px), 1100px)`，最大 1100px，左右 auto margin。
- 窄屏正文：`width: calc(100% - 16px)`，无最大宽度限制，内边距收窄。
- 图片/SVG/video/canvas：`max-width: 100%`、`height: auto`、左右 auto margin，自动居中。
- 保留 v8 三层独立样式、亮色代码块、parsererror 隐藏、左侧无文字悬浮按钮、无 alert。

## 静态检查

| 检查 | 结果 |
|---|---|
| JSON parse | pass |
| JavaScript syntax | pass |
| Automa 1.30.02 metadata | pass |
| `drawflow.nodes` / `drawflow.edges` | pass |
| unique nodes / valid handles / edge IDs/classes | pass |
| reachability | pass；3/3 |
| default panel collapsed | pass |
| wide responsive width | pass；max 1100px |
| narrow responsive width | pass；viewport minus 16px |
| centered media | pass |
| independent base/typography/panel controls | pass |
| bright `pre/code/kbd/samp` | pass |
| left floating icon button | pass |
| no alert | pass |
| file URL trigger field | pass static；runtime unverified |

## 运行验收

- 导入 v9，确认 3 个节点和 `visit-web` 参数面板。
- 访问匹配 Calibre `file://` 页面，记录 URL Trigger 是否自动激活。
- 宽屏检查正文最大宽度约 1100px、左右对称留白。
- 窄屏检查正文随 viewport 缩放、无横向滚动。
- 打开包含图片和 `pre/code` 的页面，检查图片居中、代码块亮色。
- 确认面板初始折叠，左侧悬浮按钮可打开；三个开关独立工作。
