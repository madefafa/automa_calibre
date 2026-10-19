# Decision v9

workflow_file: "workflow-v9-calibre-reader-responsive-fix.automa.json"
workflow_version: "v9"
automa_version: "1.30.02"
source_asset: "workflow-v8-calibre-reader-control-split.automa.json"
status: testing

- 用户批准生成 v9 并静态校验。
- v9 保留 v8，修复面板初始化、宽屏正文过宽和图片未居中。
- 静态检查通过：JSON/JS、schema、节点边、可达性、响应式规则、图片规则和独立控制均通过。
- 待运行：导入识别、file:// 自动触发、宽窄屏布局、图片居中、面板交互。
