# 预检记录

workflow_file: "automaplans/calibre-file-probe-20261019/workflow-v1-calibre-file-probe.automa.json"
workflow_version: "v1"
automa_version: "1.30.02"
source_asset: "automa-trigger-007-visit-web-baidu-alert"
status: draft

- 请求 ID 碰撞检查：工作区初始仅有 `.DS_Store`，不存在 `automaplans/calibre-file-probe-20261019/`；项目根 `MEMORY.md`、`PLAN.md`、`docs/SOP.md` 均未见，分别记为 unavailable。
- 根：user-project-root = 当前项目；knowledge-root = Automa skill 知识包（独立根）。跨根材料仅记录稳定 ID、版本和摘要，不记机器绝对路径。
- 用户原始诉求：建立验证性 Automa JSON；浏览器地址栏以 `file:///path/to/user/Calibre%20书库` 开头，检测 `.calibreMain`，用 alert 汇报。截图为 Chrome 风格浏览器页面及开发者工具中 `div.calibreMain`，说明图片展示的页面包含该元素，不证明扩展注入已成功；浏览器实际版本未知。
- evidence：documentation=confirmed（Trigger、JavaScript 页面执行文档）；source=partial（manifest 定义了 `<all_urls>` 与 `file://*/*` Web accessible resources，但尚不能由此证明已授权或注入成功）；json=confirmed（1.30.02 当前结构示例及节点配置）；runtime=unavailable（仅有百度 URL 的 visit-web + alert 样本成功、本地文件场景未测）；feedback=partial（用户截图显示 DOM，但非本工作流运行反馈）；freshness=unknown。page_scope=file:// 本地 Calibre 页面，permissions=Automa 允许访问文件网址，实际是否授予未知。
- 知识根事实：根 `index.md` 和 `troubleshooting.md` 已读。当前契约为 `drawflow.nodes` / `drawflow.edges`；手动 Trigger 不得显式写入空 `triggers`；边使用精确 source/target handles。材料 ID `automa-trigger-007-visit-web-baidu-alert`（版本 1.30.02，索引标记已导入实测）：访问 HTTPS 百度时 `trigger -> javascript-code` 弹窗成功；`automa-trigger-001-manual`（版本 1.30.02，已导入实测）手动触发成功；`automa-interaction-01-09-javascript-code-basic`（版本 1.30.02，索引标记已实测）页面 JS + alert + workflow-state 成功。完整 exemplar 已阅读，但均未针对 file:// 测试。
- 可行性判断：页面存在 `.calibreMain` 有图片线索；以 `window.location.href.startsWith` 严格检查前缀、用 `document.querySelector('.calibreMain')` 检查存在性并将 URL 是否匹配/元素是否存在分别用 alert 汇报是推荐逻辑。空白页面或无权限必须报告为运行错误/未执行，不可误报元素不存在。脚本 alert 关闭后才继续执行。
- 建议选项 A：访问匹配地址自动触发，使用 visit-web Trigger + website JavaScript code；缺点是 `file://` URL 是否被 Automa 的匹配/注入链路接受未验证，需浏览器实测。
- 备选 B：用户先打开目标页并手动执行 Trigger + website JavaScript code；可减少文件 URL 触发匹配的不确定性，仍需文件网址访问权限。B 不能证明“访问时自动触发”。
- 不建议以 Notification 代替网页 `alert`；不下载外部依赖，不访问本地文件内容，不使用 HTTP Request，也不创建纯诊断块。
- 未解决的关键用户决策：选择 A 或 B；是否能在浏览器扩展管理页给 Automa 开启 Allow access to file URLs。推荐选择 B 做最小验证，若需证明地址栏访问自动触发再选择 A。
- recommendation: awaiting-user-input。用户确定后进入知识合同整理及计划审批；本阶段禁止生成 workflow.json、禁止宣称 file:// 已验证。
