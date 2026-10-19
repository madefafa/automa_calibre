# Plan v3 - Calibre 内容渲染

workflow_file: "workflow-v3-calibre-ebook-content-render.automa.json"
workflow_version: "v3"
automa_version: "1.30.02"
source_asset: "workflow-v2-calibre-file-probe-url-normalized.automa.json"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "reuse v2 contracts; change existing JavaScript code only"
status: awaiting-user-decision

## 目标

用户在当前已打开的 Calibre file:// 页面手动运行工作流后，仅显示 `.calibreEbookContent` 内容；其余页面内容隐藏；白色背景；内容区域宽度为视口 80%，水平自适应居中。

## 执行链

沿用 v2：`manual trigger -> active-tab -> javascript-code (website) -> natural end`。URL 中文路径规范化比较及 `.calibreMain` 验证保留在新脚本中，渲染前先验证当前 URL 与目标容器。

## 页面变更

- 目标：唯一的 `.calibreEbookContent`。若不存在或命中多个，alert 报错并不修改样式。
- 幂等性：查找固定 ID `automa-calibre-reader-style-v3`；存在时替换其 textContent，否则创建并添加一个 style 节点。重复运行不会累计 style 标签。
- 隐藏范围：`body > *` 默认隐藏；仅显示承载 `.calibreEbookContent` 的祖先链，以及 `.calibreEbookContent` 本身。`.calibreMain` 内导航、目录与元信息因此隐藏。
- 正文样式：白色背景、`width: 80vw`、`max-width: none`、水平居中、`min-height: 100vh`、`box-sizing: border-box`、必要内边距。
- 所有规则限定在已验证的目标页；不变更或清空书籍正文，不删除原节点、不改磁盘文件、不发网络请求。
- alert 报告 URL 前缀、容器命中数量、样式注入结果；Alert 关闭后调用 `automaNextBlock()`。

## 关键 CSS 意图

```css
body > * { display: none !important; }
body > .calibreMain { display: block !important; }
.calibreMain > * { display: none !important; }
.calibreMain > .calibreEbookContent { display: block !important; }
.calibreEbookContent {
  display: block !important;
  width: 80vw !important;
  max-width: none !important;
  min-height: 100vh;
  margin-left: auto !important;
  margin-right: auto !important;
  padding: 2rem 3rem;
  box-sizing: border-box;
  color: #111;
  background: #fff !important;
}
```

实际脚本需根据 `.calibreEbookContent` 是否直接位于 `.calibreMain` 下验证祖先显示链。为覆盖未知嵌套结构，生成时可用目标父链逐级建立专用 class 并纳入受限 CSS；不得使用 `body * { display:none }` 后只显示目标本身，以免祖先仍隐藏导致内容不可见。

## 风险与失败保护

- CSS 隐藏页面其它直接子节点是用户明确要求；导航/目录/元信息不可见属于预期效果。
- 页面缩放后 80vw 仍是视口相对宽度；小屏可能导致正文窄，应在实际页面观察，不擅自改变为固定像素。
- 如果 body 结构不符预期、目标缺失或数量不为 1，先 alert 报告，不注入样式。
- 使用 `try/catch`；错误提示限长，不伪称渲染成功。
- 此修订会改变当前页面视觉 DOM；重载页面可恢复原始 HTML/CSS，因为不改本地文件。

## 来源与契约

- 基于已验证 v2 完整工作流深拷贝；保留其顶层结构、Trigger、Active Tab、边及 URL 解码逻辑。
- 只修改 workflow name/description 与现有 JavaScript code 节点 ID/描述/代码，以及相应 edge target handle/id/class。
- 不新增 Automa block；无需新 block contract。
- v2 已收到运行截图：URL true、`.calibreMain` true、匹配数量 1；浏览器/版本、导入重导出和节点结束日志尚未反馈。
- 新行为渲染尚无 runtime 证据，必须由用户实际运行 v3 截图反馈。

## 验收

- RENDER-01：运行后只显示 `.calibreEbookContent` 及其祖先容器；书籍正文文本仍完整。
- RENDER-02：内容容器背景为白色，宽度约为视口 80%，左右边距自适应且近似相等。
- RENDER-03：页面其余内容（书名信息、上/下页、目录、开始导航）隐藏。
- RENDER-04：重复运行不新增重复 style 节点，布局保持一致。
- RENDER-05：重载本地页面后原始 DOM/CSS 恢复，确认未改文件。
- 未执行 case 必须在 acceptance 里记 `not-run`，直到用户反馈实际结果。

## 状态与审批

用户已提出渲染目标，但尚未明确批准创建新版本 JSON。当前状态 `awaiting-user-decision`；批准前不生成 v3 工作流 JSON。批准后由 Code 从 v2 深拷贝生成，静态校验后进入 testing。
