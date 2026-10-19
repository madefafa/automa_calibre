# Acceptance v10

workflow_file: "workflow-v10-calibre-reader-floating-ball-fixed.automa.json"
workflow_version: "v10"
automa_version: "1.30.02"
status: testing

```yaml
case_id: V10-01
scenario: 左侧悬浮球呈圆形图标并可见
input: 匹配 Calibre 页面运行 v10
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 左侧垂直居中显示无文字圆形悬浮球，点击可切换 overlay 面板
actual: not-run
runtime_status: not-run
evidence: ["v10-validation.md"]
executed_at: not-run
blocking_reason: 尚无 v10 页面运行反馈
next_step: 导入 v10 并运行
---
case_id: V10-02
scenario: 宽屏正文居中
input: 宽屏浏览器运行 v10
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 正文最大宽度约 1100px，左右留白近似相等
actual: not-run
runtime_status: not-run
evidence: ["v10-validation.md"]
executed_at: not-run
blocking_reason: 尚无 v10 宽屏截图
next_step: 宽屏运行并截图
---
case_id: V10-03
scenario: 默认折叠与图片居中
input: 页面初次加载及含图片页面
version_browser: Automa 1.30.02；浏览器版本待确认
expected: 面板默认折叠，图片居中且不溢出正文容器
actual: not-run
runtime_status: not-run
evidence: ["v10-validation.md"]
executed_at: not-run
blocking_reason: 尚无 v10 runtime feedback
next_step: 运行并验证
---
case_id: V10-04
scenario: file:// URL 自动触发
input: 导航至 Calibre file URL
version_browser: Automa 1.30.02；浏览器版本待确认
expected: visit-web 自动启动工作流
actual: not-run
runtime_status: not-run
evidence: ["v10-validation.md", "plan-v5-reader-panel-url-trigger.md"]
executed_at: not-run
blocking_reason: file URL Trigger 尚未 runtime 验证
next_step: 记录是否自动触发；如未触发，保留失败事实并评估替代触发方案
```
