# Acceptance v3

workflow_file: "workflow-v3-calibre-ebook-content-render.automa.json"
workflow_version: "v3"
automa_version: "1.30.02"
status: testing

```yaml
case_id: RENDER-01
scenario: 仅显示 calibreEbookContent
input: 当前 Calibre file:// 页面，手动运行 v3
version_browser: Automa 1.30.02；Chrome 具体版本待确认
expected: .calibreEbookContent 及其必要祖先可见，正文文本保留
actual: not-run
runtime_status: not-run
evidence: ["v3-validation.md", "plan-v3-render.md"]
executed_at: not-run
blocking_reason: v3 尚未导入并运行
next_step: 导入 v3 后手动运行并截图反馈
---
case_id: RENDER-02
scenario: 白底、80vw、水平居中
input: 同上
version_browser: Automa 1.30.02；Chrome 具体版本待确认
expected: 内容区域白色，宽度约视口 80%，左右边距近似相等
actual: not-run
runtime_status: not-run
evidence: ["v3-validation.md"]
executed_at: not-run
blocking_reason: 尚无浏览器渲染反馈
next_step: 运行后观察计算样式或截图
---
case_id: RENDER-03
scenario: 页面附属内容隐藏
input: 同上
version_browser: Automa 1.30.02；Chrome 具体版本待确认
expected: calibreMeta、calibreToc、上下页导航等非正文内容不可见
actual: not-run
runtime_status: not-run
evidence: ["plan-v3-render.md"]
executed_at: not-run
blocking_reason: 尚无浏览器渲染反馈
next_step: 运行后截图确认
---
case_id: RENDER-04
scenario: 重复运行幂等
input: 在同一页面连续运行 v3 两次
version_browser: Automa 1.30.02；Chrome 具体版本待确认
expected: 只有一个 automa-calibre-reader-style-v3，布局不叠加
actual: not-run
runtime_status: not-run
evidence: ["v3-validation.md"]
executed_at: not-run
blocking_reason: 尚无重复运行反馈
next_step: 连续运行两次并检查页面
---
case_id: RENDER-05
scenario: 重载恢复
input: v3 运行后重新加载本地页面
version_browser: Automa 1.30.02；Chrome 具体版本待确认
expected: 原始 DOM/CSS 恢复，工作流没有修改磁盘文件
actual: not-run
runtime_status: not-run
evidence: ["plan-v3-render.md"]
executed_at: not-run
blocking_reason: 尚无重载反馈
next_step: 重载页面并截图确认
```
