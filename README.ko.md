<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="codexspec-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="codexspec-logo-light.svg">
    <img alt="CodexSpec Logo" src="codexspec-logo-light.svg" width="420">
  </picture>
</div>

<h1 align="center">CodexSpec</h1>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.pt-BR.md">Português</a> | <b>한국어</b> | <a href="README.de.md">Deutsch</a> | <a href="README.fr.md">Français</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/v/codexspec.svg?style=for-the-badge" alt="PyPI version"></a>
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/pyversions/codexspec.svg?style=for-the-badge" alt="Python versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License: MIT"></a>
</p>

<p align="center">
  <strong>Claude Code와 OpenAI Codex를 위한 요구사항 우선 SDD 도구 모음</strong>
</p>

CodexSpec은 확인된 요구사항을 추적 가능한 명세서, 설계, 계획, 태스크, 구현으로 연결합니다.
**무엇을** 만들고 **왜** 만드는지는 사용자가 결정합니다. 에이전트는 확인된 요구사항 안에서
리뷰 점검 단계와 지속적으로 보존되는 프로젝트 지식을 활용해 **어떻게** 구현할지를 구체화합니다.

Claude Code의 슬래시 명령어, Codex 스킬 또는 두 가지를 함께 사용할 수 있습니다.
일반 기능 개발에는 기본적으로 별도의 Git worktree를 사용합니다. 선택 사항인 공유 블루프린트를 이용하면
에이전트가 확인된 요구사항의 대기열을 자율적으로 개발할 수 있습니다.

[📖 문서](https://zts0hg.github.io/codexspec/) | [中文文档](https://zts0hg.github.io/codexspec/zh/) | [日本語ドキュメント](https://zts0hg.github.io/codexspec/ja/) | [한국어 문서](https://zts0hg.github.io/codexspec/ko/) | [Documentación](https://zts0hg.github.io/codexspec/es/) | [Documentation](https://zts0hg.github.io/codexspec/fr/) | [Dokumentation](https://zts0hg.github.io/codexspec/de/) | [Documentação](https://zts0hg.github.io/codexspec/pt-BR/)

## 목차

- [CodexSpec을 선택하는 이유](#codexspec을-선택하는-이유)
- [30초 빠른 시작](#30초-빠른-시작)
- [설치](#설치)
- [핵심 워크플로우](#핵심-워크플로우)
- [공유 블루프린트와 자율 개발](#공유-블루프린트와-자율-개발)
- [worktree 개발](#worktree-개발)
- [기존 코드 작업](#기존-코드-작업)
- [리뷰와 디버깅](#리뷰와-디버깅)
- [프로젝트 지식](#프로젝트-지식)
- [Git 워크플로우](#git-워크플로우)
- [사용 가능한 명령어](#사용-가능한-명령어)
- [설정과 국제화](#설정과-국제화)
- [프로젝트 구조](#프로젝트-구조)
- [확장 기능 작성 자료](#확장-기능-작성-자료)
- [개발](#개발)
- [기여](#기여)
- [라이선스](#라이선스)

## CodexSpec을 선택하는 이유

| 필요 사항 | CodexSpec이 제공하는 기능 |
|------|-------------------------|
| 명확한 제품 의도 | 명세서 작성 전에 명시적으로 확인하고 `requirements.md`에 지속적으로 기록 |
| 추적 가능한 개발 | 요구사항 → 명세 → 설계 → 계획 → 태스크 전 과정의 출처 링크 |
| 리뷰 가능한 결정 | 네 가지 산출물 리뷰 명령어, 산출물 간 분석, 별도의 코드 결함 게이트 |
| 세션과 팀 간 연속성 | 기능 기록, 프로젝트 원칙, 재사용 가능한 지식, 관련 과거 결정 |
| 여러 기능의 동시 진행 | 일반 기능마다 하나의 Git worktree를 사용하고 같은 작업 공간을 안정적으로 재사용 |
| 더 많은 자동화 | 선택적인 단계 자동 진행과 확인된 블루프린트 요구사항의 자율 개발 |
| 팀의 언어 설정 | 대화, 문서, 커밋 언어를 독립적으로 설정 |

### 요구사항 우선 SDD란?

요구사항 우선 명세 주도 개발은 **확인된 요구사항을 기능에 대한 최우선 판단 기준**으로 삼습니다.
에이전트는 구현 산출물을 도출하기 전에 목표, 제약, 결정, 제외 사항, 미해결 질문, 확인 근거를 기록합니다.

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

제품 의도는 사람과의 협업을 통해 수립하고 변경합니다. 자동 리뷰는 도출된 산출물이 그 의도에 부합하는지 확인합니다.
자동화를 켜면 통과한 단계에서 다음 단계로 진행하지만, 에이전트가 확인된 요구사항을 알리지 않고 대체할 수는 없습니다.

## 30초 빠른 시작

CodexSpec을 설치하고 사용할 어시스턴트에 맞게 초기화합니다.

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

초기화한 프로젝트에서 설치된 어시스턴트를 시작하세요. 같은 워크플로우에 다음 두 가지 호출 형식을 사용할 수 있습니다.

| 어시스턴트 | 요구사항 탐색 시작 |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

필요하면 `constitution`으로 프로젝트 원칙을 조정하세요. 최종 요구사항 요약을 확인한 다음,
반환된 기능 디렉터리와 작업 공간에서 계속 진행하세요. 나머지 명령어는 [핵심 워크플로우](#핵심-워크플로우)를 참고하세요.

Codex 데스크톱 앱을 사용하시나요? [Codex에 프로젝트 설치와 초기화를 요청할 수 있습니다](#codex-데스크톱-앱으로-설치).

## 설치

### Codex 데스크톱 앱으로 설치

데스크톱 앱에서 Codex에 CodexSpec 설치와 프로젝트 설정을 직접 요청할 수 있습니다.

1. Codex 데스크톱 앱에 로컬 프로젝트를 추가하고 작업할 폴더를 선택합니다.
2. 해당 프로젝트에서 채팅을 시작하고 아래 프롬프트를 붙여 넣습니다.
3. 앱에서 의존성 다운로드 또는 설치 권한을 요청하면 해당 작업을 승인해 계속 진행합니다.

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

중국어 답변과 문서를 원하면 `--lang en`을 `--lang zh-CN`으로 바꾸고, Codex에 결과를 중국어로 설명해 달라고 요청하세요.

Codex는 아래 수동 설정과 동일한 CLI와 프로젝트 스킬을 설치합니다.
`$codexspec:specify I want to build a todo application` 같은 프롬프트로 사용을 시작할 수 있습니다.
로컬 스킬 검색과 갱신 동작은 [OpenAI 스킬 가이드](https://learn.chatgpt.com/docs/build-skills)를 참고하세요.

### 사전 요구사항

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)(권장) 또는 pip
- 사용할 어시스턴트: Claude Code 또는 Codex
- worktree 개발과 Git 워크플로우를 위한 Git

### CLI 설치

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

새 프로젝트는 `codexspec init my-project --ai claude`로, 현재 디렉터리는
`codexspec init . --ai codex`로 초기화합니다. 두 연동을 모두 사용하려면 `--ai both`를 지정하세요.
어시스턴트 선택의 기본값은 `claude`입니다. Codex 또는 두 가지 모두를 사용하려면 값을 명시적으로 선택하세요.

<details>
<summary>다른 설치 방법</summary>

#### 일회성 초기화

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

일회성 초기화는 프로젝트 명령어와 독립 실행형 커밋 런타임을 설치합니다.
worktree 작업 위치 선택, blueprint/auto-dev, 수동 프로파일 리뷰는 여전히 CodexSpec CLI를 호출하므로,
해당 워크플로우에서 CLI를 사용할 수 있도록 준비하세요.

#### 개발 버전

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Windows 설치</summary>

PowerShell을 사용합니다.

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

PATH와 설치 문제 해결은 [Windows 문제 해결 가이드](docs/en/WINDOWS-TROUBLESHOOTING.md)를 참고하세요.

</details>

### 업그레이드와 프로젝트 갱신

CLI 업데이트와 프로젝트에 설치된 명령어 갱신은 별도의 단계입니다.

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

한 가지 연동만 필요하면 `--ai claude` 또는 `--ai codex`를 사용하세요.
`--force`는 배포 명령어와 스크립트를 다시 생성하고 리뷰 리소스를 갱신합니다.
또한 마이그레이션, 명령어 업데이트, 프로젝트 헌법 준수 확인을 자동 승인합니다.
기존 요구사항과 프로젝트 원칙은 유지하며, 기존 컨텍스트 파일의 본문을 보존한 채 관리 대상 지침을 업데이트합니다.
명시적으로 설정하지 않은 설정 키도 유지합니다.

계획 작성 명령어는 `design-to-plan`입니다. 설치 업데이트 시 기존 `spec-to-plan` 항목은 별칭 없이 제거됩니다.

### 플러그인 마켓플레이스 설치

Claude Code에서는 마켓플레이스에서 플러그인을 설치합니다.

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

플러그인은 명령어와 함께, 스테이징된 커밋 분석과 과거 요구사항 참조에 대한 세션 시작 지침을 제공합니다.
재개한 세션에도 적용됩니다. 플러그인 설치는 프로젝트를 초기화하지 않습니다.
`/codexspec:config`로 언어, 워크플로우, 리뷰 설정을 만들거나 수정하세요.
전체 프로젝트 뼈대가 필요하면 CLI 초기화를 사용하세요.

직접 커밋 미리보기와 승인된 현재 위치의 커밋은 Python 3.11+와 Git이 있으면 상시 설치된 CodexSpec CLI 없이도
번들 런타임으로 실행할 수 있습니다. worktree 작업 위치 선택, blueprint/auto-dev, 수동 프로파일 리뷰에는 여전히 CLI가 필요합니다.
플러그인 시작 훅에는 PATH에 등록된 Git과 명령어 훅의 `args`(exec 형식)를 지원하는 Claude Code 버전이 필요합니다.
이 지침은 에이전트용이며 수동 Git 명령어를 가로채지 않습니다.

자세한 설정은 [설치](docs/en/getting-started/installation.md)를 참고하세요.

## 핵심 워크플로우

표준 기능 워크플로우는 출처가 연결된 흐름을 유지합니다.

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

아래 예시는 Claude의 `/codexspec:` 접두사를 사용합니다.
Codex에서는 같은 명령어 이름과 인수에 `$codexspec:`을 사용하세요.

| 단계 | 명령어 | 목적과 출력 |
|------|---------|--------------------|
| 프로젝트 원칙 | `/codexspec:constitution` | `constitution.md`를 작성·업데이트하고 영향을 받는 산출물 검증 |
| 요구사항 | `/codexspec:specify <idea>` | 의도를 논의하고 최종 요약을 확인한 뒤 `requirements.md`에 지속적으로 저장 |
| 명세서 | `/codexspec:generate-spec <feature-dir>` | 확인된 요구사항을 출처 참조가 포함된 `spec.md`로 정리 |
| 시스템 설계 | `/codexspec:spec-to-design <feature-dir>` | 컴포넌트, 인터페이스, 주요 설계 결정을 담은 `design.md` 작성 |
| 구현 계획 | `/codexspec:design-to-plan <feature-dir>` | 단계, 순서, 검증을 담은 `plan.md` 작성 |
| 태스크 | `/codexspec:plan-to-tasks <feature-dir>` | 추적·검증 가능한 `tasks.md`를 작성하고 산출물 간 분석 실행 |
| 구현 | `/codexspec:implement-tasks <feature-dir>` | 태스크를 수행하고 결과를 검증하며 독립적으로 검증된 리뷰 지적 수정 |

`<feature-dir>`를 탐색 과정에서 반환된 기능 디렉터리로 바꾸세요.
해당 worktree에서 계속 작업하거나 명시적인 경로를 전달하면, 명령어와 세션이 바뀌어도 같은 기능의 식별 정보를 유지합니다.

### specify, clarify, analyze

- **specify**는 요구사항 탐색을 시작하거나 다시 진행합니다. 명시적으로 확인한 경우에만 요구사항 요약이 구속력을 갖습니다.
- **clarify**는 기존 요구사항과 명세의 모호함을 해결합니다. 한 번 실행할 때 네 가지 범주에 걸쳐 최대 다섯 가지 질문을 합니다.
  먼저 `requirements.md`를 업데이트한 뒤 `spec.md`를 동기화합니다.
- **analyze**는 요구사항 → 명세 → 설계 → 계획 → 태스크의 전체 흐름을 확인합니다.
  상위 산출물의 판단 기준에서 수정 내용이 하나로 결정되면 하위 산출물에 그 수정을 자동 적용하지만,
  `requirements.md`는 절대 편집하지 않습니다. 해결되지 않은 지적은 보고합니다.
  태스크 리뷰 통과 후 자동 실행되며, 정보를 제공하는 절차로서 구현 게이트가 되지는 않습니다.

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### Quick으로 작은 변경 수행

국소적인 수정처럼 작고 범위가 명확한 변경에는 `quick`을 사용하세요.

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick은 간결한 요구사항 요약을 확인하고 저장한 다음, 생성 명령어의 리뷰와 함께 명세 작성, 계획, 태스크, 구현을 진행합니다.
범위가 넓거나 제품·설계 선택이 해결되지 않은 변경은 표준 워크플로우를 사용해야 합니다.
Quick은 새로운 결정이 필요하면 일시 중지합니다.

### 워크플로우 자동화

`workflow.auto_next`의 기본값은 **false**입니다. 현재 작업 공간의 설정이 `true`이면 최종 요구사항 확인 후 명세 작성으로 진행합니다.
각 생성 단계는 `PASS` 또는 `PASS_WITH_WARNINGS` 이후 다음으로 넘어가며, `NEEDS_REVISION`이나 `BLOCKED`이면 흐름이 중단됩니다.
`implement-tasks`가 마지막 단계입니다.

자동 산출물 수정은 상위 근거에서 수정 내용이 도출되는 검증된 결함으로 제한되며, 수정과 리뷰는 최대 두 라운드까지 수행합니다.
권고 사항은 별도로 유지합니다. 구현 리뷰·수정 반복에는 아래에서 설명하는 자체 완료 규칙이 있습니다.

자세한 계약은 [워크플로우 가이드](docs/en/user-guide/workflow.md)를 참고하세요.

## 공유 블루프린트와 자율 개발

개발 전에 여러 확인된 요구사항을 준비하려면 `blueprint`를, 해당 대기열을 개발하려면 `auto-dev`를 사용하세요.

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

블루프린트 탐색은 요구사항이 대기열에 들어가기 전에 사용자가 결정할 방향, 선택, 제약을 해결합니다.
공유 `.codexspec/blueprint.md`는 `pending`, `in_progress`, `completed` 상태를 사용합니다.
대기 중인 요구사항은 추가, 교체, 삭제, 순서 변경이 가능합니다. 진행 중이거나 완료된 항목은 블루프린트 유지보수에서 읽기 전용입니다.

Auto-dev는 문서 순서를 따르며, 다른 기능을 시작하기 전에 진행 중인 기능을 재개합니다.
완료할 때마다 대기열을 다시 읽으므로 새로 추가된 대기 작업도 현재 실행에 합류할 수 있습니다.
확인된 요구사항 안에서 SDD 단계, 구현, 검증, 리뷰, 수정을 수행합니다.
`auto-dev` 호출은 `workflow.auto_next`와 독립적으로 자동화를 활성화하며 그 설정을 변경하지 않습니다.

두 명령어는 `worktree-for-codexspec-auto-dev`를 공유하며, 해당 브랜치는 `codexspec/auto-dev`입니다.
공유 소유권과 쓰기 보호 아래 동시에 사용할 수 있지만, 해당 작업 공간에서 요구사항은 순차적으로 개발합니다.
확인된 요구사항으로 해결할 수 없는 제품 결정이 있으면, 일반 자율 실행 도중에 질문하는 대신 근거를 제시하고 실행을 멈춥니다.

현재 공유 블루프린트를 변경하지 않고 확인합니다.

```bash
codexspec show-blueprint
```

## worktree 개발

Git worktree는 같은 리포지토리의 또 다른 작업 디렉터리이며, 자체적으로 체크아웃한 브랜치를 가집니다.
CodexSpec은 일반 기능마다 기본적으로 하나를 사용하고 첫 요구사항 쓰기 전에 생성해,
해당 기능의 문서, 구현, 테스트, 수정을 함께 보관합니다.

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

기능 작업을 이어가면 해당 작업 공간을 재사용합니다. 독립적인 설정, 프로젝트 헌법, 프로파일 변경은 유지보수 worktree를 사용하며,
진행 중인 기능에서 수행한 변경은 그 작업 공간에 남습니다. 설정은 **체크아웃별**로 적용됩니다.
작업 대상으로 선택된 worktree에서 바꾼 설정은 먼저 그곳에 적용되고, Git 통합을 통해 다른 체크아웃에 전달됩니다.
CLI 명령어와 검사는 반환된 작업 공간에서 실행하세요.

새 기능의 기준은 커밋된 로컬 main 브랜치와 가져온 원격 main 브랜치의 이력을 Git 조상 관계로 비교해 결정합니다.
갈라진 이력은 새 worktree 안에서 병합되며 검증이 필요합니다. 가져오기에 실패하면 경고하고 로컬에서 사용 가능한 참조를 허용합니다.
생성 실패 시 main 체크아웃에 쓰는 방식으로 되돌아가지 않습니다.

`workflow.worktrees`의 기본값은 **true**이며, YAML 리터럴 `false`만 일반 기능과 유지보수의 격리를 끕니다.
Blueprint/auto-dev는 어느 경우에도 고정된 공유 worktree를 유지합니다. 초기화와 설치 업데이트는 명시적으로 선택한 체크아웃에서 수행합니다.
완료된 worktree는 보존하며, 완료 시 자동으로 병합하거나 삭제하지 않습니다.

[worktree 개발](docs/en/user-guide/workflow.md#worktree-development)과 [설정](docs/en/reference/configuration.md#workflowworktrees)을 참고하세요.

## 기존 코드 작업

목적에 따라 두 가지 진입점을 사용합니다.

| 명령어 | 용도 | 출력과 범위 |
|---------|-----------|-----------------|
| `onboard [path]` | 기존 코드베이스에서 재사용 가능한 프로젝트 지식의 기반 마련 | 후보 관례와 제한된 근거가 뒷받침하는 제약을 프로파일에 기록하며 코드는 읽기 전용 |
| `reverse-spec [path]` | 기존 아키텍처를 이해하거나 코드를 확인된 의도와 비교 | 산출물 초안 또는 차이 보고서이며 코드는 읽기 전용 |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard는 관찰 가능한 코드에서 관례를 추론하며 명시적인 금지 사항에서만 제약을 제안합니다.
관례 후보는 로컬에 즉시 적용됩니다. 제약 후보는 세션 안에서 저장·편집·제외 결정을 내려야 합니다.
기존 지식을 보존하고, 처음 수행하는 스캔에서 과거 결정의 이유나 경험상의 함정을 지어내지 않습니다.

Reverse-spec에는 세 가지 모드가 있습니다.

- **개요**: 경로가 없거나 리포지토리 루트인 경우, 조사할 모듈을 선택하기 위한 간결한 아키텍처 `design.md`와 `slices.md`를 만듭니다.
- **생성**: 확인된 기준이 없는 모듈 경로인 경우, `spec.md`, `design.md`, 미확정·추론된 요구사항의 초안을 만듭니다.
- **대조**: 확인된 기준이 있는 모듈인 경우 `reconcile.md`를 만듭니다.
  확인된 명세·설계와 비교해 문서화되지 않은 동작, 구현되지 않은 명세, 의미 불일치를 보고하며 의도는 요구사항을 기준으로 판단합니다.

추론한 초안은 사람의 확인을 받아야 기준이 될 수 있습니다.
대조 작업은 코드 수정, 문서 업데이트, 의도 결정과 같은 제안 방향을 보고하며 자동으로 적용하지 않습니다.

## 리뷰와 디버깅

네 가지 산출물 리뷰어 `review-spec`, `review-design`, `review-plan`, `review-tasks`는 충실도, 범위 충족, 실현 가능성, 내부 품질을 확인합니다.
생성 후 자동으로 실행되며 수동 호출도 가능합니다. 보고서는 검증된 결함을 통과 여부에 영향을 주지 않는 위험 권고 및 설계 개선 기회와 구분하고,
적합도 점수도 제공합니다.

`review-code`는 변경 범위에 대한 별도의 결함 게이트와 명시적인 코드 전체 품질 평가를 제공합니다.

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

기본 리뷰는 커밋된 변경, 스테이징된 변경, 스테이징되지 않은 변경, 추적되지 않으면서 무시 대상이 아닌 변경을 포함한 기능 브랜치 전체 차이를 다룹니다.
커밋된 변경, 미커밋 변경, 단일 커밋의 근거를 명시적으로 선택할 수도 있습니다.
`--feature`는 Git 범위를 좁히지 않고 요구사항 맥락을 연결합니다.
`--audit`는 지정된 경로를 평가하고 완료 판정 대신 권고용 평가표를 작성합니다.

리뷰는 `.codexspec/review-code/`에서 공유 기준을 불러와 관련 동작 관점과 언어·프레임워크 검사를 선택합니다.
지적에는 구체적인 근거, 실제로 도달 가능한 발생 조건, 선택된 변경에 대한 귀속, 영향이 필요합니다.
리뷰어는 파일을 편집하지 않고 결함과 근거 있는 유지보수 제안을 보고하며, 수정을 수행하는 호출자가 이를 독립적으로 검증합니다.

구현 시 코드 태스크에는 테스트 우선 방식을 사용하고, 문서·설정에는 적절한 검사를 포함한 직접 구현을 사용합니다.
수정 후 점진적인 재리뷰에서는 영향을 받지 않은 범위의 확인 결과를 재사용할 수 있습니다.
최종 승인을 위해서는 새로 수행하는 기능 전체 리뷰의 `PASS`, 범위 확인과 검증 완료, 채택된 P0–P3 결함 0개가 필요합니다.
근거 있는 유지보수 제안은 별도로 보고합니다.

`workflow.auto_maintenance`의 기본값은 **true**이며, 수정을 수행하는 호출자가 검증된 호환 가능한 유지보수 개선도 적용할지 제어합니다.
끄더라도 제안은 계속 보고하며 결함이나 필수 검사를 면제하지 않습니다.
단계 진행과는 독립적이고 `implement-tasks`의 인수가 아닙니다.

근본 원인부터 조사하는 디버깅에는 다음을 사용합니다.

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug는 조사 → 패턴 분석 → 단일 가설 검증 → 실패하는 테스트를 먼저 작성한 뒤 수정 순으로 진행합니다.
구현 과정에서는 수정이 막히거나, 단순하지 않은 정확성 결함을 추적해야 하거나,
같은 근본 원인 유형이 여러 리뷰 라운드에서 재발할 때 이 절차로 전환합니다. 수정이 세 번 실패하면 아키텍처를 재평가합니다.

요구사항의 명확성, 완전성, 일관성을 평가하려면 `checklist`를 사용하세요.

```text
/codexspec:checklist Check the authentication requirements for completeness
```

리뷰 선택자, 인수, 자세한 절차는 [명령어 참조](docs/en/user-guide/commands.md)를 참고하세요.

## 프로젝트 지식

프로젝트 프로파일은 `.codexspec/profile/`에 재사용 가능한 지식을 저장합니다.

| 범주 | 내용 |
|----------|----------|
| `constraints/` | 명시적인 금지 사항과 엄격한 경계로, 가장 먼저 읽음 |
| `conventions/` | 패턴, 명명, 여러 기능에 걸친 지침 |
| `pitfalls/` | 경험한 함정, 원인, 우회 방법, 교훈 |
| `decisions/` | 재사용 가능한 아키텍처 및 여러 기능에 걸친 결정 |
| `strategies/` | 작업 접근 방식의 변경이 필요한 신호 |
| `runbooks/` | 순서가 정해진 절차와 실패 복구 |

`distill`은 작업에서 재사용 가능한 지식을 추출하며, 기능별 의도는 해당 기능의 요구사항·설계·계획에 남깁니다.
Init은 본격적인 작업 전에 모든 제약과 관련 지식을 읽도록 CLAUDE.md 또는 AGENTS.md, 혹은 두 파일 모두에 지침을 설치합니다.
나중에 추가한 지식도 재초기화 없이 적용될 수 있습니다. 후보 기록은 신중하게 사용하며, 검토·승인된 기록에는 결과 검증과 사람의 지지가 필요합니다.

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

수동 `distill review` 또는 새로 추출할 자료 없이 직접 호출한 `distill`은 로컬 오프라인 브라우저 작업 공간을 엽니다.
기록을 수정, 검토·승인, 폐기, 보류, 통합하고 최종 Markdown을 미리 본 다음 **모두 적용**을 선택할 수 있습니다.
결정은 적용할 때까지 복구 가능한 초안에 남으며, 충돌 검사로 부분 적용이나 알림 없는 덮어쓰기를 막습니다.
브라우저가 없는 환경에서는 명시적으로 텍스트 대체 방식을 사용할 수 있습니다.

`workflow.auto_distill`의 기본값은 **true**이며, 세 가지 마무리 훅을 제어합니다.
성공한 `implement-tasks`, `commit-staged`를 통해 실행한 커밋, `pr` 생성입니다. 커밋 미리보기는 지식 추출을 실행하지 않습니다.

설치된 프로젝트 지침은 일반 대화, SDD 밖의 수정, 긴 `implement-tasks` 실행 중에도 재사용 가능한 지식이 생기는 시점에 기록하도록 요구합니다.
이 지침은 마무리 설정과 독립적으로 적용되며, 태스크 종료 시 추출이 마지막 누락 방지 수단이 됩니다.

같은 세션에서 반복 호출되면 새 자료만 처리합니다. 세션이 바뀌면 `distill`은 프로파일을 읽고 이미 다룬 지식을 건너뜁니다.
재사용 가능한 내용이 없으면 쓰지 않고 종료합니다. 자동 추출은 수동 리뷰를 열거나 사람을 기다리거나 호출한 워크플로우를 막지 않습니다.

`evolve`는 프로젝트 밖에서도 유용한 검토·승인된 지식만 선택해 명령어·스킬 초안으로 정리합니다.
푸시하거나 사람이 리뷰할 기여 PR을 열기 전에 명시적인 승인을 받습니다.

자세한 지침은 [프로젝트 지식](docs/en/user-guide/commands.md#codexspecdistill)을 참고하세요.

### 과거 결정 재사용

일반 대화와 SDD 워크플로우 모두에서 본격적인 요구사항, 설계, 구현, 디버깅, 리뷰 판단 전에 `.codexspec/specs/`의 관련 이력도 참조합니다.
에이전트는 사용자에게 질문하기 전에 변경되지 않은 결정, 이후 추가 사항, 명시적인 대체 내용을 재구성합니다.

변경되지 않은 이전 요구사항은 계속 적용됩니다. 사용자의 최신 명시적 결정이 항상 우선하며, 미확정 제안은 확인된 의도로 취급하지 않습니다.
검색 범위는 해당 작업에 한정하고 충분히 준비한 배경 정보를 재사용합니다. 이 지침을 받으려면 기존 프로젝트 설치를 갱신하세요.

## Git 워크플로우

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged**는 정확한 스테이징 영역을 분석해 Conventional Commits 메시지를 생성합니다.
  `-p`는 커밋하지 않고 미리 봅니다. 파일 선택과 스테이징은 호출한 워크플로우가 수행합니다.
  승인된 실행은 보호된 런타임을 사용해 커밋 내용이 분석과 일치하는지 다시 확인합니다.
  에이전트 커밋 지침은 일반 대화, SDD, blueprint, auto-dev 워크플로우에 적용되지만,
  명령어를 사용할 수 있다는 사실만으로 호출하거나 커밋 권한을 부여하지는 않습니다.
- **pr**은 차이에서 구조화된 GitHub PR 또는 GitLab MR 설명을 생성합니다.
  `--spec`은 선택적으로 `spec.md` 파일 경로, 또는 그 파일로 해석되는 기능 디렉터리 이름이나 접두사에서 기능 맥락을 추가합니다.
  기본 출력은 호스팅 플랫폼에서 사용할 텍스트입니다.
- **release-notes**는 Git 이력에서 Keep a Changelog 항목과 릴리스 본문을 도출합니다.
  기본 섹션은 `[Unreleased]`이며 `--version`은 제공된 라벨을 사용합니다.
  스테이징, 커밋, 버전 변경, 태그, 게시, 릴리스 생성을 수행하지 않습니다.
- **tasks-to-issues**는 기존 태스크에서 의존성과 승인 기준을 포함한 GitHub 이슈를 생성합니다.
  인증된 GitHub CLI가 필요하며 이슈 리포지토리가 설정된 원격과 일치하는지 확인합니다.

직접 커밋 미리보기와 승인된 현재 위치의 커밋에는 Python 3.11+와 Git이 필요합니다.
런타임은 CLI 프로젝트에 설치되며 Claude 플러그인에도 포함됩니다. 내용 변경을 포함하는 에이전트 생성 병합도 스테이징 분석을 사용합니다.
이력만 연결하는 병합은 트리와 부모를 검증하면서 Git의 기본 메시지를 유지하며, fast-forward는 커밋을 만들지 않습니다.

## 사용 가능한 명령어

CLI에는 여섯 가지 공개 명령어가 있습니다. 에이전트 연동은 28개 명령어를 배포합니다.
Claude는 `/codexspec:<name>`, Codex는 `$codexspec:<name>`을 사용합니다.
아래 표는 가독성을 위해 Claude 표기를 사용합니다.

### CLI 명령어

| 명령어 | 목적 |
|---------|---------|
| `codexspec init` | Claude, Codex 또는 둘 모두를 위한 프로젝트 초기화·갱신 |
| `codexspec check` | 설치된 도구와 의존성 확인 |
| `codexspec version` | 버전과 시스템 정보 표시 |
| `codexspec config` | 프로젝트 설정 확인·수정 |
| `codexspec list-commands` | 사용 가능한 에이전트 명령어를 범주별로 나열 |
| `codexspec show-blueprint` | 공유 worktree의 블루프린트를 변경하지 않고 출력 |

### 핵심 워크플로우 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:constitution` | 산출물 간 검증을 포함해 프로젝트 원칙 작성·업데이트 |
| `/codexspec:specify` | 기능 요구사항 논의·확인·저장 |
| `/codexspec:blueprint` | 확인된 대기 중 블루프린트 요구사항 준비·유지 |
| `/codexspec:generate-spec` | 확인된 요구사항을 추적 가능한 명세서로 정리하고 자동 리뷰 |
| `/codexspec:spec-to-design` | 아키텍처, 컴포넌트, 인터페이스, 결정을 정의하고 자동 리뷰 |
| `/codexspec:design-to-plan` | 구현 단계, 순서, 검증을 계획하고 자동 리뷰 |
| `/codexspec:plan-to-tasks` | 상위 산출물의 내용을 포괄하는 검증 가능한 태스크를 만들고 자동 리뷰 및 분석 |
| `/codexspec:implement-tasks` | 태스크 수행, 결과 검증, 리뷰와 수정 |
| `/codexspec:auto-dev` | 확인된 블루프린트 요구사항을 문서 순서에 따라 자율 개발 |

### 산출물 리뷰 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:review-spec` | 명세서의 충실도와 내부 품질 확인 |
| `/codexspec:review-design` | 설계의 충실도, 실현 가능성, 계획 준비 상태 확인 |
| `/codexspec:review-plan` | 계획의 충실도, 실현 가능성, 구현 준비 상태 확인 |
| `/codexspec:review-tasks` | 태스크의 충실도, 의존성, 실행 가능성, 검증 확인 |

### 요구사항, 기존 코드, 디버깅

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:clarify` | 요구사항의 모호함을 해결하며 명세서보다 먼저 요구사항 업데이트 |
| `/codexspec:analyze` | 전 과정의 추적 가능성을 확인하고 하위 산출물을 판단 기준에 맞춤 |
| `/codexspec:checklist` | 요구사항 품질 체크리스트 생성 |
| `/codexspec:tasks-to-issues` | 기존 태스크를 실행 가능한 GitHub 이슈로 변환 |
| `/codexspec:debug` | 수정을 적용하기 전에 근본 원인 조사 |
| `/codexspec:reverse-spec` | 기존 아키텍처 조사, 모듈 산출물 초안 작성 또는 기준과의 차이 보고 |

### 프로젝트 지식 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:distill` | 재사용 가능한 지식 추출 또는 로컬 작업 공간에서 후보 리뷰 |
| `/codexspec:evolve` | 검토·승인된 지식을 업스트림 기여 초안으로 정리 |
| `/codexspec:onboard` | 기존 코드에서 관례 후보와 근거 있는 제약의 기반 마련 |

### Git 및 코드 리뷰 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:commit-staged` | 스테이징된 변경에서 메시지를 생성하고 미리 보거나 승인된 커밋 실행 |
| `/codexspec:pr` | 구조화된 PR/MR 설명 생성 |
| `/codexspec:release-notes` | 변경 이력 항목을 유지하고 Git 이력에서 릴리스 본문 생성 |
| `/codexspec:review-code` | 선택한 변경을 결함 게이트로 리뷰하고 경로 품질에는 `--audit` 사용 |

### 유틸리티 명령어

| 명령어 | 목적 |
|---------|---------|
| `/codexspec:config` | 대화형으로 프로젝트 설정 작성·조회·수정·초기화 |
| `/codexspec:quick` | 작은 변경에 대해 간결한 요구사항 우선 SDD 워크플로우 실행 |

## 설정과 국제화

설정은 `.codexspec/config.yml`에 저장합니다. 템플릿은 영어로 유지하며, 에이전트는 설정된 언어로 대화와 산출물을 작성합니다.
표준 언어 코드는 13개로 `en`, `zh-CN`, `zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar`, `hi`입니다.
포르투갈어 CLI 코드는 `pt`이며 현지화된 문서와 번역 카탈로그는 `pt-BR`을 사용합니다.

### 언어 구분

| 구분 | 설정 키 | 초기화 시 | 나중에 설정 | 적용 대상 |
|-----------|------------|-------------------|-----------|----------|
| 출력·기본 | `language.output` | `--lang` | `config --set-lang` | 다른 언어 구분의 대체 기본값 |
| 대화 | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | 대화와 CLI 출력 |
| 문서 | `language.document` | `--document-lang` | `config --set-document-lang` | 요구사항, 명세서, 설계, 계획, 태스크 |
| 커밋 | `language.commit` | `--commit-lang` | `config --set-commit-lang` | 커밋 메시지와 Git 전달용 콘텐츠 |

각 언어 구분은 독립적으로 `language.output`, 그다음 `en`으로 대체됩니다. `language.templates`는 `en`으로 유지합니다.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

첫 TTY 초기화에서는 `--lang` 또는 세 가지 개별 언어 옵션을 모두 지정하지 않으면 기본 언어를 묻습니다.
`--force`는 다른 초기화 확인을 자동 승인하지만 이 언어 선택은 생략하지 않습니다.
비 TTY 초기화의 기본값은 영어입니다. 재초기화는 명시적으로 설정하지 않은 언어 키를 유지합니다.

### 워크플로우와 리뷰 설정

| 설정 | 기본값 | 효과 | CLI 제어 |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | 통과한 일반 SDD 단계 진행 | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | 마무리 성공 후 비대화형 지식 추출 | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | 자동 수정 중 검증된 점진적 유지보수 적용 | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | 일반 기능과 독립적인 유지보수 격리 | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | 프로젝트의 운영 맥락 밖에서 발생하는 지적의 결정 주체 | `config --decided-by reviewer\|ask` |

불리언 CLI 스위치는 대소문자를 구분하지 않고 앞뒤 공백도 허용하며 `on/true/1/yes`와 `off/false/0/no`를 받습니다.
값 없는 불리언 스위치는 대상 체크아웃의 현재 값을 전환합니다. YAML에는 불리언 값으로 저장합니다.

`review.decided_by: reviewer`에서는 리뷰어가 결함 채택 여부를 결정합니다.
`ask`에서는 맥락 밖의 발생 조건이 보류 중인 시나리오 결정이 됩니다. 사용자는 수정할지 해당 시나리오를 제외할지 한 번 결정하며,
확인된 결정은 이후 라운드를 위해 보존됩니다. 보류 중인 결정은 완료를 막습니다.
단일 `review-code` 실행은 `--decided-by`로 설정된 모드를 재정의할 수 있습니다.

설정 쓰기는 worktree 작업 위치 선택을 따릅니다. main 체크아웃에서 독립적으로 수행하는 변경은 유지보수 worktree에 기록되며
main의 유효 설정을 즉시 바꾸지 않습니다. 기능 worktree의 변경은 그곳에 적용됩니다.

<details>
<summary>CLI 초기화 옵션</summary>

| 옵션 | 의미 |
|--------|---------|
| `PROJECT_NAME` | 새 디렉터리 이름이며 현재 디렉터리에는 `.` 사용 |
| `--here`, `-h` | 현재 디렉터리 초기화 |
| `--ai`, `-a` | `claude`, `codex`, `both` 중 선택하며 기본값은 `claude` |
| `--lang`, `-l` | 기본 출력 언어 설정 |
| `--interaction-lang` | 대화 언어 설정 |
| `--document-lang` | 문서 언어 설정 |
| `--commit-lang` | 커밋 메시지 언어 설정 |
| `--force`, `-f` | 설치된 산출물을 다시 생성하고 마이그레이션·업데이트·준수 확인을 자동 승인하며 프로젝트에서 작성한 컨텍스트와 무관한 설정 보존 |
| `--no-git` | Git 리포지토리 초기화 생략 |
| `--debug`, `-d` | 상세한 디버그 출력 표시 |

</details>

<details>
<summary>CLI 설정 옵션</summary>

| 옵션 | 의미 |
|--------|---------|
| `--set-lang`, `-l` | 기본 출력 언어 설정 |
| `--set-interaction-lang` | 대화 언어 설정 |
| `--set-document-lang` | 문서 언어 설정 |
| `--set-commit-lang`, `-c` | 커밋 메시지 언어 설정 |
| `--list-langs` | 지원하는 언어 코드 목록 표시 |
| `--auto-next` | 자동 단계 진행 전환·설정 |
| `--auto-distill` | 자동 지식 추출 전환·설정 |
| `--auto-maintenance` | 자동 점진적 유지보수 전환·설정 |
| `--worktrees` | 체크아웃별 worktree 격리 전환·설정 |
| `--decided-by` | 리뷰 결정 모드를 `reviewer` 또는 `ask`로 설정 |

</details>

<details>
<summary>설정 예시</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

언어와 설정의 자세한 동작은 [설정](docs/en/reference/configuration.md)과 [국제화](docs/en/user-guide/i18n.md)를 참고하세요.

## 프로젝트 구조

초기화는 공통 리소스와 선택한 어시스턴트 연동을 설치합니다.

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

공유 블루프린트는 각 일반 체크아웃의 별도 편집 가능 복사본이 아니라 전용 auto-dev worktree에 있습니다.
수동 지식 리뷰 초안은 Git에서 제외합니다.

## 확장 기능 작성 자료

리포지토리에는 확장 기능 매니페스트 템플릿, 예제 명령어, [확장 기능 개발 가이드](extensions/EXTENSION-DEVELOPMENT-GUIDE.md)가 있습니다.
이 자료들은 작성용 자료입니다. 현재 CLI에는 확장 기능 설치·목록·제거 명령어가 없으며,
`extension.yml`의 명령어나 훅을 자동으로 불러오지 않습니다.
공유 리뷰 리소스는 `.codexspec/review-code/` 아래 프로젝트별 추가 자료를 지원합니다.
초기화는 교체를 요청하지 않는 한 기존 리소스 수정과 추가 파일을 보존합니다.

## 개발

```bash
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Development tools are an optional dependency extra
uv sync --extra dev
# For documentation builds too: uv sync --extra dev --extra docs

uv run codexspec --help
uv run pytest
uv run ruff check src/
uv build
```

템플릿, 패키징, 초기화를 변경하기 전에 [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md),
[리포지토리 구조](docs/internal/repository-layout.md)를 읽으세요.
배포 명령어와 스킬의 복사본은 생성된 설치 산출물입니다. 기준이 되는 원본을 편집하고 다시 생성하세요.

## 기여

로컬 설정과 기여 지침은 [기여 가이드](docs/en/development/contributing.md)를 참고하세요.
기여 시 확인된 요구사항, 출처 추적 가능성, 사용자용·유지보수자용 패키징 경계를 유지해야 합니다.

## 라이선스

MIT — [LICENSE](LICENSE)를 참고하세요.

## 감사의 말

[GitHub spec-kit](https://github.com/github/spec-kit)에서 영감을 받았습니다.
Claude Code 및 OpenAI Codex와 연동합니다.
