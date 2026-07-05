# Commands

CodexSpec의 슬래시 명령어 레퍼런스입니다. 이 명령어들은 Claude Code의 채팅 인터페이스에서 호출합니다.

워크플로우 패턴과 각 명령어를 사용해야 하는 시점은 [Workflow](workflow.md)를 참고하세요. CLI 명령어는 [CLI](../reference/cli.md)를 참고하세요.

## Quick Reference

카테고리별로 분류했으며, README의 카탈로그 구성과 동일합니다. 각 그룹 안에서 명령어는 워크플로우 순서대로 배치되어 있습니다.

### Core Workflow Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:constitution` | 크로스 아티팩트 검증과 함께 프로젝트 헌법을 생성하거나 갱신 |
| `/codexspec:specify` | 대화를 통해 요구사항을 명확화·확정하고 `requirements.md`에 저장 |
| `/codexspec:generate-spec` | 명확화된 요구사항으로부터 `spec.md` 생성 (★ 자동 리뷰) |
| `/codexspec:spec-to-plan` | 명세서를 기술 구현 계획으로 변환 (★ 자동 리뷰) |
| `/codexspec:plan-to-tasks` | 계획을 추적 가능하고 검증 가능한 태스크로 분해 (★ 자동 리뷰) |
| `/codexspec:implement-tasks` | 조건부 TDD 워크플로우로 태스크 실행 |

### Review Commands (Quality Gates)

| Command | Purpose |
|---------|---------|
| `/codexspec:review-spec` | 명세서의 완전성과 품질 검증 |
| `/codexspec:review-plan` | 기술 계획의 실현 가능성과 정합성 리뷰 |
| `/codexspec:review-tasks` | 태스크의 커버리지, 순서, 실현 가능성 검증 |

### Enhancement Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:config` | 프로젝트 설정을 대화형으로 관리 (생성/조회/수정/초기화) |
| `/codexspec:clarify` | 기존 명세서에서 모호한 부분을 스캔 (4개 카테고리, 최대 5개 질문) |
| `/codexspec:analyze` | 크로스 아티팩트 일관성 분석 (읽기 전용, 심각도 기반) |
| `/codexspec:checklist` | 요구사항 품질 체크리스트 생성 |
| `/codexspec:tasks-to-issues` | 태스크를 GitHub 이슈로 변환 |

### Git Workflow Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:commit-staged` | 스테이지된 변경 사항으로부터 커밋 메시지 생성 (세션 컨텍스트 인식) |
| `/codexspec:pr` | git diff로부터 PR/MR 설명 생성 (플랫폼 자동 감지) |

### Code Review Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:review-code` | 모든 언어의 코드 리뷰 (관용적 표명, 정확성, 견고성, 아키텍처) |
| `/codexspec:review-python-code` | Python 코드 리뷰 (PEP 8, 타입 안전성, 견고성, 헌법 일관성) |
| `/codexspec:review-react-code` | React/TypeScript 코드 리뷰 (컴포넌트 아키텍처, Hooks 규칙, 상태, 성능) |

### Fast Track

| Command | Purpose |
|---------|---------|
| `/codexspec:quick` | 작은 변경을 위한 간소화된 Requirements-First SDD 흐름 실행 |

---

## Command Categories

### Core Workflow Commands

핵심 Requirements-First SDD 워크플로우를 담당하는 명령어들입니다. 흐름은 Constitution → 확정된 요구사항 → 명세서 → 계획 → 태스크 → 구현입니다. 여기서 확정된 요구사항이 최우선 권위이며, 사용자가 Confirmation Gate에서 명시적으로 확정하기 전까지는 연쇄 과정 어디도 확정된 것으로 간주하지 않습니다.

### Review Commands (Quality Gates)

각 워크플로우 단계의 산출물을 **증거 기반 리뷰(evidence-based review)** 원칙 아래 검증하는 명령어들입니다. 모든 결함은 구체적인 `Evidence`, `Location`, `Mismatch`, `Impact`, `Remediation`을 포함해야 합니다. 권고性质的 설계 제안은 분리해서 보고되며, 상태를 변경하거나 자동 변경을 유발하지 않습니다. 검증된 결함은 최대 두 라운드까지 수정 및 재리뷰할 수 있으며, 권고는 끝까지 선택 사항으로 남습니다.

### Enhancement Commands

반복적 다듬기, 크로스 아티팩트 검증, 설정, 프로젝트 관리 연동을 위한 명령어들입니다.

### Git Workflow Commands

완료된 작업을 공유 가능한 산출물로 바꾸는 명령어들입니다. 스테이지된 diff로부터 커밋 메시지를, 브랜치 diff로부터 구조화된 PR/MR 설명을 만듭니다.

### Code Review Commands

소스 코드(모든 언어, Python 특화, React/TypeScript 특화)를 관용적 표명, 정확성, 견고성, 아키텍처, 헌법 정합성 측면에서 리뷰하는 명령어들입니다. 발견 사항은 산출물 리뷰와 동일한 심각도 원칙을 따릅니다. CRITICAL/HIGH 이슈는 구체적인 증거를 반드시 인용해야 하며, LOW 제안은 권고 성격입니다.

### Fast Track

작고 범위가 명확한 변경에 대해 Requirements-First SDD 흐름을 엔드투엔드로 실행하는 간소화 명령어입니다.

---

## Command Reference

### `/codexspec:constitution`

프로젝트 헌법을 생성하거나 갱신합니다. 헌법은 아키텍처 원칙, 기술 스택, 코드 표준, 거버넌스 규칙을 정의하며, 이후 모든 개발 결정을 안내합니다.

**Syntax:**

```
/codexspec:constitution [principles description]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `principles description` | No | 포함할 원칙에 대한 설명 (제공하지 않으면 프롬프트로 묻습니다) |

**What it does:**

- `.codexspec/memory/constitution.md`가 없으면 생성
- 기존 헌법에 새 원칙을 반영하여 갱신
- 템플릿과의 크로스 아티팩트 일관성 검증
- 변경 내용과 영향받는 파일을 보여주는 Sync Impact Report 생성
- 의존 템플릿에 대한 헌법 적합성 리뷰 포함

**What it creates:**

```
.codexspec/
└── memory/
    └── constitution.md    # Project governance document
```

**Example:**

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

**Tips:**

- 일관된 의사결정을 위해 프로젝트 초반에 원칙을 정의하세요
- 기술 원칙과 프로세스 원칙을 모두 포함하세요
- 주요 기능 개발에 앞서 헌법을 검토하세요
- 헌법 변경은 크로스 아티팩트 검증을 유발합니다

---

### `/codexspec:specify`

대화형 Q&A로 요구사항을 명확화하고, 도출된 요약을 확정한 뒤 이후 세션에서 사용할 수 있게 저장합니다.

**Syntax:**

```
/codexspec:specify [your idea or requirement]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `your idea or requirement` | No | 구축하고자 하는 것에 대한 초기 설명 (제공하지 않으면 프롬프트로 묻습니다) |

**What it does:**

- 아이디어를 이해하기 위한 명확화 질문
- 놓칠 수 있는 엣지 케이스 탐색
- 대화를 통해 고품질 요구사항을 함께 도출
- "무엇"과 "왜"에 집중하며 기술 구현은 다루지 않음
- 확정된 필요사항, 제약, 결정, 제외 항목, 미해결 질문에 안정적인 ID 부여
- 사용자 증거와 확정 로그 기록
- 기능 워크스페이스와 `requirements.md` 생성

**What it creates:**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

오직 확정된 항목만 권위 있는 요구사항이 됩니다. 미해결 질문은 명시적으로 열린 상태로 남습니다. 이것이 요구사항의 Confirmation Gate입니다. 최종 요약을 명시적으로 확정하기 전까지는 어떤 것도 확정된 것으로 간주하지 않습니다.

**Example:**

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

**Tips:**

- 초기 요구사항 탐색에 사용하세요
- 완벽할 필요는 없습니다. 다듓기는 반복적인 과정입니다
- AI가 가정하면 질문하세요
- spec 생성 전에 요약을 검토하세요

---

### `/codexspec:generate-spec`

명확화된 요구사항으로부터 `spec.md` 문서를 생성합니다. 이 명령어는 "요구사항 컴파일러" 역할을 하여 명확화된 요구사항을 구조화된 명세서로 변환합니다.

**Syntax:**

```
/codexspec:generate-spec
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| Feature path | No | 명시적인 기능 디렉토리, `requirements.md` 또는 대상 `spec.md`. 해석이 모호할 때 필요 |

**What it does:**

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

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**Example:**

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
     - Or proceed to /codexspec:spec-to-plan
```

**Tips:**

- `/codexspec:specify`가 요구사항을 명확화한 뒤에 실행하세요
- 진행하기 전에 생성된 spec을 검토하세요
- 품질 검증에는 `/codexspec:review-spec`을 사용하세요
- 사소한 조정이 필요하면 spec.md를 직접 편집하세요

---

### `/codexspec:clarify`

기존 명세서에서 모호한 부분과 빈 공백을 스캔합니다. 초기 spec 생성 이후의 반복적 다듬기에 사용하세요.

**Syntax:**

```
/codexspec:clarify [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | spec 파일 경로 (제공하지 않으면 자동 감지) |

**What it does:**

- 초점이 맞춰진 모호성 카테고리로 요구사항과 spec을 스캔
- 타겟팅된 명확화 질문 (최대 5개)
- 사용자 확인 후 `requirements.md`를 먼저 갱신하고, 이어서 `spec.md`를 동기화
- review-spec 결과가 있으면 통합

**Ambiguity Categories:**

| Category | What it Detects |
|----------|-----------------|
| **Completeness Gaps** | 누락된 섹션, 빈 콘텐츠, 부재한 인수 조건 |
| **Specificity Issues** | 모호한 용어("fast", "scalable"), 정의되지 않은 제약 |
| **Behavioral Clarity** | 에러 처리 누락, 정의되지 않은 상태 전이 |
| **Measurability Problems** | 측정 지표가 없는 비기능 요구사항 |

**Example:**

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

**Tips:**

- spec.md가 있지만 다듬어야 할 때 사용하세요
- `/codexspec:review-spec` 결과와 통합됩니다
- 세션당 최대 5개 질문
- 복잡한 명세서는 여러 번 실행하세요

---

### `/codexspec:spec-to-plan`

기능 명세서를 기술 구현 계획으로 변환합니다. 이 단계에서 기능을 **어떻게** 구축할지 정의합니다.

**Syntax:**

```
/codexspec:spec-to-plan [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | spec 파일 경로 (제공하지 않으면 `.codexspec/specs/`에서 자동 감지) |

**What it does:**

- 명세서와 헌법을 읽음
- 확정된 요구사항과 리포지토리 제약에 필요한 기술적 디테일만 포함
- 적용 가능한 헌법 규칙을 점검하되, 선택적 관례를 기능 요구사항으로 취급하지는 않음
- 명세서 요구사항으로 향하는 `Covers` 링크 추가
- 기술 결정과 그 근거를 문서화
- 결정이 확정된 의도를 변경하는 경우 정지

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # Technical implementation plan
```

**Example:**

```text
You: /codexspec:spec-to-plan Use Python FastAPI for backend, React for frontend, PostgreSQL for database

AI:  Generating technical plan...

     Constitutionality Review:
     ✓ Clean Architecture: Modular design with clear boundaries
     ✓ TDD: Test-first approach enforced in phases
     ✓ Code Quality: Linting and type hints required

     Architecture:
     - Backend: FastAPI with layered architecture
     - Frontend: React with component structure
     - Database: PostgreSQL with migration strategy

     Module Dependency Graph:
     ┌─────────────┐
     │    API      │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Services   │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │    Data     │
     └─────────────┘

     ✓ Created plan.md
     5 Implementation Phases defined
```

**Tips:**

- spec이 검토되어 안정된 뒤에 실행하세요
- 적용 가능한 헌법 규칙은 필수이지만, 무관한 템플릿 관례는 그렇지 않습니다
- 프로젝트 유형에 맞춰 관련 섹션을 포함하세요
- 태스크로 넘어가기 전에 계획을 검토하세요

---

### `/codexspec:plan-to-tasks`

기술 계획을 실행 가능한 태스크로 분해하며, 명시적인 커버리지와 검증 가능한 결과물을 제공합니다.

**Syntax:**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `paths` | No | spec과 plan 경로 (제공하지 않으면 자동 감지) |

**What it does:**

- 검증 가능한 하나의 결과물을 갖는 태스크를 생성. 한 태스크는 밀접하게 관련된 여러 파일을 다룰 수 있음
- 계획, 헌법, 확정된 필요사항 또는 위험이 요구할 때만 테스트 우선 순서를 적용
- 태스크가 진정으로 독립적인 경우에만 `[P]` 표시
- 각 태스크에 대해 정확한 파일 경로를 명시
- 계획과 요구사항 ID로 향하는 `Covers` 링크 추가

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # Task breakdown
```

**Task Structure:**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**Example:**

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

**Tips:**

- 각 태스크는 검증 가능한 하나의 결과물을 낳고, 밀접하게 관련된 파일을 다룰 수 있습니다
- 테스트 태스크는 test-first가 요구될 때만 구현에 앞섭니다
- `[P]`는 진정으로 독립적인 병렬화 가능 태스크에만 표시됩니다
- 구현 전에 의존성을 검토하세요

---

### `/codexspec:implement-tasks`

조건부 TDD 워크플로우로 구현 태스크를 실행합니다. 태스크 목록을 체계적으로 따라 진행합니다.

**Syntax:**

```
/codexspec:implement-tasks [tasks_path]
/codexspec:implement-tasks [spec_path plan_path tasks_path]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `tasks_path` | No | tasks.md 경로 (제공하지 않으면 자동 감지) |
| `spec_path plan_path tasks_path` | No | 세 개 문서 모두에 대한 명시적 경로 |

**File Resolution:**

- **인자 없음**: `.codexspec/specs/`에서 자동 감지
- **인자 1개**: `tasks.md` 경로로 취급하고 나머지는 같은 디렉토리에서 유추
- **인자 3개**: spec.md, plan.md, tasks.md에 대한 명시적 경로

**What it does:**

- tasks.md를 읽고 미완료 태스크를 식별
- 코드 태스크에 TDD 워크플로우 적용:
  - **Red**: 실패하는 테스트를 먼저 작성
  - **Green**: 테스트를 통과하도록 구현
  - **Verify**: 모든 테스트를 실행
  - **Refactor**: 테스트를 green으로 유지하면서 개선
- 테스트 불가능한 태스크(문서, 설정)는 직접 구현
- 진행에 따라 태스크 체크박스를 갱신
- 막힘 사항이 발생하면 issues.md에 기록

**TDD Workflow for Code Tasks:**

```
Red → Green → Verify → Refactor → Mark Complete
```

**Direct Implementation for Non-Testable:**

- 문서 파일
- 설정 파일
- 정적 자산
- 인프라 파일

**Example:**

```text
You: /codexspec:implement-tasks

AI:  Starting implementation...

     Loading context:
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     Tech Stack: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Working on Task 1.1: Setup Project Structure
     ✓ Created src/taskman/__init__.py
     ✓ Created pyproject.toml
     [x] Task 1.1 Complete

     Working on Task 2.1: Write Tests for Task Entity [P]
     ✓ Created tests/test_task.py
     Running tests... 5 passed (all expected failures)
     [x] Task 2.1 Complete

     Working on Task 2.2: Implement Task Entity
     ✓ Created src/taskman/models/task.py
     Running tests... 5 passed
     [x] Task 2.2 Complete

     ...
```

**Tips:**

- 중간에 중단되더라도 이어서 진행할 수 있습니다
- 막힘 사항은 issues.md에 기록됩니다
- 의미 있는 태스크/단계가 끝난 뒤에 커밋이 이루어집니다
- 검증을 위해 먼저 `/codexspec:review-tasks`를 실행하세요

---

### `/codexspec:review-spec`

명세서를 확정된 요구사항과 대조하고, 그 자체의 내적 품질을 검증합니다.

**Syntax:**

```
/codexspec:review-spec [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | spec 파일 경로 (제공하지 않으면 자동 감지) |

**What it does:**

- 확정된 `requirements.md` 항목에 대한 충실도 점검
- 내적 일관성, 명확성, 검증 가능성 점검
- 권위 있는 콘텐츠가 필요로 할 때만 누락된 템플릿 섹션을 결함으로 간주
- 각 결함은 `Evidence`, `Location`, `Mismatch`, `Impact`, `Remediation`을 포함해야 함
- `Risk Advisories / Design Opportunities`를 결함과 분리
- 분류된 발견 사항으로부터 도출된 상태와 호환성 점수를 생성

**Shared review contract:**

| Category | Meaning |
|----------|---------|
| Fidelity defect | 권위 있는 소스와 충돌하거나 이를 누락 |
| Intrinsic defect | 내적으로 모순되거나, 실행 불가능하거나, 검증 불가능 |
| Advisory | 현재 결함의 증거 없이 제시되는 선택적 개선 |

상태는 `PASS`, `PASS_WITH_WARNINGS`, `NEEDS_REVISION`, `BLOCKED` 중 하나입니다. 권고는 상태나 점수를 결코 변경하지 않습니다.

**Example:**

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

**Tips:**

- `/codexspec:spec-to-plan` 이전에 실행하세요
- `BLOCKED`와 `NEEDS_REVISION`은 진행할 준비가 안 된 상태로 취급하세요
- 권고를 요구사항으로 끌어올리지 마세요
- 수정한 뒤에 다시 실행하세요

---

### `/codexspec:review-plan`

기술 구현 계획의 충실도, 실현 가능성, 그리고 정당화된 기술 결정을 리뷰합니다.

**Syntax:**

```
/codexspec:review-plan [path_to_plan.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_plan.md` | No | plan 파일 경로 (제공하지 않으면 자동 감지) |

**What it does:**

- `Covers` 링크와 필수 spec 커버리지 검증
- 적용 가능한 헌법 규칙과 리포지토리 팩트 점검
- 구체적인 비용이나 충돌을 유발하는 경우에만 정당화되지 않은 복잡성에 플래그
- 모든 결함에 증거 필드를 요구하고 동일한 근본 원인을 가진 발견 사항은 병합
- 선택적 아키텍처 개선 사항은 권고로 보고
- 공유 상태 및 호환성 점수 계약을 사용

**Example:**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**Tips:**

- `/codexspec:plan-to-tasks` 이전에 실행하세요
- 태스크 생성 전에 증거 기반 결함을 해결하세요
- 추측성 아키텍처 아이디어는 권고 섹션에 두세요
- 기술 스택이 팀 역량과 맞는지 확인하세요

---

### `/codexspec:review-tasks`

태스크 분해의 커버리지, 검증 가능한 결과물, 올바른 순서, 실현 가능한 의존성을 검증합니다.

**Syntax:**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_tasks.md` | No | tasks 파일 경로 (제공하지 않으면 자동 감지) |

**What it does:**

- 필수 plan 항목과 요구사항이 모두 태스크로 커버되는지 점검
- 권위 있는 소스가 요구할 때만 테스트 우선 순서를 검증
- 각 태스크가 검사 가능한 하나의 결과물을 갖는지 확인
- 의존성 검증 (사이클 없음, 올바른 순서)
- 병렬화 마커 검토
- 파일 경로 검증
- 모든 결함에 증거 필드 요구
- 선택적 프로세스 개선 사항은 권고로 보고
- 공유 상태 및 호환성 점수 계약을 사용

**Example:**

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

**Tips:**

- `/codexspec:implement-tasks` 이전에 실행하세요
- 테스트 순서 발견 사항은 권위 있는 소스가 테스트를 요구할 때만 결함입니다
- 병렬화 마커가 정확한지 확인하세요
- 파일 경로가 프로젝트 구조와 일치하는지 검증하세요

---

### `/codexspec:analyze`

requirements.md, spec.md, plan.md, tasks.md에 걸쳐 비파괴적 일관성 분석을 수행합니다. 권위 충돌, 추적 가능성 공백, 중복, 누락된 커버리지를 식별합니다.

**Syntax:**

```
/codexspec:analyze
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| None | - | 현재 기능의 산출물을 분석 |

**What it does:**

- 산출물 간 중복 감지
- 측정 가능한 기준이 없는 모호성 식별
- 명세가 불충분한 항목 발견
- 헌법 정합성 점검
- 요구사항 커버리지를 태스크에 매핑
- 용어와 순서의 불일치 보고

**Severity Levels:**

| Level | Definition |
|-------|------------|
| **CRITICAL** | 헌법 위반, 핵심 산출물 누락, 커버리지 제로 |
| **HIGH** | 중복/충돌하는 요구사항, 모호한 보안 속성 |
| **MEDIUM** | 용어 표류, 비기능 커버리지 누락 |
| **LOW** | 스타일/표현 개선 |

**Example:**

```text
You: /codexspec:analyze

AI:  Analyzing artifacts...

     # Specification Analysis Report

     ## Coverage Summary
     | Requirement Key | Has Task? | Task IDs |
     |-----------------|-----------|----------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | None |

     ## Issues Found

     | ID | Category | Severity | Summary |
     |----|----------|----------|---------|
     | A1 | Coverage | CRITICAL | REQ-003 has no task coverage |
     | A2 | Duplication | HIGH | REQ-005 and REQ-008 overlap |
     | A3 | Ambiguity | MEDIUM | NFR-002 "secure" not defined |

     ## Metrics
     - Total Requirements: 12
     - Total Tasks: 24
     - Coverage: 92% (11/12 requirements)
     - Critical Issues: 1

     ## Next Actions
     1. Add tasks for REQ-003 (CRITICAL)
     2. Consider merging REQ-005 and REQ-008
     3. Define "secure" in NFR-002

     Resolve CRITICAL issues before /codexspec:implement-tasks
```

**Tips:**

- `/codexspec:plan-to-tasks` 이후, 구현 이전에 실행하세요
- CRITICAL 이슈는 구현을 막아야 합니다
- 읽기 전용 분석이며 어떤 파일도 수정하지 않습니다
- 발견 사항으로 산출물 품질을 개선하세요

---

### `/codexspec:checklist`

요구사항의 완전성, 명확성, 일관성을 검증하기 위한 품질 체크리스트를 생성합니다. 이것은 "요구사항 작성을 위한 단위 테스트"입니다.

**Syntax:**

```
/codexspec:checklist [focus_area]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `focus_area` | No | 도메인 초점 (예: "ux", "api", "security", "performance") |

**What it does:**

- 품질 차원별로 구성된 체크리스트 생성
- `FEATURE_DIR/checklists/` 디렉토리에 체크리스트 생성
- 항목은 구현 테스트가 아닌 요구사항 품질에 초점

**Quality Dimensions:**

- **Requirement Completeness**: 필요한 요구사항이 모두 있는가?
- **Requirement Clarity**: 요구사항이 구체적이고 모호하지 않은가?
- **Requirement Consistency**: 요구사항이 충돌 없이 정합하는가?
- **Acceptance Criteria Quality**: 성공 기준이 측정 가능한가?
- **Scenario Coverage**: 모든 흐름/사례가 다뤄졌는가?
- **Edge Case Coverage**: 경계 조건이 정의되었는가?
- **Non-Functional Requirements**: 성능, 보안, 접근성이 명시되었는가?
- **Dependencies & Assumptions**: 문서화되었는가?

**Example Checklist Types:**

- `ux.md` - 시각적 위계, 상호작용 상태, 접근성
- `api.md` - 에러 형식, 속도 제한, 인증
- `security.md` - 데이터 보호, 위협 모델, 침해 대응
- `performance.md` - 지표, 부하 조건, 성능 저하

**Example:**

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

**Tips:**

- 체크리스트는 구현 정확성이 아닌 요구사항 품질을 검증합니다
- 요구사항 리뷰와 개선에 사용하세요
- 초점을 맞춘 검증을 위해 도메인 특화 체크리스트를 만드세요
- 기술 계획으로 넘어가기 전에 실행하세요

---

### `/codexspec:tasks-to-issues`

`tasks.md`의 태스크를 GitHub 이슈로 변환하여 프로젝트 추적과 협업에 활용합니다.

**Syntax:**

```
/codexspec:tasks-to-issues
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| None | - | 현재 기능의 모든 태스크를 변환 |

**What it does:**

- 태스크 ID, 설명, 의존성, 파일 경로를 파싱
- 구조화된 본문으로 GitHub 이슈 생성
- 태스크 유형(setup, implementation, testing, documentation)에 따라 라벨 추가
- 이슈 간 의존성 연결
- URL과 함께 생성된 이슈 보고

**Prerequisites:**

- GitHub remote가 있는 Git 리포지토리
- GitHub CLI(`gh`) 설치 및 인증 완료
- `tasks.md` 파일 존재

**Example:**

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

**Tips:**

- GitHub CLI 인증이 필요합니다 (`gh auth login`)
- GitHub 리포지토리에서만 동작합니다
- 리포지토리의 기본 설정으로 이슈를 생성합니다
- 실행 전에 중복을 확인하세요

---

### `/codexspec:commit-staged`

스테이지된 git 변경 사항을 기반으로 세션 컨텍스트를 이해하여 Conventional Commits 규격을 준수하는 커밋 메시지를 생성합니다. 이 명령어는 개발 세션의 맥락을 이해해 의미 있는 커밋 메시지를 만듭니다.

**Syntax:**

```
/codexspec:commit-staged [-p]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `-p` | No | Preview mode - 커밋하지 않고 메시지만 표시 |

**What it does:**

- `git diff --staged`를 실행하여 스테이지된 변경 사항을 가져옴
- 의도 파악을 위해 변경 사항과 세션 컨텍스트 분석
- Conventional Commits 사양 준수
- 실행 모드(기본)에서는 메시지 생성 후 즉시 커밋
- 미리보기 모드(`-p`)에서는 커밋하지 않고 메시지만 표시
- 스테이지된 변경 사항이 없으면 에러 보고

**Example:**

```text
You: /codexspec:commit-staged

AI:  Analyzing staged changes...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Generated commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Executing commit...

     ✓ Committed: def5678
```

**Preview Mode Example:**

```text
You: /codexspec:commit-staged -p

AI:  Preview mode - no commit will be executed

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow
```

**Tips:**

- 먼저 `git add`로 변경 사항을 스테이지하세요
- 스테이지된 콘텐츠만 분석하며, Git의 2단계 커밋 워크플로우를 존중합니다
- 의미 있는 커밋 메시지를 위해 세션 컨텍스트를 고려합니다
- 커밋 전에 `-p` 플래그로 미리보기하세요
- 기본적으로 Conventional Commits 사양을 따릅니다

---

### `/codexspec:review-code`

모든 언어의 코드를 관용적 표명, 정확성, 견고성, 아키텍처, 헌법 정합성 측면에서 리뷰합니다.

**Syntax:**

```
/codexspec:review-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | 리뷰할 하나 이상의 소스 파일 또는 디렉토리 (공백으로 구분). 생략 시 기본값은 `src/` |

**What it does:**

- 파일 확장자로 주 언어를 감지하고, 다중 언어 대상에는 언어별 패스를 실행
- 해당 설정이 존재할 때 정적 분석 도구를 실행 (`ruff`/`mypy`, `eslint`/`tsc`, `go vet`/`gofmt`, `cargo check`/`cargo clippy`, `shellcheck`). 없으면 우아하게 건너뛰고 축소된 커버리지를 보고
- 4개 차원을 평가: Idiomatic Clarity & Simplicity, Correctness & Explicit Contracts, Runtime Robustness & Resource Discipline, Architecture & Design Integrity
- 감지된 프레임워크에 대해 필수 하위 섹션을 주입 (예: React의 Hooks Compliance, Rust의 Ownership & Borrowing, Go의 Goroutine & Context Discipline, C/C++의 Memory & Lifetime Safety, Shell의 Execution Safety)
- `.codexspec/memory/constitution.md`가 있을 때 발견 사항을 교차 참조. 없으면 헌법 축을 제외하고 그 가중치를 재분배
- 발견 사항을 심각도로 분류: CRITICAL, HIGH, MEDIUM, LOW (LOW 제안은 총 5점 감점으로 제한)

**Example:**

```text
You: /codexspec:review-code src/

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

**Tips:**

- 여러 경로를 전달하면 원하는 일부만 리뷰할 수 있습니다 (예: `src/ tests/`)
- 점수는 참고용이며, CRITICAL/HIGH 발견 사항이 실행 가능한 신호입니다
- Python 전용 또는 React 전용 프로젝트는 더 깊은 언어 특화 검사를 위해 `/codexspec:review-python-code`나 `/codexspec:review-react-code`를 사용하세요
- 수정 후 다시 실행하여 점수가 회복되는지 확인하세요 (CRITICAL/HIGH 이슈를 해결하면 95점 이상 예상)

---

### `/codexspec:review-python-code`

Python 코드를 PEP 8 준수, 타입 안전성, 엔지니어링 견고성, 헌법 일관성 측면에서 리뷰합니다.

**Syntax:**

```
/codexspec:review-python-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | 리뷰할 하나 이상의 Python 파일 또는 디렉토리 (공백으로 구분). 생략 시 기본값은 `src/` |

**What it does:**

- PEP 8 / 린팅 결과를 위해 `ruff check`를, 타입 검사 결과를 위해 `mypy`를 실행
- Python 특화 4개 차원을 리뷰: Pythonic & KISS Principle, Type Safety & Explicitness, Engineering Robustness, Constitution Alignment
- 타입 어노테이션 완전성, 광범위 예외 처리, `raise ... from err` 컨텍스트 보존 점검
- 리소스 관리(`with` 컨텍스트 매니저), async/await 정확성, 구조화된 `logging` 규율 검증
- `.codexspec/memory/constitution.md`의 MUST/SHOULD 원칙이 있을 때 발견 사항을 교차 참조
- 발견 사항을 심각도로 분류: CRITICAL (헌법 MUST 위반, 논리 버그, 보안 취약점), HIGH (타입 안전성 공백, ruff/mypy 에러, 리소스 누수), MEDIUM (설계/리팩터 기회, 어노테이션 누락), LOW (가독성, Pythonic 표현)

**Example:**

```text
You: /codexspec:review-python-code src/codexspec/

AI:  # Python Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | ruff  | Pass   | 0      |
     | mypy  | Pass   | 0      |

     ## Findings
     ### Warnings (HIGH)
     - [ ] [CODE-002] src/codexspec/__init__.py:218 - public function missing return type annotation
       Suggestion: add the return type and verify with mypy.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/codexspec/cli.py:140 - use `pathlib.Path` instead of `os.path` string concatenation
```

**Tips:**

- 대상이 Python 전용이고 PEP 8 / 타입 안전성 심도가 필요할 때 `/codexspec:review-code` 대신 사용하세요
- 완전한 커버리지를 위해서는 `ruff`와 `mypy`가 대상 프로젝트에 설치·설정되어야 합니다. 없으면 축소된 커버리지를 보고합니다
- 헌법 MUST 원칙은 평가에 반영되며, 헌법이 없을 때는 언어 비의존적 메타 원칙(테스트 가능성, 단순성)을 적용합니다

---

### `/codexspec:review-react-code`

React/TypeScript 코드를 컴포넌트 아키텍처, Hooks 규칙, 상태 관리, 성능, 헌법 일관성 측면에서 리뷰합니다.

**Syntax:**

```
/codexspec:review-react-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | 리뷰할 하나 이상의 React/TypeScript 파일 또는 디렉토리 (공백으로 구분, `.tsx`, `.ts`, `.jsx`, `.js` 대상). 생략 시 기본값은 `src/` |

**What it does:**

- (ESLint 설정이 있을 때) `npx eslint`를, (`tsconfig.json`이 있을 때) `npx tsc --noEmit`을 실행
- React 특화 4개 차원을 리뷰: Component Atomicity & Single Responsibility, Hooks Compliance & Side-Effects Management, State Management & Data Flow, Performance & Robustness
- `useEffect` 의존성 배열의 완전성을 검증하고, 파생 상태를 state로 오용하는 사례를 감지하며, 불필요한 이펙트에 플래그
- stale closure 위험, 이펙트 클린업 누락, prop drilling, 비메모화된 비싼 렌더, 로딩/에러 상태 누락을 점검
- `.codexspec/memory/constitution.md`가 있을 때 발견 사항을 교차 참조
- 발견 사항을 심각도로 분류: CRITICAL (Hooks 위반, 레이스 컨디션), HIGH (클린업 누락, 미처리 promise rejection), MEDIUM (리팩터 후보), LOW (가독성)

**Example:**

```text
You: /codexspec:review-react-code src/components/

AI:  # React Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | eslint| Warn   | 2      |
     | tsc   | Pass   | 0      |

     ## Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/components/UserProfile.tsx:38 - `useEffect` missing `userId` in dependency array
       Impact: stale closure fetches the wrong user after navigation.
       Suggestion: add `userId` to the dependency array or extract to a custom hook.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/components/Button.tsx:12 - extract derived value instead of `useState`
```

**Tips:**

- 대상이 React/TypeScript 전용이고 Hooks/컴포넌트 아키텍처 심도가 필요할 때 `/codexspec:review-code` 대신 사용하세요
- 완전한 커버리지를 위해서는 ESLint와 `tsconfig.json`이 있어야 합니다. 없으면 축소된 커버리지를 보고합니다
- React 발견 사항은 기본 TypeScript 검사 위에 겹쳐지므로, 타입 안전성 이슈도 여전히 드러납니다

---

### `/codexspec:quick`

작은 변경을 위한 간소화된 Requirements-First SDD 흐름을 실행합니다.

**Syntax:**

```
/codexspec:quick [describe a small requirement]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `describe a small requirement` | No | 작고 범위가 명확한 변경에 대한 짧은 설명 (제공하지 않으면 프롬프트로 묻습니다) |

**What it does:**

- 범위(접하는 파일, 모듈 범위, 새 의존성, 미해결 제품 결정)를 평가하고, 변경이 광범위하거나 여러 독립적 결과물을 가지면 표준 흐름을 권장
- `/codexspec:specify`와 동일한 타임스탬프 관례로 기능 워크스페이스와 `requirements.md`를 생성
- 구현을 materially 변경하는 모호성만 해결하고, 간결한 확정 요약을 제시 (`NEED-*`, 관련 `CON-*`/`DEC-*`, `OUT-*`, 미해결 `OPEN-*`)
- Confirmation Gate에서 멈춤: 요약을 확정하기 전에는 아무것도 생성하지 않음
- 새 기능 디렉토리에 대해 생성 명령어들을 연쇄 실행: `/codexspec:generate-spec`, `/codexspec:spec-to-plan`, `/codexspec:plan-to-tasks`, `/codexspec:implement-tasks`
- 각 생성 명령어의 자체 자동 리뷰 루프에 위임. 리뷰가 새 제품 또는 아키텍처 결정을 필요로 하면 멈추고 사용자에게 묻습니다
- 기능 디렉토리, 산출물 경로, 리뷰 결과, 구현 검증, 미해결 권고를 분리해서 보고

**What it creates:**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**Example:**

```text
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → spec-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**Tips:**

- Quick은 진정으로 작고 단일 결과물인 변경에만 사용하세요. 그렇지 않으면 `/codexspec:specify`와 표준 흐름을 실행하세요
- 확정은 여전히 필요합니다. Quick은 자동화를 진행하기 위해 제품 결정을 추론하지 않습니다
- 어느 생성 리뷰가 `NEEDS_REVISION`/`BLOCKED`를 반환하면 Quick은 멈추고 제어권을 사용자에게 돌려줍니다

---

### `/codexspec:pr`

git diff로부터 구조화된 GitHub Pull Request / GitLab Merge Request 설명을 생성합니다. 선택적으로 `spec.md`를 통합해 SDD 추적 컨텍스트를 제공합니다.

**Syntax:**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--target-branch <branch>` | No | 비교 대상 브랜치 (기본값: `origin/main`) |
| `--sections <list>` | No | `summary, changes, testing, verify, checklist, notes`의 쉼표로 구분된 부분 집합 (기본값: `all`) |
| `--spec <id-or-path>` | No | 옵트인 spec 통합: `.codexspec/specs/` 아래에서 해석되는 기능 id(예: `2025-0321-1430k7-auth`) 또는 명시적인 `path/to/spec.md`. 생략하면 git만으로 생성 |
| `--output <file>` | No | 터미널 대신 파일로 설명을 저장 |

**What it does:**

- 대상 브랜치를 기준으로 git 컨텍스트 수집 (현재 브랜치, remote URL, 앞선 커밋, 파일 변경 사항, 전체 diff, 커밋 메시지)
- remote URL로부터 플랫폼 자동 감지: GitHub → "Pull Request", GitLab → "Merge Request", 기타/없음 → GitHub 용어로 기본화하고 경고
- `.codexspec/memory/constitution.md`가 있으면 불러와서 설명을 문서/코드 리뷰 표준에 맞춤
- 설명 언어로 `language.commit`(그다음 `language.output`, 그다음 영어)을 존중. 기술 용어(API, JWT, PR, MR)는 적절한 경우 영어로 유지
- `--spec`이 주어지면 spec.md에서 가져온 사용자 스토리와 요구사항으로 Context 섹션을 추가. 그렇지 않으면 diff만으로 생성
- `--sections`에 따라 섹션을 출력 (Summary, Changes, Testing, Verification Steps, Pre-merge Checklist, Notes / Breaking Changes)

**Example:**

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

**Tips:**

- 공식 명세가 없는 작은 버그 수정이나 변경에는 `--spec`을 생략하세요
- `/codexspec:commit-staged`와 조합해 같은 작업으로부터 커밋 메시지와 PR 설명을 함께 만들 수 있습니다
- 이 명령어의 엔드투엔드 실전 사례(spec.md 컨텍스트가 어떻게 연결되는지 포함)는 [PR description generator case study](../case-studies/case-study-pr-description-generator.md)를 참고하세요

---

### `/codexspec:config`

프로젝트 설정을 대화형으로 관리합니다 (생성/조회/수정/초기화). 이것은 `codexspec config` CLI의 슬래시 명령어 버전이며, Plugin Marketplace 설치에 적합합니다.

**Syntax:**

```
/codexspec:config [--view]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--view` | No | 수정 없이 현재 설정을 표시. 인자가 없으면 대화형 관리 메뉴를 엽니다 |

**What it does:**

- `.codexspec/config.yml`만을 대상
- `--view`(또는 "View current config" 메뉴 옵션)는 파일을 읽기 쉬운 형태로 출력. 없으면 "Configuration Not Found"를 보고
- 대화형 모드에서 설정이 있으면 View, Modify, Reset to defaults, Cancel을 제공
- 설정이 없으면 최소한의 `output` 전용 설정을 작성하는 생성 흐름을 실행 (interaction/document/commit은 `output` 그다음 `en`으로 해결되므로 `output` 전용 파일이 완전히 기능함)
- 각 언어 차원(output, interaction, document, commit)을 독립적으로 설정하고 `auto_next` 같은 워크플로우 옵션을 토글할 수 있게 함

**What it creates/edits:**

```
.codexspec/config.yml
```

**Example:**

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

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Tips:**

- 무언가를 변경하기 전에 현재 상태를 점검하려면 `/codexspec:config --view`를 사용하세요
- 새로 만들거나 초기화한 설정은 `output`만 작성합니다. `output`과 달라야 할 때만 `interaction`/`document`를 설정하세요
- 터미널에서 스크립트로 변경하려면 `codexspec config` CLI를 사용하세요 (`--set-lang`, `--set-interaction-lang`, `--set-document-lang`, `--set-commit-lang`, `--auto-next`)

---

## Workflow Overview

```text
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

각 리뷰는 사람이 확인하는 체크포인트입니다. 증거 기반 발견 사항으로 충실도와 내적 품질을 검증합니다. 권고性质的 설계 제안은 분리되어 있으며 진행을 결코 막지 않습니다. 검증된 결함은 최대 두 라운드까지 수정 및 재리뷰할 수 있습니다.

---

## Troubleshooting

### "Feature directory not found"

명령어가 기능 디렉토리를 찾지 못했습니다.

**Solutions:**

- 먼저 `codexspec init`을 실행하여 프로젝트를 초기화하세요
- `.codexspec/specs/` 디렉토리가 존재하는지 확인하세요
- 올바른 프로젝트 디렉토리에 있는지 확인하세요
- 여러 후보가 있을 때는 명시적으로 기능 디렉토리나 산출물 경로를 전달하세요

### "No spec.md found"

명세 파일이 아직 존재하지 않습니다.

**Solutions:**

- 먼저 `/codexspec:specify`를 실행하여 요구사항을 명확화하세요
- 그 다음 `/codexspec:generate-spec`을 실행하여 spec.md를 생성하세요

### "Constitution not found"

프로젝트 헌법이 존재하지 않습니다.

**Solutions:**

- `/codexspec:constitution`을 실행하여 생성하세요
- 헌법은 선택 사항이지만, 일관된 결정을 위해 권장됩니다

### "Tasks file not found"

태스크 분해가 존재하지 않습니다.

**Solutions:**

- 먼저 `/codexspec:spec-to-plan`을 실행했는지 확인하세요
- 그 다음 `/codexspec:plan-to-tasks`를 실행하여 tasks.md를 생성하세요

### "GitHub CLI not authenticated"

`/codexspec:tasks-to-issues` 명령어는 GitHub 인증이 필요합니다.

**Solutions:**

- GitHub CLI 설치: `brew install gh` (macOS) 또는 이에 상응하는 방법
- 인증: `gh auth login`
- 확인: `gh auth status`

---

## Next Steps

- [Workflow](workflow.md) - 일반적인 패턴과 각 명령어를 사용할 시점
- [CLI](../reference/cli.md) - 프로젝트 초기화를 위한 터미널 명령어
