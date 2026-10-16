# 빠른 시작

<a id="30-second-quick-start"></a>

## 30초 빠른 시작

CodexSpec을 설치하고 사용할 어시스턴트에 맞게 프로젝트를 초기화합니다.

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

초기화한 프로젝트에서 설치된 어시스턴트를 실행하세요.
워크플로우는 같지만 어시스턴트에 따라 호출 형식이 다릅니다.

| 어시스턴트 | 요구사항 논의를 시작하는 명령어 |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

필요하면 `constitution`으로 프로젝트 원칙을 조정하세요.
최종 요구사항 요약을 확인한 다음, 반환된 기능 디렉터리와 작업 공간에서 계속 진행합니다.
이후에 사용할 명령어는 [핵심 워크플로우](../user-guide/workflow.md#core-workflow)를 참고하세요.

Codex 데스크톱 앱에서는 [Codex에 설치와 프로젝트 초기화를 요청할 수 있습니다](installation.md#install-with-the-codex-desktop-app).

<a id="core-workflow"></a>

## 핵심 워크플로우

표준 기능 개발 워크플로우에서는 각 산출물에 출처를 연결하며 다음 순서로 진행합니다.

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

아래 예시는 Claude의 `/codexspec:` 접두사를 사용합니다.
Codex에서는 명령어 이름과 인수는 그대로 두고 `$codexspec:`을 사용하세요.

| 단계 | 명령어 | 목적과 산출물 |
|------|---------|--------------------|
| 프로젝트 원칙 | `/codexspec:constitution` | `constitution.md`를 작성·업데이트하고 영향을 받는 산출물 검증 |
| 요구사항 | `/codexspec:specify <idea>` | 의도를 논의하고 최종 요약을 확인한 뒤 `requirements.md`에 저장 |
| 명세서 | `/codexspec:generate-spec <feature-dir>` | 확정된 요구사항을 바탕으로 출처 참조가 포함된 `spec.md` 작성 |
| 시스템 설계 | `/codexspec:spec-to-design <feature-dir>` | 컴포넌트, 인터페이스, 주요 설계 결정을 담은 `design.md` 작성 |
| 구현 계획 | `/codexspec:design-to-plan <feature-dir>` | 구현 단계, 순서, 검증 방법을 담은 `plan.md` 작성 |
| 태스크 | `/codexspec:plan-to-tasks <feature-dir>` | 추적·검증 가능한 `tasks.md`를 작성하고 산출물 간 분석 실행 |
| 구현 | `/codexspec:implement-tasks <feature-dir>` | 태스크를 수행하고 결과를 검증하며, 독립적으로 검증된 리뷰 지적 수정 |

`<feature-dir>`를 요구사항 논의 중 반환된 기능 디렉터리로 바꾸세요.
해당 worktree에서 작업을 이어가거나 경로를 명시적으로 전달하면, 명령어나 세션이 바뀌어도 같은 기능으로 처리됩니다.

<a id="specify-clarify-and-analyze"></a>

### specify, clarify, analyze

- **specify**는 요구사항 논의를 시작하거나 다시 진행합니다. 요구사항 요약은 명시적인 확인을 받아야 공식적인 판단 기준이 됩니다.
- **clarify**는 기존 요구사항과 명세의 모호함을 해소합니다. 한 번 실행할 때 네 가지 범주에 걸쳐 최대 다섯 가지 질문을 합니다.
  먼저 `requirements.md`를 업데이트하고, 그다음 `spec.md`를 동기화합니다.
- **analyze**는 요구사항 → 명세 → 설계 → 계획 → 태스크의 전체 흐름을 확인합니다.
  상위 판단 기준에 따라 수정 내용이 하나로 정해지는 경우 하위 산출물을 자동으로 수정합니다. `requirements.md`는 절대 편집하지 않습니다.
  해결되지 않은 지적은 보고합니다. 태스크 리뷰를 통과하면 자동으로 실행되지만, 정보를 제공하는 절차이며 구현의 통과 여부를 판정하지는 않습니다.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### Quick으로 작은 변경 수행

국소적인 수정처럼 작고 범위가 명확한 변경에는 `quick`을 사용하세요.

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick은 간결한 요구사항 요약을 확인하고 저장한 다음 명세 작성, 계획, 태스크, 구현을 순서대로 진행합니다.
각 생성 명령어의 리뷰도 함께 수행합니다. 변경 범위가 넓거나 제품·설계 선택이 아직 해결되지 않았다면 표준 워크플로우를 사용하세요.
Quick은 새로운 결정이 필요할 때 일시 중지합니다.

<a id="workflow-automation"></a>

### 워크플로우 자동화

`workflow.auto_next`의 기본값은 **false**입니다.
현재 작업 공간의 설정이 `true`이면 최종 요구사항 확인 후 명세 작성으로 진행합니다.
각 생성 단계는 `PASS` 또는 `PASS_WITH_WARNINGS`이면 다음 단계로 넘어가고, `NEEDS_REVISION` 또는 `BLOCKED`이면 멈춥니다.
`implement-tasks`가 마지막 단계입니다.

산출물 자동 수정은 검증된 결함 중 상위 근거에 따라 수정 방향이 정해지는 경우에만 적용됩니다.
수정과 리뷰는 최대 두 라운드까지 수행하며, 권고 사항은 별도로 다룹니다.
구현의 리뷰·수정 반복에는 아래에서 설명하는 별도의 완료 조건이 있습니다.

자세한 동작과 조건은 [워크플로우 가이드](../user-guide/workflow.md)를 참고하세요.

<a id="project-structure"></a>

## 프로젝트 구조

초기화는 공통 리소스와 선택한 어시스턴트 연동에 필요한 파일을 설치합니다.

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

공유 블루프린트는 전용 auto-dev worktree에 저장합니다. 일반 체크아웃마다 편집할 수 있는 별도 복사본을 두지는 않습니다.
수동 지식 리뷰의 초안은 Git 관리 대상에서 제외됩니다.
