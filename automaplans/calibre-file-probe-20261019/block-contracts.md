# Block Contracts

workflow_file: "workflow-v1-calibre-file-probe.automa.json"
workflow_version: "v1"
automa_version: "1.30.02"
source_asset: "automa-browser-001-tab-navigation-alert"
status: contract-ready

## 证据定位约定

以下相对路径以独立 Automa knowledge-root 为根；为避免暴露机器绝对路径，以稳定 material ID 标识该根。`source=confirmed` 表示对应源码快照已读，不能表述成上游项目当前版本源码确认。所有三个请求 Block 的完整节点/边/top-level JSON 结构已阅读。

## Trigger

- material_id: `automa-trigger-001-manual`; version: `1.30.02`; state: 已导入、运行验证。
- exemplar: `trigger/001-manual.json`；顶层字段包括 `extVersion`、`name`、`icon`、`table`、`version`、`drawflow.nodes`、`drawflow.edges`、`settings`、`globalData`、`description`。
- label: `trigger`；Vue node type: `BlockBasic`；data.type: `manual`。
- data: 已验证手动样本字段；基础 manual 不出现 `data.triggers: []`。参数列表使用样本现有 `parameters: []`。
- handles: exemplar edge `sourceHandle=<triggerId>-output-1`；作为本流程起点，其 target handle 由目标节点 id 加 `-input-1` 得到，按该 exemplar 精确映射。
- editor/runtime: 知识根索引称手动运行显示 Execute、执行后续 Block 成功；文档 `.docs/blocks/trigger.md` 说明点击运行触发。
- prerequisites: 用户手动启动。
- known failures: 空 `triggers` 会导致 Trigger UI 无选项（TP-001），禁止带入。
- evidence: documentation=confirmed, source=partial, json=confirmed, runtime=confirmed（仅此 Block 的手动触发一般行为）, feedback=partial, freshness=aging。runtime 不覆盖本工作流 JSON 导入或后续链路。

## Active Tab

- material_id: `automa-browser-001-tab-navigation-alert`; version: `1.30.02`; state: 知识根索引列为通过。
- exemplar: `browser/001-tab-navigation-alert.json`；完整节点 shape：`id`、`type=BlockBasic`、`initialized`、`position`、`data: { disableBlock: false }`、`label=active-tab`。
- label: `active-tab`；Vue node type: `BlockBasic`；data.type: 不适用，样本中无 `data.type`。
- parameters: data 仅 `disableBlock`。
- handles: 输出 `active-tab-browser-tab-001-output-1`；下游 target handle `javascript-code` id 加 `-input-1`，边其余字段复制 exemplar family。
- editor/runtime: `.docs/blocks/active-tab.md` 描述将当前页面设置为活动标签；source `src/workflowEngine/blocksHandler/handlerActiveTab.js` 查询 active tab，URL filter 为 `*://*/*` 与 `file://*`，最终校验接受 `http` 或 `file://` URL。
- prerequisites: 目标 Calibre 页面打开并成为用户当前活动页面；用户允许 Automa 文件 URL access。
- known failures: 没有符合条件的 active tab 会报 `Can't find active tab`；先前活动 tab 指向非网页页面时应避免运行。
- evidence: documentation=confirmed, source=confirmed（material snapshot）, json=confirmed, runtime=partial（样本在常规网页运行；file 页面语义有 source 支持但无本请求 runtime）, feedback=partial, freshness=aging。

## JavaScript code

- material_id: `automa-interaction-01-09-javascript-code-basic`; version: `1.30.02`; state: 索引与资产记录列为实测通过。
- exemplar: `interaction/01-09-interaction-javascript-code-basic.json`；完整 node shape 与参数已读。
- label: `javascript-code`；Vue node type: `BlockBasic`；data.type: 不适用，行为由 label 及 `data.context` 选择。
- parameters: `code`；`context=website`；`timeout=20000`；`everyNewTab=false`；`preloadScripts=[]`；`runBeforeLoad=false`；`disableBlock=false`。复用样本字段，只替换 code 与描述。
- handles: 输出 handle 为 `${nodeId}-output-1`；下游按 workflow-state node ID `-input-1`；edge shape 沿用 exemplar。
- editor/runtime: `.docs/blocks/javascript-code.md` 说明网页 JS 与 `automaNextBlock`；`.docs/reference/javascript-execution-context.md` 说明 Active Tab 注入。source `src/workflowEngine/blocksHandler/handlerJavascriptCode.js` 在非 background context 下要求 `activeTab.id`，未绑定时抛 `no-tab`。
- script: 查 URL 前缀，query selector `.calibreMain`，收集符合类选择器的数量；alert 汇报。只回报截断 URL，不读正文、不改 DOM。
- prerequisites: 上游 Active Tab 成功、允许 file URL access；目标 tab 页面可注入脚本。
- known failures: 缺活动标签/文件权限/注入拒绝时 block 失败，需依据实际 Automa 日志判断，不将其误报为 selector 未命中。
- evidence: documentation=confirmed, source=confirmed（material snapshot）, json=confirmed, runtime=partial（普通网站有测试，file:// 无测试）, feedback=partial, freshness=aging。

## Workflow State

- material_id: `automa-general-workflow-state`; version `1.30.02`。
- exemplar `general/001-general-http-pipeline.json` 中有 Workflow State 正常路径，但该资产整体仅部分通过；源材料尚未提取完整节点上下文作为 generation exemplar。
- label: `workflow-state`；Vue node type/参数/handle 的请求本地合同尚未通过完整 JSON exemplar 核验。
- 当前结论：不作为生成节点；依赖 JavaScript 节点显式 `automaNextBlock()` 后流程自然结束。若 JSON 原生格式要求显式 terminal 节点，则必须在生成前补读取完整可信资产并建立合同；不得猜 schema。
- evidence: documentation=partial, source=partial, json=partial, runtime=partial, feedback=partial, freshness=unknown。

## Schema 生成门

- 计划目标 family: `drawflow.nodes` + `drawflow.edges`；不得生成 `drawflow.Home.data`。
- 候选拷贝资产：`automa-browser-001-tab-navigation-alert` 提供 Active Tab 节点和完整 edge shape；`automa-trigger-001-manual` 提供 manual trigger 节点；`automa-interaction-01-09-javascript-code-basic` 提供 JS 参数节点。
- 生成前仍须确认是否要终止节点，以及根据 Code 阶段前最后一次核对，读取完整选定 exemplars 并按实际 top-level/Settings shape 深拷贝；不可凭这份摘要手写完整 JSON。
- unresolved_conflicts: none known；file URL runtime permission/extension behavior remains unverified, not a schema conflict。
