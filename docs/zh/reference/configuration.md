# 配置

## 配置文件位置

`.codexspec/config.yml`

## 配置模式

```yaml
version: "1.0"

language:
  output: "en"      # 文档输出语言
  templates: "en"   # 模板语言（保持为 "en"）

project:
  ai: "claude"      # AI 助手
  created: "2025-02-15"
```

## 语言设置

### `language.output`

Claude 交互和生成文档的语言。

**支持的值：** 参见[国际化](../user-guide/i18n.md#supported-languages)

### `language.templates`

模板语言。应保持为 `"en"` 以确保兼容性。

## 项目设置

### `project.ai`

正在使用的 AI 助手。当前支持：

- `claude`（默认）

### `project.created`

项目初始化的日期。
