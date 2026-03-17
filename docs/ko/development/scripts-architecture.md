# 스크립트 아키텍처 분석

이 문서는 CodexSpec 프로젝트에서 스크립트의 코드 논리 흐름과 Claude Code에서 사용되는 방법을 자세히 설명합니다.

## 1. 전체 아키텍처 개요

CodexSpec은 **Spec-Driven Development (SDD)** 툴킷으로, CLI + 템플릿 + 보조 스크립트의 3계층 아키텍처를 채택합니다:

```
┌─────────────────────────────────────────────────────────────────┐
│                        사용자 계층 (CLI)                         │
│  codexspec init | check | version | config                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code 상호작용 계층                     │
│  /specify | /analyze | ...                                      │
│  (.claude/commands/*.md)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      보조 스크립트 계층                          │
│  .codexspec/scripts/*.sh (Bash) 또는 *.ps1 (PowerShell)        │
└─────────────────────────────────────────────────────────────────┘
```

## 2. 스크립트 배포 흐름

### 단계 1: `codexspec init` 초기화

`src/codexspec/__init__.py`의 `init()` 함수(343-368행)에서 운영 체제에 따라 해당 스크립트를 자동으로 복사합니다:

```python
# 플랫폼에 따라 보조 스크립트 복사
scripts_source_dir = get_scripts_dir()
if scripts_source_dir.exists():
    if sys.platform == "win32":
        # Windows: PowerShell 스크립트 복사
        ps_scripts = scripts_source_dir / "powershell"
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = codexspec_dir / "scripts" / script_file.name
            dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # macOS/Linux: Bash 스크립트 복사
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

## 3. Claude Code에서 스크립트 호출 메커니즘

### 핵심 메커니즘: YAML Frontmatter 선언

템플릿 파일은 YAML frontmatter를 통해 스크립트 의존성을 선언합니다:

```yaml
---
description: 명령 설명
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---
```

### 플레이스홀더 교체

템플릿에서 `{SCRIPT}` 플레이스홀더를 사용합니다:

```markdown
### 1. 컨텍스트 초기화

저장소 루트에서 `{SCRIPT}`를 실행하고 다음을 위해 JSON 구문 분석:
- `FEATURE_DIR` - 기능 디렉토리 경로
- `AVAILABLE_DOCS` - 사용 가능한 문서 목록
```

### 호출 흐름

1. 사용자가 Claude Code에서 `/analyze` 입력
2. Claude가 `.claude/commands/codexspec:analyze.md` 템플릿 읽기
3. 운영 체제에 따라 `{SCRIPT}`를 다음으로 교체:
   - **macOS/Linux**: `.codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks`
   - **Windows**: `.codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
4. Claude가 스크립트 실행, JSON 출력 구문 분석, 후속 작업 계속

## 4. 스크립트 기능 상세

### 4.1 `check-prerequisites.sh/ps1` - 사전 확인 스크립트

가장 중요한 스크립트로, 환경 상태를 검증하고 구조화된 정보를 반환합니다.

#### 핵심 기능

- 현재 feature 브랜치에 있는지 확인 (형식: `001-feature-name`)
- 필수 파일 존재 여부 감지 (`plan.md`, `tasks.md`)
- JSON 형식의 경로 정보 반환

#### 매개변수 옵션

| 매개변수 | Bash | PowerShell | 기능 |
|------|------|------------|------|
| JSON 출력 | `--json` | `-Json` | JSON 형식으로 출력 |
| tasks.md 요구 | `--require-tasks` | `-RequireTasks` | tasks.md 존재 검증 |
| tasks.md 포함 | `--include-tasks` | `-IncludeTasks` | AVAILABLE_DOCS에 tasks.md 포함 |
| 경로만 | `--paths-only` | `-PathsOnly` | 검증 건너뛰고 경로만 출력 |

#### JSON 출력 예시

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-my-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md", "tasks.md"]
}
```

### 4.2 `common.sh/ps1` - 공통 유틸리티 함수

크로스 플랫폼 공통 기능을 제공합니다:

#### Bash 버전 함수

| 함수 | 기능 |
|------|------|
| `get_feature_id()` | Git 브랜치 또는 환경 변수에서 feature ID 가져오기 |
| `get_specs_dir()` | specs 디렉토리 경로 가져오기 |
| `is_codexspec_project()` | CodexSpec 프로젝트인지 확인 |
| `require_codexspec_project()` | CodexSpec 프로젝트인지 확인, 아니면 종료 |
| `log_info/success/warning/error()` | 컬러 로그 출력 |
| `command_exists()` | 명령 존재 여부 확인 |

#### PowerShell 버전 함수

| 함수 | 기능 |
|------|------|
| `Get-RepoRoot` | Git 저장소 루트 디렉토리 가져오기 |
| `Get-CurrentBranch` | 현재 브랜치 이름 가져오기 |
| `Test-HasGit` | Git 저장소가 있는지 감지 |
| `Test-FeatureBranch` | feature 브랜치에 있는지 검증 |
| `Get-FeaturePathsEnv` | 모든 feature 관련 경로 가져오기 |
| `Test-FileExists` | 파일 존재 여부 확인 |
| `Test-DirHasFiles` | 디렉토리에 파일이 있는지 확인 |

### 4.3 `create-new-feature.sh/ps1` - 새 기능 생성

#### 기능

- 자동 증가 feature ID 생성 (001, 002, ...)
- feature 디렉토리 및 초기 spec.md 생성
- 해당 Git 브랜치 생성

#### 사용 예시

```bash
./create-new-feature.sh -n "user authentication" -i 001
```

## 5. 스크립트를 사용하는 명령

다음 4개 명령이 스크립트를 사용합니다:

| 명령 | 스크립트 매개변수 | 기능 |
|------|--------------|------|
| `/clarify` | `--json --paths-only` | 경로 가져오기, 파일 검증 안 함 |
| `/checklist` | `--json` | plan.md 존재 검증 |
| `/analyze` | `--json --require-tasks --include-tasks` | plan.md + tasks.md 검증 |
| `/tasks-to-issues` | `--json --require-tasks --include-tasks` | plan.md + tasks.md 검증 |

## 6. 전체 워크플로우 다이어그램

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        초기화 단계                                        │
│                                                                          │
│  $ codexspec init my-project                                             │
│       │                                                                  │
│       ├── .codexspec/ 디렉토리 구조 생성                                  │
│       ├── scripts/*.sh → .codexspec/scripts/ 복사                       │
│       ├── templates/commands/*.md → .claude/commands/ 복사              │
│       └── constitution.md, config.yml, CLAUDE.md 생성                   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                        사용 단계 (Claude Code)                            │
│                                                                          │
│  사용자: /analyze                                                        │
│       │                                                                  │
│       ├── Claude가 .claude/commands/codexspec:analyze.md 읽기           │
│       │                                                                  │
│       ├── YAML frontmatter의 scripts 선언 구문 분석                      │
│       │   scripts:                                                       │
│       │     sh: .codexspec/scripts/check-prerequisites.sh --json ...    │
│       │                                                                  │
│       ├── {SCRIPT} 플레이스홀더 교체                                     │
│       │                                                                  │
│       ├── 스크립트 실행:                                                 │
│       │   $ .codexspec/scripts/check-prerequisites.sh --json ...        │
│       │                                                                  │
│       ├── JSON 출력 구문 분석:                                           │
│       │   {"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}               │
│       │                                                                  │
│       ├── spec.md, plan.md, tasks.md 읽기                               │
│       │                                                                  │
│       └── 분석 보고서 생성                                               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 7. 설계 하이라이트

### 7.1 크로스 플랫폼 호환

Bash와 PowerShell 버전을 모두 유지하며 `sys.platform`으로 자동 선택:

```python
if sys.platform == "win32":
    # PowerShell 스크립트 복사
else:
    # Bash 스크립트 복사
```

### 7.2 선언적 구성

YAML frontmatter를 통해 스크립트 의존성을 선언하여 명확하고 직관적:

```yaml
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json
```

### 7.3 JSON 출력

스크립트가 구조화된 데이터를 출력하여 Claude가 구문 분석하기 쉬움:

```json
{
  "FEATURE_DIR": "/path/to/.codexspec/specs/001-feature",
  "AVAILABLE_DOCS": ["research.md", "data-model.md"]
}
```

### 7.4 점진적 검증

다른 명령이 다른 매개변수를 사용하여 필요에 따라 검증:

| 단계 | 명령 | 검증 수준 |
|------|------|----------|
| 계획 전 | `/clarify` | 경로만 |
| 계획 후 | `/checklist` | plan.md |
| 작업 후 | `/analyze` | plan.md + tasks.md |

### 7.5 Git 통합

- 브랜치 이름에서 자동으로 feature ID 추출
- 브랜치 이름 검증 지원 (`^\d{3}-` 형식)
- 환경 변수 오버라이드 지원 (`SPECIFY_FEATURE` / `CODEXSPEC_FEATURE`)

## 8. 핵심 코드 경로

| 파일 | 행 번호/위치 | 기능 |
|------|-----------|------|
| `src/codexspec/__init__.py` | 343-368 | 스크립트 복사 논리 |
| `src/codexspec/__init__.py` | 71-90 | `get_scripts_dir()` 경로 해결 |
| `scripts/bash/check-prerequisites.sh` | 전체 | Bash 사전 확인 메인 스크립트 |
| `scripts/powershell/check-prerequisites.ps1` | 56-146 | PowerShell 사전 확인 스크립트 |
| `scripts/bash/common.sh` | 전체 | Bash 공통 유틸리티 함수 |
| `scripts/powershell/common.ps1` | 전체 | PowerShell 공통 유틸리티 함수 |
| `templates/commands/*.md` | YAML frontmatter | 스크립트 선언 |

## 9. 스크립트 파일 목록

### Bash 스크립트 (`scripts/bash/`)

```
scripts/bash/
├── check-prerequisites.sh   # 사전 확인 메인 스크립트
├── common.sh                # 공통 유틸리티 함수
└── create-new-feature.sh    # 새 기능 생성
```

### PowerShell 스크립트 (`scripts/powershell/`)

```
scripts/powershell/
├── check-prerequisites.ps1  # 사전 확인 메인 스크립트
├── common.ps1               # 공통 유틸리티 함수
└── create-new-feature.ps1   # 새 기능 생성
```

---

*이 문서는 CodexSpec 프로젝트에서 스크립트의 전체 아키텍처와 사용 흐름을 기록합니다. 업데이트가 있으면 동기화하여 수정하세요.*
