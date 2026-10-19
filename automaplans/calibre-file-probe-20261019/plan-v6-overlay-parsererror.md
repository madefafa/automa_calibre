# Plan v6 - 全宽正文、Overlay 面板与 parsererror 隐藏

workflow_file: "workflow-v6-calibre-reader-overlay-fullwidth.automa.json"
workflow_version: "v6"
automa_version: "1.30.02"
source_asset: "workflow-v5-calibre-reader-panel-url-trigger.automa.json"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "reuse v5 contracts; runtime file:// trigger remains unverified"
status: awaiting-user-decision

## 用户反馈

1. 隐藏 `parsererror`。
2. `.calibreEbookContent` 与 `body` 一样宽，消除当前右侧大量空白。
3. 面板默认折叠，展开后 overlay 在 `.calibreEbookContent` 上方，不占正文横向空间。

用户截图显示：正文可见，但右侧有大块空白；右侧面板区域占据页面空间；顶部存在 `parsererror` 元素和 XHTML namespace 错误提示。

## v6 修改

### parsererror

在页面样式中加入：

```css
parsererror { display: none !important; }
```

只隐藏浏览器错误渲染节点，不删除原始 XHTML，也不伪造解析成功。若 `parsererror` 仍存在，Automa 日志不报告页面修复成功；用户应知道原始 XHTML 仍有解析错误。

### 正文全宽

移除 v5 的 `min(80vw, 1100px)` 和 `max-width: calc(100vw - 48px)`，改为：

```css
html, body, .calibreMain, .calibreEbookContent {
  width: 100% !important;
  max-width: none !important;
  min-width: 0 !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  box-sizing: border-box !important;
}
.calibreEbookContent {
  padding: 2rem 3rem !important;
  overflow-x: hidden !important;
}
```

正文与 body 同宽；图片、SVG、video、canvas 继续 `max-width: 100%`、`height: auto`，防止横向溢出。不得使用 `width: auto` 让大图突破容器。

### Overlay 面板

- 保留独立面板样式节点和内容风格样式节点。
- 面板 `position: fixed`，`top: 0; right: 0; width: 300px; height: 100vh;`，`z-index` 高于正文。
- 默认创建时 `hidden`，按钮文案为“显示面板”，`aria-expanded=false`。
- 展开时仅切换 `hidden`，不修改正文宽度、不添加 body padding、不改变 `.calibreEbookContent` 布局。
- 折叠按钮固定在右上角，面板隐藏时仍可见；按钮始终 overlay，不占正文空间。
- 面板内部依次保留：风格控制开关、calibreMeta 美化信息、上一页/下一节导航、目录。
- 风格控制开关默认 on；关闭只禁用内容风格 style，不禁用 panel style，不影响面板按钮。
- 运行前清理 v3/v4/v5 style、panel、toggle 节点，避免旧样式残留。

### URL 触发

沿用 v5：`visit-web` + `isUrlRegex=true` + `supportSPA=true`，匹配 `^file:///path/to/user/Calibre%20`。

- 该字段结构来源于已验证 HTTPS `visit-web` exemplar。
- `file://` 自动触发仍未获得 runtime 证据，v6 验收必须单独记录。

## 不变项

- 不使用 alert。
- 不修改本地 `序言.xhtml` 或其他书库文件。
- 不访问网络、不下载依赖。
- 保留 v1 到 v5 历史资产。

## 静态验收

- v6 使用 `drawflow.nodes` + `drawflow.edges`。
- Trigger 保留 v5 visit-web 结构。
- JavaScript 无 `window.alert`。
- CSS 包含 `parsererror { display: none !important; }`。
- CSS 不包含 `min(80vw, 1100px)` 或 `max-width: calc(100vw - 48px)`。
- 正文和 body 同宽规则存在；图片 `max-width: 100%` 存在。
- 面板初始 `hidden`、`aria-expanded=false`、position fixed、overlay，不设置正文右侧 padding。
- 节点/边/句柄/class/ID/可达性通过。

## 运行验收

- V6-01：页面顶部 parsererror 不可见；原始 XHTML 错误仍记录为页面事实。
- V6-02：正文横向占满 body，不再有 v5 的右侧大空白。
- V6-03：图片不超出正文，横向滚动条不出现。
- V6-04：面板默认折叠，正文宽度不变。
- V6-05：点击“显示面板”后面板覆盖正文，不推动正文、不改变正文宽度。
- V6-06：风格开关默认 on，关闭/开启只影响正文风格，不影响面板。
- V6-07：Meta、上一页/下一节、目录仍在面板中可用。
- V6-08：file:// URL 自动触发实际运行结果单独记录，不与页面脚本成功混为一谈。

## 状态

当前为 `awaiting-user-decision`。批准前不生成 v6 JSON。