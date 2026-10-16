<a id="available-commands"></a>

# 사용 가능한 명령어

CLI에는 여섯 가지 공개 명령어가 있습니다. 에이전트 연동에서는 28개 명령어를 배포합니다.
Claude에서는 `/codexspec:<name>`, Codex에서는 `$codexspec:<name>`으로 호출합니다.
아래 표는 읽기 쉽도록 Claude 표기로 통일했습니다.

<a id="cli-commands"></a>

## CLI 명령어

| 명령어 | 목적 |
|---------|---------|
| `codexspec init` | Claude, Codex 또는 둘 모두에 맞게 프로젝트 초기화·갱신 |
| `codexspec check` | 설치된 도구와 의존성 확인 |
| `codexspec version` | 버전과 시스템 정보 표시 |
| `codexspec config` | 프로젝트 설정 조회·수정 |
| `codexspec list-commands` | 사용할 수 있는 에이전트 명령어를 범주별로 표시 |
| `codexspec show-blueprint` | 공유 worktree의 블루프린트를 변경하지 않고 출력 |

<a id="core-workflow-commands"></a>

## 핵심 워크플로우 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:constitution` | 프로젝트 원칙을 작성·업데이트하고 산출물 간 검증 수행 |
| `/codexspec:specify` | 기능 요구사항을 논의하고 확인해 저장 |
| `/codexspec:blueprint` | 블루프린트의 확정된 대기 요구사항 준비·관리 |
| `/codexspec:generate-spec` | 확정된 요구사항으로 추적 가능한 명세서를 작성하고 자동 리뷰 |
| `/codexspec:spec-to-design` | 아키텍처, 컴포넌트, 인터페이스, 결정을 정의하고 자동 리뷰 |
| `/codexspec:design-to-plan` | 구현 단계, 순서, 검증을 계획하고 자동 리뷰 |
| `/codexspec:plan-to-tasks` | 상위 산출물의 내용을 포괄하는 검증 가능한 태스크를 작성하고 자동 리뷰 및 분석 |
| `/codexspec:implement-tasks` | 태스크 수행, 결과 검증, 리뷰와 수정 |
| `/codexspec:auto-dev` | 확정된 블루프린트 요구사항을 문서에 나온 순서대로 자율 개발 |

<a id="artifact-review-commands"></a>

## 산출물 리뷰 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:review-spec` | 명세서의 충실도와 내부 품질 확인 |
| `/codexspec:review-design` | 설계의 충실도, 실현 가능성, 계획 단계로 진행할 준비가 되었는지 확인 |
| `/codexspec:review-plan` | 계획의 충실도, 실현 가능성, 구현할 준비가 되었는지 확인 |
| `/codexspec:review-tasks` | 태스크의 충실도, 의존성, 실행 가능성, 검증 확인 |

<a id="requirements-existing-code-and-debugging"></a>

## 요구사항, 기존 코드, 디버깅

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:clarify` | 요구사항의 모호함을 해소하고 명세서보다 먼저 요구사항 업데이트 |
| `/codexspec:analyze` | 전체 과정의 추적 가능성을 확인하고 하위 산출물을 상위 판단 기준에 맞게 수정 |
| `/codexspec:checklist` | 요구사항 품질 체크리스트 생성 |
| `/codexspec:tasks-to-issues` | 기존 태스크를 실행에 옮길 수 있는 GitHub 이슈로 변환 |
| `/codexspec:debug` | 수정하기 전에 근본 원인 조사 |
| `/codexspec:reverse-spec` | 기존 아키텍처 조사, 모듈 산출물 초안 작성 또는 기준과의 차이 보고 |

<a id="project-knowledge-commands"></a>

## 프로젝트 지식 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:distill` | 재사용할 수 있는 지식 기록 또는 로컬 작업 공간에서 후보 리뷰 |
| `/codexspec:evolve` | 검토·승인된 지식을 업스트림 기여 초안으로 정리 |
| `/codexspec:onboard` | 기존 코드에서 관례 후보와 근거가 있는 제약 초기 등록 |

<a id="git-and-code-review-commands"></a>

## Git 및 코드 리뷰 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:commit-staged` | 스테이징된 변경에서 메시지를 생성하고 미리 보거나 승인된 커밋 실행 |
| `/codexspec:pr` | 구조화된 PR/MR 설명 생성 |
| `/codexspec:release-notes` | 변경 이력 항목을 유지하고 Git 이력에서 릴리스 본문 생성 |
| `/codexspec:review-code` | 선택한 변경을 결함 게이트로 리뷰. 경로 품질 평가에는 `--audit` 사용 |

<a id="utility-commands"></a>

## 유틸리티 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:config` | 대화형으로 프로젝트 설정 작성·조회·수정·초기화 |
| `/codexspec:quick` | 작은 변경을 위한 간결한 요구사항 우선 SDD 워크플로우 실행 |

기존 Python／React 검토 진입점은 플러그인 호환성 유지를 위한 것으로, 설치되는 28개 명령에 포함되지 않습니다. 언어와 프레임워크에 맞는 기준을 불러오는 `review-code`를 사용하고, 경로별 평가에는 `--audit`를 지정하세요.

## 명령어 참조

### `/codexspec:constitution`

프로젝트 헌법을 생성하거나 갱신합니다. 헌법은 아키텍처 원칙, 기술 스택, 코드 표준, 거버넌스 규칙을 정의하며, 이후 모든 개발 결정을 안내합니다.

**구문：**

```
/codexspec:constitution [principles description]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `principles description` | 아니요 | 포함할 원칙에 대한 설명 (제공하지 않으면 프롬프트로 묻습니다) |

**동작：**

- `.codexspec/memory/constitution.md`가 없으면 생성
- 기존 헌법에 새 원칙을 반영하여 갱신
- 템플릿과의 산출물 간 일관성 검증
- 변경 내용과 영향받는 파일을 보여주는 Sync Impact Report 생성
- 의존 템플릿에 대한 헌법 적합성 리뷰 포함

**생성 파일：**

```
.codexspec/
└── memory/
    └── constitution.md    # Project governance document
```

**예제：**

```text
You: /codexspec:constitution Focus on code quality, testing standards, and clean architecture

AI:  Creating constitution...

     ✓ Created .codexspec/memory/constitution.md
     Version: 1.0.0

     Sync Impact Report:
     - plan-template-*.md: ✅ aligned
     - spec-template-*.md: ✅ aligned
     - tasks-template-*.md: ✅ aligned

     Core Principles:
     1. Code Quality First
     2. Test-Driven Development
     3. Clean Architecture

     Suggested commit: docs: create constitution v1.0.0
```

**사용 팁：**

- 일관된 의사결정을 위해 프로젝트 초반에 원칙을 정의하세요
- 기술 원칙과 프로세스 원칙을 모두 포함하세요
- 주요 기능 개발에 앞서 헌법을 검토하세요
- 헌법 변경은 산출물 간 검증을 유발합니다

---

### `/codexspec:specify`

대화형 Q&A로 요구사항을 명확화하고, 도출된 요약을 확정한 뒤 이후 세션에서 사용할 수 있게 저장합니다.

**구문：**

```
/codexspec:specify [your idea or requirement]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `your idea or requirement` | 아니요 | 구축하고자 하는 것에 대한 초기 설명 (제공하지 않으면 프롬프트로 묻습니다) |

**동작：**

- 아이디어를 이해하기 위한 명확화 질문
- 놓칠 수 있는 엣지 케이스 탐색
- 대화를 통해 고품질 요구사항을 함께 도출
- "무엇"과 "왜"에 집중하며 기술 구현은 다루지 않음
- 확정된 필요사항, 제약, 결정, 제외 항목, 미해결 질문에 안정적인 ID 부여
- 사용자 증거와 확정 로그 기록
- 기능 워크스페이스와 `requirements.md` 생성

**생성 파일：**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

오직 확정된 항목만 권위 있는 요구사항이 됩니다. 미해결 질문은 명시적으로 열린 상태로 남습니다. 이것이 요구사항의 Confirmation Gate입니다. 최종 요약을 명시적으로 확정하기 전까지는 어떤 것도 확정된 것으로 간주하지 않습니다.

**예제：**

```text
You: /codexspec:specify I want to build a task management app

AI:  Great! Let me help you clarify the requirements.

     First, who are the target users for this app?
     - Individual professionals
     - Small teams
     - Enterprise organizations
     - All of the above

You: Small teams, mainly software development teams

AI:  Got it. For small dev teams:
     - Do you need real-time collaboration features?
     - Should tasks support sub-tasks or just flat lists?
     - Any integration requirements (GitHub, Slack, etc.)?

You: Real-time is important. Sub-tasks yes. GitHub integration would be nice.

AI:  [Continues exploring requirements...]

     Summary of clarified requirements:
     - Target: Small dev teams (5-20 people)
     - Core: Tasks with sub-tasks, real-time updates
     - Integration: GitHub (optional)
     - Priority: Real-time collaboration > Sub-tasks > GitHub

     Ready to generate the spec document?
     Use /codexspec:generate-spec to create spec.md
```

**사용 팁：**

- 초기 요구사항 탐색에 사용하세요
- 완벽할 필요는 없습니다. 반복해서 다듬어 가면 됩니다
- AI가 가정하면 질문하세요
- spec 생성 전에 요약을 검토하세요

---

### `/codexspec:blueprint`

개발 전에 확정된 요구사항을 여러 개 준비하려면 `blueprint`를, 그 대기열을 개발하려면 `auto-dev`를 사용하세요.

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

블루프린트의 요구사항 논의에서는 사용자가 정해야 할 방향, 선택, 제약을 해결한 다음 요구사항을 대기열에 넣습니다.
공유 `.codexspec/blueprint.md`에서는 `pending`, `in_progress`, `completed` 상태를 사용합니다.
대기 중인 요구사항은 추가, 교체, 삭제하거나 순서를 바꿀 수 있습니다. 진행 중이거나 완료된 항목은 블루프린트 관리 작업에서 읽기 전용입니다.

Auto-dev는 문서에 나온 순서대로 개발하며, 진행 중인 기능이 있으면 다른 기능을 시작하기 전에 재개합니다.
기능이 완료될 때마다 대기열을 다시 읽으므로 새로 추가한 대기 작업도 현재 실행에서 처리할 수 있습니다.
확정된 요구사항의 범위 안에서 SDD 단계, 구현, 검증, 리뷰, 수정을 수행합니다.
`auto-dev`를 호출하면 `workflow.auto_next`와 관계없이 자동화가 활성화되며, 이 설정 자체는 바꾸지 않습니다.

두 명령어는 `codexspec/auto-dev` 브랜치의 `worktree-for-codexspec-auto-dev`를 공유합니다.
공통 소유권 관리와 쓰기 보호에 따라 동시에 사용할 수 있지만, 요구사항 개발은 그 작업 공간에서 순차적으로 진행합니다.
확정된 요구사항만으로 정할 수 없는 제품 결정이 필요하면, 일반적인 자율 실행 중에는 질문하지 않고 근거를 제시한 뒤 실행을 멈춥니다.

현재 공유 블루프린트를 변경하지 않고 확인하려면 다음을 실행합니다.

```bash
codexspec show-blueprint
```

---

### `/codexspec:generate-spec`

확인된 요구사항으로 추적 가능한 명세서를 작성하고 자동 검토를 실행합니다.

**구문：**

```
/codexspec:generate-spec
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| 기능 경로 | 아니요 | 명시적인 기능 디렉토리, `requirements.md` 또는 대상 `spec.md`. 해석이 모호할 때 필요 |

**동작：**

- 선택된 기능 워크스페이스에서 확정된 요구사항을 읽음
- `spec.md`만 있는 레거시 워크스페이스도 지원 (추적 가능성 경고 포함)
- 포괄적인 `spec.md` 생성:
  - 기능 개요와 목표
  - 인수 조건이 포함된 사용자 스토리
  - 기능 요구사항 (REQ-XXX 형식)
  - 비기능 요구사항 (NFR-XXX 형식)
  - 엣지 케이스와 처리 방식
  - 범위 외 항목
- 요구사항 ID로 되돌아가는 `Sources` 참조 추가
- 권위 충돌을 가정으로 해결하지 않고 사용자 확인을 위해 정지
- 증거 기반 결함을 최대 두 라운드까지 자동 리뷰 및 수정 가능

**생성 파일：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**예제：**

```text
You: /codexspec:generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec:review-spec
     - Or proceed to /codexspec:spec-to-design
```

---

### `/codexspec:spec-to-design`

확인된 `requirements.md`와 `spec.md`, 프로젝트 원칙, 관련 저장소 사실을 읽습니다. 컴포넌트, 인터페이스, 데이터 흐름, 대안과 결정을 상위 요구사항에 연결한 `design.md`를 만들고 `review-design`을 자동 실행합니다. 설계 선택이 확인된 의도를 바꾸거나 사용자의 새 결정이 필요하면 진행을 멈춥니다.

```text
/codexspec:spec-to-design <feature-dir>
```

---

### `/codexspec:design-to-plan`

확인된 설계를 구현 계획으로 변환합니다. 먼저 `spec-to-design`을 실행해 아키텍처, 구성 요소, 인터페이스와 기술 선택을 정의합니다.

```text
/codexspec:design-to-plan [design.md | spec.md | feature-directory]
```

`requirements.md`, `spec.md`, `design.md`와 프로젝트 헌법을 읽고 구현 단계, 순서와 검증 방법을 계획합니다. 시스템을 다시 설계하지 않고 기존 설계를 참조합니다. 각 계획 구성 요소에는 `Covers: REQ-xxx; Design: <design component>`를 명시합니다.

`plan.md`를 생성하고 `review-plan`을 실행합니다. `auto_next`가 활성화되어 있으면 리뷰 통과 후 `plan-to-tasks`로 진행합니다. 확인된 의도를 바꾸는 결정에는 사용자 확인이 필요합니다. 명시적 경로를 우선하고 그다음 현재 기능 브랜치를 사용하며, 기능이 모호하면 선택을 요청합니다. `design.md`가 없는 기존 기능은 계속 `spec.md`를 바탕으로 계획할 수 있습니다.

---

### `/codexspec:plan-to-tasks`

기술 계획을 실행 가능한 태스크로 분해하며, 명시적인 커버리지와 검증 가능한 결과물을 제공합니다.

**구문：**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `paths` | 아니요 | spec과 plan 경로 (제공하지 않으면 자동 감지) |

**동작：**

- 검증 가능한 하나의 결과물을 갖는 태스크를 생성. 한 태스크는 밀접하게 관련된 여러 파일을 다룰 수 있음
- 계획, 헌법, 확정된 필요사항 또는 위험이 요구할 때만 테스트 우선 순서를 적용
- 태스크가 진정으로 독립적인 경우에만 `[P]` 표시
- 각 태스크에 대해 정확한 파일 경로를 명시
- 계획과 요구사항 ID로 향하는 `Covers` 링크 추가

**생성 파일：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # Task breakdown
```

**작업 구조：**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**예제：**

```text
You: /codexspec:plan-to-tasks

AI:  Breaking down plan into tasks...

     ✓ Created tasks.md
     Total: 24 tasks
     Parallelizable: 8 tasks (33%)

     Phase 1: Foundation (4 tasks)
     Phase 2: Core Implementation - TDD (10 tasks)
     Phase 3: Integration (4 tasks)
     Phase 4: Interface Layer (3 tasks)
     Phase 5: Testing & Documentation (3 tasks)

     Execution Order:
     Phase 1 → [Phase 2 tasks in parallel groups] → Phase 3 → Phase 4 → Phase 5

     Checkpoints defined at each phase boundary.
```

**사용 팁：**

- 각 태스크는 검증 가능한 하나의 결과물을 낳고, 밀접하게 관련된 파일을 다룰 수 있습니다
- 테스트 태스크는 test-first가 요구될 때만 구현에 앞섭니다
- `[P]`는 진정으로 독립적인 병렬화 가능 태스크에만 표시됩니다
- 구현 전에 의존성을 검토하세요

작업을 작성한 뒤 `review-tasks`를 실행합니다. 결과가 `PASS` 또는 `PASS_WITH_WARNINGS`이면 `analyze`를 한 번 실행하며, 이 분석이 별도의 완료 게이트를 추가하지는 않습니다. 작업은 확인된 요구사항, 명세, 설계, 계획을 모두 포괄해야 합니다.

---

### `/codexspec:implement-tasks`

태스크 수행, 결과 검증, 리뷰와 수정.

```text
/codexspec:implement-tasks <feature-dir>
```

네 가지 산출물 리뷰어 `review-spec`, `review-design`, `review-plan`, `review-tasks`는 충실도, 요구사항 충족 범위, 실현 가능성, 내부 품질을 확인합니다.
생성 후 자동으로 실행되며 수동으로 호출할 수도 있습니다. 보고서는 검증된 결함과 통과 여부에 영향을 주지 않는 위험 권고 및 설계 개선안을 구분하고, 적합도 점수도 제공합니다.

`review-code`는 선택한 변경에 적용되는 별도의 결함 게이트와 명시적인 코드 전체 품질 평가를 제공합니다.

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

기본 리뷰 대상은 기능 브랜치의 전체 변경분입니다. 커밋된 변경, 스테이징된 변경, 스테이징되지 않은 변경, Git 무시 대상이 아닌 미추적 변경이 모두 포함됩니다.
커밋된 변경, 미커밋 변경, 단일 커밋 중 하나를 명시적으로 선택할 수도 있습니다.
`--feature`는 요구사항 맥락을 추가하지만 Git 범위를 좁히지는 않습니다.
`--audit`는 지정된 경로를 평가하고 완료 판정 대신 권고용 평가표를 작성합니다.

리뷰는 `.codexspec/review-code/`에서 공통 기준을 읽고, 관련 동작 관점과 언어·프레임워크 검사를 선택합니다.
지적에는 구체적인 근거, 실제로 발생할 수 있는 조건, 선택한 변경에서 비롯되었다는 설명, 영향이 필요합니다.
리뷰어는 파일을 편집하지 않고 결함과 근거가 있는 유지보수 제안을 보고합니다. 수정을 수행하는 호출자는 이를 독립적으로 검증합니다.

구현할 때 코드 태스크는 테스트를 먼저 작성하고, 문서와 설정은 직접 변경한 뒤 적절한 검사를 수행합니다.
수정 후의 점진적인 재리뷰에서는 영향을 받지 않은 범위의 확인 결과를 재사용할 수 있습니다.
최종 승인을 받으려면 새로 수행한 기능 전체 리뷰에서 `PASS`를 받아야 하며, 대상 범위 확인과 검증이 완료되고,
인정된 P0–P3 결함이 하나도 남지 않아야 합니다. 근거가 있는 유지보수 제안은 별도로 보고합니다.

`workflow.auto_maintenance`의 기본값은 **true**입니다.
수정을 수행하는 호출자가 검증되었으며 호환성을 유지하는 유지보수 개선도 적용할지 이 설정으로 제어합니다.
꺼도 제안은 계속 보고하며, 결함 수정이나 필수 검사가 면제되지는 않습니다.
단계 자동 진행과는 별개이며 `implement-tasks`의 인수가 아닙니다.

근본 원인부터 조사하는 디버깅에는 다음 명령어를 사용합니다.

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug는 조사 → 패턴 분석 → 단일 가설 검증 → 실패하는 테스트를 먼저 작성한 뒤 수정하는 순서로 진행합니다.
구현 중 수정이 막히거나, 단순하지 않은 동작상 결함의 원인을 추적해야 하거나,
같은 유형의 근본 원인이 여러 리뷰 라운드에서 재발하면 이 절차로 전환합니다.
수정이 세 번 실패하면 아키텍처를 재검토합니다.

요구사항의 명확성, 완전성, 일관성을 평가하려면 `checklist`를 사용하세요.

```text
/codexspec:checklist Check the authentication requirements for completeness
```

리뷰 대상을 선택하는 방법, 인수, 자세한 절차는 [명령어 참조](commands.md)를 참고하세요.

---

### `/codexspec:auto-dev`

확정된 블루프린트 요구사항을 문서에 나온 순서대로 자율 개발.

참고 [`blueprint`](#codexspecblueprint).

```text
/codexspec:auto-dev
```

---

### `/codexspec:review-spec`

명세서를 확정된 요구사항과 대조하고, 그 자체의 내적 품질을 검증합니다.

**구문：**

```
/codexspec:review-spec [path_to_spec.md]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `path_to_spec.md` | 아니요 | spec 파일 경로 (제공하지 않으면 자동 감지) |

**동작：**

- 확정된 `requirements.md` 항목에 대한 충실도 점검
- 내적 일관성, 명확성, 검증 가능성 점검
- 권위 있는 콘텐츠가 필요로 할 때만 누락된 템플릿 섹션을 결함으로 간주
- 각 결함은 `Evidence`, `Location`, `Mismatch`, `Impact`, `Remediation`을 포함해야 함
- `Risk Advisories / Design Opportunities`를 결함과 분리
- 분류된 발견 사항으로부터 도출된 상태와 호환성 점수를 생성

**공통 검토 규칙：**

| 분류 | 의미 |
|----------|---------|
| 상위 근거와의 불일치 | 권위 있는 소스와 충돌하거나 이를 누락 |
| 내부 결함 | 내적으로 모순되거나, 실행 불가능하거나, 검증 불가능 |
| 권고 | 현재 결함의 증거 없이 제시되는 선택적 개선 |

상태는 `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION`, `BLOCKED` 중 하나입니다. 권고는 상태나 점수를 결코 변경하지 않습니다.

**예제：**

```text
You: /codexspec:review-spec

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning SPEC-001
     Evidence: CON-002 requires a measurable response-time limit.
     Location: spec.md, REQ-006
     Mismatch: "Respond quickly" has no measurable threshold.
     Impact: Acceptance cannot be verified.
     Remediation: Ask the user to confirm a threshold, update requirements.md,
                  then synchronize REQ-006.

     Risk Advisories / Design Opportunities:
     - None
```

**사용 팁：**

- `/codexspec:spec-to-design` 이전에 실행하세요
- `BLOCKED`와 `NEEDS_REVISION`은 진행할 준비가 안 된 상태로 취급하세요
- 권고를 요구사항으로 끌어올리지 마세요
- 수정한 뒤에 다시 실행하세요

---

### `/codexspec:review-design`

확인된 요구사항과 명세를 기준으로 `design.md`의 충실성, 실현 가능성, 계획 단계로 넘어갈 준비가 되었는지를 검토합니다. 근거가 있는 결함과 선택적인 설계 개선을 구분해 보고하며, 다른 산출물 검토와 동일한 상태 및 수정 횟수 제한을 적용합니다.

```text
/codexspec:review-design <feature-dir>
```

---

### `/codexspec:review-plan`

기술 구현 계획의 충실도, 실현 가능성, 그리고 정당화된 기술 결정을 리뷰합니다.

**구문：**

```
/codexspec:review-plan [path_to_plan.md]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `path_to_plan.md` | 아니요 | plan 파일 경로 (제공하지 않으면 자동 감지) |

**동작：**

- `Covers` 링크와 필수 spec 커버리지 검증
- 적용 가능한 헌법 규칙과 검증된 저장소 사실 점검
- 구체적인 비용이나 충돌을 유발하는 경우에만 근거 없는 복잡성을 문제로 보고
- 모든 결함에 증거 필드를 요구하고 동일한 근본 원인을 가진 발견 사항은 병합
- 선택적 아키텍처 개선 사항은 권고로 보고
- 공유 상태 및 호환성 점수 계약을 사용

**예제：**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**사용 팁：**

- `/codexspec:plan-to-tasks` 이전에 실행하세요
- 태스크 생성 전에 증거 기반 결함을 해결하세요
- 추측성 아키텍처 아이디어는 권고 섹션에 두세요
- 기술 스택이 팀 역량과 맞는지 확인하세요

계획은 확인된 `design.md`를 구현하기 위한 것으로, 아키텍처 선택을 다시 결정하지 않습니다. 검토에서는 요구사항 범위와 함께 계획이 설계를 올바르게 참조하는지도 확인합니다.

---

### `/codexspec:review-tasks`

태스크 분해의 커버리지, 검증 가능한 결과물, 올바른 순서, 실현 가능한 의존성을 검증합니다.

**구문：**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `path_to_tasks.md` | 아니요 | tasks 파일 경로 (제공하지 않으면 자동 감지) |

**동작：**

- 필수 plan 항목과 요구사항이 모두 태스크로 커버되는지 점검
- 권위 있는 소스가 요구할 때만 테스트 우선 순서를 검증
- 각 태스크가 검사 가능한 하나의 결과물을 갖는지 확인
- 의존성 검증 (사이클 없음, 올바른 순서)
- 병렬화 마커 검토
- 파일 경로 검증
- 모든 결함에 증거 필드 요구
- 선택적 프로세스 개선 사항은 권고로 보고
- 공유 상태 및 호환성 점수 계약을 사용

**예제：**

```text
You: /codexspec:review-tasks

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning TASK-001
     Evidence: Task 2.5 declares a dependency on Task 2.4.
     Location: tasks.md, Task 2.5
     Mismatch: Task 2.5 is also marked [P].
     Impact: Parallel execution can start before its prerequisite completes.
     Remediation: Remove [P] or remove the dependency if the plan proves independence.
```

**사용 팁：**

- `/codexspec:implement-tasks` 이전에 실행하세요
- 테스트 순서 발견 사항은 권위 있는 소스가 테스트를 요구할 때만 결함입니다
- 병렬화 마커가 정확한지 확인하세요
- 파일 경로가 프로젝트 구조와 일치하는지 검증하세요

---

### `/codexspec:clarify`

기존 명세서에서 모호한 부분과 누락 사항을 스캔합니다. 초기 명세 생성 후의 반복적인 개선에 사용하세요.

**구문：**

```
/codexspec:clarify [path_to_spec.md]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `path_to_spec.md` | 아니요 | spec 파일 경로 (제공하지 않으면 자동 감지) |

**동작：**

- 초점이 맞춰진 모호성 카테고리로 요구사항과 spec을 스캔
- 핵심을 짚는 구체적인 질문 (최대 5개)
- 사용자 확인 후 `requirements.md`를 먼저 갱신하고, 이어서 `spec.md`를 동기화
- review-spec 결과가 있으면 통합

**모호성 분류：**

| 분류 | 확인 항목 |
|----------|-----------------|
| **정보 누락** | 누락된 섹션, 빈 콘텐츠, 부재한 인수 조건 |
| **구체성 부족** | 모호한 용어("fast", "scalable"), 정의되지 않은 제약 |
| **동작의 명확성** | 에러 처리 누락, 정의되지 않은 상태 전이 |
| **측정 가능성 문제** | 측정 지표가 없는 비기능 요구사항 |

**예제：**

```text
You: /codexspec:clarify

AI:  Scanning spec.md for ambiguities...

     Found issues in 3 categories.

     ## Question 1/5: Specificity

     **Context**: NFR-001 states "System should respond quickly"

     **Question**: What is the target response time?

     | Option | Description | Impact |
     |--------|-------------|--------|
     | A | < 100ms for all operations | High performance requirement |
     | B | < 500ms for reads, < 1s for writes | Balanced approach |
     | Custom | Provide a different answer | - |

     **Recommendation**: Option B - balanced for typical web app

You: B

AI:  ✓ Updated NFR-001: Response time < 500ms reads, < 1s writes
     Added to Clarifications section in spec.md
```

**사용 팁：**

- spec.md가 있지만 다듬어야 할 때 사용하세요
- `/codexspec:review-spec` 결과와 통합됩니다
- 실행 한 번당 최대 5개 질문
- 복잡한 명세서는 여러 번 실행하세요

---

### `/codexspec:analyze`

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

기존 기능에 `requirements.md`가 없으면 `spec.md`부터 분석하고 원래 논의의 근거가 없음을 밝힙니다. 이 경우 산출물을 수정하지 않고 결과만 보고합니다. 기존 `design.md`가 없어도 분석할 수 있습니다.

---

### `/codexspec:checklist`

요구사항의 완전성, 명확성, 일관성을 검증하기 위한 품질 체크리스트를 생성합니다. 이것은 "요구사항 작성을 위한 단위 테스트"입니다.

**구문：**

```
/codexspec:checklist [focus_area]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `focus_area` | 아니요 | 도메인 초점 (예: "ux", "api", "security", "performance") |

**동작：**

- 품질 차원별로 구성된 체크리스트 생성
- `FEATURE_DIR/checklists/` 디렉토리에 체크리스트 생성
- 항목은 구현 테스트가 아닌 요구사항 품질에 초점

**품질 기준：**

- **요구사항 완전성**: 필요한 요구사항이 모두 있는가?
- **요구사항 명확성**: 요구사항이 구체적이고 모호하지 않은가?
- **요구사항 일관성**: 요구사항이 충돌 없이 정합하는가?
- **인수 조건 품질**: 성공 기준이 측정 가능한가?
- **시나리오 범위**: 모든 흐름/사례가 다뤄졌는가?
- **경계 사례 범위**: 경계 조건이 정의되었는가?
- **비기능 요구사항**: 성능, 보안, 접근성이 명시되었는가?
- **의존성과 가정**: 문서화되었는가?

**체크리스트 유형 예：**

- `ux.md` - 시각적 위계, 상호작용 상태, 접근성
- `api.md` - 에러 형식, 속도 제한, 인증
- `security.md` - 데이터 보호, 위협 모델, 침해 대응
- `performance.md` - 지표, 부하 조건, 성능 저하

**예제：**

```text
You: /codexspec:checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

     ## Security Requirements Quality Checklist

     ### Authentication Requirements
     - [ ] CHK001 - Are authentication requirements defined for all protected endpoints? [Completeness]
     - [ ] CHK002 - Is password complexity explicitly specified? [Clarity]
     - [ ] CHK003 - Are session timeout requirements quantified? [Measurability]

     ### Data Protection
     - [ ] CHK004 - Are data encryption requirements specified at rest? [Completeness]
     - [ ] CHK005 - Are data encryption requirements specified in transit? [Completeness]
     - [ ] CHK006 - Is PII handling explicitly documented? [Clarity]

     Total: 15 items across 4 categories
```

**사용 팁：**

- 체크리스트는 구현 정확성이 아닌 요구사항 품질을 검증합니다
- 요구사항 리뷰와 개선에 사용하세요
- 초점을 맞춘 검증을 위해 도메인 특화 체크리스트를 만드세요
- 기술 계획으로 넘어가기 전에 실행하세요

---

### `/codexspec:tasks-to-issues`

`tasks.md`의 태스크를 GitHub 이슈로 변환하여 프로젝트 추적과 협업에 활용합니다.

**구문：**

```
/codexspec:tasks-to-issues
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| 없음 | - | 현재 기능의 모든 태스크를 변환 |

**동작：**

- 태스크 ID, 설명, 의존성, 파일 경로를 파싱
- 구조화된 본문으로 GitHub 이슈 생성
- 태스크 유형(setup, implementation, testing, documentation)에 따라 라벨 추가
- 이슈 간 의존성 연결
- URL과 함께 생성된 이슈 보고

**사전 조건：**

- GitHub remote가 있는 Git 리포지토리
- GitHub CLI(`gh`) 설치 및 인증 완료
- `tasks.md` 파일 존재

**예제：**

```text
You: /codexspec:tasks-to-issues

AI:  Converting tasks to GitHub issues...

     Repository: github.com/example/taskman

     Creating issues:
     ✓ #42: Task 1.1 - Setup Project Structure (setup)
     ✓ #43: Task 2.1 - Write Tests for Task Entity (testing)
     ✓ #44: Task 2.2 - Implement Task Entity (implementation)
     ...

     Summary:
     - Issues created: 24
     - Labels applied: setup(4), implementation(12), testing(5), documentation(3)
     - Dependencies linked: 18

     View issues: https://github.com/example/taskman/issues
```

**사용 팁：**

- GitHub CLI 인증이 필요합니다 (`gh auth login`)
- GitHub 리포지토리에서만 동작합니다
- 리포지토리의 기본 설정으로 이슈를 생성합니다
- 실행 전에 중복을 확인하세요

issue를 만들기 전에 원격 정보와 대조해 대상 저장소를 확인하고 명시적인 허가를 받아야 합니다. 작업 목록을 생성했다고 해서 게시까지 허가된 것은 아닙니다.

---

### `/codexspec:debug`

수정하기 전에 근본 원인 조사.

참고 [워크플로](workflow.md#review-and-debugging).

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

---

### `/codexspec:reverse-spec`

기존 코드에는 목적에 따라 두 가지 명령어를 사용합니다.

| 명령어 | 용도 | 산출물과 작업 범위 |
|---------|-----------|-----------------|
| `onboard [path]` | 기존 코드베이스에서 재사용할 수 있는 프로젝트 지식을 초기 등록 | 관례 후보와 근거에 따라 범위를 한정한 제약을 프로파일에 기록. 코드는 읽기 전용 |
| `reverse-spec [path]` | 기존 아키텍처를 이해하거나 확정된 의도와 코드를 비교 | 산출물 초안 또는 차이 보고서. 코드는 읽기 전용 |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard는 관찰할 수 있는 코드에서 관례를 추론하며, 명시적인 금지 사항이 있을 때만 제약을 제안합니다.
관례 후보는 로컬에 즉시 적용됩니다. 제약 후보는 세션 안에서 저장·편집·제외 여부를 결정해야 합니다.
기존 지식은 보존합니다. 처음 수행하는 코드 스캔만으로 과거 결정의 이유나 실제로 경험했는지 알 수 없는 함정을 지어내지 않습니다.

Reverse-spec에는 세 가지 모드가 있습니다.

- **개요**: 경로를 지정하지 않거나 리포지토리 루트를 지정한 경우입니다. 조사할 모듈을 선택할 수 있도록 아키텍처의 요점을 담은 `design.md`와 `slices.md`를 만듭니다.
- **생성**: 확정된 기준이 없는 모듈 경로를 지정한 경우입니다. `spec.md`, `design.md`, 미확정·추론 단계의 요구사항을 초안으로 만듭니다.
- **대조**: 확정된 기준이 있는 모듈을 지정한 경우입니다. `reconcile.md`를 만들고,
  확정된 명세·설계와 비교해 문서화되지 않은 동작, 구현되지 않은 명세, 의미 불일치를 보고합니다. 제품 의도는 요구사항을 기준으로 판단합니다.

추론으로 만든 초안은 사람이 확인해야 기준으로 사용할 수 있습니다.
대조에서는 코드 수정, 문서 업데이트, 의도 결정 중 어느 방향으로 진행할지 제안하며, 이를 자동으로 적용하지는 않습니다.

---

### `/codexspec:distill`

재사용 가능한 여러 기능에서 활용할 수 있는 지식을 `.codexspec/profile/`에 담고, 보류 중인 후보를 Markdown 파일을 직접 편집하지 않고 검토합니다.

**구문：**

```text
/codexspec:distill [interaction segment]
/codexspec:distill review
```

**수동 검토：**

- `/codexspec:distill review` 또는 추출할 새로운 내용이 없는 직접 호출은 `127.0.0.1`에서만 제공되는 오프라인 HTML 페이지를 엽니다. 헤더에 이 세션이 기록할 프로젝트 디렉터리 이름이 표시되므로, 나란히 열어 둔 두 검토를 혼동할 수 없습니다.
- 페이지는 구조화된 수정, 승인, 폐기, 보류, 통합, 스테이징된 결정의 전체 요약, 그리고 명시적인 **모두 적용**을 지원합니다. 수정과 병합은 같은 동작을 스테이징하기 전에 최종 Markdown의 정확한 미리보기를 보여야 합니다. 결정 컨트롤을 사용하기 전에, 각 레코드가 세 가지 미리보기 상태 중 어디에 있는지(미리보기 안 됨 / 현재 편집과 일치 / 미리보기 이후 변경됨)를 페이지가 알려 줍니다.
- 레코드 파일을 삭제하는 모든 동작은 그 결과를 밝히는 2차 확인을 요구합니다. 폐기는 적용 시 삭제될 파일을, 병합은 삭제될 통합 대상 레코드 수를, 초안 폐기는 사라질 스테이징된 결정 수를 알려 줍니다.
- 레코드는 사람의 승인과 결과 기반 검증 근거가 모두 있어야 `vetted`가 됩니다. 승인을 고르기 전에 저장된 근거가 이미 그 요건을 충족하는지 페이지가 보여 줍니다.
- 대기열은 결정된 내용으로 레코드를 묶고, 보류 중인 레코드 가운데 몇 건이 이미 정리되었는지 보여 줍니다. 결정을 스테이징하면 다음 미결정 레코드로 이동하며, 헤더의 스위치로 끌 수 있습니다.
- 페이지는 키보드로 조작할 수 있습니다. `?`를 누르면 키 목록이 나옵니다. 일괄 적용, 세션 취소, 초안 폐기를 단일 키로 수행하지는 않습니다.
- 스테이징된 결정은 Git에서 제외된 복구 가능한 프로젝트 초안에 보관됩니다. 쓰기 가능한 검토는 프로젝트당 하나만 활성화됩니다.
- 구조가 손상된 초안은 해결 방법을 안내하는 진단과 함께 보존되며, 명시적인 폐기 동작으로만 제거됩니다.
- 적용 시 원본 해시를 다시 확인하고, 레코드가 하나라도 변경되었으면 배치 전체를 거부합니다. 동시 편집을 덮어쓰거나 부분 성공을 보고하지 않습니다.
- 페이지 리소스은 모두 CodexSpec과 함께 배포됩니다. CDN, 원격 모델 호출, 텔레메트리를 쓰지 않습니다.
- 브라우저를 열 수 없으면 토큰으로 보호된 로컬 URL을 출력합니다. 브라우저가 적절하지 않을 때는 명시적인 텍스트 모드를 요청하세요. 검증과 쓰기 경로는 동일합니다.

자동 distill은 비대화식이고 차단하지 않습니다. 페이지를 열거나, 텍스트 검토를 시작하거나, 저장된 초안을 기다리지 않습니다.

---

### `/codexspec:evolve`

`evolve`는 검토·승인된 지식 중 프로젝트 밖에서도 유용한 것만 선택해 명령어·스킬 초안으로 정리합니다.
푸시하거나 사람이 리뷰할 기여 PR을 만들기 전에 명시적인 승인을 받습니다.

```text
/codexspec:evolve
```

---

### `/codexspec:onboard`

기존 코드에서 관례 후보와 근거가 있는 제약 초기 등록.

참고 [`reverse-spec`](#codexspecreverse-spec).

```text
/codexspec:onboard src/
```

---

### `/codexspec:commit-staged`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged**는 스테이징 영역의 실제 내용을 분석해 Conventional Commits 메시지를 생성합니다.
  `-p`는 커밋하지 않고 미리 보는 옵션입니다. 파일 선택과 스테이징은 호출한 워크플로우가 수행합니다.
  승인된 실행에서는 보호된 런타임을 사용해 커밋할 내용이 분석 대상과 일치하는지 다시 확인합니다.
  에이전트 커밋 지침은 일반 대화, SDD, blueprint, auto-dev에도 적용됩니다.
  명령어를 사용할 수 있다는 사실만으로 호출이 이루어지거나 커밋 권한이 부여되는 것은 아닙니다.
- **pr**은 변경분에서 구조화된 GitHub PR 또는 GitLab MR 설명을 생성합니다.
  `--spec`을 지정하면 `spec.md` 파일 경로, 또는 그 파일로 연결되는 기능 디렉터리 이름이나 접두사를 통해 기능 맥락을 추가할 수 있습니다.
  기본 출력은 호스팅 플랫폼에서 사용할 텍스트입니다.
- **release-notes**는 Git 이력에서 Keep a Changelog 항목과 릴리스 본문을 작성합니다.
  기본 섹션은 `[Unreleased]`이며, `--version`을 지정하면 제공한 라벨을 사용합니다.
  스테이징, 커밋, 버전 변경, 태그, 게시, 릴리스 생성을 수행하지 않습니다.
- **tasks-to-issues**는 기존 태스크에서 의존성과 수용 기준을 포함한 GitHub 이슈를 생성합니다.
  인증된 GitHub CLI가 필요합니다. 이슈 리포지토리가 설정된 원격과 일치하는지도 검증합니다.

커밋 미리보기나 승인된 커밋을 현재 체크아웃에서 실행하려면 Python 3.11+와 Git이 필요합니다.
런타임은 CLI로 초기화한 프로젝트에 설치되며 Claude 플러그인에도 포함됩니다.
에이전트가 생성하는 병합 중 내용 변경을 포함하는 병합도 스테이징 분석을 사용합니다.
이력만 연결하는 병합은 트리와 부모를 검증하면서 Git의 기본 메시지를 유지합니다.
fast-forward는 커밋을 만들지 않습니다.

공통 도우미 `.codexspec/scripts/commit-staged-helper.py` 또는 플러그인에 포함된 사본은 Python 3.11+와 Git이 필요합니다. LLM을 호출하지 않고 Git hooks를 유지하며, 분석 후 스테이징된 내용이 바뀌면 커밋을 거부합니다. 일회성 초기화로도 이 런타임이 설치되지만 작업 공간 라우팅, blueprint, auto-dev에는 계속 CLI가 필요합니다.

---

### `/codexspec:pr`

git diff로부터 구조화된 GitHub Pull Request / GitLab Merge Request 설명을 생성합니다. 선택적으로 `spec.md`를 통합해 SDD 추적 컨텍스트를 제공합니다.

**구문：**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `--target-branch <branch>` | 아니요 | 비교 대상 브랜치 (기본값: `origin/main`) |
| `--sections <list>` | 아니요 | `summary, changes, testing, verify, checklist, notes`의 쉼표로 구분된 부분 집합 (기본값: `all`) |
| `--spec <id-or-path>` | 아니요 | 옵트인 spec 통합: `.codexspec/specs/` 아래에서 해석되는 기능 id(예: `2025-0321-1430k7-auth`) 또는 명시적인 `path/to/spec.md`. 생략하면 git만으로 생성 |
| `--output <file>` | 아니요 | 터미널 대신 파일로 설명을 저장 |

**동작：**

- 대상 브랜치를 기준으로 git 컨텍스트 수집 (현재 브랜치, remote URL, 앞선 커밋, 파일 변경 사항, 전체 diff, 커밋 메시지)
- remote URL로부터 플랫폼 자동 감지: GitHub → "Pull Request", GitLab → "Merge Request", 기타/없음 → GitHub 용어로 기본화하고 경고
- `.codexspec/memory/constitution.md`가 있으면 불러와서 설명을 문서/코드 리뷰 표준에 맞춤
- 설명 언어로 `language.commit`(그다음 `language.output`, 그다음 영어)을 존중. 기술 용어(API, JWT, PR, MR)는 적절한 경우 영어로 유지
- `--spec`이 주어지면 spec.md에서 가져온 사용자 스토리와 요구사항으로 Context 섹션을 추가. 그렇지 않으면 diff만으로 생성
- `--sections`에 따라 섹션을 출력 (Summary, Changes, Testing, Verification Steps, Pre-merge Checklist, Notes / Breaking Changes)

**예제：**

```text
You: /codexspec:pr --spec 2026-0613-1200ab-task-management

AI:  Generating Pull Request description...

     Platform: GitHub (github.com/example/taskman)
     Branch:   feature/task-management  →  origin/main
     Commits:  8 ahead

     ## Pull Request: Task management for small dev teams

     ### Context
     - User stories and REQ-* pulled from spec.md

     ### Summary
     - Adds task CRUD, sub-tasks, and real-time updates

     ### Changes
     - src/taskman/models/task.py (new)
     - src/taskman/api/tasks.py (new)
     - ...

     ### Verification Steps
     1. `uv run pytest`
     2. `uv run codexspec check`
```

**사용 팁：**

- 공식 명세가 없는 작은 버그 수정이나 변경에는 `--spec`을 생략하세요
- `/codexspec:commit-staged`와 조합해 같은 작업으로부터 커밋 메시지와 PR 설명을 함께 만들 수 있습니다
- 이 명령어의 엔드투엔드 실전 사례(spec.md 컨텍스트가 어떻게 연결되는지 포함)는 [PR description generator case study](../case-studies/case-study-pr-description-generator.md)를 참고하세요

---

### `/codexspec:release-notes`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged**는 스테이징 영역의 실제 내용을 분석해 Conventional Commits 메시지를 생성합니다.
  `-p`는 커밋하지 않고 미리 보는 옵션입니다. 파일 선택과 스테이징은 호출한 워크플로우가 수행합니다.
  승인된 실행에서는 보호된 런타임을 사용해 커밋할 내용이 분석 대상과 일치하는지 다시 확인합니다.
  에이전트 커밋 지침은 일반 대화, SDD, blueprint, auto-dev에도 적용됩니다.
  명령어를 사용할 수 있다는 사실만으로 호출이 이루어지거나 커밋 권한이 부여되는 것은 아닙니다.
- **pr**은 변경분에서 구조화된 GitHub PR 또는 GitLab MR 설명을 생성합니다.
  `--spec`을 지정하면 `spec.md` 파일 경로, 또는 그 파일로 연결되는 기능 디렉터리 이름이나 접두사를 통해 기능 맥락을 추가할 수 있습니다.
  기본 출력은 호스팅 플랫폼에서 사용할 텍스트입니다.
- **release-notes**는 Git 이력에서 Keep a Changelog 항목과 릴리스 본문을 작성합니다.
  기본 섹션은 `[Unreleased]`이며, `--version`을 지정하면 제공한 라벨을 사용합니다.
  스테이징, 커밋, 버전 변경, 태그, 게시, 릴리스 생성을 수행하지 않습니다.
- **tasks-to-issues**는 기존 태스크에서 의존성과 수용 기준을 포함한 GitHub 이슈를 생성합니다.
  인증된 GitHub CLI가 필요합니다. 이슈 리포지토리가 설정된 원격과 일치하는지도 검증합니다.

커밋 미리보기나 승인된 커밋을 현재 체크아웃에서 실행하려면 Python 3.11+와 Git이 필요합니다.
런타임은 CLI로 초기화한 프로젝트에 설치되며 Claude 플러그인에도 포함됩니다.
에이전트가 생성하는 병합 중 내용 변경을 포함하는 병합도 스테이징 분석을 사용합니다.
이력만 연결하는 병합은 트리와 부모를 검증하면서 Git의 기본 메시지를 유지합니다.
fast-forward는 커밋을 만들지 않습니다.

#### 릴리스 노트 옵션

| 명령어 | 참조 |
|---|---|
| `--version <X.Y.Z>` | 지정한 버전 라벨. 생략하면 `[Unreleased]` |
| `--from <ref>` | 시작 참조. 생략하면 가장 가까운 도달 가능한 태그, 위치를 확인할 수 있는 변경 로그 버전, 전체 이력 순으로 사용 |
| `--to <ref>` | 끝 참조. 기본값은 `HEAD` |
| `--output <file>` | 릴리스 본문을 저장할 파일. 생략하면 터미널에 출력 |
| `--spec <feature>` | 선택적인 기능 컨텍스트. 기능을 찾지 못하면 알리고 Git 정보로 계속 생성 |

---

### `/codexspec:review-code`

선택한 Git 변경을 병합 전의 엄격한 결함 게이트로 검토합니다. 기본 대상은 기능의 전체 변경분이며, 명시적 선택기로 커밋됨, 커밋되지 않음 또는 단일 커밋 증거를 선택할 수 있지만 경로 필터는 허용하지 않습니다.

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**기본 검토 모드:**

- 기본 명령은 광범위한 품질 점수표가 아니라 변경 범위 결함 게이트입니다.
- 위치 경로 인수는 더 이상 유효하지 않습니다. 권고용 경로 품질 감사에는 `--audit`를 명시하세요.

**결함 게이트 구문:**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code [--committed] --incremental-from <fingerprint> [--feature <feature-dir>]
```

모든 결함 게이트 형식에 `--decided-by reviewer|ask`를 붙일 수 있으며, 해당 실행에 한해 `review.decided_by`를 재정의합니다.

<!-- REVIEW-CODE-SYSTEM-CONTRACT -->
<!-- REVIEW-CODE-VARIANT-SEARCH -->
<!-- REVIEW-CODE-NEUTRAL-HANDOFF -->

게이트는 대상의 모든 산출물을 빠짐없이 확인하고 적용 가능한 요구사항을 평가한 뒤 Scope, System Contract, Behavior, Risk, Verification의 다섯 단계를 순서대로 실행합니다. 근거가 있는 모듈 간 계약과 의미 단위 검토 파티션을 기록하며, 검증된 반복 가능 근본 원인마다 라운드가 끝나기 전에 범위가 제한된 관련 발생 위치 검색을 수행합니다. 여섯 개의 보고서 섹션 뒤에는 `schema_version: "3"`를 사용하는 기계 판독 가능한 `<review-code-result>` 결과 블록 하나가 옵니다. 이 결과 블록는 대상 식별자, 커버리지, 수정 후 객관적으로 다시 확인해야 할 사항를 전달합니다. 호출자는 이 중립적인 확인 사항를 새로운 전체 검토에 제공하지만 수정 이유나 이전의 정확성 결론은 제공하지 않습니다. 판정은 `PASS`, `FAIL`, `INCONCLUSIVE` 중 하나입니다. 모든 P0-P3 결함은 `FAIL`, 필수 증거나 커버리지 부족은 `INCONCLUSIVE`입니다.

**증분 라운드.** 수정 후에는 `--incremental-from <fingerprint>`로 해당 결과 이후에 바뀐 부분만 다시 검토합니다. 대상은 변경된 파일, 그 파일이 관련된 검토 파티션과 계약, 이전 검토에서 이어진 확인 사항입니다. 변경되지 않았고 영향도 받지 않는 파일은 이전 커버리지를 재사용하지만, 검토자는 다른 곳에서 발견한 결함도 그대로 보고합니다. 증분 `PASS`로 기능이 완료되지는 않습니다. `implement-tasks`는 먼저 전체 검토를 실행하고, 수정할 때마다 증분 검토를 실행한 뒤, 최종 인수로 새로운 전체 검토를 한 번 더 실행합니다. 검토 기록은 저장소 밖의 사용자 캐시 디렉터리(`~/.cache/codexspec/review/` 또는 `%LOCALAPPDATA%\codexspec\review\`)에 기록되며, 대화에는 보고서와 결과 블록만 표시됩니다.

**판정 모드.** `.codexspec/config.yml`의 `review.decided_by`는 트리거가 프로젝트의 실제 사용 범위 밖에 있는 결함(예: 프로젝트가 절대 받지 않는 입력)을 누가 판정할지 정합니다. 기본값 `reviewer`에서는 검토가 이전과 똑같이 동작합니다. `ask`로 설정하면 검토는 해당 항목으로 실패 처리하지 않고 보류 중인 시나리오 판정으로 보고하며, `implement-tasks`가 수정할지, 아니면 해당 시나리오를 범위 밖으로 받아들일지 한 번 묻습니다. 답변은 확정된 `CON` 또는 `OUT` 항목으로 `requirements.md`에 기록되므로 이후 라운드에서 다시 제기되지 않습니다.

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — all required review and verification completed with no findings.
```

**적용 기준과 유지보수 제안.** 모든 리뷰는 공통 규칙과 선택한 모드를 읽고 일곱 검토 차원을 평가한 뒤, 실제 동작·계약·의존 관계에 필요한 상세 체크만 불러옵니다. 추적 중 발견한 변경되지 않은 의존 코드도 언어·프레임워크 체크를 활성화할 수 있습니다. 유지보수 제안에는 현재 문제의 구체적 근거와 기존 동작을 유지하는 국소적 개선이 필요합니다. 가정한 미래 복잡도나 스타일 수치만으로 수정을 정당화할 수 없습니다. 결함 결과는 버전 3을 유지하며, 같은 대상 지문에 연결된 버전 1 `<review-code-maintenance>`에서 제안을 별도로 보고합니다. 단독 리뷰는 보고만 하고, `implement-tasks`는 `workflow.auto_maintenance`(기본 `true`)에 따라 검증하고 적용합니다. 실질적인 진전이 있는 동안 수정을 계속하되 기존 중단 조건을 따릅니다. 고정된 반복 횟수 상한은 없으며, 최종 완료 판정에는 새로운 전체 리뷰가 필요합니다.

불리언 CLI 스위치는 대소문자를 구분하지 않고 `on/true/1/yes`와 `off/false/0/no`를 받으며, 앞뒤 공백도 허용합니다.
값을 지정하지 않고 사용하면 대상 체크아웃의 현재 값을 전환합니다. YAML에는 불리언 값으로 저장합니다.

`codexspec init`은 Claude Code와 Codex가 공유하는 리뷰 리소스를 `.codexspec/review-code/`에 설치합니다. `--force`는 배포 리소스를 갱신하고 다른 경로의 확장 파일은 보존합니다. CLI 설치만으로 프로젝트 파일을 만들지는 않습니다. 플러그인만 사용할 때 프로젝트에 리소스 트리가 없으면 호스트가 해석한 플러그인 루트에서 같은 리소스를 읽습니다.

<!-- REVIEW-CODE-AUDIT -->

#### 경로 품질 감사

명시적 audit 분기는 현재 파일 전체 내용을 대상으로 언어 관례에 맞는 명확성, 정확성, 견고성, 아키텍처 및 프로젝트 헌법 준수 여부을 평가합니다. 이 점수표는 권고용이며 `implement-tasks` 완료 게이트로 사용할 수 없습니다.

**구문：**

```
/codexspec:review-code --audit [paths...]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `path...` | 아니요 | 리뷰할 하나 이상의 소스 파일 또는 디렉토리 (공백으로 구분). 생략 시 기본값은 `src/` |

**동작：**

- 파일 확장자로 주 언어를 감지하고, 다중 언어 대상에는 언어별 패스를 실행
- 해당 설정이 존재할 때 정적 분석 도구를 실행 (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`). 없으면 해당 검사를 건너뛰고 검토 범위가 줄었음을 보고
- 4개 차원을 평가: Idiomatic Clarity & Simplicity, Correctness & Explicit Contracts, Runtime Robustness & Resource Discipline, Architecture & Design Integrity
- 감지된 프레임워크에 대해 필수 하위 섹션을 주입 (예: React의 Hooks Compliance, Rust의 Ownership & Borrowing, Go의 Goroutine & Context Discipline, C/C++의 Memory & Lifetime Safety, Shell의 Execution Safety)
- `.codexspec/memory/constitution.md`가 있을 때 발견 사항을 교차 참조. 없으면 헌법 축을 제외하고 그 가중치를 재분배
- 발견 사항을 심각도로 분류: CRITICAL, HIGH, MEDIUM, LOW (LOW 제안은 총 5점 감점으로 제한)

**예제：**

```text
You: /codexspec:review-code --audit src/

AI:  # Code Review Report

     ## Summary
     - Overall Status: Needs Work
     - Quality Score: 78/100
     - Detected Language: Python

     ## Static Analysis Results
     | Tool   | Status | Issues | Details                |
     |--------|--------|--------|------------------------|
     | ruff   | Warn   | 3      | Unused imports, line length |
     | mypy   | Pass   | 0      | No type errors         |

     ## Detailed Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/auth/service.py:42 - bare `except Exception:` swallows the original cause
       Impact: Original error context is lost during debugging.
       Suggestion: narrow the exception and re-raise with `raise ... from err`.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/auth/service.py:120 - manual loop where a comprehension suffices

     ## Recommendations
     1. Priority 1: Fix CODE-001 before merge.
     2. Priority 2: Apply LOW suggestions opportunistically.
```

**사용 팁：**

- 여러 경로를 전달하면 원하는 일부만 리뷰할 수 있습니다 (예: `src/ tests/`)
- 점수는 참고용이며, CRITICAL/HIGH 발견 사항이 실행 가능한 신호입니다

---

### `/codexspec:config`

프로젝트 설정을 대화형으로 관리합니다 (생성/조회/수정/초기화). 이것은 `codexspec config` CLI의 슬래시 명령어 버전이며, Plugin Marketplace 설치에 적합합니다.

**구문：**

```
/codexspec:config [--view]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `--view` | 아니요 | 수정 없이 현재 설정을 표시. 인자가 없으면 대화형 관리 메뉴를 엽니다 |

**동작：**

- `.codexspec/config.yml`만을 대상
- `--view`(또는 "View current config" 메뉴 옵션)는 파일을 읽기 쉬운 형태로 출력. 없으면 "Configuration Not Found"를 보고
- 대화형 모드에서 설정이 있으면 View, Modify, Reset to defaults, Cancel을 제공
- 설정이 없으면 최소한의 `output` 전용 설정을 작성하는 생성 흐름을 실행 (interaction/document/commit은 `output` 그다음 `en`으로 해결되므로 `output` 전용 파일이 완전히 기능함)
- 각 언어 차원(output, interaction, document, commit)을 독립적으로 설정하고 `auto_next` 같은 워크플로우 옵션을 토글할 수 있게 함

**생성·편집 파일：**

```
.codexspec/config.yml
```

**예제：**

```text
You: /codexspec:config

AI:  ## Configuration Manager

     Configuration file found at .codexspec/config.yml.
     What would you like to do?
     - View current config
     - Modify config
     - Reset to defaults
     - Cancel

You: Modify config

AI:  Select a dimension to change:
     - Output language (base)
     - Interaction language
     - Document language
     - Commit-message language
     - workflow.auto_next
     - workflow.auto_distill
     - workflow.auto_maintenance
     - workflow.worktrees (default on; checkout-local)
     - review.decided_by

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**사용 팁：**

- 무언가를 변경하기 전에 현재 상태를 점검하려면 `/codexspec:config --view`를 사용하세요
- 새로 만들거나 초기화한 설정은 `output`만 작성합니다. `output`과 달라야 할 때만 `interaction`/`document`를 설정하세요
- 터미널에서 스크립트로 변경하려면 `codexspec config` CLI를 사용하세요 (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

대화형 메뉴에서 `workflow.auto_distill`, `workflow.auto_maintenance`, `workflow.worktrees`, `review.decided_by`도 관리할 수 있습니다. 설정 변경은 각 체크아웃에 독립적으로 적용되는 worktree 라우팅 규칙을 따릅니다.

---

### `/codexspec:quick`

작은 변경을 위한 간소화된 Requirements-First SDD 흐름을 실행합니다.

**구문：**

```
/codexspec:quick [describe a small requirement]
```

**인수：**

| 인수 | 필수 | 설명 |
|----------|----------|-------------|
| `describe a small requirement` | 아니요 | 작고 범위가 명확한 변경에 대한 짧은 설명 (제공하지 않으면 프롬프트로 묻습니다) |

**동작：**

- 범위(접하는 파일, 모듈 범위, 새 의존성, 미해결 제품 결정)를 평가하고, 변경이 광범위하거나 여러 독립적 결과물을 가지면 표준 흐름을 권장
- `/codexspec:specify`와 동일한 타임스탬프 관례로 기능 워크스페이스와 `requirements.md`를 생성
- 구현에 실질적인 영향을 주는 모호성만 해결하고, 간결한 확정 요약을 제시 (`NEED-*`, 관련 `CON-*`/`DEC-*`, `OUT-*`, 미해결 `OPEN-*`)
- Confirmation Gate에서 멈춤: 요약을 확정하기 전에는 아무것도 생성하지 않음
- 새 기능 디렉토리에 대해 생성 명령어들을 연쇄 실행: `/codexspec:generate-spec`, `/codexspec:design-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- 각 생성 명령어의 자체 자동 리뷰 루프에 위임. 리뷰가 새 제품 또는 아키텍처 결정을 필요로 하면 멈추고 사용자에게 묻습니다
- 기능 디렉토리, 산출물 경로, 리뷰 결과, 구현 검증, 미해결 권고를 분리해서 보고

**생성 파일：**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**예제：**

```text
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → design-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**사용 팁：**

- Quick은 진정으로 작고 단일 결과물인 변경에만 사용하세요. 그렇지 않으면 `/codexspec:specify`와 표준 흐름을 실행하세요
- 확정은 여전히 필요합니다. Quick은 자동화를 진행하기 위해 제품 결정을 추론하지 않습니다
- 어느 생성 리뷰가 `NEEDS_REVISION`/`BLOCKED`를 반환하면 Quick은 멈추고 제어권을 사용자에게 돌려줍니다

---
