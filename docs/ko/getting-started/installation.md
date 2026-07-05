# 설치

## 사전 요구 사항

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (권장) 또는 pip

## 옵션 1: uv로 설치 (권장)

CodexSpec을 설치하는 가장 쉬운 방법은 uv를 사용하는 것입니다:

```bash
uv tool install codexspec
```

## 옵션 2: pip로 설치

대안으로 pip를 사용할 수 있습니다:

```bash
pip install codexspec
```

## 옵션 3: 일회성 실행

설치하지 않고도 직접 실행할 수 있습니다:

```bash
# 새 프로젝트 생성
uvx codexspec init my-project

# 기존 프로젝트에서 Claude Code 용으로 초기화
cd your-existing-project
uvx codexspec init . --ai claude

# Codex CLI 용으로 초기화
uvx codexspec init . --ai codex

# Claude Code 와 Codex CLI 모두를 위해 초기화 (.claude/ 와 .agents/ 둘 다 작성)
uvx codexspec init . --ai both
```

## 옵션 4: GitHub에서 설치

최신 개발 버전이 필요할 때:

```bash
# uv 사용
uv tool install git+https://github.com/Zts0hg/codexspec.git

# pip 사용
pip install git+https://github.com/Zts0hg/codexspec.git

# 특정 브랜치 또는 태그
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.5.6
```

## 옵션 5: 플러그인 마켓플레이스 설치 (대안)

CodexSpec은 Claude Code 플러그인으로도 제공됩니다. CLI 도구를 설치하지 않고 Claude Code 안에서 CodexSpec의 슬래시 명령어를 바로 사용하고 싶을 때 적합한 방식입니다. CLI는 Requirements-First SDD 의 전체 경험을 제공하고, 플러그인은 Claude Code 위에 슬래시 명령어 세트를 얹어 줍니다.

### 설치 단계

Claude Code 안에서:

```bash
# 마켓플레이스 추가
> /plugin marketplace add Zts0hg/codexspec

# 플러그인 설치
> /plugin install codexspec@codexspec-market
```

### 플러그인 사용자를 위한 언어 설정

플러그인 마켓플레이스로 설치한 뒤에는 `/codexspec:config` 슬래시 명령어로 선호하는 언어를 설정합니다(CLI 설치가 없으면 `codexspec config` CLI 명령어는 사용할 수 없습니다):

```bash
# 대화형 설정 시작
> /codexspec:config

# 또는 현재 설정 확인
> /codexspec:config --view
```

이 config 명령어는 출력 언어(생성되는 문서의 언어)와 커밋 메시지 언어를 선택하는 과정을 안내하고, `.codexspec/config.yml`을 작성합니다. 다국어 지원은 CLI와 동일한 LLM 동적 번역을 사용합니다.

### 설치 방법 비교

| 방식 | 적합한 경우 | 제공 기능 |
|------|------------|----------|
| **CLI 설치** (`uv tool install` 또는 `pip install`) | 전체 개발 워크플로우 | CLI 명령어(`init`, `check`, `config`, `version`) + 슬래시 명령어 |
| **플러그인 마켓플레이스** | 빠른 시작, 기존 프로젝트 | 슬래시 명령어만 (언어 설정은 `/codexspec:config` 사용) |

**참고**: 플러그인은 `strict: false` 모드를 사용하며, LLM 동적 번역을 통한 기존 다국어 지원을 그대로 재사용합니다.

## 설치 확인

```bash
codexspec --help
codexspec version
```

(플러그인 마켓플레이스로 설치한 경우, Claude Code 안에서 `/codexspec:config --view` 같은 슬래시 명령어를 실행해 확인할 수 있습니다.)

## 업그레이드

```bash
# uv 사용
uv tool install codexspec --upgrade

# pip 사용
pip install --upgrade codexspec
```

(플러그인 마켓플레이스 설치는 Claude Code의 플러그인 매니저가 업데이트합니다.)

## 다음 단계

[빠른 시작](quick-start.md)
