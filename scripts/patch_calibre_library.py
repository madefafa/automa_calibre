#!/usr/bin/env python3
"""Patch the Calibre library URL in an Automa workflow JSON file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

DEFAULT_INPUT = Path(
    "automaplans/calibre-file-probe-20261019/"
    "workflow-v10-calibre-reader-floating-ball-fixed.automa.json"
)
DEFAULT_OUTPUT = Path("workflows/calibre-reader-v10-local.automa.json")
OLD_TRIGGER_PREFIX = "^file:///path/to/user/Calibre%20"
OLD_SCRIPT_PREFIX = "file:///path/to/user/Calibre%20书库"


def library_url_prefix(value: str) -> str:
    """Return a normalized file URL prefix for a local library directory."""
    raw = value.strip()
    if not raw:
        raise ValueError("书库路径不能为空")

    if raw.startswith("file://"):
        parsed = urlsplit(raw)
        if parsed.scheme != "file" or parsed.netloc not in ("", "localhost"):
            raise ValueError("只支持本机 file:// URL")
        path = unquote(parsed.path)
    else:
        path = raw

    path = path.replace("\\", "/")
    if not path.startswith("/"):
        raise ValueError("请提供绝对路径，例如 /path/to/user/Calibre Library")

    encoded_path = quote(path, safe="/:@-._~!$&'()*+,;=")
    return "file://" + encoded_path.rstrip("/")


def find_trigger_urls(workflow: dict) -> list[dict]:
    matches = []
    for node in workflow.get("drawflow", {}).get("nodes", []):
        for trigger in node.get("data", {}).get("triggers", []):
            data = trigger.get("data", {})
            if trigger.get("type") == "visit-web" and "url" in data:
                matches.append(data)
    return matches


def find_script_code(workflow: dict) -> list[dict]:
    return [
        node["data"]
        for node in workflow.get("drawflow", {}).get("nodes", [])
        if node.get("label") == "javascript-code"
        and isinstance(node.get("data", {}).get("code"), str)
    ]


def patch_workflow(workflow: dict, prefix: str) -> tuple[int, int]:
    triggers = find_trigger_urls(workflow)
    scripts = find_script_code(workflow)
    if not triggers:
        raise ValueError("未找到 visit-web Trigger 的 URL 字段")
    if not scripts:
        raise ValueError("未找到 javascript-code 节点")

    trigger_count = 0
    for data in triggers:
        current = data["url"]
        pattern = re.compile(r"^\^?file:///[^\s*]+")
        if not pattern.match(current):
            raise ValueError(f"无法识别 Trigger URL 路径模式：{current!r}")
        anchor = "^" if current.startswith("^") else ""
        data["url"] = anchor + prefix + re.sub(
            r"^\^?file:///[^\s*]+", "", current, count=1
        )
        trigger_count += 1

    script_count = 0
    for data in scripts:
        code = data["code"]
        # Locate the URL literal in the normalizedPrefix declaration only.
        declaration = re.search(r"const\s+normalizedPrefix\s*=\s*decodeURIComponent\(", code)
        if declaration is None:
            raise ValueError("JavaScript 中未找到 normalizedPrefix 声明")
        pattern = re.compile(
            r"(?<=decodeURIComponent\()['\"](file:///[^'\"]+)['\"](?=\))"
        )
        matches = list(pattern.finditer(code, declaration.end()))
        target = [m for m in matches if code.count("\n", 0, m.start()) == code.count("\n", 0, declaration.start())]
        if len(target) != 1:
            raise ValueError(
                "每个 JavaScript 节点必须恰好有一个 Calibre URL 前缀字面量；"
                f"实际找到 {len(target)} 个"
            )
        match = target[0]
        replacement = prefix.replace(" ", "%20")
        code = code[: match.start(1)] + replacement + code[match.end(1) :]
        data["code"] = code
        script_count += 1

    return trigger_count, script_count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="询问 Calibre 书库路径，并更新 Automa 工作流中的 URL 匹配前缀。"
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="源工作流 JSON")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="输出工作流 JSON")
    parser.add_argument("--library", help="绝对书库路径或本机 file:// URL；省略时交互询问")
    args = parser.parse_args()

    try:
        library = args.library or input("请输入 Calibre 书库绝对路径: ")
        prefix = library_url_prefix(library)
        if not args.input.is_file():
            raise ValueError(f"找不到输入工作流：{args.input}")
        if args.input.resolve() == args.output.resolve():
            raise ValueError("输入与输出不能相同；为保留原始工作流，请使用新输出路径")
        if args.output.exists():
            raise ValueError(f"输出文件已存在，拒绝覆盖：{args.output}")

        workflow = json.loads(args.input.read_text(encoding="utf-8"))
        trigger_count, script_count = patch_workflow(workflow, prefix)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(workflow, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        # Validate the exact bytes written to disk.
        json.loads(args.output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1

    print(f"书库 URL 前缀：{prefix}")
    print(f"已更新 Trigger URL：{trigger_count} 处")
    print(f"已更新 JavaScript 前缀：{script_count} 处")
    print(f"工作流已写入：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
