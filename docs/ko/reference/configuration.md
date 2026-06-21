# 구성

## 구성 파일 위치

`.codexspec/config.yml`

## 구성 스키마

```yaml
version: "1.0"

language:
  output: "zh-CN"        # 기본 언어; 아래 세 가지는 이 언어로, 그 다음 "en"으로 폴백
  interaction: "zh-CN"   # LLM 대화 + codexspec CLI 출력 (선택 → 기본값은 output)
  document: "en"         # 생성된 requirements/spec/plan/tasks (선택 → 기본값은 output)
  commit: "en"           # git 커밋 메시지 (선택 → 기본값은 output)
  templates: "en"        # 템플릿 언어 ("en"으로 유지)

project:
  ai: "claude"      # AI 어시스턴트
  created: "2025-02-15"
```

## 언어 설정

CodexSpec은 언어를 개별적으로 구성 가능한 네 가지 차원으로 나눕니다. `output`이 기반이며, `interaction`, `document`, `commit`은 이를 덮어쓰고 설정되지 않았을 때 이 언어(그 다음 `en`)로 폴백합니다. 예를 들어 Claude와는 한 언어로 대화하면서 생성된 산출물이나 커밋 메시지는 다른 언어로 유지할 수 있습니다.

| 차원 | 키 | init에서 설정 | 이후에 설정 | 제어 대상 | 폴백 |
|-----------|-----|-------------|-----------|----------|---------------|
| 출력 (기본) | `output` | `--lang` | `config --set-lang` | 나머지 세 가지의 기반 | `en` |
| 상호작용 | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM 대화 + CLI 출력 | output → `en` |
| 문서 | `document` | `--document-lang` | `config --set-document-lang` | 생성된 spec/plan/tasks | output → `en` |
| 커밋 | `commit` | `--commit-lang` | `config --set-commit-lang` | git 커밋 메시지 | output → `en` |
| 템플릿 | `templates` | — | — | 명령 템플릿 소스 (항상 `en`) | — |

**지원되는 값:** [국제화](../user-guide/i18n.md#supported-languages) 참조

### `language.output`

기본 출력 언어입니다. 다른 차원이 명시적으로 설정되지 않았을 때 이 언어로 폴백합니다.

### `language.interaction`

사용자와 LLM 간의 대화, 그리고 `codexspec` CLI 터미널 출력의 언어입니다. 선택 사항이며, 기본값은 `output`입니다.

### `language.document`

생성된 산출물 파일(requirements/spec/plan/tasks)의 언어입니다. 선택 사항이며, 기본값은 `output`입니다.

### `language.commit`

git 커밋 메시지의 언어입니다. 선택 사항이며, 기본값은 `output`입니다.

### `language.templates`

템플릿 언어입니다. 호환성을 위해 `"en"`으로 유지해야 합니다.

## 프로젝트 설정

### `project.ai`

사용 중인 AI 어시스턴트입니다. 현재 다음을 지원합니다:

- `claude` (기본값)

### `project.created`

프로젝트가 초기화된 날짜입니다.
