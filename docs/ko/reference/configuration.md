# 설정

## 설정 파일 위치

`.codexspec/config.yml`

## 설정 스키마

```yaml
version: "1.0"

language:
  output: "ko-KR"        # 기반 언어; 아래 세 가지는 여기로, 그 다음 "en"으로 폴백
  interaction: "ko-KR"   # LLM 대화 + codexspec CLI 출력 (선택 → 기본값은 output)
  document: "en"         # 생성된 requirements/spec/plan/tasks (선택 → 기본값은 output)
  commit: "en"           # git 커밋 메시지 (선택 → 기본값은 output)
  templates: "en"        # "en"으로 유지

project:
  ai: "claude"
  created: "2025-02-15"

workflow:
  auto_next: false       # 워크플로우 단계 간 자동 진행 (옵트인)
```

## 언어 설정

CodexSpec은 언어를 개별적으로 설정 가능한 네 가지 차원으로 나눕니다. `output`이 기반이며, `interaction`, `document`, `commit`은 이를 덮어쓰되 설정되지 않았을 때 이 언어(그 다음 `en`)로 폴백합니다. 이를 통해 예컨대 Claude와는 한 언어로 대화하면서 생성되는 산출물이나 커밋 메시지는 다른 언어로 유지할 수 있습니다.

| 차원 | 키 | init 시 설정 | 이후 설정 | 제어 대상 | 폴백 |
|-----------|-----|-------------|-----------|----------|---------------|
| 출력 (기반) | `output` | `--lang` | `config --set-lang` | 나머지 세 가지의 기반 | `en` |
| 상호작용 | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM 대화 + CLI 출력 | output → `en` |
| 문서 | `document` | `--document-lang` | `config --set-document-lang` | 생성된 spec/plan/tasks | output → `en` |
| 커밋 | `commit` | `--commit-lang` | `config --set-commit-lang` | git 커밋 메시지 | output → `en` |
| 템플릿 | `templates` | — | — | 명령어 템플릿 소스(항상 `en`) | — |

**지원 값:** [국제화](../user-guide/i18n.md#supported-languages) 참조

### `language.output`

기반 출력 언어입니다. 다른 차원이 명시적으로 설정되지 않았을 때 여기로 폴백합니다.

### `language.interaction`

사용자와 LLM 사이의 대화, 그리고 `codexspec` CLI 터미널 출력의 언어입니다. 선택 사항이며, 기본값은 `output`입니다.

### `language.document`

생성되는 산출물 파일(requirements/spec/plan/tasks)의 언어입니다. 선택 사항이며, 기본값은 `output`입니다.

### `language.commit`

git 커밋 메시지의 언어입니다. 선택 사항이며, 기본값은 `output`입니다.

### `language.templates`

템플릿 언어입니다. 호환성을 위해 `"en"`으로 유지해야 합니다.

## 프로젝트 설정

### `project.ai`

사용 중인 AI 어시스턴트입니다. `codexspec init`이 어떤 에이전트 컨텍스트 파일을 내려놓을지 결정합니다:

- `claude` (기본값) — `CLAUDE.md`(및 `.claude/commands/`)를 작성합니다.
- `codex` — 대신 `AGENTS.md`와 `.agents/skills/`를 작성합니다.
- `both` — 위의 모두를 작성하여 프로젝트가 Claude Code 와 Codex CLI 모두에 대비하게 합니다.

`CLAUDE.md`는 항상 생성되어(Claude Code 에서도 프로젝트를 계속 쓸 수 있도록), `AGENTS.md` 와 `.agents/skills/`는 `project.ai`가 `codex` 또는 `both`일 때만 생성됩니다.

### `project.created`

프로젝트가 초기화된 날짜입니다.

## 워크플로우 설정

### `workflow.auto_next`

Requirements-First SDD 파이프라인이 현재 단계를 통과하면 **자동으로 다음 워크플로우 단계로 진행** 할지를 결정합니다. 매번 다음 명령을 수동으로 호출할 필요가 없어집니다.

- **기본값:** `false` (옵트인). 리터럴 값 `true`일 때만 자동 진행이 활성화됩니다.
- **토글 / 설정:** `codexspec config --auto-next` (플래그만 쓰면 현재 값을 토글, `on`/`off`를 명시해 설정 가능).

**체인:**

```
specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks
```

**통과 게이트:**

- `generate-spec`, `spec-to-plan`, `plan-to-tasks`: 명령어에 내장된 리뷰 루프가 Overall Status로 `PASS` 또는 `PASS_WITH_WARNINGS`를 보고해야 합니다.
- `specify`: 리뷰 루프가 없으므로 게이트는 사용자가 요구사항 탐색이 끝났음을 명시적으로 확인하는 것입니다(각 중간 단계 요약이 아니라 **최종** 단계 요약).
- `implement-tasks`: 종착 단계 — 이후에 자동으로 발동하는 것은 없습니다.

리뷰 루프가 `NEEDS_REVISION` 또는 `BLOCKED`를 보고하면 체인은 멈추고 제어가 사용자에게 돌아갑니다. 각 진행 전에 에이전트는 알림 한 줄을 출력합니다(예: `auto_next: review passed → invoking /codexspec:spec-to-plan`).
