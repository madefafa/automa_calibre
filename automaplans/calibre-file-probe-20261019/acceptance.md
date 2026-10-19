# Acceptance v1/v2

## CAL-01 / v1 execution record

```yaml
case_id: CAL-01
scenario: 本地 Calibre 页面 URL 与 calibreMain 元素检测（v1）
input: 用户打开目标 file:// 页面并手动触发 v1
version_browser: Automa 1.30.02；Chrome 具体版本未提供
expected: URL 前缀 true；.calibreMain 存在 true；数量 >= 1
actual: URL 前缀 false；.calibreMain 存在 true；匹配数量 1；alert 成功显示
runtime_status: warning
evidence: ["feedback.md", "troubleshooting.md"]
executed_at: 2026-10-19T01:42:21Z
blocking_reason: v1 URL 比较逻辑不兼容中文路径的百分号编码
next_step: 使用 v2 重新导入并运行
```

## CAL-02 / not-run

```yaml
case_id: CAL-02
scenario: 非目标 URL 负向检查
input: 非目标 file/http 页面
version_browser: Automa 1.30.02；Chrome 具体版本未提供
expected: URL 前缀 false，元素结果独立报告
actual: not-run
runtime_status: not-run
evidence: ["plan.md"]
executed_at: not-run
blocking_reason: 当前优先修复 v1 URL 编码问题，v2 尚未完成导入运行
next_step: v2 正常场景通过后运行边界场景
```

## CAL-03 / not-run

```yaml
case_id: CAL-03
scenario: 文件网址访问权限缺失的预期失败
input: 关闭 Automa Allow access to file URLs 后运行
version_browser: Automa 1.30.02；Chrome 具体版本未提供
expected: 权限/注入错误由日志识别，不误报元素不存在
actual: not-run
runtime_status: not-run
evidence: ["block-contracts.md", "troubleshooting.md"]
executed_at: not-run
blocking_reason: 暂未执行权限负向测试
next_step: 正常 v2 运行完成后再决定是否执行负向测试
```

## CAL-04 / v2 import and runtime

```yaml
case_id: CAL-04
scenario: v2 导入识别、参数往返及目标页运行
input: workflow-v2-calibre-file-probe-url-normalized.automa.json
version_browser: Automa 1.30.02；Chrome 具体版本未提供
expected: 节点识别正常；URL 前缀 true；.calibreMain true；数量 1；流程结束
actual: not-run
runtime_status: not-run
evidence: ["v2-validation.md", "workflow-v2-calibre-file-probe-url-normalized.automa.json"]
executed_at: not-run
blocking_reason: v2 已静态通过，但尚未收到重新导入和运行反馈
next_step: 导入 v2，保持文件网址权限，手动运行并返回 alert/日志结果
```
