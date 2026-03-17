# 설치

## 사전 요구사항

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (권장) 또는 pip

## 옵션 1: uv로 설치 (권장)

CodexSpec을 설치하는 가장 쉬운 방법은 uv를 사용하는 것입니다:

```bash
uv tool install codexspec
```

## 옵션 2: pip로 설치

또는 pip를 사용할 수 있습니다:

```bash
pip install codexspec
```

## 옵션 3: 일회성 사용

설치하지 않고 직접 실행:

```bash
# 새 프로젝트 생성
uvx codexspec init my-project

# 기존 프로젝트에서 초기화
cd your-existing-project
uvx codexspec init . --ai claude
```

## 옵션 4: GitHub에서 설치

최신 개발 버전의 경우:

```bash
# uv 사용
uv tool install git+https://github.com/Zts0hg/codexspec:git

# pip 사용
pip install git+https://github.com/Zts0hg/codexspec:git

# 특정 브랜치 또는 태그
uv tool install git+https://github.com/Zts0hg/codexspec:git@main
uv tool install git+https://github.com/Zts0hg/codexspec:git@v0.2.0
```

## 설치 확인

```bash
codexspec --help
codexspec version
```

## 업그레이드

```bash
# uv 사용
uv tool install codexspec --upgrade

# pip 사용
pip install --upgrade codexspec
```

## 다음 단계

[빠른 시작](quick-start.md)
