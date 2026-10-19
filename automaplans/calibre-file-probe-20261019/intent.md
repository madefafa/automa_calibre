# Intent

workflow_file: "workflow-v1-calibre-file-probe.automa.json"
workflow_version: "v1"
automa_version: "1.30.02"
source_asset: "automa-trigger-001-manual + automa-browser-001-tab-navigation-alert + automa-interaction-01-09-javascript-code-basic"
status: awaiting-user-decision

## 目标

构建一个最小、可导入的 Automa 验证工作流：用户先打开本地 Calibre HTML 页面，再手动执行工作流；工作流绑定当前活动文件标签页，检查 URL 前缀和 `.calibreMain` 元素，并用网页 alert 汇报。

## 执行链

```text
manual trigger -> active-tab -> javascript-code website -> natural end
```

- Trigger：手动运行，不配置 `visit-web`。
- Active Tab：绑定当前活动 tab；必须在运行前让 Calibre 页面处于浏览器当前活动标签页。
- JavaScript code：website 上下文，执行 DOM 查询与 alert。
- 终止：脚本 alert 关闭后调用 `automaNextBlock()`；不额外加入未完成合同的终止节点。

## 输入与检测

- `prefix`: `file:///path/to/user/Calibre%20书库`
- `currentUrl`: `window.location.href`
- `urlMatches`: `currentUrl.startsWith(prefix)`
- `matchedElements`: `document.querySelectorAll('.calibreMain')`
- `elementExists`: `matchedElements.length > 0`

## 输出

单个 alert，内容包含：

- 当前 URL 的安全截断文本；
- URL 前缀是否匹配；
- `.calibreMain` 是否存在；
- 匹配数量；
- 总结：通过 / 未通过 / 页面检查异常。

不展示 HTML 正文、书籍内容、完整本地文件路径的额外部分或其他敏感页面数据。

## 异常行为

- 脚本内部使用 `try/catch`；异常时 alert 报告“检测异常”和有限错误文本，并继续到自然结束。
- Active Tab 找不到有效 `file://` 页面、文件网址权限未授予或网页脚本注入失败：由 Automa 节点错误记录；这类情况不能被脚本伪装成“元素不存在”。
- 若 URL 前缀不匹配但页面脚本可运行，alert 必须明确报告 URL 不匹配，并仍报告元素检测结果。

## 验收边界

- 必测正常场景：用户截图所示页面，预期 `urlMatches=true` 且 `elementExists=true`。
- 必测边界场景：打开不以指定前缀开头的 file/http 页面，预期 URL 匹配为 false；是否存在 `.calibreMain` 依页面而定。
- 权限失败场景：关闭 Automa 的 Allow access to file URLs 后运行，记录实际错误；此项为预期失败，不计为业务通过。
- 本计划不验证自动访问触发、不修改 DOM、不读取本地文件系统。

## 证据状态

| 断言 | documentation | source | json | runtime | feedback | freshness |
|---|---|---|---|---|---|---|
| 手动 Trigger 可启动工作流 | confirmed | partial | confirmed | confirmed | partial | aging |
| Active Tab 支持当前 file:// tab | confirmed | confirmed | confirmed | partial | unavailable | aging |
| website JavaScript 可读取 DOM 并 alert | confirmed | confirmed | confirmed | partial | partial | aging |
| `.calibreMain` 在用户目标页面存在 | partial | unavailable | unavailable | unavailable | partial | unknown |
| 本组合在用户目标 file:// 页面运行成功 | unavailable | unavailable | partial | unavailable | unavailable | unknown |
