# Decision

workflow_file: "workflow-v2-calibre-file-probe-url-normalized.automa.json"
workflow_version: "v2"
automa_version: "1.30.02"
source_asset: "automa-trigger-001-manual + automa-browser-001-tab-navigation-alert + automa-interaction-01-09-javascript-code-basic"
status: testing

- v1 审批：用户批准生成并静态校验 v1。
- v1 运行反馈：`.calibreMain` 命中 1 个；页面脚本和 alert 成功；URL 前缀因中文目录百分号编码不匹配。
- 修订原因：v1 `startsWith` 仅将空格写成 `%20`，没有对中文目录部分统一规范化。
- 修订动作：保留 v1；生成 v2 `workflow-v2-calibre-file-probe-url-normalized.automa.json`，仅修复 URL 比较规范化。
- v2 静态校验：通过；3 节点、2 边、全链路可达、句柄一致。
- 当前状态：repaired -> testing；不得直接声明 verified。
- 待完成：v2 导入识别、重新导出往返、同一 file:// Calibre 页面运行反馈。
