# 配置矩阵（与 macos-kit 默认行为对齐）

## 核心开关

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `MACOS_KIT_ENABLE_RAW_SCRIPT` | `true` | 是否启用 `run_macos_script` 能力 |
| `MACOS_KIT_ENABLE_AX_QUERY` | `true` | 是否启用 AX 相关能力 |
| `MACOS_KIT_SAFE_MODE` | `balanced` | 风险策略档位：`strict` / `balanced` / `off` |
| `MACOS_KIT_ALLOWED_SCRIPT_ROOTS` | 空 | 脚本路径白名单（逗号分隔）；不配置则不限制路径 |

## 超时配置

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `MACOS_KIT_DEFAULT_TIMEOUT_SECONDS` | `30` | 默认执行超时 |
| `MACOS_KIT_MAX_TIMEOUT_SECONDS` | `120` | 可允许的最大超时 |

## AX 依赖配置

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `MACOS_KIT_AX_BINARY_PATH` | `ax` | AX 可执行文件命令或路径 |
| `MACOS_KIT_AX_AUTO_INSTALL` | `true` | 未命中本地 ax 时是否自动下载 |
| `MACOS_KIT_AX_DOWNLOAD_URL` | 空 | 下载地址模板，支持 `{platform}`、`{arch}` |
| `MACOS_KIT_AX_CACHE_DIR` | `~/.cache/moryflow/macos-kit/bin` | AX 下载缓存目录 |

## 推荐档位

- 日常默认：`balanced`
- 高安全要求：`strict` + 设置 `MACOS_KIT_ALLOWED_SCRIPT_ROOTS`
- 临时救急：`off`（必须有用户明确授权）
