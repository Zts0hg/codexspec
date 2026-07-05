# 빠른 시작

이 페이지는 완전한 **Requirements-First SDD** 흐름을 여덟 단계로 안내합니다. 확정된 요구사항이 가장 높은 우선순위의 권위이며, 명시적으로 확인하기 전에는 그 어떤 것도 확정되지 않습니다. 각 단계는 사용자가 통제하는 **컨펌 게이트(Confirmation Gate)** 에서 끝납니다.

작고 범위가 명확한 변경이라면 전체 흐름을 건너뛰고 [`/codexspec:quick`](#작은-변경-codexspecquick) 을 실행하는 것이 더 빠릅니다.

## 1. 프로젝트 초기화

설치 후 프로젝트를 생성하거나 초기화합니다:

```bash
# 새 프로젝트 생성
codexspec init my-awesome-project

# 또는 현재 디렉토리에서 초기화
codexspec init . --ai claude

# 한국어 출력(출력 기준 언어)으로 설정
codexspec init my-project --lang ko-KR

# 완전한 비대화형(CI/스크립트): ko-KR 출력 기준, 영어 커밋 메시지
codexspec init my-project --lang ko-KR --commit-lang en

# 모든 언어 차원을 명시적으로 지정(스크립트용, 프롬프트 없음)
codexspec init my-project \
  --interaction-lang ko-KR --document-lang en --commit-lang en
```

그런 다음 프로젝트로 이동해 Claude Code를 실행합니다:

```bash
cd my-awesome-project
claude
```

## 2. 프로젝트 원칙 수립

constitution 명령어로 이후 모든 산출물이 검증받게 될 기준을 세웁니다:

```
/codexspec:constitution 코드 품질과 테스트에 집중하는 원칙을 만들어 줘
```

## 3. 요구사항 명확화

`/codexspec:specify`로 요구사항을 탐색합니다:

```
/codexspec:specify 작업 관리 애플리케이션을 만들고 싶어
```

이 명령어는 명확화 질문을 던지고, 엣지 케이스를 드러내며, 최종 요구사항 요약을 확정하도록 요청합니다. 확정된 요약은 `requirements.md`에 저장됩니다.

> **컨펌 게이트**: `/codexspec:specify`는 사용자가 명시적으로 확인한 항목만 기록합니다. 명령어가 제시하는 요구사항 요약은 사용자가 수락하기 전까지는 확정 사항이 **아닙니다**. 예(Yes)라고 답하기 전에 거부·수정·재검토가 가능합니다. 이 자리에서 확인한 내용은 하단 어느 단계도 덮어쓸 수 없습니다.

## 4. 명세서 생성

요구사항 요약이 확정되면 명세 문서를 생성합니다:

```
/codexspec:generate-spec
```

`generate-spec`은 확정된 항목들을 추적 가능성을 위한 소스 참조와 함께 구조화된 `spec.md`로 정리한 뒤, 자동 리뷰를 실행합니다(결함은 구체적인 증거를 요구하고, 권고 제안은 자동 변경을 트리거하지 않으며, 검증된 결함은 최대 두 라운드까지 수정 및 재리뷰될 수 있습니다).

## 5. 리뷰 및 검증

**권장:** 다음 단계로 넘어가기 전에 명세를 검증합니다:

```
/codexspec:review-spec
```

이것은 **증거 기반 리뷰**입니다. 보고된 모든 결함은 구체적인 증거를 인용하며, 설계 권고는 수용 여부와 분리되어 있습니다.

## 6. 기술 계획 수립

```
/codexspec:spec-to-plan 백엔드에는 Python FastAPI 사용
```

계획은 명세 요구사항을 향한 `Covers` 링크를 기록하고, 적용 가능한 헌법 원칙을 검증합니다.

## 7. 태스크 생성

```
/codexspec:plan-to-tasks
```

태스크는 검증 가능한 결과 중심으로 구성되며, 계획과 요구사항을 향한 추적 링크를 유지합니다. 테스트 우선 순서는 **조건부로** 적용됩니다. 계획·헌법·태스크 리스크가 요구하는 곳에서만 적용하며, 테스트 불가능한 태스크(문서, 설정)는 직접 구현합니다.

## 8. 구현

```
/codexspec:implement-tasks
```

구현은 **조건부 TDD**를 따릅니다. 코드 태스크는 필요한 경우 Red → Green → Verify → Refactor 주기를 사용하고, 문서 및 설정 태스크는 직접 구현합니다.

## 작은 변경: `/codexspec:quick`

작고 범위가 명확한 변경이라면 여덟 단계 전체 흐름을 밟을 필요가 없습니다. `/codexspec:quick`은 단일 명령으로 Requirements-First SDD 의 압축된 흐름을 실행합니다:

```
/codexspec:quick 로그인 폼에 '로그인 상태 유지' 체크박스 추가
```

Quick 역시 전체 흐름과 동일한 가이드라인을 지킵니다:

- `/codexspec:specify`와 동일한 타임스탬프 규칙으로 기능 워크스페이스와 `requirements.md`를 생성합니다.
- 간결한 확정 요구사항 요약(`NEED-*`, 관련 `CON-*`/`DEC-*`, `OUT-*`, 미해결 `OPEN-*`)을 제시하고, 사용자의 명시적 확인을 기다립니다. **컨펌 게이트**는 여전히 적용됩니다.
- 그런 다음 `/codexspec:generate-spec` → `/codexspec:spec-to-plan` → `/codexspec:plan-to-tasks` → `/codexspec:implement-tasks`를 해당 기능 디렉토리에 대해 연쇄 실행하며, 각 생성 명령은 자체적인 자동 리뷰 루프를 갖습니다.

변경이 광범위하거나 여러 독립적인 결과로 이어진다면 Quick은 잠시 멈추고 표준 흐름을 권합니다.

## 프로젝트 구조

초기화 후:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # 프로젝트 헌법
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # 기능 명세
│   │       ├── plan.md        # 기술 계획
│   │       ├── tasks.md       # 태스크 분해
│   │       └── checklists/    # 품질 체크리스트
│   ├── templates/             # 커스텀 템플릿
│   ├── scripts/               # 헬퍼 스크립트
│   └── extensions/            # 커스텀 확장
├── .claude/
│   └── commands/              # Claude Code 슬래시 명령어
├── .agents/
│   └── skills/                # Codex 스킬 (--ai codex 또는 both 로 초기화한 경우)
├── CLAUDE.md                  # Claude Code 컨텍스트
└── AGENTS.md                  # Codex 컨텍스트
```

## 다음 단계

[전체 워크플로우 가이드](../user-guide/workflow.md)
