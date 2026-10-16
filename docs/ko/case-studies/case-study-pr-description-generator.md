# CodexSpec 사례 연구: 프로젝트에 PR 설명 생성기 추가

> 과거 개발 사례입니다. 아래 대화, 중간 결정, 명령 순서, 검토 점수는 당시의 워크플로를 기록한 것으로 현재 명령 규칙을 뜻하지는 않습니다. 현재 표준 흐름에는 별도의 설계 단계와 `review-design`이 있으며, `clarify`는 확인된 요구사항을 먼저 갱신한 뒤 명세에 반영합니다. [현재 워크플로](../user-guide/workflow.md)와 [PR 명령 참조](../user-guide/commands.md#codexspecpr)를 참고하세요.

> 이 문서는 CodexSpec 도구 체인으로 CodexSpec 프로젝트 자체에 새 기능을 추가하는 전 과정을 기록한 것으로, 명세 기반 개발(SDD)을 실전에서 보여 줍니다.

## 개요

**대상 기능**: 구조화된 GitHub PR / GitLab MR 설명을 생성하는 `/codexspec:pr` 명령어 추가. (공개된 명령어의 사용자용 요약은 프로젝트 [README 의 `/codexspec:pr` 항목](https://github.com/Zts0hg/codexspec/blob/main/README.md)을 참조하세요.)

**개발 흐름**: `specify → generate-spec → review-spec → clarify → design-to-plan`

**핵심 특징**: 중간에 요구사항 이슈가 하나 드러났고 `clarify` 명령을 통해 수정되었습니다. 이는 SDD 의 유연성을 보여 줍니다. 동시에 CodexSpec **컨펌 게이트(Confirmation Gate)** 의 구체적인 사례이기도 합니다. 명시적으로 확인하기 전에는 그 어떤 것도 확정되지 않으며, 한 번 수락된 결정도 clarify 체크포인트에서 다시 열어 뒤집을 수 있습니다.

---

## 1단계: 초기 요구사항 명확화 (`/codexspec:specify`)

### 사용자 초기 입력

```
I want to add a feature to the project: a new Git-related command that generates accurate, detailed, and standards-compliant GitHub PR descriptions (or MR descriptions, for GitLab). Below are two PR commands I have used in other projects, provided for reference.

[Reference Example 1 - Structured Description]
Now, acting as a project maintainer, based on all the work we have done so far, write a clear Pull Request description for this submission.
The PR description should be aimed at the other reviewers on the team and include the following sections:
1. Context
2. Implementation
3. Testing
4. How to Verify

[Reference Example 2 - Simple Description]
Based on the code diff between the current branch and origin/main, use Markdown to produce a Merge Request title and description that comply with Git conventions. (Describe in Chinese.)
```

### 명확화 과정

**Q1: 출력 언어**

- 옵션: 프로젝트 설정을 따름 / 중국어 / 자동 감지
- **사용자 선택**: 프로젝트 설정을 따름(현재: en)

**Q2: 플랫폼 지원**

- 옵션: GitHub 와 GitLab 모두 지원 / GitHub 만 / 플랫폼 자동 감지
- **사용자 선택**: 플랫폼 자동 감지

**Q3: PR 설명 내용**

- 옵션: 상세 구조화 설명 / 간결한 설명 / 사용자 정의 템플릿
- **사용자 선택**: 상세 구조화 설명(권장)

**Q4: 트리거 조건**

- 옵션: 현재 브랜치 vs origin/main / 푸시되지 않은 커밋 / 대상 브랜치 설정 가능
- **사용자 선택**: 대상 브랜치 설정 가능

**Q5: Spec 소스**

- 옵션: spec.md 우선 / git 정보만 / 모든 소스 통합
- **사용자 선택**: 모든 소스 통합(권장)

**Q6: 명명**

- 옵션: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **사용자 선택**: codexspec.pr(권장)

**Q7: spec 이 없을 때 처리**

- 옵션: 그냥 생성, Context 건너뜀 / 먼저 spec 생성을 권유 / 경고하고 계속
- **사용자 선택**: 그냥 생성, Context 건너뜀

**Q8: 출력 방식**

- 옵션: 터미널 출력 / 파일로 저장 / 터미널 + 선택적 파일
- **사용자 선택**: 터미널 + 선택적 파일(권장)

**Q9: 기본 섹션**

- 옵션: Context, Implementation, Testing, How to Verify(모두 선택)
- **사용자 선택**: 네 섹션 모두

**Q10: 명령어 매개변수**

- **사용자 선택**: 모든 매개변수는 선택적
  - `--target-branch`: 기본값 origin/main
  - `--output`: 지정하지 않으면 기본적으로 터미널 출력만
  - `--sections`: 지정하지 않으면 기본값을 따름
  - `--no-spec`: spec.md 조회를 건너뜀

### 언어 설정 정정

**사용자 피드백**: 언어 동작은 `/commit-staged` 명령어와 같아야 합니다. 즉 `config.yml`의 `language.commit`을 먼저 따르고, `language.commit`이 설정되지 않았을 때만 `language.output`으로 폴백.

**수정된 요구사항 요약**:

```
Language priority: language.commit > language.output > English (default)
```

---

## 2단계: 명세 문서 생성 (`/codexspec:generate-spec`)

### 생성된 문서 구조

생성된 `spec.md`는 다음 섹션을 담습니다:

- **Overview**: 기능 개요
- **Goals**: 4개 목표
- **User Stories**: 수용 기준이 붙은 4개 사용자 스토리
- **Functional Requirements**: 8개 요구사항(REQ-001 ~ REQ-008)
- **Command Parameters**: 4개 매개변수 정의
- **Non-Functional Requirements**: 3개 요구사항(성능, 호환성, 오류 처리)
- **Acceptance Criteria (Test Cases)**: 10개 테스트 케이스
- **Edge Cases**: 6개 엣지 케이스
- **Output Format Example**: GitHub PR 과 GitLab MR 예시
- **Out of Scope**: 명시적으로 제외된 기능
- **Dependencies**: 의존성
- **Related Commands**: 관련 명령어

### 핵심 요구사항 발췌

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## 3단계: 명세 리뷰 (`/codexspec:review-spec`)

### 리뷰 결과

- **전체 상태**: ✅ Pass
- **품질 점수**: 92/100
- **준비도**: Ready for Planning

### 발견된 이슈

**경고(Should Fix)**:

1. **SPEC-001**: 테스트 파일 발견 로직이 명시적으로 정해지지 않음
2. **SPEC-002**: spec.md 파일이 여러 개일 때 "가장 최근 수정"으로 고르는 것이 부정확할 수 있음

**제안(Nice to Have)**:

1. `--title` 매개변수 추가를 고려
2. 출력 형식 검증 요구사항 추가
3. GitHub Enterprise URL 패턴 지원을 고려

### 리뷰 보고서 위치

`.codexspec/specs/2026-0613-1200ab-pr-description-generator/review-spec.md`

이것은 **증거 기반 리뷰**입니다. 위의 모든 경고와 제안은 spec 안의 구체적으로 확인할 수 있는 누락 사항에 연결되어 있으며, 권고 항목(Nice to Have)은 수용 여부에 영향을 주지도, 자동 변경을 트리거하지도 않습니다.

---

## 4단계: 요구사항 명확화와 조정 (`/codexspec:clarify`) — 결정적 전환점

### 발견된 이슈

**사용자 피드백**:
> spec.md 사용 방식에 문제가 하나 있습니다. 예를 들어 사용자가 아주 작은 변경을 하느라 CodexSpec 의 표준 흐름인 specify → plan → tasks → implement 를 밟지 않았을 수 있습니다. 대신 대화로 곧장 변경하거나 Claude Code 의 내장 플랜 모드를 썼고, 변경을 마친 뒤에야 별도로 CodexSpec 명령어를 불러 규범에 맞는 PR 설명을 만들려는 경우입니다. 이때 "가장 최근에 수정된" spec.md 가 기본값이면 이번 변경과 아무 상관없는 이전 spec.md 의 내용을 끌어오게 됩니다.

이것이 바로 **컨펌 게이트**가 작동하는 모습입니다. 앞선 결정("기본값: 가장 최근에 수정된 spec.md 사용")은 기록되어 있었지만 되돌릴 수 없을 정도로 확정된 것은 아니었습니다. 사용자가 실제 사용 패턴에 대한 새 정보를 가지고 clarify 체크포인트에서 다시 열었고, 이전에 수락된 기본값이 뒤집어졌습니다.

### 명확화 Q&A 과정

**Q1: spec 선택 전략**

**맥락**: 현재 EC-004는 "spec.md 가 여러 개 → 가장 최근 수정된 것 사용"이라고 되어 있습니다. 하지만 사용자가 SDD 흐름을 밟지 않고 작은 변경을 했다면, 가장 최근의 spec.md 가 현재 변경과 무관할 수 있습니다.

| 옵션 | 설명 |
|--------|-------------|
| A | 사용자가 명시적으로 `--spec`을 넘기지 않으면 기본으로 spec.md 사용 안 함 |
| B | 브랜치 이름으로 매칭 |
| C | 사용자에게 고르라고 프롬프트 |
| D | 파일 변경으로 매칭 |

**사용자 선택**: 옵션 A
**이유**: 잘못된 참조를 피합니다. `--spec` 매개변수로 SDD 연동을 원하는 사용자가 명시적으로 옵트인하게 합니다.

---

**Q2: spec 내용 추출 전략**

**맥락**: 사용자가 `--spec`을 넘길 때, spec.md 구조가 불완전하면 어떻게 할까요?

| 옵션 | 설명 |
|--------|-------------|
| A | 베스트에포트 추출, 누락 섹션은 건너뜀 |
| B | 경고하고 Context 건너뜀 |
| C | 완전한 구조를 요구, 아니면 에러 |

**사용자 선택**: 옵션 A
**이유**: spec 형식 이슈가 워크플로우를 막지 않게 합니다.

---

**Q3: 테스트 파일 발견**

**맥락**: Testing 섹션은 테스트 파일을 어떻게 발견해야 할까요?

| 옵션 | 설명 |
|--------|-------------|
| A | 일반적인 디렉토리 패턴(tests/, test/) |
| B | 언어 비의존 휴리스틱(디렉토리 + 파일명 패턴) |
| C | 능동적 발견은 하지 않고 커밋 메시지에서만 추론 |

**사용자 선택**: 옵션 B
**이유**: 여러 언어의 다양한 프로젝트 구조에 대응합니다.

---

**Q4: PR 제목 생성**

**맥락**: PR 제목을 어떻게 생성할까요?

| 옵션 | 설명 |
|--------|-------------|
| A | 브랜치명 파싱을 먼저 |
| B | 첫 커밋 메시지를 먼저 |
| C | 종합(git diff + 브랜치명 + 커밋 메시지) |

**사용자 선택**: 옵션 C
**사용자 이유**: 첫 커밋은 변경의 일부분만 대표할 수 있고, 브랜치명은 강한 명명 규율을 가정합니다. 참고할 수 있는 풍부한 git 정보와 코드 변경이 있으니 종합 분석이 더 정확합니다.

---

**Q5: 검증 명령 생성**

**맥락**: "How to Verify" 섹션은 검증 명령을 어떻게 생성할까요?

| 옵션 | 설명 |
|--------|-------------|
| A | 일반 템플릿 |
| B | 프로젝트 감지(pyproject.toml → pytest, package.json → npm test) |
| C | 커밋 메시지에서 추론 |

**사용자 선택**: 옵션 B
**이유**: 프로젝트 감지가 더 실용적인 검증 명령을 만듭니다.

---

### 명확화 세션 요약

| 질문 | 결정 | 영향 |
|----------|----------|--------|
| spec 선택 전략 | `--spec`으로 옵트인 | REQ-007, EC-004, 매개변수 표 |
| spec 내용 추출 | 베스트에포트 추출 | REQ-005b, EC-004c |
| 테스트 파일 발견 | 언어 비의존 휴리스틱 | REQ-006b |
| PR 제목 생성 | 종합 분석 | REQ-008a |
| 검증 명령 생성 | 프로젝트 파일 감지 | REQ-010 |

### 핵심 변경: 매개변수 논리의 반전

```
Original design: --no-spec (skip spec)
New design:      --spec (enable spec, opt-in)
```

이 반전이 본 사례에서 컨펌 게이트가 가장 선명하게 드러나는 부분입니다. 원래 "확정"이었던 기본값(`--no-spec`, 즉 spec 이 기본 켜짐)이, 사용자가 그 기본값 때문에 문제가 생길 실제 워크플로우를 제시하면서 다시 열리고, 뒤집히고, 옵트인으로 재확정되었습니다.

---

## 5단계: 기술 구현 계획 (`/codexspec:design-to-plan`)

### 계획 개요

**구현 방식**: Markdown 템플릿 파일(`/commit-staged`와 일관되게)

**새 의존성 없음** — 슬래시 명령어 템플릿 하나로 기능을 전달하며 Python 코드는 필요하지 않습니다.

### 기술 결정 요약

| 결정 | 선택 | 이유 |
|----------|--------|--------|
| 구현 방식 | Markdown 템플릿 | 기존 명령어와 일관, 유지보수 용이 |
| 언어 우선순위 | commit > output > en | `/codexspec:commit-staged`와 일관 |
| 플랫폼 감지 | Remote URL 파싱 | 단순하고 신뢰 가능 |
| spec 연동 | 옵트인(`--spec`) | 잘못된 참조 회피 |
| 내용 추출 | 베스트에포트 | 워크플로우를 막지 않음 |
| 테스트 발견 | 디렉토리 + 파일명 패턴 | 언어 비의존 |
| 제목 생성 | 종합 분석 | 가장 정확 |
| 명령 감지 | 프로젝트 파일 감지 | 더 실용적 |
| 출력 모드 | 터미널 먼저, 파일은 선택 | 유연 |

### 구현 단계

1. **1단계**: 템플릿 작성(YAML frontmatter, 언어 설정, Git 컨텍스트)
2. **2단계**: 핵심 기능(spec 연동, 테스트 발견, 명령 감지, 제목 생성)
3. **3단계**: 엣지 케이스 처리
4. **4단계**: 테스트
5. **5단계**: 문서 업데이트

### 파일 목록

**생성**:

- `templates/commands/pr.md`

**수정**:

- `CLAUDE.md` - 명령어 설명 추가
- `README.md` - 명령어를 목록에 추가

**테스트**:

- `tests/test_pr_template.py`

---

## 전체 흐름도

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CodexSpec SDD Development Flow                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:specify                                                     │
│  ├─ Clarify requirements through Q&A                                    │
│  ├─ User provides reference examples                                    │
│  └─ 10 questions covering language, platform, content, parameters, etc. │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:generate-spec                                               │
│  ├─ Generate a complete spec.md                                         │
│  ├─ 4 user stories, 8 functional requirements, 10 test cases            │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/spec.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:review-spec                                                 │
│  ├─ Quality score: 92/100                                               │
│  ├─ Found 2 warnings (test-file discovery, multi-spec handling)         │
│  └─ Status: Pass, can proceed to planning                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:clarify  (Critical adjustment)                              │
│  ├─ User surfaces a real-world usage issue                              │
│  ├─ 5 clarification questions, all answered                             │
│  ├─ Key change: --no-spec → --spec (opt-in)                             │
│  └─ Added 5 requirements (REQ-005b, 006b, 008a, 010, updated 007)       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:design-to-plan                                                │
│  ├─ Update the technical implementation plan                            │
│  ├─ 9 technical decisions, including 5 new ones                         │
│  ├─ 5 implementation phases                                             │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/plan.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Subsequent steps (not completed in this session)                       │
│  ├─ /codexspec:review-plan - Validate plan quality                      │
│  ├─ /codexspec:plan-to-tasks - Break down into executable tasks         │
│  └─ /codexspec:implement-tasks - Execute the implementation             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 핵심 교훈

### 1. clarify 단계의 가치

이 사례는 `clarify` 명령의 결정적 역할을 보여 줍니다:

- **사용 중에 실제 문제를 발견** — 작은 변경 시나리오에서 spec.md 가 잘못 쓰일 위험
- **명확화 Q&A 로 설계 결함을 해결** — 자동 감지에서 옵트인으로 전환
- **요구사항 변화를 체계적으로 기록** — 모든 변경이 spec.md 의 Clarifications 섹션에 저장

### 2. SDD 흐름의 유연성

- 선형 흐름이 아니며, 어느 단계에서든 돌아가 조정할 수 있습니다.
- `clarify`는 `review-spec` 이후, `design-to-plan` 이전에 끼워 넣을 수 있습니다.
- 명세 문서와 기술 계획 모두 변경을 반영하도록 갱신됩니다.

### 3. 매개변수 설계의 진화

```
Initial design:
  --no-spec: skip spec.md (used by default)

Final design:
  --spec: enable spec.md (not used by default)
```

이 변화는 "기본 SDD 워크플로우"에서 "비-SDD 워크플로우도 함께 지원"으로의 설계 전환을 반영하며, 도구를 더 범용으로 만듭니다.

### 4. 문서 산출물

| 단계 | 산출 파일 | 내용 |
|-------|-------------|---------|
| generate-spec | spec.md | 완전한 명세 문서 |
| review-spec | review-spec.md | 품질 리뷰 보고서 |
| clarify | (spec.md 갱신) | 명확화 기록 + 요구사항 갱신 |
| design-to-plan | plan.md | 기술 구현 계획 |

---

## 부록: 명령어 빠른 참조

```bash
# 1. Initial requirement clarification
/codexspec:specify

# 2. Generate the specification document
/codexspec:generate-spec

# 3. Review the specification quality
/codexspec:review-spec

# 4. Clarify/adjust requirements (optional; use when an issue is found)
/codexspec:clarify [issue description]

# 5. Generate the technical plan
/codexspec:design-to-plan

# 6. Review the plan quality (optional)
/codexspec:review-plan

# 7. Break down into tasks
/codexspec:plan-to-tasks

# 8. Execute the implementation
/codexspec:implement-tasks
```

---

*이 문서는 CodexSpec SDD 워크플로우로 생성되었으며, 실제 개발 대화를 기록합니다.*
