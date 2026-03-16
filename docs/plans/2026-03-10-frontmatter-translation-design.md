# Frontmatter Translation Design

## Context

CodexSpec 的 `init` 命令在初始化项目时会复制 slash command 模板到 `.claude/commands/` 目录。模板的 Markdown 正文有 Language Preference 机制，会在运行时由 Claude 根据用户语言配置动态翻译。但 YAML frontmatter 中的 `description` 和 `argument-hint` 字段目前保持英文，用户希望这些字段也能根据选择的语言进行翻译。

## Problem

- `description` 字段：用于命令列表显示，用户看到的是英文
- `argument-hint` 字段：用于命令使用提示，用户看到的是英文
- 这些内容不频繁变化，但直接影响用户体验

## Solution: Hybrid Translation Approach

采用**预翻译缓存 + 动态翻译**的混合方案：

1. **预翻译缓存**：为 7 种常用语言维护翻译文件
2. **动态翻译**：其他语言使用 Claude CLI 翻译
3. **静默回退**：失败时使用英文模板

### Supported Languages

与 README 多语言版本一致：

| 语言 | 代码 |
|------|------|
| 简体中文 | zh-CN |
| 日语 | ja |
| 韩语 | ko |
| 西班牙语 | es |
| 法语 | fr |
| 德语 | de |
| 巴西葡萄牙语 | pt-BR |

## Architecture

### File Structure

```
codexspec/
├── templates/
│   ├── commands/              # 英文模板（主版本）
│   │   ├── constitution.md
│   │   ├── specify.md
│   │   └── ...
│   └── translations/          # 预翻译缓存（新增）
│       ├── zh-CN.json
│       ├── ja.json
│       ├── ko.json
│       ├── es.json
│       ├── fr.json
│       ├── de.json
│       └── pt-BR.json
├── src/codexspec/
│   ├── __init__.py           # 修改：init() 中调用翻译
│   ├── i18n.py               # 现有
│   └── translator.py         # 新增：翻译逻辑
```

### Translation Cache Format

```json
{
  "constitution": {
    "description": "通过交互式或提供的原则输入创建或更新项目宪法...",
    "argument-hint": "[quick|deep | 项目原则] (可选)..."
  },
  "specify": {
    "description": "通过交互式问答澄清需求...",
    "argument-hint": "[功能描述] (必填)..."
  }
}
```

### Translation Flow

```
codexspec init --lang <LANG>
        │
        ▼
┌─────────────────────────────────────────┐
│ 1. 检查语言类型                          │
│    - en → 跳过翻译                       │
│    - 支持的语言 → 使用预翻译缓存          │
│    - 其他语言 → 尝试动态翻译              │
└─────────────────────────────────────────┘
        │
        ├──────────────────┬───────────────┐
        ▼                  ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ 预翻译缓存    │ │ 动态翻译      │ │ 英文模板      │
│ - 读取 JSON   │ │ - 检查 CLI    │ │ - 直接复制    │
│ - 应用到模板  │ │ - 批量翻译    │ │               │
│ - 快速无依赖  │ │ - 失败回退    │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
```

## Implementation Details

### Core Functions

```python
# src/codexspec/translator.py

SUPPORTED_LANGUAGES = ["zh-CN", "ja", "ko", "es", "fr", "de", "pt-BR"]

def translate_frontmatters(
    templates_dir: Path,
    target_lang: str,
    output_dir: Path
) -> bool:
    """翻译模板 frontmatter，返回是否成功"""

def _apply_cached_translation(...) -> bool:
    """应用预翻译缓存"""

def _dynamic_translate(...) -> bool:
    """使用 Claude CLI 动态翻译"""

def _check_claude_cli_available() -> bool:
    """检查 Claude CLI 是否可用"""
```

### Claude CLI Integration

动态翻译时调用 Claude CLI：

```bash
claude --print "Translate the following JSON values to <LANG>.
Keep keys unchanged. Return only valid JSON.

<JSON content>"
```

### Error Handling

- 预翻译缓存文件不存在 → 回退到英文
- Claude CLI 不可用 → 静默回退到英文
- 翻译 API 失败 → 静默回退到英文
- JSON 解析失败 → 静默回退到英文

## Files to Modify

| File | Change |
|------|--------|
| `src/codexspec/__init__.py` | 在 `init()` 中调用 `translate_frontmatters()` |
| `src/codexspec/translator.py` | **新增** - 翻译逻辑 |
| `templates/translations/*.json` | **新增** - 7 个预翻译缓存文件 |
| `tests/test_translator.py` | **新增** - 单元测试 |

## Future Extensions

1. **缓存更新命令**：`codexspec translate-cache <LANG>` 更新翻译缓存
2. **配置选项**：在 `config.yml` 中配置翻译行为
3. **更多语言**：根据需求添加更多预翻译语言

## Decision Log

- **2026-03-10**: 采用混合方案（预翻译缓存 + 动态翻译）
- **2026-03-10**: 支持语言与 README 多语言版本保持一致
- **2026-03-10**: 翻译失败时静默回退到英文，不中断 init 流程
