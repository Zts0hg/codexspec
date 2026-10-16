<a id="installation"></a>

# 설치

<a id="install-with-the-codex-desktop-app"></a>

## Codex 데스크톱 앱에서 설치

데스크톱 앱에서 Codex에 요청하면 CodexSpec 설치와 프로젝트 설정을 직접 진행할 수 있습니다.

1. Codex 데스크톱 앱에 로컬 프로젝트를 추가하고 작업할 폴더를 선택합니다.
2. 해당 프로젝트에서 채팅을 시작하고 아래 프롬프트를 붙여 넣습니다.
3. 앱이 의존성 다운로드나 설치 권한을 요청하면 해당 작업을 승인해 계속 진행합니다.

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

중국어 답변과 문서를 원한다면 `--lang en`을 `--lang zh-CN`으로 바꾸고, 결과도 중국어로 설명해 달라고 Codex에 요청하세요.

이 방법으로 설치되는 CLI와 프로젝트 스킬은 아래 수동 설정과 동일합니다.
`$codexspec:specify I want to build a todo application` 같은 프롬프트로 사용을 시작할 수 있습니다.
로컬 스킬을 찾고 갱신하는 방식은 [OpenAI 스킬 가이드](https://learn.chatgpt.com/docs/build-skills)를 참고하세요.

<a id="prerequisites"></a>

## 사전 요구사항

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)(권장) 또는 pip
- 사용할 어시스턴트: Claude Code 또는 Codex
- worktree 개발 및 Git 워크플로우를 사용할 경우 Git

<a id="cli-installation"></a>

## CLI 설치

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
어시스턴트의 기본값은 `claude`입니다. Codex 또는 두 가지를 모두 사용하려면 값을 명시적으로 지정해야 합니다.

<details>
<summary>다른 설치 방법</summary>

<a id="one-time-initialization"></a>

### 일회성 초기화

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

일회성 초기화는 프로젝트 명령어와 독립 실행형 커밋 런타임을 설치합니다.
worktree 작업 위치 선택, blueprint/auto-dev, 수동 프로파일 리뷰는 여전히 CodexSpec CLI를 호출합니다.
이 워크플로우를 사용하려면 CLI도 사용할 수 있도록 준비하세요.

<a id="development-versions"></a>

### 개발 버전

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Windows 설치</summary>

PowerShell에서 실행합니다.

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

PATH와 설치 문제를 해결하는 방법은 [Windows 문제 해결 가이드](../WINDOWS-TROUBLESHOOTING.md)를 참고하세요.

</details>

<a id="upgrade-and-refresh-a-project"></a>

## 업그레이드와 프로젝트 갱신

CLI 업데이트와 프로젝트에 설치된 명령어 갱신은 각각 따로 진행해야 합니다.

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

한 가지 연동만 필요하면 `--ai claude` 또는 `--ai codex`를 지정하세요.
`--force`는 배포 명령어와 스크립트를 다시 생성하고 리뷰 리소스를 갱신합니다.
마이그레이션, 명령어 업데이트, 프로젝트 헌법 준수에 관한 확인도 자동으로 승인합니다.
기존 요구사항과 프로젝트 원칙은 유지합니다. 컨텍스트 파일은 기존 본문을 보존하면서 관리 대상 지침만 업데이트합니다.
명시적으로 설정하지 않은 설정 키도 그대로 유지합니다.

계획을 작성하는 명령어는 `design-to-plan`입니다. 설치를 업데이트하면 기존 `spec-to-plan` 항목이 제거되며 별칭도 남기지 않습니다.

<a id="plugin-marketplace-installation"></a>

## 플러그인 마켓플레이스 설치

Claude Code에서는 마켓플레이스에서 플러그인을 설치할 수 있습니다.

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

플러그인은 명령어와 함께 스테이징된 내용의 커밋 분석 및 과거 요구사항 참조를 위한 세션 시작 지침을 제공합니다.
재개한 세션에도 적용됩니다. 플러그인을 설치하는 것만으로 프로젝트가 초기화되지는 않습니다.
언어, 워크플로우, 리뷰 설정을 만들거나 수정하려면 `/codexspec:config`를 사용하세요.
프로젝트의 기본 구조를 모두 준비해야 한다면 CLI로 초기화합니다.

커밋 미리보기나 승인된 커밋을 현재 체크아웃에서 실행하는 작업은 Python 3.11+와 Git이 있으면
상시 설치된 CodexSpec CLI 없이도 번들 런타임으로 실행할 수 있습니다.
worktree 작업 위치 선택, blueprint/auto-dev, 수동 프로파일 리뷰에는 여전히 CLI가 필요합니다.
플러그인 시작 훅에는 PATH에 등록된 Git과 명령어 훅의 `args`(exec 형식)를 지원하는 Claude Code 버전이 필요합니다.
이 지침은 에이전트에 적용되며, 수동으로 실행하는 Git 명령어에는 개입하지 않습니다.

자세한 설정 방법은 [설치](installation.md)를 참고하세요.
