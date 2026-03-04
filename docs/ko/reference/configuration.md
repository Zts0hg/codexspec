# 구성

## 구성 파일 위치

`.codexspec/config.yml`

## 구성 스키마

```yaml
version: "1.0"

language:
  output: "en"      # 문서의 출력 언어
  templates: "en"   # 템플릿 언어 ("en"으로 유지)

project:
  ai: "claude"      # AI 어시스턴트
  created: "2025-02-15"
```

## 언어 설정

### `language.output`

Claude 상호작용 및 생성된 문서의 언어입니다.

**지원되는 값:** [국제화](../user-guide/i18n.md#supported-languages) 참조

### `language.templates`

템플릿 언어입니다. 호환성을 위해 `"en"`으로 유지해야 합니다.

## 프로젝트 설정

### `project.ai`

사용 중인 AI 어시스턴트입니다. 현재 다음을 지원합니다:

- `claude` (기본값)

### `project.created`

프로젝트가 초기화된 날짜입니다.
