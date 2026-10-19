# Plan v10 - 悬浮球绑定修复

workflow_file: "workflow-v10-calibre-reader-floating-ball-fixed.automa.json"
workflow_version: "v10"
automa_version: "1.30.02"
source_asset: "workflow-v9-calibre-reader-responsive-fix.automa.json"
status: awaiting-user-decision

## 问题

v9 清理了旧 toggle 节点并创建了 v8/v9 版本，但按钮 CSS 选择器未完整迁移到 v9 ID，导致按钮节点退化为浏览器默认小胶囊，悬浮球视觉丢失。

## 修复

- v10 从 v9 深拷贝，不覆盖 v9。
- 统一所有 toggle CSS、伪元素、hover、active、focus 选择器为 `#automa-calibre-reader-toggle-v10`。
- 统一按钮 DOM ID 为 `automa-calibre-reader-toggle-v10`。
- 运行前清理 v3-v9 旧 toggle/panel/style 节点。
- 保持左侧 `position: fixed`、垂直居中、40px 圆形、半透明背景、渐变 hover、阴影、无可见文字、aria-label。
- 保持 v9 的默认折叠面板、1100px 响应式正文和图片居中。
- 不改变三个开关、亮色代码块、URL trigger、无 alert。

## 静态验收

- CSS 不含 `toggle-v8` 或 `toggle-v9` 的旧选择器。
- CSS 同时包含 v10 toggle ID、`::before`、`content: '☰'`、left/top/transform、hover/active/focus。
- DOM ID 与 CSS ID 一致。
- v9 的 panel hidden、responsive width、image centered 规则保留。
- JSON/JS/schema/edge/handle/可达性通过。

## 运行验收

- V10-01：左侧悬浮球可见且为圆形图标，无文字。
- V10-02：点击悬浮球显示 overlay 面板，再次点击隐藏。
- V10-03：面板初始折叠，正文宽度和图片布局不受影响。
