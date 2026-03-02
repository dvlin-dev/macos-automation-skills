#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from _shared import build_failure, build_success, print_json, substitute_placeholders

CODE_BLOCK_PATTERN = re.compile(r"```(applescript|javascript)\s*\n([\s\S]*?)\n```", re.IGNORECASE)
FRONTMATTER_PATTERN = re.compile(r"^---\n([\s\S]*?)\n---\n", re.MULTILINE)


def parse_frontmatter(raw: str) -> dict[str, Any]:
    match = FRONTMATTER_PATTERN.match(raw)
    if not match:
        return {}

    result: dict[str, Any] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip('"\'') for item in value[1:-1].split(",")]
            result[key] = [item for item in items if item]
        else:
            result[key] = value.strip('"\'')
    return result


def parse_template_file(path: Path) -> dict[str, Any] | None:
    raw = path.read_text(encoding="utf-8")
    code_match = CODE_BLOCK_PATTERN.search(raw)
    if not code_match:
        return None

    frontmatter = parse_frontmatter(raw)
    script_language = code_match.group(1).strip().lower()
    script_content = code_match.group(2).strip()

    template_id = frontmatter.get("id")
    if not template_id:
        template_id = f"{path.parent.name}_{path.stem}".lower().replace("-", "_")

    return {
        "id": template_id,
        "title": frontmatter.get("title", template_id),
        "description": frontmatter.get("description", ""),
        "keywords": frontmatter.get("keywords", []),
        "arguments_prompt": frontmatter.get("argumentsPrompt", ""),
        "notes": frontmatter.get("notes", ""),
        "category": path.parent.name,
        "source_path": str(path),
        "language": script_language,
        "script": script_content,
    }


def load_shared_handlers(kb_root: Path, language: str) -> list[str]:
    handler_dir = kb_root / "_shared_handlers"
    if not handler_dir.exists() or not handler_dir.is_dir():
        return []

    extensions = {"applescript": ".applescript", "javascript": ".js"}
    target_ext = extensions[language]

    handlers: list[str] = []
    for path in sorted(handler_dir.iterdir()):
        if not path.is_file() or path.suffix != target_ext:
            continue
        handlers.append(path.read_text(encoding="utf-8").strip())
    return handlers


def load_templates(kb_root: Path) -> list[dict[str, Any]]:
    templates: list[dict[str, Any]] = []
    for category_dir in sorted(kb_root.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith("_"):
            continue
        for path in sorted(category_dir.glob("*.md")):
            if path.name.startswith("_"):
                continue
            parsed = parse_template_file(path)
            if parsed:
                templates.append(parsed)
    return templates


def get_kb_root(path_text: str | None) -> Path:
    if path_text:
        return Path(path_text).expanduser().resolve()
    return Path.cwd()


def list_templates(args: argparse.Namespace) -> dict[str, Any]:
    kb_root = get_kb_root(args.kb_path)
    if not kb_root.exists() or not kb_root.is_dir():
        return build_failure("INVALID_INPUT", f"知识库目录不存在: {kb_root}")

    templates = load_templates(kb_root)
    if args.category:
        templates = [item for item in templates if item["category"] == args.category]

    summaries = [
        {
            "id": item["id"],
            "title": item["title"],
            "category": item["category"],
            "description": item["description"],
            "language": item["language"],
            "keywords": item["keywords"],
        }
        for item in templates
    ]
    return build_success({"kb_path": str(kb_root), "count": len(summaries), "templates": summaries})


def search_templates(args: argparse.Namespace) -> dict[str, Any]:
    kb_root = get_kb_root(args.kb_path)
    if not kb_root.exists() or not kb_root.is_dir():
        return build_failure("INVALID_INPUT", f"知识库目录不存在: {kb_root}")

    query = args.query.strip().lower()
    if not query:
        return build_failure("INVALID_INPUT", "query 不能为空")

    templates = load_templates(kb_root)
    matched: list[dict[str, Any]] = []
    for item in templates:
        searchable = " ".join(
            [
                item["id"],
                item["title"],
                item["description"],
                item["category"],
                " ".join(item["keywords"] if isinstance(item["keywords"], list) else []),
            ]
        ).lower()
        if query in searchable:
            matched.append(item)

    return build_success(
        {
            "kb_path": str(kb_root),
            "query": args.query,
            "count": len(matched),
            "templates": [
                {
                    "id": item["id"],
                    "title": item["title"],
                    "category": item["category"],
                    "description": item["description"],
                    "language": item["language"],
                    "keywords": item["keywords"],
                }
                for item in matched
            ],
        }
    )


def render_template(args: argparse.Namespace) -> dict[str, Any]:
    kb_root = get_kb_root(args.kb_path)
    if not kb_root.exists() or not kb_root.is_dir():
        return build_failure("INVALID_INPUT", f"知识库目录不存在: {kb_root}")

    templates = load_templates(kb_root)
    target = next((item for item in templates if item["id"] == args.template_id), None)
    if not target:
        return build_failure("NOT_FOUND", f"模板不存在: {args.template_id}")

    input_data: dict[str, Any] = {}
    if args.input_json:
        try:
            parsed = json.loads(args.input_json)
        except json.JSONDecodeError as error:
            return build_failure("INVALID_INPUT", f"input_json 不是合法 JSON: {error}")
        if isinstance(parsed, dict):
            input_data = parsed
        else:
            return build_failure("INVALID_INPUT", "input_json 必须是 JSON 对象")

    script = target["script"]
    if args.include_shared_handlers:
        handlers = load_shared_handlers(kb_root, target["language"])
        if handlers:
            script = "\n\n".join([*handlers, script])

    rendered = substitute_placeholders(
        script=script,
        language=target["language"],
        input_data=input_data,
        args=args.arg,
    )

    payload = {
        "template": {
            "id": target["id"],
            "title": target["title"],
            "category": target["category"],
            "language": target["language"],
            "source_path": target["source_path"],
        },
        "rendered_script": rendered,
    }

    if args.output_script_file:
        output_path = Path(args.output_script_file).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        payload["output_script_file"] = str(output_path)

    return build_success(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="macos-kit 知识库模板工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="列出模板")
    list_parser.add_argument("--kb-path", default=None, help="知识库根目录")
    list_parser.add_argument("--category", default=None, help="按分类过滤")

    search_parser = subparsers.add_parser("search", help="搜索模板")
    search_parser.add_argument("--kb-path", default=None, help="知识库根目录")
    search_parser.add_argument("--query", required=True, help="关键词")

    render_parser = subparsers.add_parser("render", help="渲染模板并替换占位符")
    render_parser.add_argument("--kb-path", default=None, help="知识库根目录")
    render_parser.add_argument("--template-id", required=True, help="模板 ID")
    render_parser.add_argument("--input-json", default="{}", help="JSON 形式的输入参数")
    render_parser.add_argument("--arg", action="append", default=[], help="模板参数，可重复")
    render_parser.add_argument(
        "--include-shared-handlers",
        action="store_true",
        help="自动拼接 _shared_handlers 中同语言公共脚本",
    )
    render_parser.add_argument("--output-script-file", default=None, help="将渲染后的脚本写入文件")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        result = list_templates(args)
    elif args.command == "search":
        result = search_templates(args)
    elif args.command == "render":
        result = render_template(args)
    else:
        result = build_failure("INVALID_INPUT", f"不支持的命令: {args.command}")

    print_json(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
