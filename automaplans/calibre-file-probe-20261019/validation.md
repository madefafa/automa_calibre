# Validation v1

workflow_file: "workflow-v1-calibre-file-probe.automa.json"
workflow_version: "v1"
automa_version: "1.30.02"
source_asset: "automa-trigger-001-manual + automa-browser-001-tab-navigation-alert + automa-interaction-01-09-javascript-code-basic"
source_asset_version: "1.30.02"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "pass"
status: static-validated

## Generation record

- copied_fields: 顶层元数据结构、settings/globalData 结构、drawflow.nodes/edges 容器、BlockBasic 节点字段、VueFlow edge 字段、manual Trigger 字段、Active Tab 字段、JavaScript code 参数字段。
- request_specific_fields: workflow name/description、三个节点 ID、节点坐标、Trigger 描述、JavaScript 描述和检测代码、两条 edge 的 ID/source/target/handles/class。
- unresolved_conflicts: none。
- intentional_design: 不添加 Workflow State；JavaScript alert 关闭后调用 `automaNextBlock()`，末端无后续边，作为自然结束。该设计未经过导入运行验证。

## Static checks

| 检查 | 结果 | 证据/说明 |
|---|---|---|
| JSON parse | pass | Python JSON parser 成功读取目标资产 |
| Automa version | pass | `extVersion` 与 `version` 均为 `1.30.02` |
| Native schema | pass | 使用 `drawflow.nodes` + `drawflow.edges`；未生成 `drawflow.Home.data` |
| Node inventory | pass | 3 个 `BlockBasic`：`trigger`、`active-tab`、`javascript-code` |
| Trigger contract | pass | `data.type=manual`；未写入空 `data.triggers` |
| Node identity | pass | 节点 ID 唯一：`trigger-calibre-001`、`active-tab-calibre-001`、`javascript-calibre-001` |
| Node fields | pass | 每个节点具备 `id`、`type`、`initialized`、`position`、`data`、`label` |
| Edge endpoints | pass | 2 条边两端均指向现有节点 |
| Edge handles | pass | handles 均为 `${nodeId}-output-1` / `${nodeId}-input-1` |
| Edge identity/class | pass | edge ID 和 class 与 source/target handles 一致 |
| Reachability | pass | Trigger 可达 Active Tab，Active Tab 可达 JavaScript code |
| Geometry | pass | 坐标非负、无重复坐标、横向间距为 340px |
| Script logic | pass | 包含 `window.location.href`、URL `startsWith`、`.calibreMain` query、`alert`、`automaNextBlock()` |
| External dependency | pass | 无 CDN、HTTP Request、外部脚本或网络依赖 |
| Import recognition | not-run | 尚未导入 Automa |
| Parameter round-trip | not-run | 尚未导入、保存、重新导出 |
| Browser runtime | not-run | 尚未在真实 Calibre `file://` 页面执行 |
| File URL permission | not-run | 用户同意开启，但实际授权结果尚未反馈 |

## Scope statement

静态校验通过只证明 JSON 结构符合已选 1.30.02 exemplar family；不证明 Automa 编辑器已识别节点、不证明 file:// 页面脚本注入成功，也不证明 `.calibreMain` 在运行页面中存在。

## Next gate

1. 在 Automa 导入 `workflow-v1-calibre-file-probe.automa.json`。
2. 逐节点确认标题、图标、编辑面板及参数回显；保存后重新导出检查边和字段。
3. 开启 Automa 的 `Allow access to file URLs`。
4. 打开目标 Calibre 页面并保持为活动标签页，手动执行。
5. 记录 alert、节点日志、浏览器版本、权限状态、URL 前缀结果和 `.calibreMain` 数量到 `feedback.md` 与 `acceptance.md`。
