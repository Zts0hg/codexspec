# CLI 참조

<a id="cli-commands"></a>

## CLI 명령어

| 명령어 | 목적 |
|---------|---------|
| `codexspec init` | Claude, Codex 또는 둘 모두에 맞게 프로젝트 초기화·갱신 |
| `codexspec check` | 설치된 도구와 의존성 확인 |
| `codexspec version` | 버전과 시스템 정보 표시 |
| `codexspec config` | 프로젝트 설정 조회·수정 |
| `codexspec list-commands` | 사용할 수 있는 에이전트 명령어를 범주별로 표시 |
| `codexspec show-blueprint` | 공유 worktree의 블루프린트를 변경하지 않고 출력 |

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

<details>
<summary>CLI 초기화 옵션</summary>

| 옵션 | 의미 |
|--------|---------|
| `PROJECT_NAME` | 새 디렉터리 이름. 현재 디렉터리에는 `.` 사용 |
| `--here`, `-h` | 현재 디렉터리 초기화 |
| `--ai`, `-a` | `claude`, `codex`, `both` 중 선택. 기본값은 `claude` |
| `--lang`, `-l` | 기본 출력 언어 설정 |
| `--interaction-lang` | 대화 언어 설정 |
| `--document-lang` | 문서 언어 설정 |
| `--commit-lang` | 커밋 메시지 언어 설정 |
| `--force`, `-f` | 설치된 산출물을 다시 생성하고 마이그레이션·업데이트·준수 확인을 자동 승인. 프로젝트에서 작성한 컨텍스트와 지정한 옵션에 관계없는 설정은 보존 |
| `--no-git` | Git 리포지토리 초기화 생략 |
| `--debug`, `-d` | 자세한 디버그 정보 표시 |

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
| `--auto-maintenance` | 점진적 유지보수 개선 자동 적용 전환·설정 |
| `--worktrees` | 체크아웃별 worktree 격리 전환·설정 |
| `--decided-by` | 리뷰 판단 모드를 `reviewer` 또는 `ask`로 설정 |

</details>

## `codexspec show-blueprint`

고정 브랜치 `codexspec/auto-dev`와 `worktree-for-codexspec-auto-dev`의 전체
`.codexspec/blueprint.md`를 표준 출력에 원문 그대로 표시합니다. 저장소, 브랜치, worktree 또는
파일이 없으면 표준 오류에 진단을 출력하고 0이 아닌 상태로 종료합니다. 읽기 전용이며 fetch,
merge, 쓰기 또는 잠금을 수행하지 않습니다.

```bash
codexspec show-blueprint
```
