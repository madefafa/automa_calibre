# Validation v6

workflow_file: "workflow-v6-calibre-reader-overlay-fullwidth.automa.json"
workflow_version: "v6"
automa_version: "1.30.02"
source_asset: "workflow-v5-calibre-reader-panel-url-trigger.automa.json + automa-trigger-007-visit-web-baidu-alert"
source_asset_version: "1.30.02"
schema_family: "drawflow.nodes + drawflow.edges"
contract_status: "pass; file URL trigger runtime unverified"
status: testing

## 静态检查

| 检查 | 结果 |
|---|---|
| JSON parse | pass |
| Automa version metadata | pass |
| native schema `drawflow.nodes` / `drawflow.edges` | pass |
| node IDs unique | pass |
| edge endpoint/handles/id/class | pass |
| reachable nodes | pass；3/3 |
| non-negative geometry | pass |
| `parsererror` hidden by CSS | pass |
| body/main/content width 100% | pass；v5 `80vw` cap removed |
| image/SVG/video/canvas max-width | pass；100%，height auto |
| panel default hidden | pass；`panel.hidden=true`, toggle text `显示面板`, aria-expanded=false |
| panel overlay | pass；fixed positioning; no body/content width compensation |
| panel/content styles independent | pass；style toggle only disables content style |
| alert | none |
| URL pattern | static match prefix `^file:///path/to/user/Calibre%20` |
| JavaScript syntax | not-run by dedicated JS parser; JSON/script token checks pass |
| XHTML structure | pass against workspace `序言.xhtml` classes |
| Automa import recognition | not-run |
| file:// automatic trigger runtime | not-run; risk remains |

## Generation record

- copied_fields: v5 complete top-level shape, settings/globalData, trigger family, Active Tab node, JavaScript node parameter shape, native edges.
- request_specific_fields: v6 workflow name/description, JavaScript node ID/description/code, affected edge target id/handle/class.
- schema-risk: none observed.
- unresolved_conflicts: `visit-web` HTTPS behavior is verified in knowledge package; `file://` matching and activation remain runtime-unverified.

## Runtime test order

1. Import v6 and confirm visit-web trigger configuration/editor round-trip.
2. Open the target Calibre file URL and determine whether visit-web triggers automatically.
3. If it triggers, confirm `parsererror` hidden,正文全宽、图像无溢出、面板默认折叠。
4. Open panel: verify overlay does not change content width; close panel again.
5. Toggle style off/on and confirm panel remains operable.
6. Report browser/version, whether URL trigger fired, screenshots, and any Automa node error.
