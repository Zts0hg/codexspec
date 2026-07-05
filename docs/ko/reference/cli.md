# CLI 참조

## 명령어

### `codexspec init`

새 CodexSpec 프로젝트를 초기화합니다.

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**인자:**

| 인자 | 설명 |
|----------|-------------|
| `PROJECT_NAME` | 새 프로젝트 디렉토리의 이름(현재 디렉토리는 `.` 또는 `--here` 사용) |

**옵션:**

| 옵션 | 단축 | 설명 |
|--------|-------|-------------|
| `--here` | `-h` | 현재 디렉토리에서 초기화 |
| `--ai` | `-a` | 사용할 AI 어시스턴트: `claude`, `codex`, 또는 `both` (기본값: claude) |
| `--lang` | `-l` | 출력(기반) 언어; interaction/document/commit이 여기로 폴백 (예: en, zh-CN, ja) |
| `--interaction-lang` | | 상호작용 언어(LLM 대화 + `codexspec` CLI 출력); `--lang`을 덮어씀 |
| `--document-lang` | | 문서 언어(생성된 requirements/spec/plan/tasks); `--lang`을 덮어씀 |
| `--commit-lang` | | 커밋 메시지 언어; `--lang`을 덮어씀 |
| `--force` | `-f` | 기존 파일을 덮어쓰고 프롬프트를 자동 확정; `config.yml`은 재생성하지 않음 |
| `--no-git` | | git 리포지토리 초기화 건너뛰기 |
| `--debug` | `-d` | 디버그 출력 활성화 |

`--lang`은 `output` 기반 언어를 설정하며, `--interaction-lang`, `--document-lang`, `--commit-lang`은 각자의 차원에서 이를 덮어씁니다(각각 `output` → `en` 순으로 폴백). 전체 모델은 [국제화](../user-guide/i18n.md)를 참조하세요.

TTY 환경에서 `--lang`(그리고 세 차원 플래그 모두) 없이 처음 init을 실행하면 기반 언어를 묻습니다. non-TTY(CI/스크립트)에서는 `en`이 기본값이 되며 **완전히 비대화형**으로 동작합니다. `init`을 다시 실행할 때 지정하지 않은 언어 키는 보존되며, `--force`는 절대 `config.yml`을 재생성하지 않습니다.

**예제:**

```bash
# 새 프로젝트 생성
codexspec init my-project

# 현재 디렉토리에서 초기화
codexspec init . --ai claude

# 일회성 실행(설치 없음) — Codex CLI 또는 both 로 초기화
uvx codexspec init . --ai codex
uvx codexspec init . --ai both

# 완전한 비대화형: zh-CN 기반, 영어 커밋 메시지
codexspec init my-project --lang zh-CN --commit-lang en

# 모든 차원을 명시적으로 설정(스크립트용, 프롬프트 없음)
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

---

### `codexspec check`

설치된 도구를 확인합니다.

```bash
codexspec check
```

---

### `codexspec version`

버전 정보를 표시합니다.

```bash
codexspec version
```

---

### `codexspec config`

프로젝트 설정을 보거나 수정합니다.

```bash
codexspec config [OPTIONS]
```

**옵션:**

| 옵션 | 단축 | 설명 |
|--------|-------|-------------|
| `--set-lang` | `-l` | 출력(기반) 언어 설정 |
| `--set-interaction-lang` | | 상호작용 언어 설정(LLM 대화 + CLI 출력) |
| `--set-document-lang` | | 문서 언어 설정(생성된 spec/plan/tasks) |
| `--set-commit-lang` | `-c` | 커밋 메시지 언어 설정 |
| `--list-langs` | | 지원하는 모든 언어 나열 |
| `--auto-next` | | `workflow.auto_next` 토글/설정(플래그만 쓰면 토글, 또는 on/off 명시) |

각 `--set-*-lang`은 하나의 [언어 차원](../user-guide/i18n.md)을 업데이트합니다. 설정하지 않은 차원은 `output` → `en` 순으로 폴백합니다.
