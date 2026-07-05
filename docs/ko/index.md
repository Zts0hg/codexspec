<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# CodexSpec에 오신 것을 환영합니다

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Claude Code를 위한 Requirements-First SDD 툴킷**

CodexSpec은 **Requirements-First SDD(요구사항 우선 명세 기반 개발)** 를 통해 고품질 소프트웨어를 구축하도록 돕습니다. 핵심은 **확정된 요구사항이 가장 높은 우선순위의 권위**를 가지며, 명시적으로 확인하기 전에는 그 무엇도 확정으로 간주하지 않는다는 점입니다. 곧바로 코드로 넘어가는 대신, **무엇을** 만들고 **왜** 만들지를 먼저 확정한 뒤에 **어떻게** 구현할지를 결정합니다.

## 왜 CodexSpec인가요?

Claude Code 위에서 왜 CodexSpec을 써야 할까요? 두 환경을 비교해 보면:

| 측면 | Claude Code만 사용 | CodexSpec + Claude Code |
|------|-------------------|-------------------------|
| **다국어 지원** | 기본적으로 영어로 상호작용 | 팀 언어를 설정해 협업과 리뷰를 더 매끄럽게 진행 |
| **추적 가능성** | 세션이 끝나면 의사결정을 거슬러 따라가기 어려움 | 모든 명세, 계획, 태스크가 `.codexspec/specs/`에 저장 |
| **세션 복구** | 플랜 모드가 중간에 끊기면 복구가 어려움 | 여러 명령으로 분할 + 문서가 영속적으로 저장되어 쉽게 복구 |
| **팀 거버넌스** | 통일된 원칙이 없고 스타일이 들쭉날쭉 | `constitution.md`가 팀 표준과 품질을 강제 |

### Requirements-First SDD란?

**Requirements-First SDD** 는 명세 기반 개발(SDD) 방법론에 핵심적인 업그레이드 하나를 더한 것입니다. 바로 **확정된 요구사항이 가장 높은 우선순위의 권위**를 갖는다는 원칙입니다. *무엇을* 만들고 *왜* 만들지를 먼저 정의하고 확정한 다음에야 *어떻게* 만들지를 결정하며, 명시적으로 확인하기 전에는 그 어떤 것도 확정되지 않습니다.

```
전통적 방식:  아이디어 → 코드 → 디버그 → 다시 작성
SDD:          아이디어 → 확정된 요구사항 → 명세 → 계획 → 태스크 → 코드
```

### 주요 기능

- **헌법(Constitution) 기반 개발** - 모든 결정을 이끄는 프로젝트 원칙을 확립
- **요구사항의 영속적 캡처** - `/specify`가 문서 생성 전에 확정된 논의를 `requirements.md`로 기록
- **자동 리뷰** - 생성된 모든 명세, 계획, 태스크 산출물에 품질 검사가 내장
- **대화형 명확화** - Q&A 기반 요구사항 정제
- **교차 산출물 분석** - 구현 전 불일치를 조기에 발견
- **추적 가능한 태스크** - 태스크 분해가 요구사항과 계획의 커버리지를 보존하며, **조건부 TDD(Conditional TDD)** 를 적용합니다(계획·헌법·리스크가 요구하는 곳에서만 테스트 우선 순서를 적용하고, 문서/설정 등 테스트 불가능한 태스크는 직접 구현)
- **네이티브 Claude Code 연동** - 슬래시 명령어가 자연스럽게 동작
- **다국어 지원** - LLM 동적 번역으로 13개 이상 언어 지원
- **크로스 플랫폼** - Bash와 PowerShell 스크립트를 함께 제공
- **확장 가능** - 커스텀 명령어를 위한 플러그인 아키텍처

## 빠른 시작

```bash
# 설치
uv tool install codexspec

# 새 프로젝트 생성
codexspec init my-project

# 또는 기존 프로젝트에서 초기화
codexspec init . --ai claude
```

[전체 설치 가이드](getting-started/installation.md)

## 워크플로우 개요

CodexSpec은 개발을 **검토 가능한 체크포인트** 로 구성합니다. 확정된 요구사항이 명세, 계획, 태스크를 거쳐 코드로 흘러가며, 매 단계마다 리뷰가 이루어집니다.

```
아이디어 → 확정된 요구사항 → 명세 → 계획 → 태스크 → 코드
```

모든 산출물은 전용 명령어가 생성하며, 다음 단계로 넘어가기 전에 검증됩니다:

```
아이디어 → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                       │                        │                           │
                                                  명세 리뷰                계획 리뷰                  태스크 리뷰
```

### 컨펌 게이트(Confirmation Gate)

결정적인 차별점은 **컨펌 게이트(Confirmation Gate)** 입니다. 요구사항, 명세, 계획, 태스크는 사용자가 명시적으로 확인한 이후에만 확정 사항이 됩니다. 확정된 요구사항이 가장 높은 우선순위의 기능 권위이므로, AI가 몰래 결정을 고정할 수 없습니다. 파생 산출물은 명시적인 소스 링크를 담고 있으며, 충돌이 전파되는 대신 원천까지 거슬러 추적됩니다.

### 반복적 품질 루프

모든 생성 명령에는 **자동화된, 증거 기반 리뷰** 가 포함됩니다. 결함은 구체적인 증거를 요구하고, 권고 제안은 자동 변경을 트리거하지 않으며, 검증된 결함은 최대 두 라운드까지 수정 및 재리뷰될 수 있습니다. 이 루프가 세세한 부분까지 일일이 챙기지 않아도 품질을 계속 끌어올려 줍니다.

[워크플로우 알아보기](user-guide/workflow.md)

## 라이선스

MIT 라이선스 - 자세한 내용은 [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE)를 참조하세요.
