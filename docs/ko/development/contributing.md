# 기여하기

## 사전 요구사항

- Python 3.11+
- uv 패키지 매니저
- Git

## 로컬 개발

```bash
# Clone the repository
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Install development dependencies
uv sync --extra dev

# Run locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/
```

## 문서화

```bash
# Install docs dependencies
uv sync --extra dev --extra docs

# Preview documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build --strict
```

## 빌드

```bash
uv build
```

## 풀 리퀘스트 프로세스

1. 저장소 포크
2. 기능 브랜치 생성
3. 변경 사항 만들기
4. 테스트 및 린트 실행
5. 풀 리퀘스트 제출

## 코드 스타일

- 줄 길이: 최대 120자
- PEP 8 따르기
- 공개 함수에 타입 힌트 사용

템플릿, 패키징, 초기화를 변경하기 전에 [CLAUDE.md](https://github.com/Zts0hg/codexspec/blob/main/CLAUDE.md), [AGENTS.md](https://github.com/Zts0hg/codexspec/blob/main/AGENTS.md),
[리포지토리 구조](https://github.com/Zts0hg/codexspec/blob/main/docs/internal/repository-layout.md)를 읽으세요.
배포 명령어와 스킬의 복사본은 자동 생성된 설치 산출물입니다. 기준이 되는 원본을 편집하고 다시 생성하세요.
