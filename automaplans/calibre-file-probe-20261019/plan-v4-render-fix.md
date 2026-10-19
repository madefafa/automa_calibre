# Plan v4 - Calibre 渲染修复

workflow_file: "workflow-v4-calibre-ebook-content-render-fixed.automa.json"
workflow_version: "v4"
automa_version: "1.30.02"
source_asset: "workflow-v3-calibre-ebook-content-render.automa.json"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "reuse v3 contracts; fix JavaScript rendering logic"
status: awaiting-user-decision

## 已确认问题

v3 在用户提供的静态页面上产生纯白空白区域。根因是通配 CSS：

```css
body > *:has(.calibreEbookContent) *:not(:has(.calibreEbookContent)):not(.calibreEbookContent) { display: none !important; }
```

该规则不仅隐藏目录/导航，也隐藏 `.calibreEbookContent` 内没有子节点的正文叶子节点，例如 `h1`、`p`、`span`，因此正文不可见。

## v4 变更

1. 删除所有 `window.alert(...)` 调用；工作流不再弹窗。
2. 保留 URL 解码检查和唯一 `.calibreEbookContent` 检查，但错误时通过 `throw new Error(...)` 让 Automa 节点日志记录失败，不弹窗。
3. 不再用祖先链通配规则隐藏正文后代。
4. 只隐藏页面明确的外围类：
   - `.calibreMeta`
   - `.calibreToc`
   - `.calibreEbNav`
   - `.calibreEbNavTop`
5. 设置纯白背景：`html, body, .calibreMain, .calibreEbookContent { background: #fff !important; }`；同时去除页面外层默认边距、保持内容容器水平居中。
6. 保留正文内容：`.calibreEbookContent * { display: revert !important; }` 不再使用，避免破坏原有 display；仅设置目标容器本身的显示、宽度和居中。
7. `.calibreMain` 和 `.calibreEbookContent` 设置 `display: block !important`，`.calibreEbookContent` 设置 `width: 80vw !important`、`margin-left/right: auto !important`、`box-sizing: border-box`、内边距和黑色文字。
8. 写入 v4 样式之前先移除由本工作流注入的 `style#automa-calibre-reader-style-v3`，否则旧 `!important` 通配隐藏规则可能在同一页面继续生效；再使用固定 style ID `automa-calibre-reader-style-v4`，重复执行时更新同一节点。不删除页面原有 stylesheet 或其他非本工作流样式。
9. 不修改 [`序言.xhtml`](序言.xhtml:1) 文件，不修改其他书库文件，不请求网络。

## 依据的页面结构

来自用户提供的 [`序言.xhtml`](序言.xhtml:18)：

```text
body
├── .calibreMeta
└── .calibreMain
    ├── .calibreEbookContent
    │   ├── .calibreEbNavTop
    │   └── 正文 h1 / p / span / sub
    ├── .calibreToc
    └── .calibreEbNav
```

## 预期脚本行为

```js
const rawUrl = window.location.href;
const normalizedUrl = decodeURIComponent(rawUrl);
const normalizedPrefix = decodeURIComponent('file:///path/to/user/Calibre%20书库');
const content = document.querySelector('.calibreEbookContent');
const contents = document.querySelectorAll('.calibreEbookContent');
if (!normalizedUrl.startsWith(normalizedPrefix)) throw new Error('URL prefix mismatch');
if (!content || contents.length !== 1) throw new Error('Expected exactly one .calibreEbookContent');
// create/update style#automa-calibre-reader-style-v4
// no alert
// automaNextBlock()
```

## 静态验收

- 保留 v3，v4 文件名不冲突。
- JSON 使用 Automa 1.30.02 的 `drawflow.nodes` + `drawflow.edges`。
- 3 节点、2 边、节点 ID 唯一、handles/class/id 一致、全链路可达。
- JavaScript 不包含 `window.alert`，包含 `automaNextBlock()`。
- JavaScript 不包含祖先通配隐藏正文的规则。
- JavaScript 包含四个外围隐藏选择器、`background: #fff`、`width: 80vw` 和 v4 style ID。
- 使用 [`序言.xhtml`](序言.xhtml:1) 的真实结构做 selector 静态检查。

## 运行验收

- V4-01：页面显示序言标题、作者和段落正文，不再空白。
- V4-02：`.calibreMeta`、`.calibreToc`、`.calibreEbNav`、`.calibreEbNavTop` 隐藏。
- V4-03：正文背景纯白，宽度约为视口 80%，水平居中。
- V4-04：页面没有 alert；工作流可自然结束。
- V4-05：重复运行只保留一个 v4 style 节点。
- V4-06：重载 [`序言.xhtml`](序言.xhtml:1) 后原始样式恢复，证明未写回文件。

## 状态

当前为 `awaiting-user-decision`。v3 已保留；v4 尚未生成。