<p align="left">
  <strong>English</strong> | <a href="./README.zh-CN.md">简体中文</a>
</p>

# macos-automation-skills — agent skills for macOS automation workflows

A skills repository for macOS automation, built for the open skills ecosystem.

This repo currently ships one production-ready skill: `macos-automation`, with a unified tool surface, script execution engine, template knowledge base, AX integration, and machine-readable input schemas.

## Installation

### Option 1: Install from repository

```bash
# list installable skills
npx skills add dvlin-dev/macos-automation-skills --list

# install the macOS automation skill
npx skills add dvlin-dev/macos-automation-skills --skill macos-automation
```

### Option 2: Copy manually

```bash
# Claude Code
cp -r skills/* ~/.claude/skills/

# Codex
cp -r skills/* ~/.codex/skills/

# Project-level
cp -r skills/* .agents/skills/
```

## Quick Start

```bash
cd skills/macos-automation

# environment check
python scripts/check_env.py --prewarm-ax

# list tools
python scripts/macos_automation.py list-tools

# inspect input schema for one tool
python scripts/macos_automation.py describe-tool --tool run_macos_script

# call a semantic tool
python scripts/macos_automation.py call --tool get_frontmost_app --input-json '{}'

# run raw script
python scripts/macos_automation.py call \
  --tool run_macos_script \
  --input-json '{"script_content":"return \"ok\""}'
```

## Available Skills

| Skill | Description | Main Triggers |
|-------|-------------|---------------|
| [`macos-automation`](./skills/macos-automation/SKILL.md) | End-to-end macOS automation execution with templates + raw scripts + AX | AppleScript, JXA, Finder, Shortcuts, Notes, Mail, Messages, UI automation |

## Capability Surface

`macos-automation` provides:

- 39 callable tools (core + semantic template tools)
- Unified dispatcher (`scripts/macos_automation.py`)
- Template search / render / execute pipeline
- Raw AppleScript/JXA execution with safety modes (`strict` / `balanced` / `off`)
- AX dependency prewarm + runtime fallback installation
- Machine-readable schema catalog for client autocomplete and validation

## Repository Layout

```text
skills/
  macos-automation/
    SKILL.md
    agents/
    scripts/
    references/
    assets/
```

## Documentation

- Skill instructions: [`skills/macos-automation/SKILL.md`](./skills/macos-automation/SKILL.md)
- Tool surface: [`skills/macos-automation/references/tool-surface.md`](./skills/macos-automation/references/tool-surface.md)
- Coverage matrix: [`skills/macos-automation/references/coverage-matrix.md`](./skills/macos-automation/references/coverage-matrix.md)
- Config matrix: [`skills/macos-automation/references/config-matrix.md`](./skills/macos-automation/references/config-matrix.md)
- AX strategy: [`skills/macos-automation/references/ax-strategy.md`](./skills/macos-automation/references/ax-strategy.md)
- Tool schema docs: [`skills/macos-automation/references/tool-schemas.md`](./skills/macos-automation/references/tool-schemas.md)
- Generated schema JSON: [`skills/macos-automation/assets/tool-schemas.json`](./skills/macos-automation/assets/tool-schemas.json)
