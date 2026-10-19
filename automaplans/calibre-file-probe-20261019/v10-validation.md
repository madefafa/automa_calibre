# Validation v10

workflow_file: "workflow-v10-calibre-reader-floating-ball-fixed.automa.json"
workflow_version: "v10"
automa_version: "1.30.02"
source_asset: "workflow-v9-calibre-reader-responsive-fix.automa.json"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "pass; browser runtime pending"
status: testing

## 修改

- 保留 v9，不覆盖历史资产。
- toggle DOM ID 与所有 CSS 选择器统一为 `automa-calibre-reader-toggle-v10`。
- 左侧悬浮球样式、伪元素图标、hover/active/focus 选择器均绑定 v10 ID。
- `.calibreEbookContent` 增加 `display:block`、`position:relative`、`float:none`、`clear:both`、`margin:0 auto`，以抵消书籍 stylesheet 对宽屏居中的影响。
- 保留 v9 最大 1100px 响应式阅读宽度、窄屏布局、图片自动居中、面板默认折叠和三层控制。

## 静态检查

| 检查 | 结果 |
|---|---|
| JSON parse | pass |
| JavaScript syntax | pass |
| Automa 1.30.02 metadata | pass |
| `drawflow.nodes` / `drawflow.edges` | pass |
| node IDs unique | pass |
| edge endpoints / handles / id / class | pass |
| reachability | pass；3/3 nodes |
| toggle node ID | pass；单一 v10 ID，无逗号表达式 |
| CSS selectors | pass；不引用旧 v9 toggle selector |
| floating icon | pass；left fixed, circular, pseudo icon, accessible label |
| content centering | pass；block, relative, float none, clear both, auto margins |
| panel default collapsed | pass |
| image centering | pass |
| runtime | not-run |
| file:// URL trigger runtime | not-run; remains unverified |
