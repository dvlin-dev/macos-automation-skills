# macos-automation-skills

按 `vercel-labs/skills` 生态约定组织的技能仓库，当前包含 1 个技能：`macos-automation`。

## 目录结构

```text
skills/
  macos-automation/
    SKILL.md
    scripts/
    references/
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
  - macOS 自动化执行工作流（AppleScript/JXA）
  - 环境预检与权限探测
  - 模板检索与渲染
  - 原始脚本风险分级控制（strict / balanced / off）
  - AX 可执行文件检查与运行时自动下载策略
