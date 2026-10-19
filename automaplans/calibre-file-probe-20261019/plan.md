# Plan v1

workflow_file: "workflow-v1-calibre-file-probe.automa.json"
workflow_version: "v1"
automa_version: "1.30.02"
source_asset: "automa-trigger-001-manual + automa-browser-001-tab-navigation-alert + automa-interaction-01-09-javascript-code-basic"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "request-level contracts recorded; generation must deep-copy complete version-matched exemplars"
status: awaiting-user-decision

## 方案

目标：在用户已打开的 Calibre 本地页面上手动运行工作流，确认指定 file URL 前缀与 `.calibreMain` 元素存在性，并通过页面 `alert` 汇报。

### 节点与连接顺序

| 顺序 | Block | 配置要点 | 配置证据 |
|---|---|---|---|
| 1 | Trigger | `label=trigger`，`data.type=manual`；不得写 `data.triggers: []` | `automa-trigger-001-manual` 完整 JSON + trigger index |
| 2 | Active Tab | `label=active-tab`，保留样本数据结构；先绑定当前活动页面 | `automa-browser-001-tab-navigation-alert` 完整 JSON + active-tab 文档/源码 |
| 3 | JavaScript code | `label=javascript-code`，`context=website`，`timeout=20000`；代码在页面上下文检查 URL/DOM、alert、`automaNextBlock()` | `automa-interaction-01-09-javascript-code-basic` 完整 JSON + JS 文档/源码 |

Edges：严格拷贝选定 1.30.02 exemplar 的 VueFlow 原生边结构。预计两条普通输出边；节点 ID、edge ID、handles、class 均按选定样本模板确定性替换，不凭空猜 handle。最终需 Code 阶段从 JSON 资产二次核实并记录字段映射。

### 检测伪代码

```js
try {
  const url = window.location.href;
  const prefix = 'file:///path/to/user/Calibre%20书库';
  const matches = document.querySelectorAll('.calibreMain');
  const urlOk = url.startsWith(prefix);
  const elementOk = matches.length > 0;
  const safeUrl = url.length > 240 ? url.slice(0, 240) + '…' : url;
  const status = urlOk && elementOk ? '通过' : '未通过';
  window.alert(`${status}\nURL前缀匹配：${urlOk}\n.calibreMain存在：${elementOk}\n匹配数量：${matches.length}\n当前URL：${safeUrl}`);
} catch (error) {
  window.alert(`检测异常：${String(error?.message || error).slice(0, 240)}`);
}
automaNextBlock();
```

此代码只在生成阶段作为 `javascript-code.data.code` 写入；当前文档只给出伪代码/内容约定，不是最终 workflow JSON。

### 权限和运行前置

- 用户需先打开目标 Calibre 页面，使其成为当前活动标签页；再启动工作流。
- 用户在浏览器扩展管理页为 Automa 开启 `Allow access to file URLs`。
- 仅使用 website 执行上下文；无外部网络请求、CDN、HTTP Request、文件读取权限或 DOM 修改。
- 如果实际浏览器不是 Chrome，记录实际名称/版本并确认 Automa 行为，不套用未经验证的浏览器结论。

### 成功、边界与失败路径

- 成功：active tab 是目标 file 页面、权限已开、脚本可注入；一个 alert 显示 URL 匹配 true、元素存在 true、数量大于 0；用户关闭后工作流结束。
- 边界：URL 前缀不符但注入正常；alert 报 `URL前缀匹配：false`，元素结果独立报告，整体未通过。
- 元素未匹配：报告数量 0 和未通过，不抛错。
- 权限/注入错误：Active Tab 或 JavaScript 节点失败，由 Automa 日志反馈；不得把权限失败归类成“没有元素”。
- Alert 被用户确认关闭后继续流到链路末端。脚本显式调用 `automaNextBlock()`。

## 生成源与字段合同

- Trigger 节点：复制 `automa-trigger-001-manual` 的节点数据结构，省略空 `triggers`。
- Active Tab 节点和 native edge shape：复制 `automa-browser-001-tab-navigation-alert`。
- JavaScript code 节点参数：复制 `automa-interaction-01-09-javascript-code-basic`。
- 顶层、drawflow 容器、设置对象优先采用完整同版本 exemplar 的原始结构；先生成时深拷贝完整 asset，再仅替换名称、描述、节点 ID/坐标、脚本、对应 edge 标识。不能把多个 exemplar 通过自行拼接而改变 schema family；Code 阶段应选一个顶层基准并以其他样本仅映射其节点字段。
- generation record 必须列出 `source_asset`、`source_asset_version`、`schema_family`、`contract_status`、`copied_fields`、`request_specific_fields`、`unresolved_conflicts`。
- `workflow-state` 不纳入本版：不依赖其未完成完整合同；JavaScript 显式继续且无后续边，流程自然完成。若导入测试证明需额外终止节点，返回方案修订，不得临时猜字段。

## 静态验证和导入测试

1. JSON 解析、1.30.02 元数据和 `drawflow.nodes` / `drawflow.edges` 检查；确认没有 `drawflow.Home.data`。
2. 节点 ID 唯一；edges 两端节点存在；source/target handles 指向相应 node；edge id/class 与 handle 一致；全部节点由 Trigger 可达。
3. 检查位置无负坐标、重叠，横向相邻节点留至少 300px。
4. 对比所选同版本完整 exemplar；字段差异逐一标为 copied 或 request-specific；schema-risk 必须为零。
5. 导入 Automa 后逐节点确认名称/图标/编辑面板；保存并重新导出，确认参数、handles 和边保留。
6. 浏览器打开目标 file 页面，授予 file URL 权限，手动执行；实际记录 alert 全文、Automa 节点状态、浏览器和扩展版本、URL 前缀结果、元素数量。

## 验收用例

- CASE-01 正常目标页：期望 URL 前缀 true、`.calibreMain` 存在 true、数量 >=1，alert 汇总并正常结束。
- CASE-02 URL 边界：期望不匹配前缀时 false；不将元素检测耦合为 URL 成功与否。
- CASE-03 权限负向：文件访问权限关闭时记录确切失败表现；权限错误不等同于元素缺失。
- CASE-04 导入识别：所有预期节点名称/图标/配置均被 Automa 识别，重导出参数和 edges 保持。

静态资产当前尚未生成，以上运行用例均为 not-run；运行结论只能在用户提供实际浏览器反馈后写入。

## 风险、未知与回退

- 主要风险是浏览器对本地 file URL 的扩展注入权限/策略；manifest 中 `<all_urls>` 和 `file://*/*` 可访问资源不是 runtime 成功证据。
- 当前截图说明一个页面 DOM 有 `div.calibreMain`，实际活动页面 URL 和数量待运行时确认。
- alert 会暂停工作流等待人工点击，属于用户请求的预期交互。
- 如导入或运行失败，保留失败 asset，按 JSON -> 分类索引 -> 文档 -> 源码 -> runtime 顺序排查；每次修复新增版本并回到 testing。
- 不覆盖旧资产；新版本文件应以 `workflow-v1-calibre-file-probe.automa.json` 命名，写入前再次检查是否已存在。

## 预期请求目录产物

- `request.md`
- `ask.md`
- `context-brief.md`
- `block-contracts.md`
- `intent.md`
- `plan.md`
- `decision.md`
- `workflow-v1-calibre-file-probe.automa.json`（仅计划获批准后生成）
- `validation.md`
- `feedback.md`
- `troubleshooting.md`
- `lessons.md`
- `pending-knowledge-sync.md`
- `acceptance.md`

## 状态

`awaiting-user-decision`。用户批准本计划 v1 后才进入 approved 并交由 Code 生成；当前无 workflow JSON，不具备可导入或已验证状态。
