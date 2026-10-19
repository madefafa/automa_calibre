# 请求记录

workflow_file: "workflow-v1-calibre-file-probe.automa.json"
workflow_version: "v1"
automa_version: "1.30.02"
source_asset: "automa-interaction-01-09-javascript-code-basic"
status: awaiting-user-decision

## 原始请求

建立一个验证性 JSON：
1. 浏览器地址栏以 `file:///path/to/user/Calibre%20书库` 打头的文件链接。
2. 能否捕捉到 calibreMain 类元素。
3. 使用 alert 汇报。

## 已确认决策

用户确认：“先做最小验证：打开 Calibre 页面后手动运行；我可以开启 Automa 的文件网址访问权限。”本版本因此不验证地址访问自动触发。

## 验收标准

- 在用户先打开的 Calibre 本地页面上，由用户手动启动工作流。
- 只检查当前活动页 URL 是否以 `file:///path/to/user/Calibre%20书库` 开头，以及 `document.querySelector('.calibreMain')` 是否匹配到元素。
- 页面以一个 `alert` 同时报告 URL 前缀匹配结果、元素存在结果；报告还应包含安全截断后的当前 URL，不能读取或展示页面正文。
- 页面检查完成后工作流正常终止。
- 在 Automa 中可导入、节点识别正常；Chrome/Automa 版本和实际执行结果由用户反馈后记录。不得把静态结构检查等同于 file:// 实测通过。

## 范围与约束

- 页面 scope：本地 Calibre HTML 文件，地址栏 URL 前缀如上；具体文件路径随用户当前打开的页面变化。
- 浏览器：截图看似 Chrome，但浏览器名称/版本尚未由用户明确确认；正式验收按 Chrome 待确认记录。
- 权限：用户同意开启 Automa 的 `Allow access to file URLs`。此权限仅由用户在浏览器扩展管理界面授予。
- 不访问网络，不使用外部依赖，不读取文件系统，不修改网页 DOM，不做自动触发。
- alert 是有意阻塞的交互提示；用户关闭后执行流继续并结束。

## 请求目录与状态

- 碰撞检查通过：请求目录 `automaplans/calibre-file-probe-20261019/` 在创建前不存在。
- `MEMORY.md`、`PLAN.md`、`docs/SOP.md`：当前用户项目中未发现，按 unavailable 记录。
- 当前状态：awaiting-user-decision；等待用户批准方案 v1 后才能生成 JSON。

