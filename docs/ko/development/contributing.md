# 기여하기

## 사전 요구사항

- Python 3.11+
- uv 패키지 매니저
- Git

## 로컬 개발

```bash
# 저장소 복제
git clone https://github.com/Zts0hg/codexspec:git
cd codexspec

# 개발 의존성 설치
uv sync --dev

# 로컬에서 실행
uv run codexspec --help

# 테스트 실행
uv run pytest

# 코드 린트
uv run ruff check src/
```

## 문서화

```bash
# 문서 의존성 설치
uv sync --extra docs

# 로컬에서 문서 미리보기
uv run mkdocs serve

# 문서 빌드
uv run mkdocs build
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
