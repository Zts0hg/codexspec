# 스크립트 및 설치 구조

## 런타임과 명령 원본

`src/codexspec/`의 Python CLI는 `templates/commands/`의 완성된 명령 템플릿, 문서 템플릿, 공통 검토 기준을 설치합니다. Claude Code에는 슬래시 명령을, Codex에는 같은 명령 원본에서 생성한 네이티브 스킬을 제공합니다. 28개 공개 명령은 두 호스트에서 동일한 워크플로 규칙을 따릅니다.

## 설치와 프로젝트 컨텍스트

`codexspec init`은 플랫폼별 도우미와 요청한 어시스턴트 통합을 선택합니다. 공통 리소스는 `.codexspec/`, Claude 명령은 `.claude/commands/codexspec/`, Codex 스킬은 `.agents/skills/`에 저장됩니다. 설치된 CLI는 워크플로에 필요한 작업 공간 라우팅과 보호 검사를 거치는 도우미 작업도 지원합니다.

초기화는 기존 `AGENTS.md`와 `CLAUDE.md`에서 CodexSpec이 관리하는 블록을 갱신하고, 블록 밖의 프로젝트 자체 내용은 보존합니다. `--force`는 설치 산출물을 새로 갱신하고 업데이트 확인에 응답하지만, 컨텍스트 파일 전체를 교체하거나 무관한 설정을 삭제하지는 않습니다. CLI 설치만으로 프로젝트가 초기화되지는 않습니다.

## 플랫폼별 도우미

Unix 프로젝트에는 `scripts/bash/`의 Bash 스크립트가, Windows 프로젝트에는 `scripts/powershell/`의 PowerShell 스크립트가 설치됩니다. 기능 생성과 사전 조건 검사는 선택한 기능을 식별하고 기계가 읽을 수 있는 컨텍스트를 반환합니다. `common.sh`와 `common.ps1`은 플랫폼별 공통 유틸리티를 제공하며, `review-context`는 검토 대상 정보 수집을 지원합니다. 독립적인 커밋 런타임은 두 플랫폼 모두에서 `src/codexspec/commit_runtime.py`로부터 `.codexspec/scripts/commit-staged-helper.py`로 복사됩니다.

## 기능 식별과 산출물 호환성

기능 이름은 `YYYY-MMDD-HHMMss-name` 형식이며, 분 단위 타임스탬프, 소문자 영숫자 두 글자로 된 접미사, ASCII 이름으로 구성됩니다. 전체 기능 이름이 작업 공간을 식별하므로 명시적인 경로나 브랜치를 사용해 이어서 작업합니다. 순차 번호를 사용하는 `NNN-name` 식별자는 지원하지 않습니다. 기존 기능과의 호환성은 산출물에 적용됩니다. `requirements.md`나 `design.md`가 없는 경우 최초 확인 기록을 지어내지 않고 추적 가능성의 한계를 밝힙니다.

## 기여자를 위한 유지보수

정본 소스를 수정한 뒤 파생 사본을 다시 생성하고 배포 결과를 검증합니다. 조각 기반 방식을 사용하는 명령은 `internal/command_templates/sources/`에서 작성하며, 완성된 `templates/commands/` 파일은 생성됩니다. 나머지 명령 템플릿은 직접 작성합니다. 설치된 Claude 또는 Codex 사본을 수동으로 편집하지 마세요.

패키지에는 공개 템플릿과 두 플랫폼의 스크립트 디렉터리가 포함됩니다. `internal/`의 유지보수 도구, `docs/`의 사이트 원본, 테스트, 워크플로 그림 원본과 이미지는 설치 패키지에 포함되지 않습니다. 스크립트 포함 범위를 `scripts/` 전체로 넓히지 마세요.

<a id="extension-materials"></a>

## 확장 기능 작성 자료

리포지토리에는 확장 기능 매니페스트 템플릿, 예제 명령어, [확장 기능 개발 가이드](https://github.com/Zts0hg/codexspec/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md)가 있습니다.
이 자료는 확장 기능을 작성하기 위한 것입니다. 현재 CLI에는 확장 기능 설치·목록·제거 명령어가 없으며,
`extension.yml`의 명령어나 훅을 자동으로 불러오지도 않습니다.
공통 리뷰 리소스에는 `.codexspec/review-code/` 아래에 프로젝트별 내용을 추가할 수 있습니다.
초기화할 때는 교체를 요청하지 않는 한 기존 리소스의 수정 사항과 추가 파일을 보존합니다.
