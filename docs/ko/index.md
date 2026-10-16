# CodexSpec

![CodexSpec](assets/images/codexspec-logo-light.svg#only-light){ width="420" }

![CodexSpec](assets/images/codexspec-logo-dark.svg#only-dark){ width="420" }

**Claude Code와 OpenAI Codex를 위한 요구사항 우선 SDD 도구 모음**

CodexSpec은 확정된 요구사항을 바탕으로 명세서, 설계, 계획, 태스크, 구현을 만들고, 각 단계의 근거를 추적할 수 있게 합니다.
**무엇을** 만들고 **왜** 만드는지는 사용자가 결정합니다. 에이전트는 그 요구사항의 범위 안에서
단계별 리뷰와 프로젝트에 저장된 지식을 활용해 **어떻게** 구현할지 구체화합니다.

Claude Code의 슬래시 명령어, Codex 스킬 또는 두 가지를 함께 사용할 수 있습니다.
일반적인 기능 개발에는 기본적으로 별도의 Git worktree를 사용합니다.
공유 블루프린트를 사용하면 확정된 요구사항의 대기열을 에이전트가 자율적으로 개발하도록 할 수도 있습니다.

<a id="why-choose-codexspec"></a>

## CodexSpec을 선택하는 이유

| 필요한 것 | CodexSpec이 제공하는 기능 |
|------|-------------------------|
| 제품의 목표와 의도를 명확히 정하기 | 명세서 작성 전에 요구사항을 명시적으로 확인하고 `requirements.md`에 저장 |
| 개발 과정의 근거 추적하기 | 요구사항 → 명세 → 설계 → 계획 → 태스크를 연결하는 출처 링크 |
| 결정의 타당성 검토하기 | 네 가지 산출물 리뷰 명령어, 산출물 간 분석, 별도의 코드 결함 게이트 |
| 세션이나 담당자가 바뀌어도 작업 이어가기 | 기능 기록, 프로젝트 원칙, 재사용할 수 있는 지식, 관련된 과거 결정 |
| 여러 기능을 동시에 개발하기 | 일반 기능마다 Git worktree를 하나씩 만들고 같은 작업 공간을 계속 재사용 |
| 더 많은 작업 자동화하기 | 선택적으로 켤 수 있는 단계 자동 진행과 확정된 블루프린트 요구사항의 자율 개발 |
| 팀에 맞는 언어로 작업하기 | 대화, 문서, 커밋 언어를 각각 설정 |

<a id="what-is-requirements-first-sdd"></a>

### 요구사항 우선 SDD란?

요구사항 우선 명세 주도 개발은 **확정된 요구사항을 해당 기능의 최우선 판단 기준**으로 삼습니다.
에이전트는 구현을 위한 산출물을 만들기 전에 목표, 제약, 결정, 제외 사항, 미해결 질문, 확인 근거를 기록합니다.

```text
Idea → Confirmed Requirements →     Spec    →     Design    →     Plan    →    Tasks     →     Code
                 ↓                   ↓              ↓              ↓             ↓              ↓
         User confirmation      review-spec   review-design   review-plan   review-tasks   review-code
```

요구사항은 사용자가 확정합니다. 명세부터 코드까지, 이를 바탕으로 만들어지는 각 산출물에는 해당하는 리뷰가 있습니다.

제품의 목표와 의도는 사람과의 협업을 통해 정하고 변경합니다.
자동 리뷰는 만들어진 산출물이 그 의도에 부합하는지 확인합니다.
자동화를 켜면 통과한 단계에서 다음 단계로 진행합니다. 에이전트가 확정된 요구사항을 알리지 않고 바꿀 수는 없습니다.

[![CodexSpec: 요구사항 우선 개발 절차, 단계별 검토와 경험을 다음 개발에 반영하는 순환](../../assets/workflow/workflow-ko-light.png#only-light)](../../assets/workflow/workflow-ko-light.png#only-light)

[![CodexSpec: 요구사항 우선 개발 절차, 단계별 검토와 경험을 다음 개발에 반영하는 순환](../../assets/workflow/workflow-ko-dark.png#only-dark)](../../assets/workflow/workflow-ko-dark.png#only-dark)

전체 크기로 그림 열기: [☀️](../../assets/workflow/workflow-ko-light.png) · [🌙](../../assets/workflow/workflow-ko-dark.png)

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
이후에 사용할 명령어는 [핵심 워크플로우](user-guide/workflow.md#core-workflow)를 참고하세요.

Codex 데스크톱 앱에서는 [Codex에 설치와 프로젝트 초기화를 요청할 수 있습니다](getting-started/installation.md#install-with-the-codex-desktop-app).
