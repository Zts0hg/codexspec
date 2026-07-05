# 스크립트 아키텍처 분석

이 문서는 CodexSpec 프로젝트에서 스크립트의 코드 논리 흐름과 Claude Code 에서 사용되는 방식을 자세히 설명합니다.

## 1. 전체 아키텍처 개요

CodexSpec 은 **명세 기반 개발(SDD)** 툴킷으로, CLI + 템플릿 + 보조 스크립트의 3계층 아키텍처를 채택합니다:

```
┌─────────────────────────────────────────────────────────────────┐
│                        사용자 계층(CLI)                          │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code 상호작용 계층                      │
│  /codexspec:specify | /codexspec:analyze | ...                  │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      보조 스크립트 계층                          │
│  .codexspec/scripts/*.sh (Bash) 또는 *.ps1 (PowerShell)         │
└─────────────────────────────────────────────────────────────────┘
```

## 2. 스크립트 배포 흐름

### 단계 1: `codexspec init` 초기화

`src/codexspec/__init__.py`의 `init()` 함수(343-368행)에서 운영 체제에 따라 알맞은 스크립트를 자동으로 복사합니다:

```python
# Copy helper scripts based on platform
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows: 복사 PowerShell 스크립트
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux: 복사 Bash 스크립트
        bash_scripts = scripts_source_dir / "bash"
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
```

**결과**: 운영 체제에 따라 `scripts/bash/` 또는 `scripts/powershell/`의 스크립트를 프로젝트의 `.codexspec/scripts/` 디렉토리로 복사합니다.

### 경로 해결 메커니즘

`get_scripts_dir()` 함수(71-90행)는 여러 설치 시나리오를 처리합니다:

```python
def get_scripts_dir() -> Path:
    # Path 1: Wheel install - scripts packaged inside codexspec package
    installed_scripts = Path(__file__).parent / "scripts"
    if installed_scripts.exists():
        return installed_scripts

    # Path 2: Development/editable install - scripts in project root
    dev_scripts = Path(__file__).parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    # Path 3: Fallback
    return installed_scripts
```

## 3. Claude Code 에서의 스크립트 호출 메커니즘

### 핵심 메커니즘: YAML Frontmatter 선언

템플릿 파일은 YAML frontmatter로 스크립트 의존성을 선언합니다:

```yaml
---
description: 명령어 설명
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### 플레이스홀더 치환

템플릿 안에서 `{SCRIPT}` 플레이스홀더를 사용합니다:

```markdown
### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - 기능 디렉토리 경로
- `AVAILABLE_DOCS` - 사용 가능한 문서 목록
```

### 호출 흐름

1. 사용자가 Claude Code에서 `/codexspec:analyze`를 입력
2. Claude 가 `.claude/commands/codexspec:analyze.md` 템플릿을 읽음
3. 운영 체제에 따라 `{SCRIPT}`를 다음으로 교체:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude 가 스크립트를 실행하고, JSON 출력을 파싱한 뒤 후속 작업을 계속

## 4. 스크립트 기능 상세

### 4.1 `check-prerequisites.sh/ps1` - 사전 확인 스크립트

가장 중요한 스크립트로, 환경 상태를 검증하고 구조화된 정보를 반환합니다.

#### 핵심 기능

- 현재 feature 브랜치에 있는지 확인(형식: `2026-0613-1200ab-feature-name`)
- 필수 파일이 존재하는지 감지(`plan.md`, `tasks.md`)
- JSON 형식의 경로 정보 반환

#### 매개변수 옵션

| 매개변수 | Bash | PowerShell | 기능 |
|------|------|------------|------|
| JSON 출력 | `--json` | `-Json` | JSON 형식으로 출력 |
| tasks.md 요구 | `--require-tasks` | `-RequireTasks` | tasks.md 존재 검증 |
| tasks.md 포함 | `--include-tasks` | `-IncludeTasks` | AVAILABLE_DOCS 에 tasks.md 포함 |
| 경로만 | `--paths-only` | `-PathsOnly` | 검증을 건너뛰고 경로만 출력 |

#### JSON 출력 예시

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - 공용 유틸리티 함수

크로스 플랫폼 공통 기능을 제공합니다:

#### Bash 버전 함수

| 함수 | 기능 |
|------|------|
| `get_feature_id()` | Git 브랜치 또는 환경 변수에서 feature ID 가져오기 |
| `get_specs_dir()` | specs 디렉토리 경로 가져오기 |
| `is_codexspec_project()` | CodexSpec 프로젝트인지 확인 |
| `require_codexspec_project()` | CodexSpec 프로젝트인지 확인, 아니면 종료 |
| `log_info/success/warning/error()` | 컬러 로그 출력 |
| `command_exists()` | 명령어 존재 여부 확인 |

#### PowerShell 버전 함수

| 함수 | 기능 |
|------|------|
| `Get-RepoRoot` | Git 리포지토리 루트 디렉토리 가져오기 |
| `Get-CurrentBranch` | 현재 브랜치 이름 가져오기 |
| `Test-HasGit` | Git 리포지토리가 있는지 감지 |
| `Test-FeatureBranch` | feature 브랜치에 있는지 검증 |
| `Get-FeaturePathsEnv` | feature 관련 경로 전체 가져오기 |
| `Test-FileExists` | 파일 존재 여부 확인 |
| `Test-DirHasFiles` | 디렉토리에 파일이 있는지 확인 |

### 4.3 `create-new-feature.sh/ps1` - 새 기능 생성

#### 기능

- `YYYY-MMDD-HHMMxx` 형식의 feature ID 자동 생성
- feature 디렉토리와 초기 requirements.md 생성
- 해당 Git 브랜치 생성
- short name 을 정규화한 뒤 최소 한 자 이상의 ASCII 문자/숫자를 포함하도록 요구

#### 사용 예시

```bash
./create-new-feature.sh -n "user authentication"
```

#### Feature naming contract

- Sequential `NNN-name` 식별자는 지원하지 않습니다. 타임스탬프 이름만 유일한 feature naming 형식입니다.
- 레거시 호환성은 산출물에만 적용됩니다. `requirements.md`가 없을 때 기존 `spec.md`를 사용할 수는 있지만, 디렉토리나 브랜치 naming 형식을 다르게 허용하지는 않습니다.
- 전체 feature 이름은 하나의 워크스페이스를 식별합니다: `YYYY-MMDD-HHMMxx-short-name`. 독립적으로 만들어진 워크스페이스는 short name 이 다르면 같은 타임스탬프 ID를 공유할 수 있습니다.
- Short-ID 조회는 로컬 편의 기능일 뿐입니다. 두 개 이상의 디렉토리가 매칭되면, 임의로 선택하거나 덮어쓰는 대신 모호성을 보고합니다.

## 5. 스크립트를 사용하는 명령어

다음 4개 명령어가 스크립트를 사용합니다:

| 명령어 | 스크립트 매개변수 | 기능 |
|------|--------------|------|
| `/codexspec:clarify` | `--json --paths-only` | 경로만 가져오고 파일 검증은 안 함 |
| `/codexspec:checklist` | `--json` | plan.md 존재 검증 |
| `/codexspec:analyze` | `--json --require-tasks --include-tasks` | plan.md + tasks.md 검증 |
| `/codexspec:tasks-to-issues` | `--json --require-tasks --include-tasks` | plan.md + tasks.md 검증 |

## 6. 전체 워크플로우 다이어그램

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        초기화 단계                                        │
│                                                                          │
│  $ codexspec init my-project                                             │
│       │                                                                  │
│       ├── .codexspec/ 디렉토리 구조 생성                                  │
│       ├── 복사 scripts/*.sh → .codexspec/scripts/                        │
│       ├── 복사 templates/commands/*.md → .claude/commands/               │
│       └── 생성 constitution.md, config.yml, CLAUDE.md                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        사용 단계(Claude Code)                             │
│                                                                          │
│  사용자: /codexspec:analyze                                              │
│       │                                                                  │
│       ├── Claude 가 .claude/commands/codexspec:analyze.md 를 읽음         │
│       │                                                                  │
│       ├── YAML frontmatter 의 scripts 선언을 파싱                         │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...      │
│       │                                                                  │
│       ├── {SCRIPT} 플레이스홀더 치환                                      │
│       │                                                                  │
│       ├── 스크립트 실행:                                                  │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...          │
│       │                                                                  │
│       ├── JSON 출력 파싱:                                                 │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}                │
│       │                                                                  │
│       ├── spec.md, plan.md, tasks.md 읽기                                │
│       │                                                                  │
│       └── 분석 보고서 생성                                                │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. 설계 하이라이트

### 7.1 크로스 플랫폼 호환

Bash 와 PowerShell 버전을 함께 유지하며 `sys.platform`으로 자동 선택:

```python
if sys.platform == "win32":
    # 복사 PowerShell 스크립트
else:
    # 복사 Bash 스크립트
```

### 7.2 선언적 설정

YAML frontmatter로 스크립트 의존성을 선언해 명확하고 직관적입니다:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 JSON 출력

스크립트가 구조화된 데이터를 출력해 Claude 가 파싱하기 쉽습니다:

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/2026-0613-1200ab-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 점진적 검증

명령어마다 다른 매개변수를 사용해 필요에 맞게 검증합니다:

| 단계 | 명령어 | 검증 수준 |
|------|------|----------|
| 계획 전 | `/codexspec:clarify` | 경로만 |
| 계획 후 | `/codexspec:checklist` | plan.md |
| 태스크 후 | `/codexspec:analyze` | plan.md + tasks.md |

### 7.5 Git 연동

- 브랜치 이름에서 feature ID 자동 추출
- 브랜치 이름 검증 지원(`^\d{3}-` 형식)
- 환경 변수 오버라이드 지원(`CODEXSPEC_FEATURE`)

## 8. 핵심 코드 경로

| 파일 | 행 번호/위치 | 기능 |
|------|-----------|------|
| `src/codexspec/__init__.py` | 343-368 | 스크립트 복사 로직 |
| `src/codexspec/__init__.py` | 71-90 | `get_scripts_dir()` 경로 해결 |
| `scripts/bash/check-prerequisites.sh` | 전체 | Bash 사전 확인 메인 스크립트 |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | PowerShell 사전 확인 스크립트 |
| `scripts/bash/common.sh` | 전체 | Bash 공용 유틸리티 함수 |
| `scripts/powershell/common.ps1` | 전체 | PowerShell 공용 유틸리티 함수 |
| `templates/commands/*.md` | YAML frontmatter | 스크립트 선언 |

## 9. 스크립트 파일 목록

### Bash 스크립트(`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # 사전 확인 메인 스크립트
├── common.sh                # 공용 유틸리티 함수
└── create-new-feature.sh    # 새 기능 생성
```

### PowerShell 스크립트(`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # 사전 확인 메인 스크립트
├── common.ps1               # 공용 유틸리티 함수
└── create-new-feature.ps1   # 새 기능 생성
```

---

*이 문서는 CodexSpec 프로젝트에서 스크립트의 전체 아키텍처와 사용 흐름을 기록합니다. 업데이트가 있으면 동기화해 수정하세요.*
