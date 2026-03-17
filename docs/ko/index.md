# CodexSpec에 오신 것을 환영합니다

[![PyPI version](https://img.shields.io/pypi/v/codexspec:svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec:svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Claude Code를 위한 스펙 주도 개발(SDD) 툴킷**

CodexSpec은 구조화되고 명세 중심의 접근 방식을 사용하여 고품질 소프트웨어를 구축하는 데 도움이 되는 툴킷입니다. 전통적인 개발 방식과 달리 명세를 구현을 직접 안내하는 실행 가능한 산출물로 만듭니다.

## 왜 CodexSpec인가요?

### 인간-AI 협업

CodexSpec은 **효과적인 AI 지원 개발에는 모든 단계에서 적극적인 인간 참여가 필요하다**는信念信念에 기반합니다.

| 문제점 | 해결책 |
|---------|----------|
| 불명확한 요구사항 | 구축 전 명확화를 위한 대화형 Q&A |
| 불완전한 명세 | 점수 매기기가 포함된 전용 리뷰 명령 |
| 잘못 정렬된 기술 계획 | Constitution 기반 검증 |
| 모호한 작업 분해 | TDD 적용 작업 생성 |

### 주요 기능

- **Constitution 기반** - 모든 결정을 안내하는 프로젝트 원칙 수립
- **대화형 명확화** - Q&A 기반 요구사항 정제
- **리뷰 명령** - 각 단계에서 산출물 검증
- **TDD 준비** - 작업에 내장된 테스트 우선 방법론
- **i18n 지원** - LLM 번역을 통한 13개 이상 언어 지원

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

```
Idea -> Clarify -> Review -> Plan -> Review -> Tasks -> Review -> Implement
            ^              ^              ^
         Human checks    Human checks    Human checks
```

모든 산출물에는 진행하기 전에 AI 출력을 검증하는 해당 리뷰 명령이 있습니다.

[워크플로우 알아보기](user-guide/workflow.md)

## 라이선스

MIT 라이선스 - 자세한 내용은 [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE)를 참조하세요.
