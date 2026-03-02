#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

from _shared import (
    PERMISSION_PATTERN,
    build_failure,
    build_success,
    clamp_timeout,
    is_binary_file,
    parse_bool,
    parse_csv_paths,
    print_json,
    run_osascript,
    scan_risk,
    validate_script_path_in_roots,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="执行 AppleScript/JXA 并应用安全策略")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--script", help="脚本内容")
    input_group.add_argument("--script-file", help="脚本文件路径")

    parser.add_argument(
        "--language",
        choices=["applescript", "javascript"],
        default="applescript",
        help="脚本语言",
    )
    parser.add_argument(
        "--arg",
        action="append",
        default=[],
        help="传给脚本的参数，可重复传入",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=None,
        help="执行超时时间（秒）",
    )
    parser.add_argument(
        "--safe-mode",
        choices=["strict", "balanced", "off"],
        default=os.getenv("MACOS_KIT_SAFE_MODE", "balanced"),
        help="风险策略档位",
    )
    parser.add_argument(
        "--allowed-script-roots",
        default=os.getenv("MACOS_KIT_ALLOWED_SCRIPT_ROOTS", ""),
        help="脚本路径白名单（逗号分隔）",
    )
    parser.add_argument(
        "--enable-raw-script",
        default=os.getenv("MACOS_KIT_ENABLE_RAW_SCRIPT", "true"),
        help="是否允许执行原始脚本（true/false）",
    )
    parser.add_argument(
        "--default-timeout-seconds",
        type=int,
        default=int(os.getenv("MACOS_KIT_DEFAULT_TIMEOUT_SECONDS", "30")),
        help="默认超时",
    )
    parser.add_argument(
        "--max-timeout-seconds",
        type=int,
        default=int(os.getenv("MACOS_KIT_MAX_TIMEOUT_SECONDS", "120")),
        help="最大超时",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not parse_bool(args.enable_raw_script, default=True):
        result = build_failure(
            "FEATURE_DISABLED",
            "run_macos_script 未开启",
            hint="设置 MACOS_KIT_ENABLE_RAW_SCRIPT=true 后重试",
            retryable=False,
        )
        print_json(result)
        return 1

    script_content = args.script
    script_file = args.script_file
    roots = parse_csv_paths(args.allowed_script_roots)

    if script_file:
        try:
            resolved_file = str(Path(script_file).expanduser().resolve())
        except Exception as error:
            result = build_failure(
                "INVALID_INPUT",
                "脚本路径不可读或不存在",
                hint=str(error),
                retryable=False,
            )
            print_json(result)
            return 1

        if roots and not validate_script_path_in_roots(resolved_file, roots):
            result = build_failure(
                "SAFETY_BLOCKED",
                "脚本路径不在白名单目录内",
                hint="请配置 MACOS_KIT_ALLOWED_SCRIPT_ROOTS 并确保脚本位于该目录",
                retryable=False,
            )
            print_json(result)
            return 1

        try:
            if args.safe_mode == "strict" and is_binary_file(resolved_file):
                result = build_failure(
                    "SAFETY_BLOCKED",
                    "安全模式不允许执行二进制脚本文件",
                    hint="请改用可读文本脚本，或将 MACOS_KIT_SAFE_MODE 设置为 off",
                    retryable=False,
                )
                print_json(result)
                return 1

            if script_content is None:
                script_content = Path(resolved_file).read_text(encoding="utf-8")
            script_file = resolved_file
        except Exception as error:
            result = build_failure(
                "INVALID_INPUT",
                "脚本路径不可读或不存在",
                hint=str(error),
                retryable=False,
            )
            print_json(result)
            return 1

    if args.safe_mode != "off" and script_content:
        hit_pattern = scan_risk(args.safe_mode, script_content)
        if hit_pattern:
            result = build_failure(
                "SAFETY_BLOCKED",
                "脚本命中高风险策略阻断",
                hint=f"命中规则: {hit_pattern}",
                retryable=False,
            )
            print_json(result)
            return 1

    timeout_seconds = clamp_timeout(
        args.timeout_seconds,
        default=max(1, args.default_timeout_seconds),
        maximum=max(1, args.max_timeout_seconds),
    )

    try:
        completed = run_osascript(
            language=args.language,
            timeout_seconds=timeout_seconds,
            script_content=script_content if args.script else None,
            script_path=script_file if args.script is None else None,
            args=args.arg,
        )
    except subprocess.TimeoutExpired:
        result = build_failure(
            "EXECUTION_TIMEOUT",
            "脚本执行超时",
            retryable=True,
        )
        print_json(result)
        return 1
    except Exception as error:
        result = build_failure(
            "EXECUTION_FAILED",
            str(error),
            retryable=True,
        )
        print_json(result)
        return 1

    stdout = (completed.stdout or "").strip()
    stderr = (completed.stderr or "").strip()

    if completed.returncode != 0:
        if PERMISSION_PATTERN.search(stderr):
            result = build_failure(
                "PERMISSION_DENIED",
                "macOS 自动化权限不足",
                hint="请检查 系统设置 > 隐私与安全性 > 自动化/辅助功能 权限",
                retryable=False,
            )
        else:
            result = build_failure(
                "EXECUTION_FAILED",
                stderr or "脚本执行失败",
                retryable=True,
            )
        print_json(result)
        return 1

    result = build_success(
        {
            "mode": "content" if args.script else "path",
            "language": args.language,
            "stdout": stdout,
            "stderr": stderr,
            "timeout_seconds": timeout_seconds,
        }
    )
    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
