# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | **한국어** | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[📖 문서](https://zts0hg.github.io/codexspec/)**

**Claude Code를 위한 스펙 주도 개발 (SDD) 툴킷**

CodexSpec은 구조화되고 스펙 주도적인 접근 방식을 사용하여 고품질 소프트웨어를 구축하는 데 도움이 되는 툴킷입니다. 명세를 실행 가능한 아티팩트로 변환하여 구현을 직접 안내함으로써 전통적인 개발 방식을 역전시킵니다.

## 설계 철학: 인간-AI 협업

CodexSpec은 **효과적인 AI 지원 개발에는 모든 단계에서 적극적인 인간 참여가 필요하다**는 믿음을 기반으로 구축되었습니다. 이 툴킷은 핵심 원칙을 중심으로 설계되었습니다:

> **각 아티팩트를 진행하기 전에 검토하고 검증하세요.**

### 인간 감독이 중요한 이유

AI 지원 개발에서 검토 단계를 건너뛰면 다음과 같은 문제가 발생합니다:

| 문제 | 결과 |
|------|------|
| 불명확한 요구사항 | AI가 의도와 다른 가정을 함 |
| 불완전한 명세 | 중요한 엣지 케이스 없이 기능이 구축됨 |
| 잘못 정렬된 기술 계획 | 아키텍처가 비즈니스 요구와 일치하지 않음 |
| 모호한 태스크 분해 | 구현이 잘못된 방향으로 가서 비용이 많이 드는 재작업 필요 |

### CodexSpec 접근 방식

CodexSpec은 개발을 **검토 가능한 체크포인트**로 구조화합니다:

```
아이디어 → 명확화 → 검토 → 계획 → 검토 → 태스크 → 검토 → 분석 → 구현
                ↑              ↑              ↑
            인간 검토       인간 검토       인간 검토
```

**모든 아티팩트에는 해당하는 검토 명령어가 있습니다:**
- `spec.md` → `/codexspec.review-spec`
- `plan.md` → `/codexspec.review-plan`
- `tasks.md` → `/codexspec.review-tasks`
- 모든 아티팩트 → `/codexspec.analyze`

이 체계적인 검토 프로세스는 다음을 보장합니다:
- **조기 오류 감지**: 코드가 작성되기 전에 오해를 포착
- **정렬 검증**: AI의 해석이 의도와 일치하는지 확인
- **품질 게이트**: 각 단계에서 완전성, 명확성, 실현 가능성 검증
- **재작업 감소**: 검토에 몇 분을 투자하여 재구현에 몇 시간을 절약

## 기능

### 핵심 SDD 워크플로우
- **컨스티튜션 기반**: 모든 후속 결정을 안내하는 프로젝트 원칙 수립
- **2단계 명세**: 대화형 명확화(`/specify`) 후 문서 생성(`/generate-spec`)
- **계획 주도 개발**: 기술 선택은 요구사항 검증 이후에 수행
- **TDD 준비 태스크**: 태스크 분해가 테스트 우선 방법론을 강제

### 인간-AI 협업
- **검토 명령어**: 스펙, 계획, 태스크를 위한 전용 검토 명령어로 AI 출력 검증
- **대화형 명확화**: 즉각적인 피드백과 함께 Q&A 기반 요구사항 정제
- **교차 아티팩트 분석**: 구현 전에 스펙, 계획, 태스크 간 불일치 감지
- **품질 체크리스트**: 요구사항을 위한 자동화된 품질 평가

### 개발자 경험
- **Claude Code 통합**: Claude Code 슬래시 명령어 네이티브 지원
- **국제화 (i18n)**: LLM 동적 번역을 통한 다국어 지원
- **크로스 플랫폼**: Bash 및 PowerShell 스크립트 모두 지원
- **확장 가능**: 사용자 정의 명령어를 위한 플러그인 아키텍처

## 설치

### 사전 요구사항

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (권장) 또는 pip

### 방법 1: uv로 설치 (권장)

uv를 사용하는 것이 CodexSpec을 설치하는 가장 쉬운 방법입니다:

```bash
uv tool install codexspec
```

### 방법 2: pip로 설치

또는 pip를 사용할 수 있습니다:

```bash
pip install codexspec
```

### 방법 3: 일회성 사용

설치 없이 직접 실행:

```bash
# 새 프로젝트 생성
uvx codexspec init my-project

# 기존 프로젝트에서 초기화
cd your-existing-project
uvx codexspec init . --ai claude
```

### 방법 4: GitHub에서 설치 (개발 버전)

최신 개발 버전 또는 특정 브랜치 설치:

```bash
# uv 사용
uv tool install git+https://github.com/Zts0hg/codexspec.git

# pip 사용
pip install git+https://github.com/Zts0hg/codexspec.git

# 특정 브랜치 또는 태그
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## 빠른 시작

설치 후 CLI를 사용할 수 있습니다:

```bash
# 새 프로젝트 생성
codexspec init my-project

# 한국어 출력로 프로젝트 생성
codexspec init my-project --lang ko

# 기존 프로젝트에서 초기화
codexspec init . --ai claude
# 또는
codexspec init --here --ai claude

# 설치된 도구 확인
codexspec check

# 버전 보기
codexspec version
```

최신 버전으로 업그레이드:

```bash
# uv 사용
uv tool install codexspec --upgrade

# pip 사용
pip install --upgrade codexspec
```

## 사용법

### 1. 프로젝트 초기화

[설치](#설치) 후, 프로젝트를 생성하거나 초기화합니다:

```bash
codexspec init my-awesome-project
# 또는 현재 디렉토리에서
codexspec init . --ai claude
```

### 2. 프로젝트 원칙 수립

프로젝트 디렉토리에서 Claude Code를 시작합니다:

```bash
cd my-awesome-project
claude
```

`/codexspec.constitution` 명령어를 사용하여 프로젝트의 거버넌스 원칙을 생성합니다:

```
/codexspec.constitution 코드 품질, 테스트 표준 및 클린 아키텍처에 중점을 둔 원칙 생성
```

### 3. 요구사항 명확화

`/codexspec.specify`를 사용하여 대화형 Q&A로 요구사항을 **탐색하고 명확화**합니다:

```
/codexspec.specify 태스크 관리 애플리케이션을 구축하고 싶습니다
```

이 명령은:
- 아이디어를 이해하기 위한 명확화 질문을 합니다
- 고려하지 않았을 수 있는 엣지 케이스를 탐색합니다
- 대화를 통해 고품질 요구사항을 공동 창작합니다
- 파일을 자동으로 생성하지 **않음** - 사용자가 제어

### 4. 스펙 문서 생성

요구사항이 명확해지면, `/codexspec.generate-spec`을 사용하여 `spec.md` 문서를 생성합니다:

```
/codexspec.generate-spec
```

이 명령은 명확화된 요구사항을 구조화된 스펙 문서로 변환하는 "요구사항 컴파일러" 역할을 합니다.

### 5. 스펙 검토 (권장)

**계획 단계로 진행하기 전에 스펙을 검증하세요:**

```
/codexspec.review-spec
```

이 명령은 다음을 포함한 상세 검토 보고서를 생성합니다:
- 섹션 완전성 분석
- 명확성 및 테스트 가능성 평가
- 컨스티튜션 정렬 확인
- 우선순위가 지정된 권장사항

### 6. 기술 계획 생성

`/codexspec.spec-to-plan`을 사용하여 구현 방법을 정의합니다:

```
/codexspec.spec-to-plan 백엔드에 Python과 FastAPI, 데이터베이스에 PostgreSQL, 프론트엔드에 React 사용
```

이 명령은 **컨스티튜션 리뷰**를 포함합니다 - 계획이 프로젝트 원칙과 일치하는지 검증합니다.

### 7. 계획 검토 (권장)

**태스크로 분해하기 전에 기술 계획을 검증하세요:**

```
/codexspec.review-plan
```

이것은 다음을 검증합니다:
- 스펙 정렬
- 아키텍처 건전성
- 기술 스택 적절성
- 컨스티튜션 준수

### 8. 태스크 생성

`/codexspec.plan-to-tasks`를 사용하여 계획을 분해합니다:

```
/codexspec.plan-to-tasks
```

태스크는 다음과 함께 표준 단계로 구성됩니다:
- **TDD 강제**: 테스트 태스크가 구현 태스크보다 선행
- **병렬 마커 `[P]`**: 독립적인 태스크 식별
- **파일 경로 명세**: 태스크별 명확한 산출물

### 9. 태스크 검토 (권장)

**구현 전에 태스크 분해를 검증하세요:**

```
/codexspec.review-tasks
```

이것은 다음을 확인합니다:
- 계획 커버리지
- TDD 준수
- 의존성 정확성
- 태스크 세분성

### 10. 분석 (선택사항이지만 권장)

`/codexspec.analyze`를 사용하여 아티팩트 간 일관성 검사를 수행합니다:

```
/codexspec.analyze
```

이것은 스펙, 계획, 태스크 간의 문제를 감지합니다:
- 커버리지 갭 (태스크가 없는 요구사항)
- 중복 및 불일치
- 컨스티튜션 위반
- 명세 불충분 항목

### 11. 구현

`/codexspec.implement-tasks`를 사용하여 구현을 실행합니다:

```
/codexspec.implement-tasks
```

구현은 **조건부 TDD 워크플로우**를 따릅니다:
- 코드 태스크: 테스트 우선 (Red → Green → Verify → Refactor)
- 비테스트 가능 태스크 (문서, 설정): 직접 구현

## 사용 가능한 명령어

### CLI 명령어

| 명령어 | 설명 |
|--------|------|
| `codexspec init` | 새 CodexSpec 프로젝트 초기화 |
| `codexspec check` | 설치된 도구 확인 |
| `codexspec version` | 버전 정보 표시 |
| `codexspec config` | 프로젝트 설정 보기 또는 수정 |

### `codexspec init` 옵션

| 옵션 | 설명 |
|------|------|
| `PROJECT_NAME` | 새 프로젝트 디렉토리 이름 |
| `--here`, `-h` | 현재 디렉토리에서 초기화 |
| `--ai`, `-a` | 사용할 AI 어시스턴트 (기본값: claude) |
| `--lang`, `-l` | 출력 언어 (예: en, ko, zh-CN, ja) |
| `--force`, `-f` | 기존 파일 강제 덮어쓰기 |
| `--no-git` | git 초기화 건너뛰기 |
| `--debug`, `-d` | 디버그 출력 활성화 |

### `codexspec config` 옵션

| 옵션 | 설명 |
|------|------|
| `--set-lang`, `-l` | 출력 언어 설정 |
| `--set-commit-lang`, `-c` | 커밋 메시지 언어 설정 (기본값: 출력 언어) |
| `--list-langs` | 지원되는 모든 언어 나열 |

### 슬래시 명령어

초기화 후, Claude Code에서 다음 슬래시 명령어를 사용할 수 있습니다:

#### 핵심 워크플로우 명령어

| 명령어 | 설명 |
|--------|------|
| `/codexspec.constitution` | 교차 아티팩트 검증 및 동기화 영향 보고와 함께 프로젝트 컨스티튜션 생성 또는 업데이트 |
| `/codexspec.specify` | 대화형 Q&A로 요구사항 **명확화** (파일 생성 없음) |
| `/codexspec.generate-spec` | 요구사항 명확화 후 `spec.md` 문서 **생성** |
| `/codexspec.spec-to-plan` | 컨스티튜션 리뷰 및 모듈 의존성 그래프와 함께 스펙을 기술 계획으로 변환 |
| `/codexspec.plan-to-tasks` | 병렬 마커 `[P]`와 함께 원자적, TDD 강제 태스크로 계획 분해 |
| `/codexspec.implement-tasks` | 조건부 TDD 워크플로우로 태스크 실행 (코드는 TDD, 문서/설정은 직접) |

#### 리뷰 명령어 (품질 게이트)

| 명령어 | 설명 |
|--------|------|
| `/codexspec.review-spec` | 점수 매기기와 함께 완전성, 명확성, 일관성 및 테스트 가능성에 대한 스펙 검증 |
| `/codexspec.review-plan` | 실현 가능성, 아키텍처 품질 및 컨스티튜션 정렬에 대한 기술 계획 검토 |
| `/codexspec.review-tasks` | 계획 커버리지, TDD 준수, 의존성 및 세분성에 대한 태스크 분해 검증 |

#### 확장 명령어

| 명령어 | 설명 |
|--------|------|
| `/codexspec.clarify` | 4개 초점 카테고리를 사용하여 기존 spec.md의 모호성을 스캔하고 검토 결과와 통합 |
| `/codexspec.analyze` | 심각도 기반 문제 감지와 함께 비파괴적 교차 아티팩트 분석 (스펙, 계획, 태스크) |
| `/codexspec.checklist` | 요구사항 검증을 위한 품질 체크리스트 생성 |
| `/codexspec.tasks-to-issues` | 프로젝트 관리 통합을 위해 태스크를 GitHub 이슈로 변환 |

#### Git 워크플로우 명령어

| 명령어 | 설명 |
|--------|------|
| `/codexspec.commit` | git 상태와 세션 컨텍스트를 기반으로 Conventional Commits 메시지 생성 |
| `/codexspec.commit-staged` | 스테이징된 변경사항만으로 커밋 메시지 생성 |

## 워크플로우 개요

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec 인간-AI 협업 워크플로우                       │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  교차 아티팩트 검증과 함께                          │
│         │             프로젝트 원칙 정의                                  │
│         ▼                                                                │
│  2. Specify  ───────►  대화형 Q&A로 요구사항 명확화                       │
│         │             (파일 생성 없음 - 인간 제어)                        │
│         ▼                                                                │
│  3. Generate Spec  ─►  spec.md 문서 생성                                 │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ 검토 게이트 1: /codexspec.review-spec ★                        ║   │
│  ║  검증: 완전성, 명확성, 테스트 가능성, 컨스티튜션                   ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  모호성 해결 (반복적)                              │
│         │             4개 초점 카테고리, 최대 5개 질문                   │
│         ▼                                                                │
│  5. Spec to Plan  ──►  다음과 함께 기술 계획 생성:                       │
│         │               • 컨스티튜션 리뷰 (필수)                         │
│         │               • 모듈 의존성 그래프                             │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ 검토 게이트 2: /codexspec.review-plan ★                        ║   │
│  ║  검증: 스펙 정렬, 아키텍처, 기술 스택, 단계                        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  다음과 함께 원자적 태스크 생성:                   │
│         │               • TDD 강제 (구현 전 테스트)                      │
│         │               • 병렬 마커 [P]                                  │
│         │               • 파일 경로 명세                                 │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ 검토 게이트 3: /codexspec.review-tasks ★                       ║   │
│  ║  검증: 커버리지, TDD 준수, 의존성, 세분성                         ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  교차 아티팩트 일관성 검사                         │
│         │             갭, 중복, 컨스티튜션 문제 감지                     │
│         ▼                                                                │
│  8. Implement  ─────►  조건부 TDD 워크플로우로 실행                      │
│                        코드: 테스트 우선 | 문서/설정: 직접               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**핵심 통찰**: 각 검토 게이트(★)는 더 많은 시간을 투자하기 전에 AI 출력을 검증하는 **인간 체크포인트**입니다. 이 게이트를 건너뛰면 비용이 많이 드는 재작업으로 이어지는 경우가 많습니다.

### 핵심 개념: 요구사항 명확화 워크플로우

CodexSpec은 워크플로우의 다른 단계를 위해 **두 개의 별도 명령어**를 제공합니다:

#### specify vs clarify: 언제 어떤 것을 사용할까?

| 측면 | `/codexspec.specify` | `/codexspec.clarify` |
|------|----------------------|----------------------|
| **목적** | 초기 요구사항 탐색 | 기존 스펙의 반복적 정제 |
| **사용 시기** | 새 아이디어로 시작, spec.md 없음 | spec.md 존재, 간극 채우기 필요 |
| **입력** | 초기 아이디어 또는 요구사항 | 기존 spec.md 파일 |
| **출력** | 없음 (대화만) | 명확화 내용으로 spec.md 업데이트 |
| **방법** | 개방형 Q&A | 구조화된 모호성 스캔 (4개 카테고리) |
| **질문 제한** | 무제한 | 최대 5개 질문 |
| **일반적 용도** | "할일 앱을 구축하고 싶다" | "스펙에 에러 처리 세부사항이 없다" |

#### 2단계 스펙 작성

문서 생성 전:

| 단계 | 명령어 | 목적 | 출력 |
|------|--------|------|------|
| **탐색** | `/codexspec.specify` | 대화형 Q&A로 요구사항 탐색 및 정제 | 없음 (대화만) |
| **생성** | `/codexspec.generate-spec` | 명확화된 요구사항을 구조화된 문서로 컴파일 | `spec.md` |

#### 반복적 명확화

spec.md 생성 후:

```
spec.md ──► /codexspec.clarify ──► 업데이트된 spec.md (Clarifications 섹션 포함)
                │
                └── 4개 초점 카테고리의 모호성 스캔:
                    • 완전성 갭 - 누락된 섹션, 빈 콘텐츠
                    • 구체성 문제 - 모호한 용어, 정의되지 않은 제약조건
                    • 행동 명확성 - 에러 처리, 상태 전환
                    • 측정 가능성 문제 - 메트릭 없는 비기능적 요구사항
```

#### 이 설계의 이점

- **인간-AI 협업**: 요구사항 발견에 적극적으로 참여
- **명시적 제어**: 사용자가 결정할 때만 파일 생성
- **품질 중심**: 문서화 전에 요구사항을 철저히 탐색
- **반복적 정제**: 이해가 깊어짐에 따라 스펙을 점진적으로 개선

## 프로젝트 구조

초기화 후, 프로젝트는 다음 구조를 갖게 됩니다:

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # 프로젝트 거버넌스 원칙
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # 기능 스펙
│   │       ├── plan.md        # 기술 계획
│   │       ├── tasks.md       # 태스크 분해
│   │       └── checklists/    # 품질 체크리스트
│   ├── templates/             # 사용자 정의 템플릿
│   ├── scripts/               # 헬퍼 스크립트
│   │   ├── bash/              # Bash 스크립트
│   │   └── powershell/        # PowerShell 스크립트
│   └── extensions/            # 사용자 정의 확장
├── .claude/
│   └── commands/              # Claude Code 슬래시 명령어
└── CLAUDE.md                  # Claude Code용 컨텍스트
```

## 국제화 (i18n)

CodexSpec은 **LLM 동적 번역**을 통해 여러 언어를 지원합니다. 번역된 템플릿을 유지하는 대신, Claude가 언어 설정에 따라 런타임에 콘텐츠를 번역합니다.

### 언어 설정

**초기화 시:**
```bash
# 중국어 출력으로 프로젝트 생성
codexspec init my-project --lang zh-CN

# 일본어 출력으로 프로젝트 생성
codexspec init my-project --lang ja
```

**초기화 후:**
```bash
# 현재 설정 보기
codexspec config

# 언어 설정 변경
codexspec config --set-lang zh-CN

# 지원되는 언어 나열
codexspec config --list-langs
```

### 커밋 메시지 언어

출력 언어와 다른 언어로 커밋 메시지를 구성할 수 있습니다:

```bash
# 상호작용은 한국어, 커밋 메시지는 영어
codexspec config --set-lang ko
codexspec config --set-commit-lang en
```

**커밋 메시지의 언어 우선순위:**
1. `language.commit` 설정 (지정된 경우)
2. `language.output` (대체)
3. `"en"` (기본값)

**참고:** 커밋 타입 (feat, fix, docs 등)과 스코프는 항상 영어로 유지됩니다. 설명 부분만 구성된 언어를 사용합니다.

### 설정 파일

`.codexspec/config.yml` 파일에 언어 설정이 저장됩니다:

```yaml
version: "1.0"

language:
  # Claude 상호작용 및 생성된 문서의 출력 언어
  output: "zh-CN"

  # 커밋 메시지 언어 (기본값: 출력 언어)
  # 출력 언어와 관계없이 영어 커밋 메시지를 원하면 "en"으로 설정
  commit: "zh-CN"

  # 템플릿 언어 - 호환성을 위해 "en" 유지
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### 지원되는 언어

| 코드 | 언어 |
|------|------|
| `en` | English (기본값) |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `ru` | Русский |
| `it` | Italiano |
| `ar` | العربية |
| `hi` | हिन्दी |

### 작동 방식

1. **단일 영어 템플릿**: 모든 명령어 템플릿은 영어로 유지됩니다
2. **언어 설정**: 프로젝트에서 선호하는 출력 언어를 지정합니다
3. **동적 번역**: Claude가 영어 지침을 읽고 대상 언어로 출력합니다
4. **컨텍스트 인식**: 기술 용어(JWT, OAuth 등)는 적절할 때 영어로 유지됩니다

### 이점

- **번역 유지보수 없음**: 여러 템플릿 버전을 유지할 필요가 없습니다
- **항상 최신 상태**: 템플릿 업데이트는 모든 언어에 자동으로 적용됩니다
- **컨텍스트 인식 번역**: Claude가 자연스럽고 상황에 적절한 번역을 제공합니다
- **무제한 언어**: Claude가 지원하는 모든 언어가 즉시 작동합니다

### Constitution 및 생성된 문서

`/codexspec.constitution`을 사용하여 프로젝트 constitution을 생성하면, 구성에 지정된 언어로 생성됩니다:

- **단일 파일 접근법**: Constitution은 하나의 언어로만 생성됩니다
- **Claude는 모든 언어 이해**: Claude는 지원되는 모든 언어의 constitution 파일을 처리할 수 있습니다
- **팀 협업**: 팀은 일관된 작업 언어를 사용해야 합니다

이 설계는 여러 언어 버전 간의 동기화 문제를 피하고 유지보수 오버헤드를 줄입니다.

## 확장 시스템

CodexSpec은 사용자 정의 명령어를 추가하기 위한 플러그인 아키텍처를 지원합니다:

### 확장 구조

```
my-extension/
├── extension.yml          # 확장 매니페스트
├── commands/              # 사용자 정의 슬래시 명령어
│   └── command.md
└── README.md
```

### 확장 생성

1. `extensions/template/`에서 템플릿 복사
2. `extension.yml`을 확장 세부 정보로 수정
3. `commands/`에 사용자 정의 명령어 추가
4. 로컬에서 테스트 후 게시

자세한 내용은 `extensions/EXTENSION-DEVELOPMENT-GUIDE.md`를 참조하세요.

## 개발

### 사전 요구사항

- Python 3.11+
- uv 패키지 매니저
- Git

### 로컬 개발

```bash
# 저장소 클론
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# 개발 의존성 설치
uv sync --dev

# 로컬에서 실행
uv run codexspec --help

# 테스트 실행
uv run pytest

# 코드 린트
uv run ruff check src/
```

### 빌드

```bash
# 패키지 빌드
uv build
```

## spec-kit과의 비교

CodexSpec은 GitHub의 spec-kit에서 영감을 받았지만 몇 가지 주요 차이점이 있습니다:

| 기능 | spec-kit | CodexSpec |
|------|----------|-----------|
| 핵심 철학 | 스펙 주도 개발 | 스펙 주도 개발 + 인간-AI 협업 |
| CLI 이름 | `specify` | `codexspec` |
| 주요 AI | 멀티 에이전트 지원 | Claude Code 중심 |
| 명령어 접두사 | `/speckit.*` | `/codexspec.*` |
| 컨스티튜션 시스템 | 기본 | 교차 아티팩트 검증을 갖춘 완전한 컨스티튜션 |
| 2단계 스펙 | 없음 | 있음 (명확화 + 생성) |
| 리뷰 명령어 | 선택사항 | 점수 매기기를 갖춘 3개 전용 리뷰 명령어 |
| Clarify 명령어 | 있음 | 4개 초점 카테고리, 리뷰 통합 |
| Analyze 명령어 | 있음 | 읽기 전용, 심각도 기반, 컨스티튜션 인식 |
| 태스크의 TDD | 선택사항 | 강제 (테스트가 구현보다 선행) |
| 구현 | 표준 | 조건부 TDD (코드 vs 문서/설정) |
| 확장 시스템 | 있음 | 있음 |
| PowerShell 스크립트 | 있음 | 있음 |
| i18n 지원 | 없음 | 있음 (LLM 번역을 통한 13개 이상 언어) |

### 주요 차별화 요소

1. **검토 우선 문화**: 모든 주요 아티팩트에는 전용 리뷰 명령어가 있음
2. **컨스티튜션 거버넌스**: 원칙이 단순히 문서화되는 것이 아니라 검증됨
3. **기본 TDD**: 태스크 생성에 테스트 우선 방법론이 강제됨
4. **인간 체크포인트**: 검증 게이트를 중심으로 설계된 워크플로우

## 철학

CodexSpec은 다음 핵심 원칙을 따릅니다:

### SDD 기본 사항

1. **의도 주도 개발**: 스펙은 "어떻게"보다 먼저 "무엇"을 정의합니다
2. **풍부한 스펙 생성**: 가드레일과 조직 원칙 사용
3. **다단계 정제**: 원샷 코드 생성 대신
4. **컨스티튜션 거버넌스**: 프로젝트 원칙이 모든 결정을 안내

### 인간-AI 협업

5. **인간-인-더-루프**: AI가 아티팩트를 생성하고 인간이 검증
6. **리뷰 지향**: 각 아티팩트를 진행하기 전에 검증
7. **점진적 공개**: 복잡한 정보가 점진적으로 공개됨
8. **명시적优于 암시적**: 요구사항은 가정이 아닌 명확해야 함

### 품질 보증

9. **기본 테스트 주도**: TDD 워크플로우가 태스크 생성에 내장됨
10. **교차 아티팩트 일관성**: 스펙, 계획, 태스크를 함께 분석
11. **컨스티튜션 정렬**: 모든 아티팩트가 프로젝트 원칙을 존중

### 리뷰가 중요한 이유

| 리뷰 없이 | 리뷰와 함께 |
|----------|------------|
| AI가 잘못된 가정을 함 | 인간이 조기에 잘못된 해석을 포착 |
| 불완전한 요구사항이 전파됨 | 구현 전에 갭이 식별됨 |
| 아키텍처가 의도에서 벗어남 | 각 단계에서 정렬이 검증됨 |
| 태스크가 중요 기능을 누락 | 커버리지가 체계적으로 검증됨 |
| **결과: 재작업, 낭비된 노력** | **결과: 첫 번째에 맞음** |

## 기여

기여를 환영합니다! 풀 리퀘스트를 제출하기 전에 기여 가이드라인을 읽어주세요.

## 라이선스

MIT 라이선스 - 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

## 감사의 글

- [GitHub spec-kit](https://github.com/github/spec-kit)에서 영감을 받았습니다
- [Claude Code](https://claude.ai/code)를 위해 구축되었습니다
