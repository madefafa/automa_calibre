# Plan v7 - 跨平台字体与语义阅读样式

workflow_file: "workflow-v7-calibre-reader-typography-style.automa.json"
workflow_version: "v7"
automa_version: "1.30.02"
source_asset: "workflow-v6-calibre-reader-overlay-fullwidth.automa.json"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "reuse v6 contracts; extend content style and panel controls"
status: awaiting-user-decision

## 用户目标

基于 v6 扩展：

1. 建立 macOS、Windows、Linux 兼容的中文/西文字体系统。
2. 对 HTML 语义标签增加适合阅读的 CSS 美化。
3. 在侧边面板的“风格控制（开启）”下面增加“显示面板”开关，默认开启。

保留 v6 的：

- `visit-web` URL 匹配 Trigger；
- 当前 file:// 页面检测；
- `parsererror` 隐藏；
- 正文与 body 同宽；
- 图片防溢出；
- 默认折叠的 overlay 面板；
- 无 `alert`；
- 不修改本地 XHTML 文件。

## 字体系统

在内容样式中增加 CSS 变量：

```css
:root {
  --automa-font-sans:
    "HarmonyOS Sans SC", "HarmonyOS Sans",
    system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", "Helvetica Neue", Helvetica, Arial,
    "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei UI", "Microsoft YaHei",
    "Source Han Sans SC", "Noto Sans CJK SC",
    "WenQuanYi Micro Hei", sans-serif,
    "Apple Color Emoji", "Segoe UI Emoji";
  --automa-font-mono:
    ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
    "Liberation Mono", "Roboto Mono", monospace,
    "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
}
html {
  font-family: var(--automa-font-sans) !important;
  font-size: 16px !important;
  font-synthesis: none !important;
  -webkit-text-size-adjust: 100%;
}
body {
  font-family: var(--automa-font-sans) !important;
  font-weight: 400 !important;
  line-height: 1.68 !important;
  letter-spacing: .01em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
code, pre, kbd, samp {
  font-family: var(--automa-font-mono) !important;
}
```

不下载或自托管字体；只使用本机可用字体和系统 fallback，避免 file:// 页面外部资源/CSP/网络依赖。

## 语义标签样式

在 `.calibreEbookContent` 范围内添加阅读样式，保留原有 class 结构并使用 `!important` 仅覆盖 Calibre 默认样式：

- `h1`：居中、适度标题字号、行高、上下间距、字重。
- `h2`、`h3`、`h4`：层级递减、稳定间距、避免标题孤行。
- `p`：正文字号、行高、段间距、中文断行和长词换行。
- `a`：继承可读颜色、下划线和 hover/focus 状态。
- `blockquote`：左侧边框、内边距、弱化背景，保持中文引用可读。
- `ul`、`ol`、`li`：列表缩进、行距和项目符号。
- `strong`、`b`、`em`、`i`：保留语义强调并避免字体合成异常。
- `hr`：低对比度分隔线。
- `sub`、`sup`：缩放并保持基线。
- `table`、`th`、`td`：最大宽度 100%、自动布局、边框和换行；不得产生横向溢出。
- `img`、`svg`、`video`、`canvas`：继续 `max-width: 100%`、`height: auto`、`object-fit: contain`。

不使用渐变、外部图标、外部 CSS 或网络字体。

## 面板控制

现有面板顺序保持：

1. 风格控制
2. 书籍信息
3. 页面导航
4. 目录

在“风格控制”中从上到下增加：

- `风格控制` 开关：默认 checked=true；控制正文风格 style 的 disabled 状态。
- `显示面板` 开关：默认 checked=true；控制面板的 hidden 状态。虽然 v6 面板初始折叠，v7 的用户要求将“显示面板”开关默认开启，因此 v7 采用：面板默认显示、开关默认开启；独立的顶部 toggle 仍可折叠/展开。

为消除语义歧义，面板初始状态定义为：

- 页面加载后面板可见；
- “显示面板” checkbox 为 checked；
- 顶部折叠按钮文案为“隐藏面板”；
- 面板仍是 fixed overlay，不改变正文宽度。

如果用户希望继续默认折叠，应在审批时改为“显示面板开关默认开启但面板仍折叠”；当前计划按“开关默认开启 = 面板显示”实现。

## 实现约束

- v7 从 v6 深拷贝，不覆盖 v6。
- 清理 v3、v4、v5、v6 的 style/panel/toggle 节点，再创建 v7 节点。
- content style 与 panel style 分离；关闭风格不影响面板。
- 面板内容使用 `textContent` 和原始相对 `href`，不把页面正文 HTML 直接拼接到面板。
- 不使用 `window.alert`。
- `automaNextBlock()` 保持在脚本末尾。

## 静态验收

- JSON 使用 `drawflow.nodes` + `drawflow.edges`。
- Trigger 继续使用 v6 `visit-web` 结构；`file://` runtime 仍单独标记未验证。
- JS 无 `window.alert`，语法通过。
- CSS 包含字体变量、macOS/Windows/Linux fallback、html/body 字体应用、mono 字体应用。
- CSS 包含 h1-h4、p、a、blockquote、ul/ol/li、strong/em、hr、sub/sup、table、图片等语义规则。
- 面板包含两个开关：风格控制默认开启、显示面板默认开启。
- v6 全宽正文、parsererror、图片防溢出、overlay 规则保留。
- schema、节点、边、句柄、可达性、XHTML 结构对照通过。

## 运行验收

- V7-01：macOS/Windows 浏览器分别确认字体 fallback 生效且无外部字体请求。
- V7-02：正文标题、段落、链接、引用、列表、表格和图片可读且不横向溢出。
- V7-03：风格控制关闭/开启只影响正文样式，不影响面板控制。
- V7-04：显示面板开关默认开启；关闭后面板隐藏，开启后显示。
- V7-05：顶部 toggle 与显示面板开关状态保持一致。
- V7-06：面板 overlay 不占正文横向空间。
- V7-07：file:// URL 自动触发是否生效单独记录。

## 状态

当前为 `awaiting-user-decision`。批准前不生成 v7 JSON。