# macos-automation-skills

按 `vercel-labs/skills` 生态约定组织的技能仓库，当前包含 1 个技能：`macos-automation`。

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

## 安装方式

```bash
# 列出本仓库可安装的 skills
npx skills add dvlin-dev/macos-automation-skills --list

# 安装指定 skill
npx skills add dvlin-dev/macos-automation-skills --skill macos-automation
```

## 技能说明

- `macos-automation`
  - 完整覆盖 macOS 自动化工具面（39 个工具名入口）
  - 统一调度入口：`scripts/macos_automation.py`
  - 模板检索 / 渲染 / 执行与原始脚本执行双模式
  - 环境预检、权限探测、风险分级控制（strict / balanced / off）
  - AX 可执行文件检查与运行时自动下载兜底
