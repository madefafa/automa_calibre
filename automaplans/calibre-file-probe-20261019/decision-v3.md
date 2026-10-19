# Decision v3

workflow_file: "workflow-v3-calibre-ebook-content-render.automa.json"
workflow_version: "v3"
automa_version: "1.30.02"
source_asset: "workflow-v2-calibre-file-probe-url-normalized.automa.json"
status: testing

- 用户批准：生成 v3 渲染工作流并静态校验。
- 生成：从 v2 深拷贝，保留 v1/v2 历史文件。
- 静态校验：通过；3 节点、2 边、全链路可达、句柄一致、schema family 正确、无外部依赖。
- 渲染行为：当前页注入幂等 style；仅保留 `.calibreEbookContent` 祖先链；白底、80vw、居中、min-height 100vh；不写回书籍文件。
- 当前状态：generated -> static-validated -> testing。
- 待完成：Automa 导入识别与 RENDER-01 至 RENDER-05 的浏览器反馈；不得将静态通过声明为渲染已验证。
