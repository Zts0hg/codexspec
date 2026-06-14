# Implementation Plan: Interactive Language Selection for init Command

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | >=3.11 | 项目已有约束 |
| CLI Framework | Typer | Current | 现有依赖 |
| Terminal UI | Rich | Current | 现有依赖，使用 `Prompt.ask()` |
| Configuration | YAML | Current | config.yml 格式 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 提取独立函数 `prompt_language_selection()`，保持单一职责 |
| Testing Standards | ✅ | 需要为新增函数编写单元测试 |
| Documentation | ✅ | 函数添加 docstring |
| Architecture | ✅ | 遵循现有模块结构，修改 `__init__.py` 和 `i18n.py` |
| Performance | ✅ | TTY 检测是 O(1) 操作，Prompt 显示在 100ms 内 |
| Security | ✅ | 输入通过 `normalize_locale()` 验证和规范化 |

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      codexspec init                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │ --lang None │───▶│ is TTY terminal? │───▶│ Prompt user   │  │
│  └─────────────┘    └──────────────────┘    └───────────────┘  │
│                              │                      │            │
│                              │ No                   │            │
│                              ▼                      ▼            │
│                     ┌───────────────┐    ┌─────────────────┐   │
│                     │ Use default en│    │ Get selection   │   │
│                     └───────────────┘    │ (1-9 or custom) │   │
│                                          └─────────────────┘   │
│                                                   │             │
│                                                   ▼             │
│                                          ┌─────────────────┐   │
│                                          │ normalize_locale│   │
│                                          └─────────────────┘   │
│                                                   │             │
│                                                   ▼             │
│                                          ┌─────────────────┐   │
│                                          │ Continue init   │   │
│                                          │ with language   │   │
│                                          └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
src/codexspec/
├── __init__.py           # 修改: init() 函数
│   ├── init()            # 修改: --lang 参数默认值和处理逻辑
│   └── prompt_language_selection()  # 新增: 语言选择交互函数
├── i18n.py               # 修改: 添加 ALL_LANGUAGES 常量
│   └── ALL_LANGUAGES     # 新增: 合并 en + SUPPORTED_LANGUAGES
└── translator.py         # 无需修改
    └── SUPPORTED_LANGUAGES  # 现有: 预翻译语言列表

tests/
├── test_init.py          # 新增: init 命令测试
└── test_i18n.py          # 修改: 测试 ALL_LANGUAGES
```

## 5. Module Dependencies

```
                    ┌─────────────────┐
                    │    __init__.py   │
                    │   (init command) │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
      ┌───────────┐  ┌───────────┐  ┌─────────────┐
      │  i18n.py  │  │translator │  │ rich.prompt │
      │           │  │    .py    │  │  (external) │
      └───────────┘  └───────────┘  └─────────────┘
              │              │
              │              │
              ▼              ▼
      ┌─────────────────────────┐
      │ normalize_locale()      │
      │ get_language_name()     │
      │ SUPPORTED_LANGUAGES     │
      └─────────────────────────┘
```

## 6. Data Models

### 语言选择结果

```python
@dataclass
class LanguageSelection:
    code: str           # 规范化后的语言代码，如 "zh-CN"
    is_custom: bool     # 是否为自定义输入
```

### 语言选项

```python
# 预定义语言选项 (用于 Prompt.ask)
LANGUAGE_CHOICES = {
    "1": ("en", "English"),
    "2": ("zh-CN", "简体中文"),
    "3": ("ja", "日本語"),
    "4": ("ko", "한국어"),
    "5": ("es", "Español"),
    "6": ("fr", "Français"),
    "7": ("de", "Deutsch"),
    "8": ("pt-BR", "Português (Brasil)"),
    "9": (None, "Other... (enter custom code)"),
}
```

## 7. API Contracts

### Function: `prompt_language_selection()`

```python
def prompt_language_selection(default: str = "en") -> str:
    """
    显示交互式语言选择提示。

    Args:
        default: 默认选中的语言代码

    Returns:
        用户选择的语言代码（已规范化）

    Raises:
        KeyboardInterrupt: 用户按 Ctrl+C 时
    """
```

**行为**:

- 显示 9 个编号选项
- 用户输入 1-8 选择预定义语言
- 用户输入 9 后提示输入自定义语言代码
- 无效输入时重新提示
- Ctrl+C 时抛出 KeyboardInterrupt

**Edge Case 处理**:

- Edge Case 3: "Other..." 提示中空字符串输入
  - 检测 `if not custom_code.strip()`
  - 显示静默提示：`[dim]No language code entered, using default (en)[/dim]`
  - 返回 `default` 参数值（即 "en"）

### Function: `get_all_supported_languages()` (新增到 i18n.py)

```python
def get_all_supported_languages() -> list[tuple[str, str]]:
    """
    获取所有支持的语言列表（包括 en）。

    Returns:
        List of (code, name) tuples，en 排在首位
    """
```

## 8. Implementation Phases

### Phase 1: 准备工作

- [ ] 在 `i18n.py` 中添加 `get_all_supported_languages()` 函数
- [ ] 添加 `ALL_LANGUAGES` 常量（合并 en + translator.SUPPORTED_LANGUAGES）
- [ ] 编写单元测试

### Phase 2: 核心实现

- [ ] 在 `__init__.py` 中添加 `prompt_language_selection()` 函数
- [ ] 修改 `init()` 函数的 `--lang` 参数默认值：`"en"` → `None`
- [ ] 添加 TTY 检测逻辑：`sys.stdin.isatty()`
- [ ] 添加语言选择调用逻辑
- [ ] 处理 Ctrl+C 中断（使用默认语言继续）

### Phase 3: 集成测试

- [ ] 手动测试 TTY 环境下的交互
- [ ] 测试非 TTY 环境的默认行为
- [ ] 测试 `--lang` 参数跳过交互
- [ ] 测试无效输入处理
- [ ] 测试 Ctrl+C 处理

### Phase 4: 文档更新

- [ ] 更新 `--lang` 参数的帮助文本
- [ ] 更新 README（如适用）

## 9. Technical Decisions

### Decision 1: 使用 Rich Prompt.ask() 而非箭头键选择

- **Choice**: 使用 `Prompt.ask()` 显示编号列表
- **Rationale**:
  1. 避免引入 `readchar` 新依赖
  2. Rich Prompt 跨平台兼容性更好
  3. 实现更简单，维护成本更低
- **Alternatives**:
  1. 使用 `readchar` + Rich Live 实现箭头键选择（参考 spec-kit）
  2. 使用 `questionary` 库
- **Trade-offs**: 失去箭头键导航的视觉效果，但换来更简单的实现和更少的依赖

### Decision 2: Ctrl+C 处理策略

- **Choice**: Ctrl+C 时使用默认语言继续初始化
- **Rationale**:
  1. 用户可能误按 Ctrl+C
  2. 不应中断整个初始化流程
  3. 使用默认语言是安全的回退
- **Alternatives**:
  1. 完全终止初始化
  2. 抛出异常让 Typer 处理
- **Trade-offs**: 用户可能期望 Ctrl+C 终止程序，但我们选择友好降级

### Decision 3: 语言列表数据源

- **Choice**: 从 `i18n.py` 和 `translator.py` 动态构建
- **Rationale**:
  1. 避免硬编码重复
  2. 新增预翻译语言时无需修改选择逻辑
  3. 保持数据一致性
- **Alternatives**:
  1. 在选择函数中硬编码语言列表
- **Trade-offs**: 需要跨模块导入，但换来可维护性

### Decision 4: 自定义语言输入提示

- **Choice**: 选择 "Other..." 后显示警告提示
- **Rationale**:
  1. 用户需要知道可能没有预翻译内容
  2. 管理用户期望
- **Alternatives**:
  1. 静默接受自定义代码
- **Trade-offs**: 多一步交互，但提供更好的用户体验

## 10. Code Changes Summary

### File: `src/codexspec/i18n.py`

```python
# 新增导入
from codexspec.translator import SUPPORTED_LANGUAGES

# 新增常量
ALL_LANGUAGES = ["en"] + SUPPORTED_LANGUAGES

# 新增函数
def get_all_supported_languages() -> list[tuple[str, str]]:
    """获取所有支持的语言列表（包括 en）。"""
    return [(code, get_language_name(code)) for code in ALL_LANGUAGES]
```

### File: `src/codexspec/__init__.py`

```python
# 新增导入
from rich.prompt import Prompt  # 添加到现有 rich 导入

# 新增函数
def prompt_language_selection(default: str = "en") -> str:
    """显示交互式语言选择提示。"""
    # ... 显示选项
    choice = Prompt.ask("Enter choice", default="1", choices=["1"-"9"])

    if choice == "9":
        custom_code = Prompt.ask("Enter language code (e.g., ru, ar, hi)", default="")
        # Edge Case 3: 空字符串输入 → 回退到默认语言
        if not custom_code.strip():
            console.print("[dim]No language code entered, using default (en)[/dim]")
            return default
        normalized = normalize_locale(custom_code)
        console.print(f"[dim]Note: Pre-translated content may not be available for '{normalized}'.[/dim]")
        return normalized

    return LANGUAGE_CHOICES[choice][0]

# 修改 init() 函数
@app.command()
def init(
    # ...
    lang: Optional[str] = typer.Option(  # 修改: str -> Optional[str]
        None,  # 修改: "en" -> None
        "--lang",
        "-l",
        help="Output language (interactive prompt if not specified)",
    ),
    # ...
) -> None:
    # 新增: TTY 检测和语言选择
    if lang is None:
        if sys.stdin.isatty():
            try:
                lang = prompt_language_selection()
            except KeyboardInterrupt:
                console.print("\n[yellow]Selection cancelled, using default language (en)[/yellow]")
                lang = "en"
        else:
            lang = "en"

    normalized_lang = normalize_locale(lang)
    # ... 其余逻辑不变
```

## 11. Testing Strategy

### Unit Tests

```python
# tests/test_i18n.py
def test_all_languages_includes_en():
    """ALL_LANGUAGES 应该包含 en"""
    assert "en" in ALL_LANGUAGES

def test_all_languages_includes_supported():
    """ALL_LANGUAGES 应该包含所有 SUPPORTED_LANGUAGES"""
    for lang in SUPPORTED_LANGUAGES:
        assert lang in ALL_LANGUAGES

def test_get_all_supported_languages_returns_list():
    """get_all_supported_languages() 返回正确格式"""
    langs = get_all_supported_languages()
    assert isinstance(langs, list)
    assert langs[0] == ("en", "English")

# tests/test_init.py
def test_prompt_language_selection_valid_choice():
    """有效选择返回正确语言代码"""
    with patch('sys.stdin.isatty', return_value=True):
        # 测试各选项

def test_prompt_language_selection_custom():
    """选择 Other... 后输入自定义代码"""

def test_prompt_language_selection_other_empty_input():
    """选择 Other... 后直接按 Enter → 回退到默认语言 en"""

def test_prompt_language_selection_invalid_then_valid():
    """无效输入后重新提示"""

def test_init_without_lang_in_tty():
    """TTY 环境下不传 --lang 显示选择"""

def test_init_without_lang_not_tty():
    """非 TTY 环境下不传 --lang 使用默认"""

def test_init_with_lang_skips_prompt():
    """传入 --lang 跳过选择"""
```

### Integration Tests

```bash
# 手动测试脚本
# 1. TTY 交互测试
codexspec init test-project

# 2. 非 TTY 测试
echo "" | codexspec init test-project

# 3. --lang 参数测试
codexspec init test-project --lang zh-CN
```
