# AX 策略说明

## 背景

AX（Accessibility）能力用于 UI 元素查询和动作执行。它依赖一个外部可执行文件 `ax`。

## 策略目标

- 不在 `postinstall` 阶段下载依赖，避免影响 MCP/包安装时延和超时。
- 在运行阶段兜底：
  1. 启动预热（可选）
  2. 调用前再检查一次（强制）

## 推荐流程

1. 服务启动后，执行预热：

```bash
python scripts/check_env.py --prewarm-ax
```

2. 真正执行 AX 前，再调用：

```bash
python scripts/ensure_ax.py
```

3. 若仍失败，返回 `DEPENDENCY_MISSING`，并附带明确 hint。

## 自动下载配置示例

```bash
export MACOS_KIT_AX_AUTO_INSTALL=true
export MACOS_KIT_AX_DOWNLOAD_URL='https://example.com/ax/{platform}/{arch}/ax'
export MACOS_KIT_AX_CACHE_DIR='~/.cache/moryflow/macos-kit/bin'
python scripts/ensure_ax.py
```

## 设计取舍

- **优点**：不拖慢安装；首次使用前可预热；调用时有兜底。
- **代价**：首次命中下载时会增加一次运行时延迟。
