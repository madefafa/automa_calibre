# Context Brief

workflow_file: "workflow-v1-calibre-file-probe.automa.json"
workflow_version: "v1"
automa_version: "1.30.02"
source_asset: "automa-browser-001-tab-navigation-alert + automa-interaction-01-09-javascript-code-basic"
status: contract-ready

## 环境与范围

- package_mode: full（知识包具备文档、索引、源码快照和已验证 JSON 资产；本项目没有 MEMORY.md/PLAN.md）。
- browser: Chrome，具体版本待运行反馈确认。
- page_scope: 当前活动的 `file://` Calibre HTML 页面；URL 应以 `file:///path/to/user/Calibre%20书库` 开头。
- permissions: 用户将为 Automa 开启 `Allow access to file URLs`；授予结果待反馈。
- external_dependencies: none。
- evidence_priority: real export > source implementation > test asset > documentation > inference。

## 已读取事实

- root-index: Automa `1.30.02` 当前结构为 `drawflow.nodes` / `drawflow.edges`，Trigger 是工作流入口。
- root-troubleshooting: 手动 Trigger 不应写入空 `data.triggers`；边必须保留完整 source/target handle、边 ID 和 class。
- trigger exemplar: `automa-trigger-001-manual`，1.30.02，已导入和运行验证；使用 `BlockBasic` + `label=trigger`，不含空 `triggers`。
- active-tab exemplar: `automa-browser-001-tab-navigation-alert`，1.30.02，已运行验证；Active Tab 数据为空对象，后续 JavaScript 可用当前页面。
- javascript exemplar: `automa-interaction-01-09-javascript-code-basic`，1.30.02，已运行验证；`label=javascript-code`、`context=website`、`timeout=20000`、显式 `automaNextBlock()`。
- workflow-state evidence: `automa-general-workflow-state`，1.30.02 文档与源码确认 `type=stop-current` 可结束当前工作流。
- active-tab source: `handlerActiveTab` 查询活动标签页 URL `*://*/*` 或 `file://*`，并接受 `http` / `file://`；这是 file:// 兼容性的源码证据，不等于用户浏览器运行已验证。
- javascript source: `handlerJavascriptCode` 在 `context !== background` 且无活动标签页时抛 `no-tab`；因此方案必须先接 Active Tab。

## 方案决策

- 触发：手动运行；不使用 `visit-web` 自动触发。
- 绑定：Trigger -> Active Tab -> JavaScript code -> Workflow State。
- 页面检测：`window.location.href.startsWith('file:///path/to/user/Calibre%20书库')`；元素检测：`document.querySelector('.calibreMain') !== null`。
- 汇报：一个网页 `alert`，报告 `URL前缀匹配`、`calibreMain` 存在性、元素数量和当前 URL 的长度受限版本。
- 失败保护：脚本用 `try/catch`；捕获异常时 alert 报“检测异常”，再调用 `automaNextBlock()`，避免因脚本自身错误掩盖结果。权限或注入失败由 Automa 节点错误记录，不伪造成功。
- 页面不做 DOM 修改、不访问文件内容、不下载资源。

## 未解决事实

- file:// 页面实际注入、alert 显示和工作流结束尚未运行验证。
- 用户浏览器版本、扩展权限实际状态、目标页面实际 URL 和 `.calibreMain` 数量尚未反馈。
- 截图证明 `.calibreMain` 在某个打开页面 DOM 中存在，但不作为本工作流 runtime 证据。

## 状态

`contract-ready`：上下文和关键 Block 合同已具备；待 `request.md`、`intent.md`、`plan.md` 完成后进入 `awaiting-user-decision`。
