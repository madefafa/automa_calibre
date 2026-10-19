# Validation v2

workflow_file: "workflow-v2-calibre-file-probe-url-normalized.automa.json"
workflow_version: "v2"
automa_version: "1.30.02"
source_asset: "automa-trigger-001-manual + automa-browser-001-tab-navigation-alert + automa-interaction-01-09-interaction-javascript-code-basic"
source_asset_version: "1.30.02"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "pass"
status: testing

## 修订范围

- 保留 v1 原文件，不覆盖历史事实。
- 仅替换工作流名称/说明、JavaScript 节点 ID/说明，以及 URL 前缀比较逻辑。
- v2 对 `rawUrl` 与 `rawPrefix` 分别调用 `decodeURIComponent` 后执行 `startsWith`；alert 仍显示原始、截断后的编码 URL。
- `.calibreMain` 查询逻辑、单次 alert、Active Tab、手动 Trigger、边结构未改变。

## 静态校验

| 检查 | 结果 |
|---|---|
| JSON parse | pass |
| Automa 1.30.02 metadata | pass |
| `drawflow.nodes` + `drawflow.edges` | pass |
| no `drawflow.Home.data` | pass |
| manual Trigger no empty `triggers` | pass |
| unique node IDs | pass |
| edge endpoints / handles / IDs / classes | pass |
| reachability from Trigger | pass；3/3 nodes reachable |
| non-negative unique geometry | pass |
| v2 normalized URL tokens | pass |
| import recognition | not-run；需重新导入 v2 |
| runtime | testing；需重新运行 |

## 生成字段记录

- copied_fields: v1 所有原生顶层结构、settings/globalData、Trigger/Active Tab/JavaScript 节点字段、edge 字段。
- request_specific_fields: v2 名称/描述、JavaScript 节点 ID/描述、URL normalization code、对应 target handle/edge id/class。
- schema-risk: none observed。
- unresolved_conflicts: none。

## 下一步

1. 在 Automa 导入 `workflow-v2-calibre-file-probe-url-normalized.automa.json`，不要继续运行 v1。
2. 通过导入识别门：确认 3 个节点标题/图标/配置面板；保存后重新导出并比较 v2 参数及 edges。
3. 保持 Automa 文件网址访问权限开启，打开目标 Calibre 页并保持活动。
4. 手动执行 v2，关闭 alert 后观察工作流是否结束。
5. 反馈 alert 是否显示 `URL前缀匹配：true`、`.calibreMain存在：true`、`匹配数量：1`。
