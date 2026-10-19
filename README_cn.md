# Calibre Automa Reader

[English](README.md) | 简体中文

这是一个用于 Calibre 本地电子书 HTML 页面增强阅读体验的 Automa 工作流项目。最终发布版本会在匹配 Calibre 书库页面后，自动注入阅读布局、排版样式和可折叠控制面板。

> 当前最终工作流：`workflow-v10-calibre-reader-floating-ball-fixed.automa.json`
>
> Automa 基线：`1.30.02`
>
> 状态：静态检查通过；浏览器导入、页面运行和视觉效果仍需按本文步骤确认。

## 功能

工作流运行在当前活动的 Calibre `file://` 电子书页面上，主要完成以下工作：

- 将正文 `.calibreEbookContent` 设置为响应式、块级、居中的阅读区域。
- 在宽屏下限制正文最大宽度，避免正文被 Calibre 原始浮动布局挤到一侧。
- 在窄屏下自动适配视口宽度，并限制图片尺寸，减少横向溢出。
- 添加左侧垂直居中的圆形悬浮球。
- 点击悬浮球显示或隐藏阅读控制面板，默认保持折叠。
- 提供阅读相关控制，包括字体、字号、行高或主题等由工作流脚本维护的控制项。
- 清理本工作流旧版本注入的样式和控件，避免重复运行产生多个悬浮球或面板。
- 通过 URL Trigger 匹配 Calibre 书库路径，并使用 Active Tab 将操作绑定到当前页面。



## 工具说明

### Automa 插件

Automa 是浏览器自动化扩展，用于导入并运行 `.automa.json` 工作流。本项目的工作流基于 Automa `1.30.02` 的 `drawflow.nodes` 与 `drawflow.edges` 结构。

工作流包含三个主要节点：

```text
访问 Calibre file:// 页面
        |
        v
绑定当前活动标签页
        |
        v
注入阅读布局、样式和控制面板
```

### 路径补丁脚本

[`scripts/patch_calibre_library.py`](scripts/patch_calibre_library.py) 用于将工作流中原有的 Calibre 书库路径替换为本机路径。脚本会：

- 交互询问书库路径，或通过 `--library` 接收路径。
- 将本机路径转换为浏览器使用的 `file:///` URL 前缀。
- 同时更新 URL Trigger 和 JavaScript 中的路径检查前缀。
- 默认写入 `workflows/calibre-reader-v10-local.automa.json`，拒绝覆盖已有文件或原始发布模板。
- 使用正则匹配已知路径字段，并检查替换前后的命中数量。
- 写入后重新解析 JSON，发现结构损坏时直接失败。

## 主要特性

- **响应式正文**：宽屏最大约 `1100px`，正文左右自动留白；窄屏使用视口宽度。
- **正文居中修复**：显式使用 `display: block`、`float: none`、`clear: both` 和 `margin: 0 auto`，抵消书籍 CSS 对正文布局的影响。
- **悬浮球控制**：固定在左侧垂直居中位置，使用无可见文字的圆形图标，并提供 `aria-label`。
- **重复运行可恢复**：运行前删除本工作流历史版本产生的样式、面板和悬浮球节点。
- **无外部依赖**：不加载 CDN，不请求网络，不修改电子书源文件。
- **保留历史版本**：最终发布文件与迭代设计、验收和故障记录分离保存。

## 前驱准备

### 1. 安装 Calibre 软件

安装并启动 Calibre，确认电子书能够在 Calibre 的浏览器阅读界面中打开。需要能够看到电子书的本地 HTML/XHTML 页面，而不是只停留在 Calibre 书库管理界面。

### 2. 将电子书转换为 ZIP

本工作流处理的是 Calibre 生成的本地 HTML/XHTML 阅读页面。准备电子书时：

1. 在 Calibre 中选中目标电子书。
2. 使用 Calibre 的格式转换功能，生成可被 Calibre 阅读器展开的格式。
3. 如果原始材料是压缩包，确认 ZIP 内包含完整的 HTML/XHTML、图片和样式资源。
4. 不要把 ZIP 文件直接作为浏览器页面交给 Automa；应先由 Calibre 导入或转换，再打开实际的本地阅读页面。
5. 确认页面中存在 `.calibreEbookContent`，这是 v10 工作流的正文容器。

说明：ZIP 是资源交换和导入准备格式，不是工作流的直接运行输入。工作流不会修改 ZIP，也不会修改书库中的源文件。

### 3. 确认书库路径

打开目标电子书页面后，从浏览器地址栏确认其 URL 位于正确的 Calibre 书库目录下。路径可能包含中文，浏览器通常会将其编码为百分号形式，例如：

```text
file:///path/to/user/Calibre%20%E4%B9%A6%E5%BA%93/...
```

不要手工猜测编码后的路径。推荐使用路径补丁脚本生成工作流：

```bash
python3 scripts/patch_calibre_library.py \
  --input automaplans/calibre-file-probe-20261019/workflow-v10-calibre-reader-floating-ball-fixed.automa.json \
  --output workflows/calibre-reader-v10-local.automa.json
```

脚本会提示输入本地书库目录。也可以直接传入路径：

```bash
python3 scripts/patch_calibre_library.py \
  --library "/path/to/user/Calibre 书库" \
  --output workflows/calibre-reader-v10-local.automa.json
```

### 4. 授予 Automa 文件访问权限

在浏览器扩展管理页面打开 Automa 的 **Allow access to file URLs**。没有该权限时，工作流可能无法读取或注入本地 `file://` 页面。

### 5. 保持目标页面为当前活动标签页

首次测试时，先打开目标 Calibre 电子书页面，并确保它是当前活动标签页，再在 Automa 中导入并运行工作流。不要在空白页、扩展页面或其他非目标页面上测试。

## 使用流程

1. 安装并打开 Calibre。
2. 导入或转换电子书，确认能够打开本地 HTML/XHTML 阅读页。
3. 确认书库路径。
4. 使用路径补丁脚本生成本机专用工作流。
5. 打开 Automa，导入生成的 `.automa.json` 文件。
6. 检查工作流节点和 URL Trigger 配置。
7. 授予 Automa 文件网址访问权限。
8. 打开目标 Calibre 页面并保持活动。
9. 运行工作流。
10. 检查正文是否居中、悬浮球是否显示、面板是否能够展开和折叠。

## 导入文件

推荐导入由脚本生成的 `workflows/calibre-reader-v10-local.automa.json`（生成后才存在）：

- 发布模板：[`workflows/calibre-reader-v10.automa.json`](workflows/calibre-reader-v10.automa.json)
- 原始最终版：[`automaplans/calibre-file-probe-20261019/workflow-v10-calibre-reader-floating-ball-fixed.automa.json`](automaplans/calibre-file-probe-20261019/workflow-v10-calibre-reader-floating-ball-fixed.automa.json)

如果还没有按本机路径补丁，请先运行脚本。原始最终版中的路径是开发环境示例路径，不应直接视为所有机器都适用。

## 验证状态

v10 已完成静态验证：

- JSON 可解析。
- Automa `1.30.02` 元数据存在。
- 使用 `drawflow.nodes` 与 `drawflow.edges`。
- 节点 ID 唯一，边端点和 handles 一致。
- 三个节点可达。
- 悬浮球 DOM ID 与 CSS 选择器统一为 v10 ID。
- 正文块级居中、响应式宽度、面板默认折叠和图片居中规则保留。

详细记录：

- [`v10-validation.md`](automaplans/calibre-file-probe-20261019/v10-validation.md)
- [`acceptance-v10.md`](automaplans/calibre-file-probe-20261019/acceptance-v10.md)
- [`plan-v10-floating-ball-fix.md`](automaplans/calibre-file-probe-20261019/plan-v10-floating-ball-fix.md)

以下项目仍需在目标浏览器中实际确认：

- Automa 导入识别与参数保存后的重新导出。
- 悬浮球视觉效果和点击交互。
- 宽屏正文居中、窄屏适配和图片显示。
- `file://` URL Trigger 是否按预期自动触发。

静态检查通过不等于浏览器运行已验证。

## 目录结构

```text
.
├── README.md
├── scripts/
│   └── patch_calibre_library.py
├── workflows/
│   └── calibre-reader-v10.automa.json
├── automaplans/
│   └── calibre-file-probe-20261019/
│       ├── workflow-v1...v10*.automa.json
│       ├── plan*.md
│       ├── validation*.md
│       └── acceptance*.md
└── MEMORY.md
```

`automaplans/` 保存设计过程、历史版本和验收证据；`workflows/` 保存面向使用者的发布入口；`scripts/` 保存可重复执行的配置工具。

## 已知限制

- 当前工作流依赖 Calibre 页面 DOM 结构，页面结构变化后可能需要更新选择器。
- 本工作流不修改电子书原始文件、ZIP 文件或 Calibre 书库内容。
- URL Trigger 的 `file://` 自动触发需要在实际浏览器中验证；手动运行是首选排错方式。
- 不同浏览器对本地文件权限和扩展注入行为可能不同。
- 脚本只处理工作流内已知的书库路径字段，不会扫描或修改其他文件。

## 许可证

当前仓库未指定开源许可证。如需公开发布，请在确认授权范围后添加 `LICENSE` 文件。
