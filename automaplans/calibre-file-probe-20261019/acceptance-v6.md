# Acceptance v6

workflow_file: "workflow-v6-calibre-reader-overlay-fullwidth.automa.json"
workflow_version: "v6"
automa_version: "1.30.02"
status: testing

```yaml
case_id: V6-01
scenario: 隐藏 parsererror
input: 自动访问 Calibre file:// 页面并执行 v6
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 页面可见的 parsererror 渲染节点隐藏
actual: not-run
runtime_status: not-run
evidence: ["v6-validation.md", "序言.xhtml"]
executed_at: not-run
blocking_reason: 尚未导入并运行 v6
next_step: 导入 v6 并访问页面观察
---
case_id: V6-02
scenario: 正文与 body 等宽
input: 运行 v6 后观察正文布局
version_browser: Automa 1.30.02；浏览器版本待确认
expected: calibreEbookContent 占满 body 宽度，不保留 v5 的右侧大空白
actual: not-run
runtime_status: not-run
evidence: ["v6-validation.md"]
executed_at: not-run
blocking_reason: 尚无浏览器渲染反馈
next_step: 运行后截图确认左右宽度
---
case_id: V6-03
scenario: 图片防溢出
input: 打开包含大图的书籍章节
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 图片不超出正文宽度且无横向溢出
actual: not-run
runtime_status: not-run
evidence: ["v6-validation.md"]
executed_at: not-run
blocking_reason: 尚无大图页面实测
next_step: 在包含图片的页面测试
---
case_id: V6-04
scenario: 面板默认折叠并以 overlay 展开
input: 自动触发 v6 后检查默认状态，再点击显示面板
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 初始折叠；展开面板覆盖正文且不改变正文宽度
actual: not-run
runtime_status: not-run
evidence: ["v6-validation.md"]
executed_at: not-run
blocking_reason: 尚无浏览器交互反馈
next_step: 运行并验证显示/隐藏按钮
---
case_id: V6-05
scenario: 风格开关与面板独立
input: 展开面板并依次关闭/开启风格
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 关闭/开启只影响正文风格，面板和 toggle 仍可用
actual: not-run
runtime_status: not-run
evidence: ["v6-validation.md"]
executed_at: not-run
blocking_reason: 尚无浏览器交互反馈
next_step: 运行并反复操作开关
---
case_id: V6-06
scenario: file:// URL 自动触发
input: 导航至匹配的 Calibre 本地 file URL
version_browser: Automa 1.30.02；浏览器版本待确认
expected: visit-web trigger 激活工作流
actual: not-run
runtime_status: not-run
evidence: ["v6-validation.md", "plan-v5-reader-panel-url-trigger.md"]
executed_at: not-run
blocking_reason: 知识包仅有 HTTPS visit-web 实测；file:// URL trigger 未验证
next_step: 直接运行测试；如未触发，记录为平台限制并规划替代触发方式
```
