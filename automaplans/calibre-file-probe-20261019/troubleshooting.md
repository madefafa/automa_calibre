# Troubleshooting

## TP-CAL-001：中文 Calibre 目录 URL 前缀比较失败

- symptom: v1 alert 报 `URL前缀匹配：false`，但 `.calibreMain存在：true` 且 `匹配数量：1`。
- exact_error: 无异常；业务判断为 false。
- scope: Automa 1.30.02；file:// Calibre 页面；Chrome 风格浏览器；v1 工作流。
- evidence_order_checked: [json, category-index, documentation, source, runtime]
- JSON: v1 脚本使用 `window.location.href.startsWith('file:///path/to/user/Calibre%20书库')`，只编码了空格，未编码中文目录名。
- category-index: 当前已有 Active Tab/JavaScript 资产支持普通网页；无本地中文路径规范化专项。
- documentation: JavaScript code 文档确认代码运行在当前网页；未规定 URL 编码比较策略。
- source: Active Tab handler 已支持 `file://`，且脚本成功执行；因此不是 active tab 或 file URL 权限失败。
- runtime: 用户截图实测 `.calibreMain` 数量为 1；实际 URL 为 `file:///path/to/user/Calibre%20%E4%B9%A6%E5%BA%93/...`，与 v1 原始前缀不一致。
- hypothesis: URL 的中文目录组件被浏览器百分号编码，v1 期望字符串未进行同等规范化。
- repair: v2 对当前 URL 与期望前缀都调用 `decodeURIComponent` 后比较；保留原始 URL 的截断文本用于 alert。
- result: v1 诊断已确认；v2 待生成和复测。
- retest_state: testing
- attempt: 1
- references: ["feedback.md", "validation.md", "acceptance.md"]

可复用规则：涉及中文 `file://` 路径时，比较前统一对 URL 和期望前缀做同一 URL 编码/解码规范化，不能只对空格手写 `%20`。

## TP-CAL-002：v3 正文被通配隐藏规则误伤

- symptom: 用户运行 v3 后页面为空白，边缘背景不是纯白。
- exact_error: 无脚本异常反馈；页面视觉结果失败。
- scope: Automa 1.30.02；v3；本地 XHTML 页面，证据为用户截图和 [`序言.xhtml`](../../序言.xhtml:25)。
- evidence_order_checked: [json, category-index, documentation, source, runtime]
- JSON: v3 规则 `*:not(:has(.calibreEbookContent)):not(.calibreEbookContent)` 命中正文后代的叶子 `h1`、`p`、`span`；只设置内容容器白底，没有给 html/body 全层设置白底。
- category-index: 与既有 JavaScript Block 合同无冲突；问题是用户自定义 CSS 逻辑。
- documentation: 页面 DOM 元素的后代匹配行为与已提供 XHTML 结构一致。
- source: JS Block 已成功注入样式，未观察到 Automa Block schema 错误。
- runtime: 用户截图展示无正文的空白页面与非白背景边缘。
- hypothesis: 通配 CSS 误伤正文，外层背景继续由原页面样式控制。
- repair: 待审批 v4；仅隐藏明确的元信息/目录/导航类，设置 html/body/main/content 白底，移除 v3 注入的旧 style，不再 alert。
- result: v3 失败，v4 待生成及复测。
- retest_state: awaiting-user-input
- attempt: 1
- references: ["feedback.md", "plan-v4-render-fix.md", "../../序言.xhtml"]
