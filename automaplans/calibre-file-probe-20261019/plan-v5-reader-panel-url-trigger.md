# Plan v5 - 阅读布局、侧栏面板与 URL 触发

workflow_file: "workflow-v5-calibre-reader-panel-url-trigger.automa.json"
workflow_version: "v5"
automa_version: "1.30.02"
source_asset: "workflow-v4-calibre-ebook-content-render-fixed.automa.json + automa-trigger-007-visit-web-baidu-alert"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "visit-web exemplar reviewed; file:// runtime remains unverified"
status: approved

## 用户目标

在 Calibre 本地 XHTML 页面中：

1. 修复正文真正水平居中。
2. 防止图片溢出正文区域。
3. 创建附着浏览器侧边的可显隐面板，从上到下包含：
   - 风格控制开关，默认 on；
   - `calibreMeta` 美化信息；
   - 上一页、下一节导航；
   - 目录。
4. 不再使用 alert。
5. Trigger 从手动改为 URL 匹配激活。

## 版本保留

- 保留 v1、v2、v3、v4，不覆盖历史资产。
- v5 从 v4 深拷贝；只修改 Trigger 配置、JavaScript 节点代码、工作流名称/描述及受影响的 edge 标识。

## 计划执行链

```text
visit-web trigger -> active-tab -> javascript-code website -> natural end
```

### Trigger

- `data.type` 与触发项字段必须从当前 1.30.02 `visit-web` exemplar 复制。
- URL pattern 目标为 `file:///path/to/user/Calibre%20书库/*` 或等价的 file URL 匹配表达式，具体是否允许该格式必须在生成前按 exemplar/源码合同确认。
- 目标触发行为是访问/切换到 Calibre 本地 XHTML 页面时激活，不是用户手动点击 Execute。
- 现有 `trigger/007-visit-web-baidu-alert.json` 已验证 HTTPS URL 触发，但未验证 `file://` URL 触发；v5 只能标记为待 runtime 验证。

## 页面脚本设计

### 1. 运行前清理

移除本工作流历史 style/panel 节点：

- `style#automa-calibre-reader-style-v3`
- `style#automa-calibre-reader-style-v4`
- `style#automa-calibre-reader-style-v5`
- `aside#automa-calibre-reader-panel-v5`
- `button#automa-calibre-reader-toggle-v5`

不删除页面原有 DOM，不写回 `序言.xhtml`。

### 2. 目标检测

- 解码比较 `window.location.href` 与 `file:///path/to/user/Calibre%20书库` 前缀。
- 必须存在且唯一 `.calibreEbookContent`。
- 缺失时抛错到 Automa 日志，不弹窗。

### 3. 正文布局

推荐样式约束：

```css
html, body {
  width: 100% !important;
  min-width: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  background: #fff !important;
  overflow-x: hidden !important;
}
.calibreMain {
  width: 100% !important;
  margin: 0 auto !important;
  background: #fff !important;
}
.calibreEbookContent {
  width: min(80vw, 1100px) !important;
  max-width: calc(100vw - 48px) !important;
  margin-left: auto !important;
  margin-right: auto !important;
  box-sizing: border-box !important;
  background: #fff !important;
  overflow-wrap: anywhere !important;
}
.calibreEbookContent img,
.calibreEbookContent svg,
.calibreEbookContent video,
.calibreEbookContent canvas {
  display: block !important;
  max-width: 100% !important;
  width: auto !important;
  height: auto !important;
  object-fit: contain !important;
}
```

不能对正文叶子节点使用 `display:none`；只能隐藏明确外围元素。

### 4. 侧边面板

由 JavaScript 创建 fixed side panel，默认贴右侧，使用独立 ID 和 shadow-like class names，避免与书籍样式冲突：

- toggle：固定在面板左侧或右侧，点击切换 panel `display`/`transform`；默认 panel 显示，风格开关默认 on。
- 风格开关：checkbox/switch；on 时启用正文宽度、白底、图片约束和外围隐藏；off 时移除 v5 style 并恢复原始页面样式，但保留面板。
- `calibreMeta`：从原页面读取 `.calibreMetaTitle` 与 `.calibreMetaAuthor` 的文本，显示到面板的美化信息区；不移动原节点，不重复显示原始 meta。
- 导航：读取 `.calibreEbNavTop a.calibreAPrev` 与 `.calibreEbNavTop a.calibreANext` 的 href/text；按钮点击使用原链接导航。若缺少链接，按钮禁用。
- 目录：从 `.calibreToc` 复制目录链接与文本到面板；点击使用原 href；不把原 `.calibreToc` 节点移动到面板。
- 面板自身必须固定宽度、可滚动、z-index 足够高、与正文不产生横向溢出。
- 面板内文本需使用 `textContent`，不直接拼接未经处理的 HTML。

### 5. 可见性规则

- 风格 on：隐藏 `.calibreMeta`、`.calibreToc`、`.calibreEbNav`、`.calibreEbNavTop`，显示正文。
- 风格 off：移除 v5 style，使原始页面样式恢复；面板仍可通过 toggle 操作。
- 面板 toggle 只控制面板，不影响书籍正文。
- 不使用 alert；成功状态通过页面视觉结果体现，错误通过 Automa 节点日志。

## 关键风险

1. `visit-web` 对 `file://` 的触发匹配未在知识包中运行验证；这是 v5 的关键 runtime 风险。若浏览器不触发，需保留 v5 并回退为手动 Trigger 或改为用户手动执行。
2. 侧栏导航跨文件点击后会加载下一 XHTML；URL trigger 是否会再次激活、旧页面 style/panel 是否随页面卸载，需运行验证。
3. 风格 off 的“恢复原状”只能移除本工作流注入的 style，不应覆盖页面原有 CSS。
4. 目录链接可能为相对路径；必须保留原始 `href`，不要自行拼接绝对路径。
5. `:has()` 不再用于隐藏正文，避免 v3 空白问题。

## 静态验收

- v5 使用 `drawflow.nodes` + `drawflow.edges`。
- Trigger 为已验证 exemplar 的 visit-web 结构；不猜字段。
- 无 `window.alert`。
- JavaScript 包含正文居中、图片 max-width、面板 ID、switch default on、meta/nav/toc 读取、panel toggle、style toggle。
- 节点、边、句柄、class、ID、可达性和几何布局通过检查。
- 通过 [`序言.xhtml`](../../序言.xhtml:18) 的 `.calibreMeta`、`.calibreMain`、`.calibreEbookContent`、`.calibreToc`、`.calibreEbNav`、`.calibreEbNavTop` 结构静态对照。

## 运行验收

- V5-01：访问匹配的 `file://` 页面时 Trigger 自动激活。
- V5-02：正文真正居中，左右空间基本对称。
- V5-03：图片不超过正文容器宽度，横向滚动条不出现。
- V5-04：右侧面板默认显示，风格开关默认 on。
- V5-05：关闭风格开关后正文样式恢复，重新打开后样式再次生效。
- V5-06：面板显示 meta、上一页/下一节和目录；链接可用。
- V5-07：面板 toggle 可显隐，不影响正文。
- V5-08：导航到下一 XHTML 后 URL trigger 与面板行为符合预期。

## 状态

当前为 `awaiting-user-decision`。批准前不生成 v5 JSON。