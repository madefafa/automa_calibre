# Plan v9 - 响应式正文与默认折叠面板

workflow_file: "workflow-v9-calibre-reader-responsive-fix.automa.json"
workflow_version: "v9"
automa_version: "1.30.02"
source_asset: "workflow-v8-calibre-reader-control-split.automa.json"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "reuse v8 contracts; small rendering correction"
status: awaiting-user-decision

## 用户反馈

1. 面板需要初始化为自动折叠。
2. 宽屏时正文不能与 viewport 等宽，需要响应式阅读域。
3. 图片需要自动水平居中。

## v9 修改

### 面板初始化

- `panel.hidden = true`。
- `panelInput.checked = false`，显示面板开关与实际状态一致。
- 顶部无文字悬浮按钮仍显示，`aria-expanded=false`、`aria-label=显示面板`。
- 点击按钮或面板开关后 overlay 显示；不改变正文宽度，不设置 body padding/right compensation。
- 基础阅读、风格化阅读两个开关默认仍为开启。

### 响应式正文宽度

将 v8 的正文全宽规则改为：

```css
html, body, .calibreMain {
  width: 100% !important;
  max-width: none !important;
}
.calibreEbookContent {
  width: min(calc(100% - 32px), 1100px) !important;
  max-width: 1100px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  box-sizing: border-box !important;
  padding: 2rem clamp(1rem, 4vw, 3rem) !important;
}
@media (max-width: 720px) {
  .calibreEbookContent {
    width: calc(100% - 16px) !important;
    max-width: none !important;
    padding: 1rem !important;
  }
}
```

宽屏最大正文宽度 1100px，左右自动居中；窄屏保留 8px 两侧边距；面板为 fixed overlay，不影响该宽度计算。

### 图片水平居中

```css
.calibreEbookContent img,
.calibreEbookContent svg,
.calibreEbookContent video,
.calibreEbookContent canvas {
  display: block !important;
  max-width: 100% !important;
  width: auto !important;
  height: auto !important;
  margin-left: auto !important;
  margin-right: auto !important;
  object-fit: contain !important;
}
```

保留亮色 `pre/code`、三层独立 style、左侧无文字悬浮按钮、URL trigger 和无 alert。

## 静态验收

- v9 使用 `drawflow.nodes` + `drawflow.edges`。
- 无 alert，JS 语法通过。
- `panel.hidden=true`、`panelInput.checked=false`、`aria-expanded=false`。
- 正文包含 `min(calc(100% - 32px), 1100px)`、`max-width: 1100px`、auto margins 和移动端媒体查询。
- 图片规则包含 `max-width: 100%`、`height: auto`、左右 auto margin。
- v8 的三层控制、亮色代码块、parsererror 隐藏、overlay、节点边句柄和可达性保持。
- v8 保留为历史资产。

## 运行验收

- V9-01：首次运行后面板折叠，正文不被遮挡。
- V9-02：宽屏正文最大约 1100px 且居中，左右留白对称。
- V9-03：窄屏正文随 viewport 缩放，两侧留白约 8px，无横向滚动。
- V9-04：正文图片自动居中且不溢出。
- V9-05：显示面板开关和左侧悬浮按钮仍可打开/关闭 overlay。
- V9-06：基础阅读、风格化阅读和面板显示三个开关相互独立。

## 状态

当前为 `awaiting-user-decision`。批准前不生成 v9 JSON。