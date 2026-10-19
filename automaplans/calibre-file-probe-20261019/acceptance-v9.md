# Acceptance v9

workflow_file: "workflow-v9-calibre-reader-responsive-fix.automa.json"
workflow_version: "v9"
automa_version: "1.30.02"
status: testing

```yaml
case_id: V9-01
scenario: 面板初始化折叠
input: 访问匹配页面并等待工作流执行
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 面板隐藏，左侧无文字悬浮按钮可见
actual: not-run
runtime_status: not-run
evidence: ["v9-validation.md"]
executed_at: not-run
blocking_reason: 尚未收到 v9 浏览器反馈
next_step: 导入 v9 并运行
---
case_id: V9-02
scenario: 宽屏响应式阅读域
input: 宽屏浏览器运行 v9
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 正文最大约 1100px、居中、左右留白对称
actual: not-run
runtime_status: not-run
evidence: ["v9-validation.md"]
executed_at: not-run
blocking_reason: 尚无 v9 宽屏截图
next_step: 宽屏运行并截图
---
case_id: V9-03
scenario: 窄屏响应式阅读域
input: 窄屏或缩窄浏览器窗口运行 v9
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 正文宽度随 viewport 缩放，两侧约 8px，无横向溢出
actual: not-run
runtime_status: not-run
evidence: ["v9-validation.md"]
executed_at: not-run
blocking_reason: 尚无 v9 窄屏反馈
next_step: 窄屏运行并截图
---
case_id: V9-04
scenario: 图片自动居中与防溢出
input: 包含图片的 Calibre 页面
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 图片水平居中，不超过正文容器
actual: not-run
runtime_status: not-run
evidence: ["v9-validation.md"]
executed_at: not-run
blocking_reason: 尚无图片页面反馈
next_step: 在含图片章节测试
---
case_id: V9-05
scenario: file:// URL 自动触发
input: 匹配 Calibre file URL
version_browser: Automa 1.30.02；浏览器版本待确认
expected: visit-web 自动激活工作流
actual: not-run
runtime_status: not-run
evidence: ["v9-validation.md", "plan-v5-reader-panel-url-trigger.md"]
executed_at: not-run
blocking_reason: file:// visit-web runtime 尚未验证
next_step: 访问页面并记录是否触发
```
