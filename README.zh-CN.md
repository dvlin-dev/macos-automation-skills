<p align="right">
  <a href="./README.md">English</a> | <strong>简体中文</strong>
</p>

# macos-automation-skills — 面向 macOS 自动化工作流的 Agent Skills 仓库

这是一个面向 macOS 自动化的 skills 仓库，遵循开放 skills 生态规范。

当前仓库包含一个可直接使用的技能：`macos-automation`，提供统一工具面、脚本执行引擎、模板知识库、AX 集成，以及机器可读输入 schema。

## 安装方式

### 方式 1：通过仓库安装

```bash
# 查看可安装技能
npx skills add dvlin-dev/macos-automation-skills --list

# 安装 macOS 自动化 skill
npx skills add dvlin-dev/macos-automation-skills --skill macos-automation
```

### 方式 2：手动复制

```bash
# Claude Code
cp -r skills/* ~/.claude/skills/

# Codex
cp -r skills/* ~/.codex/skills/

# 项目级安装
cp -r skills/* .agents/skills/
```

## 快速开始

```bash
cd skills/macos-automation

# 环境检测
python scripts/check_env.py --prewarm-ax

# 列出工具
python scripts/macos_automation.py list-tools

# 查看某个工具的输入 schema
python scripts/macos_automation.py describe-tool --tool run_macos_script

# 调用语义工具
python scripts/macos_automation.py call --tool get_frontmost_app --input-json '{}'

# 执行原始脚本
python scripts/macos_automation.py call \
  --tool run_macos_script \
  --input-json '{"script_content":"return \"ok\""}'
```

## 可用技能

| 技能 | 说明 | 主要触发场景 |
|------|------|-------------|
| [`macos-automation`](./skills/macos-automation/SKILL.md) | 端到端 macOS 自动化执行（模板 + 原始脚本 + AX） | AppleScript、JXA、Finder、Shortcuts、Notes、Mail、Messages、UI 自动化 |

## 能力范围

`macos-automation` 提供：

- 39 个可调用工具（核心工具 + 语义模板工具）
- 统一调度入口（`scripts/macos_automation.py`）
- 模板检索 / 渲染 / 执行流水线
- 原始 AppleScript/JXA 执行与安全分级（`strict` / `balanced` / `off`）
- AX 依赖预热与运行时自动安装兜底
- 面向客户端自动补全与参数校验的机器可读 schema

## 目录结构

```text
skills/
  macos-automation/
    SKILL.md
    agents/
    scripts/
    references/
    assets/
```

## 文档索引

- Skill 主说明：[`skills/macos-automation/SKILL.md`](./skills/macos-automation/SKILL.md)
- 工具能力面：[`skills/macos-automation/references/tool-surface.md`](./skills/macos-automation/references/tool-surface.md)
- 覆盖矩阵：[`skills/macos-automation/references/coverage-matrix.md`](./skills/macos-automation/references/coverage-matrix.md)
- 配置矩阵：[`skills/macos-automation/references/config-matrix.md`](./skills/macos-automation/references/config-matrix.md)
- AX 策略：[`skills/macos-automation/references/ax-strategy.md`](./skills/macos-automation/references/ax-strategy.md)
- 工具 schema 文档：[`skills/macos-automation/references/tool-schemas.md`](./skills/macos-automation/references/tool-schemas.md)
- 生成后的 schema JSON：[`skills/macos-automation/assets/tool-schemas.json`](./skills/macos-automation/assets/tool-schemas.json)
