#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from _shared import build_success, print_json
from tool_schemas import export_tool_schemas


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成机器可读工具 schema 清单")
    parser.add_argument("--kb-path", default=None, help="知识库目录（默认内置 assets/knowledge-base）")
    parser.add_argument(
        "--output-file",
        default=str(Path(__file__).resolve().parent.parent / "assets" / "tool-schemas.json"),
        help="输出文件路径",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = export_tool_schemas(kb_path=args.kb_path, output_path=args.output_file)
    print_json(
        build_success(
            {
                "output_file": str(Path(args.output_file).expanduser().resolve()),
                "tool_count": payload["tool_count"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
