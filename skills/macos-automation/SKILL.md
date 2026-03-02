---
name: macos-automation
description: 在 macOS 上执行 AppleScript/JXA 自动化任务。适用于应用控制、Finder/剪贴板、日历、邮件、消息、快捷指令、通知，以及需要 accessibility_query 的 UI 自动化场景。
---

# macOS Automation

这个 skill 用于把 macOS 自动化需求稳定落地为可执行流程，默认采用“先模板、后原始脚本”的策略，并提供权限预检、风险分级、AX 依赖兜底。

## 何时使用

在以下情况必须使用本 skill：

- 用户要求操作 macOS 应用（打开/退出 app、系统设置、Finder、Notes、Mail、Messages 等）。
- 用户要求执行 AppleScript 或 JXA。
- 任务涉及快捷指令（Shortcuts）或系统通知。
- 任务需要读取/操作界面元素，属于 accessibility（AX）自动化。

## 标准执行流程

### 1) 环境预检（先做）

```bash
python scripts/check_env.py --prewarm-ax
```

- 若 `automation_probe` 失败，先提示用户授权：系统设置 > 隐私与安全性 > 自动化/辅助功能。
- 若 `ax_binary` 失败，按返回 hint 处理（安装 ax 或配置下载地址）。

### 2) 模板优先（默认路径）

1. 列出模板：

```bash
python scripts/template_tool.py list --kb-path /path/to/knowledge-base
```

2. 搜索模板：

```bash
python scripts/template_tool.py search --kb-path /path/to/knowledge-base --query "shortcuts"
```

3. 渲染模板并输出脚本文件：

```bash
python scripts/template_tool.py render \
  --kb-path /path/to/knowledge-base \
  --template-id shortcuts_run_shortcut \
  --input-json '{"name":"启动闪念"}' \
  --include-shared-handlers \
  --output-script-file /tmp/run_shortcut.applescript
```

### 3) 执行脚本

- 执行渲染后的文件：

```bash
python scripts/run_macos_script.py --script-file /tmp/run_shortcut.applescript
```

- 直接执行原始脚本内容：

```bash
python scripts/run_macos_script.py \
  --language applescript \
  --script 'tell application "Finder" to get name of startup disk'
```

### 4) AX 查询（需要 UI 自动化时）

先确保 ax 可执行文件可用：

```bash
python scripts/ensure_ax.py
```

若找不到 ax，可配置自动下载：

```bash
MACOS_KIT_AX_AUTO_INSTALL=true \
MACOS_KIT_AX_DOWNLOAD_URL='https://example.com/ax/{platform}/{arch}/ax' \
python scripts/ensure_ax.py
```

## 安全与默认策略

- 默认 `safe_mode=balanced`：阻断关键危险命令（如 `rm -rf /`、`mkfs`、`shutdown -h`、`reboot`）。
- `strict`：在 `balanced` 基础上额外阻断 `curl | sh`，并拒绝二进制脚本文件。
- `off`：关闭风险扫描（仅在用户明确要求且风险可控时使用）。
- 默认不限制脚本路径；只有设置 `MACOS_KIT_ALLOWED_SCRIPT_ROOTS` 后才启用白名单限制。

遇到风险命中时：

1. 先向用户解释命中规则与风险。
2. 若用户坚持，建议改写为等价但更安全的命令。
3. 仅在用户明确授权后，才考虑降级到 `safe_mode=off`。

## 故障处理规则

- `PERMISSION_DENIED`：引导用户检查自动化/辅助功能授权。
- `EXECUTION_TIMEOUT`：缩小执行范围或提高超时（不超过 `MACOS_KIT_MAX_TIMEOUT_SECONDS`）。
- `DEPENDENCY_MISSING`（AX）：安装 ax 或配置下载地址模板。
- `SAFETY_BLOCKED`：优先改写脚本；不要静默绕过。

## 资源索引

- 配置说明：`references/config-matrix.md`
- 模板目录：`references/template-catalog.md`
- AX 策略：`references/ax-strategy.md`
- 可执行脚本：`scripts/check_env.py`、`scripts/template_tool.py`、`scripts/run_macos_script.py`、`scripts/ensure_ax.py`
