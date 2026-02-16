# CodexSpec

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | **한국어** | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Claude Code를 위한 스펙 주도 개발 (SDD) 툴킷**

CodexSpec은 구조화되고 스펙 주도적인 접근 방식을 사용하여 고품질 소프트웨어를 구축하는 데 도움이 되는 툴킷입니다. 명세를 실행 가능한 아티팩트로 변환하여 구현을 직접 안내함으로써 전통적인 개발 방식을 역전시킵니다.

## 기능

- **구조화된 워크플로우**: 개발의 각 단계별 명확한 명령어
- **Claude Code 통합**: Claude Code 슬래시 명령어 네이티브 지원
- **컨스티튜션 기반**: 프로젝트 원칙이 모든 결정을 안내
- **스펙 우선**: 어떻게보다 무엇과 왜를 먼저 정의
- **계획 주도**: 기술 선택은 요구사항 이후에 수행
- **태스크 지향**: 구현을 실행 가능한 태스크로 분해
- **품질 보증**: 리뷰, 분석 및 체크리스트 명령어 내장
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
# 새 프로젝트 생성 (한국어 출력)
codexspec init my-project --lang ko

# 기존 프로젝트에서 초기화
codexspec init . --ai claude

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
codexspec init my-awesome-project --lang ko
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

### 5. 기술 계획 생성

`/codexspec.spec-to-plan`을 사용하여 구현 방법을 정의합니다:

```
/codexspec.spec-to-plan 백엔드에 Python과 FastAPI, 데이터베이스에 PostgreSQL, 프론트엔드에 React 사용
```

### 6. 태스크 생성

`/codexspec.plan-to-tasks`를 사용하여 계획을 분해합니다:

```
/codexspec.plan-to-tasks
```

### 7. 분석 (선택사항이지만 권장)

`/codexspec.analyze`를 사용하여 아티팩트 간 일관성 검사를 수행합니다:

```
/codexspec.analyze
```

### 8. 구현

`/codexspec.implement-tasks`를 사용하여 구현을 실행합니다:

```
/codexspec.implement-tasks
```

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
| `--list-langs` | 지원되는 모든 언어 나열 |

### 슬래시 명령어

초기화 후, Claude Code에서 다음 슬래시 명령어를 사용할 수 있습니다:

#### 핵심 명령어

| 명령어 | 설명 |
|--------|------|
| `/codexspec.constitution` | 프로젝트 거버넌스 원칙 생성 또는 업데이트 |
| `/codexspec.specify` | 대화형 Q&A로 요구사항 **명확화** (파일 생성 없음) |
| `/codexspec.generate-spec` | 요구사항 명확화 후 `spec.md` 문서 **생성** |
| `/codexspec.spec-to-plan` | 스펙을 기술 계획으로 변환 |
| `/codexspec.plan-to-tasks` | 계획을 실행 가능한 태스크로 분해 |
| `/codexspec.implement-tasks` | 분해에 따라 태스크 실행 |

#### 리뷰 명령어

| 명령어 | 설명 |
|--------|------|
| `/codexspec.review-spec` | 스펙 완전성 리뷰 |
| `/codexspec.review-plan` | 기술 계획 실현 가능성 리뷰 |
| `/codexspec.review-tasks` | 태스크 분해 완전성 리뷰 |

#### 확장 명령어

| 명령어 | 설명 |
|--------|------|
| `/codexspec.clarify` | 기존 spec.md를 스캔하여 모호한 영역을 찾고 명확화 내용으로 업데이트 |
| `/codexspec.analyze` | 아티팩트 간 일관성 분석 |
| `/codexspec.checklist` | 요구사항용 품질 체크리스트 생성 |
| `/codexspec.tasks-to-issues` | 태스크를 GitHub issues로 변환 |

## 워크플로우 개요

```
┌──────────────────────────────────────────────────────────────┐
│                    CodexSpec 워크플로우                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitution  ──►  프로젝트 원칙 정의                     │
│         │                                                    │
│         ▼                                                    │
│  2. Specify  ───────►  대화형 Q&A로 요구사항                  │
│         │             명확화 (파일 생성 없음)                 │
│         │                                                    │
│         ▼                                                    │
│  3. Generate Spec  ─►  spec.md 문서 생성                     │
│         │             (사용자가 명시적으로 호출)              │
│         │                                                    │
│         ▼                                                    │
│  4. Review Spec  ───►  스펙 검증                              │
│         │                                                    │
│         ▼                                                    │
│  5. Clarify  ───────►  모호성 해결 (선택사항)                 │
│         │                                                    │
│         ▼                                                    │
│  6. Spec to Plan  ──►  기술 계획 생성                         │
│         │                                                    │
│         ▼                                                    │
│  7. Review Plan  ───►  기술 계획 검증                         │
│         │                                                    │
│         ▼                                                    │
│  8. Plan to Tasks  ─►  태스크 분해 생성                       │
│         │                                                    │
│         ▼                                                    │
│  9. Analyze  ───────►  아티팩트 간 일관성 (선택사항)           │
│         │                                                    │
│         ▼                                                    │
│  10. Review Tasks  ─►  태스크 분해 검증                       │
│         │                                                    │
│         ▼                                                    │
│  11. Implement  ─────►  구현 실행                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 핵심 개념: 요구사항 명확화 워크플로우

CodexSpec은 워크플로우의 다른 단계를 위해 **두 개의 별도 명령어**를 제공합니다:

#### specify vs clarify: 언제 어떤 것을 사용할까?

| 측면 | `/codexspec.specify` | `/codexspec.clarify` |
|------|----------------------|----------------------|
| **목적** | 초기 요구사항 탐색 | 기존 스펙의 반복적 정제 |
| **사용 시기** | 새 아이디어로 시작, spec.md 없음 | spec.md 존재, 간극 채우기 필요 |
| **입력** | 초기 아이디어 또는 요구사항 | 기존 spec.md 파일 |
| **출력** | 없음 (대화만) | 명확화 내용으로 spec.md 업데이트 |
| **방법** | 개방형 Q&A | 구조화된 모호성 스캔 (6개 카테고리) |
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
                └── 6개 카테고리의 모호성 스캔:
                    • 기능 범위 및 동작
                    • 도메인 및 데이터 모델
                    • 상호작용 및 UX 흐름
                    • 비기능적 품질 속성
                    • 엣지 케이스 및 실패 처리
                    • 충돌 해결
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
# 한국어 출력으로 프로젝트 생성
codexspec init my-project --lang ko

# 중국어 출력으로 프로젝트 생성
codexspec init my-project --lang zh-CN
```

**초기화 후:**
```bash
# 현재 설정 보기
codexspec config

# 언어 설정 변경
codexspec config --set-lang ko

# 지원되는 언어 나열
codexspec config --list-langs
```

### 설정 파일

`.codexspec/config.yml` 파일에 언어 설정이 저장됩니다:

```yaml
version: "1.0"

language:
  # Claude 상호작용 및 생성된 문서의 출력 언어
  output: "ko"

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
| 핵심 철학 | 스펙 주도 개발 | 스펙 주도 개발 |
| CLI 이름 | `specify` | `codexspec` |
| 주요 AI | 멀티 에이전트 지원 | Claude Code 중심 |
| 명령어 접두사 | `/speckit.*` | `/codexspec.*` |
| 워크플로우 | specify → plan → tasks → implement | constitution → specify → generate-spec → plan → tasks → analyze → implement |
| 2단계 스펙 | 없음 | 있음 (명확화 + 생성) |
| 리뷰 단계 | 선택사항 | 리뷰 명령어 내장 |
| Clarify 명령어 | 있음 | 있음 |
| Analyze 명령어 | 있음 | 있음 |
| Checklist 명령어 | 있음 | 있음 |
| 확장 시스템 | 있음 | 있음 |
| PowerShell 스크립트 | 있음 | 있음 |
| i18n 지원 | 없음 | 있음 (LLM 번역을 통한 13개 이상 언어) |

## 철학

CodexSpec은 다음 핵심 원칙을 따릅니다:

1. **의도 주도 개발**: 스펙은 "어떻게"보다 먼저 "무엇"을 정의합니다
2. **풍부한 스펙 생성**: 가드레일과 조직 원칙 사용
3. **다단계 정제**: 원샷 코드 생성 대신
4. **AI에 대한 높은 의존**: 스펙 해석에 AI 활용
5. **리뷰 지향**: 각 아티팩트를 진행하기 전에 검증
6. **품질 우선**: 요구사항 품질을 위한 체크리스트 및 분석 내장

## 기여

기여를 환영합니다! 풀 리퀘스트를 제출하기 전에 기여 가이드라인을 읽어주세요.

## 라이선스

MIT 라이선스 - 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

## 감사의 글

- [GitHub spec-kit](https://github.com/github/spec-kit)에서 영감을 받았습니다
- [Claude Code](https://claude.ai/code)를 위해 구축되었습니다
