# Runtime Feedback

workflow_file: "workflow-v1-calibre-file-probe.automa.json"
workflow_version: "v1"
automa_version: "1.30.02"
status: troubleshooting

## 用户反馈 v1

- 反馈形式：浏览器 alert 截图。
- 浏览器/版本：未提供具体版本；界面为 Chrome 风格，待补充。
- 页面：`file:///path/to/user/Calibre%20%E4%B9%A6%E5%BA%93/...`，实际中文目录名被浏览器按百分号编码。
- 权限/注入：未出现权限或注入错误；脚本成功执行并弹窗。
- 实际 alert：`未通过`；`URL前缀匹配：false`；`.calibreMain存在：true`；`匹配数量：1`；当前 URL 显示 `file:///path/to/user/Calibre%20%E4%B9%A6%E5%BA%93/...`。
- 结论：DOM 捕捉能力通过；URL 前缀判断失败；属于 v1 比较逻辑与浏览器 URL 编码表示不一致，不是元素不存在。
- 截图证据：用户在会话中提供的 alert 截图（稳定反馈 ID：`feedback-calibre-v1-20261019-01`）。

## 用户反馈 v2

workflow_file: "workflow-v2-calibre-file-probe-url-normalized.automa.json"
workflow_version: "v2"
automa_version: "1.30.02"

- 反馈形式：浏览器 alert 截图。
- 浏览器/版本：未提供具体版本；界面为 Chrome 风格，待补充。
- 页面：同一 Calibre 本地 HTML 文件，中文目录以百分号编码。
- 实际 alert：`通过`；`URL前缀匹配：true`；`.calibreMain存在：true`；`匹配数量：1`。
- 结论：URL 编码规范化后，前缀检查为 true；`.calibreMain` 确认存在且匹配 1 个；页面脚本注入与 alert 执行成功。
- 证据边界：未提供 Automa 工作流节点日志、导入后重新导出记录或 alert 关闭后的结束状态；这些仍未确认。
- 截图证据：用户在会话中提供的成功 alert 截图（稳定反馈 ID：`feedback-calibre-v2-20261019-01`）。

## 用户反馈 v3

workflow_file: "workflow-v3-calibre-ebook-content-render.automa.json"
workflow_version: "v3"
automa_version: "1.30.02"

- 用户反馈原文：“不再需要 alert 了；背景没��纯白；没有内容；我把静态页面放在 '序言.xhtml'。”
- 用户提供白色空白区域截图；正文未显示，页面边缘不是纯白；v3 渲染失败。浏览器版本及节点结束状态未提供。
- 结构事实：[`序言.xhtml`](../../序言.xhtml:25) 中 `.calibreEbookContent` 是 `.calibreMain` 的直接子节点，正文 `h1` 和 `p` 是其后代；导航、目录是单独的外围节点。
- 根因：v3 通配 CSS 命中正文中的叶子节点，隐藏了标题和段落；同时白底未覆盖最外层 `html/body`。
- 下一步：保留 v3，批准 v4 后定点隐藏外围内容、设置页面全层白底并取消 alert；在同一页面复测时必须清除 v3 遗留 style。
