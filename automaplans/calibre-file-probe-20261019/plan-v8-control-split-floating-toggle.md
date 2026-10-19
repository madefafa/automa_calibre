# Plan v8 - 分离风格控制与左侧无文字悬浮按钮

workflow_file: "workflow-v8-calibre-reader-control-split.automa.json"
workflow_version: "v8"
automa_version: "1.30.02"
source_asset: "workflow-v7-calibre-reader-typography-style.automa.json"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "reuse v7 contracts; split style layers and replace toggle UI"
status: awaiting-user-decision

## 用户修订目标

1. “风格控制（开启）”只控制 v6 基础阅读布局：全宽正文、白底、图片约束、`parsererror` 隐藏、外围导航隐藏。
2. v7 独占的字体系统和 HTML 语义标签美化，改为独立的“风格化阅读”开关。
3. “显示面板”继续是独立开关，不与基础布局或风格化样式混用。
4. 面板按钮改为类似苹果系统的左侧悬浮按钮：无可见文字、透明背景、渐变过渡、低干扰，并保持 overlay 不占正文空间。
5. 保留 v7 的 URL trigger、无 alert、跨平台字体 fallback、面板内容、导航和目录。

## 样式层拆分

### 基础阅读布局 style

固定 ID：`automa-calibre-reader-base-style-v8`。

包含 v6 行为：

- html/body/main/content 全宽白底；
- `parsererror { display: none !important; }`；
- `.calibreMeta`、`.calibreToc`、`.calibreEbNav`、`.calibreEbNavTop` 隐藏；
- 图片、SVG、video、canvas `max-width: 100%`、`height: auto`；
- 正文不横向溢出。

默认 enabled=true，由“风格控制（开启）”复选框控制。

### 风格化阅读 style

固定 ID：`automa-calibre-reader-typography-style-v8`。

仅包含 v7 新增行为：

- `--automa-font-sans` 跨平台字体栈；
- `--automa-font-mono` 等宽字体栈；
- html/body 字体应用、字号、字距、抗锯齿；
- h1-h6、p、a、blockquote、ul/ol/li、strong/b、em/i、hr、sub/sup、table/th/td 等语义样式；
- 不包含正文宽度、背景、图片约束、parsererror 或外围隐藏规则。

默认 enabled=true，由“风格化阅读（开启）”复选框控制。关闭后字体和语义样式恢复页面原有样式，但基础阅读布局仍保持。

### 显示面板控制

固定 ID：`automa-calibre-reader-panel-style-v8`。

- 面板默认显示；“显示面板”复选框默认 checked=true；
- 面板 fixed overlay，不设置 body padding、main margin compensation 或 content width compensation；
- 关闭显示面板只设置 `panel.hidden=true`，不影响两个样式层；
- 顶部悬浮按钮始终保留，点击切换面板显隐并同步复选框。

## 左侧悬浮按钮

替换文字按钮为无文字按钮：

- ID：`automa-calibre-reader-toggle-v8`。
- 位置：`position: fixed; left: 12px; top: 50%; transform: translateY(-50%);`。
- 尺寸：固定 36px 或 40px 正方形，圆形或胶囊形；不因页面文字流改变布局。
- 视觉：半透明白色背景、细边框、轻阴影、`backdrop-filter`（可用时）、hover/focus 渐变过渡；不使用文字标签。
- 图标：使用纯 CSS 的三条短线/面板符号，或内联无外部依赖的简单图标；按钮 `aria-label` 提供“显示面板/隐藏面板”，视觉上不显示文字。
- 交互：hover/focus/active 有透明度和 transform 过渡；点击只控制 overlay 面板。
- 面板右侧仍固定 overlay；按钮不会挤压正文或改变正文宽度。
- 面板隐藏时按钮仍可见；面板显示时按钮仍在左侧，避免遮挡右侧正文操作。

## 面板控制区顺序

```text
风格控制（开启）       -> 控制 base style
风格化阅读（开启）     -> 控制 typography style
显示面板               -> 控制 panel hidden
书籍信息
页面导航
目录
```

三个 checkbox 都默认 checked=true。顶部无文字按钮与“显示面板”checkbox 双向同步。

## 运行清理

运行前移除 v3-v7 旧 style、panel、toggle 节点，以及 v8 自身旧节点，避免重复注入。只移除本工作流 ID，不删除页面原有样式或 DOM。

## 静态验收

- JSON 使用 `drawflow.nodes` + `drawflow.edges`。
- URL trigger 继续使用 v7 的 `visit-web` 结构；file:// 自动触发仍标记 runtime 未验证。
- JS 无 `window.alert`，语法通过。
- 存在独立的 base style、typography style、panel style 三层。
- “风格控制”只引用 base style；“风格化阅读”只引用 typography style；“显示面板”只引用 panel hidden。
- 默认三个 checkbox 均 checked=true。
- 按钮无可见文字，存在 aria-label、左侧 fixed、透明/渐变/过渡 CSS。
- 保留全宽正文、图片防溢出、parsererror 隐藏、面板 overlay、XHTML selector、节点/边/句柄/可达性检查。

## 运行验收

- V8-01：关闭“风格控制”，v6 基础布局样式撤销，但字体与语义样式仍存在。
- V8-02：关闭“风格化阅读”，字体/语义样式撤销，但基础全宽/白底/图片约束仍存在。
- V8-03：关闭“显示面板”，面板隐藏，两个样式层不受影响。
- V8-04：左侧无文字悬浮按钮可显示/隐藏面板，overlay 不改变正文宽度。
- V8-05：按钮 hover/focus/active 具有平滑透明/渐变过渡。
- V8-06：三个开关状态可独立切换并保持同步。
- V8-07：file:// URL 自动触发结果单独记录。

## 状态

当前为 `awaiting-user-decision`。批准前不生成 v8 JSON。