# 빠른 시작

## 1. 프로젝트 초기화

설치 후 프로젝트를 생성하거나 초기화합니다:

```bash
# 새 프로젝트 생성
codexspec init my-awesome-project

# 또는 현재 디렉토리에서 초기화
codexspec init . --ai claude

# 중국어 출력으로
codexspec init my-project --lang zh-CN
```

## 2. 프로젝트 원칙 수립

프로젝트 디렉토리에서 Claude Code를 실행합니다:

```bash
cd my-awesome-project
claude
```

constitution 명령을 사용합니다:

```
/constitution 코드 품질과 테스트에 중점을 둔 원칙을 생성합니다
```

## 3. 요구사항 명확화

`/specify`를 사용하여 요구사항을 탐색합니다:

```
/작업 관리 애플리케이션을 구축하고 싶습니다
```

## 4. 명세서 생성

명확화가 완료되면 명세서 문서를 생성합니다:

```
/generate-spec
```

## 5. 리뷰 및 검증

**권장:** 진행하기 전에 검증합니다:

```
/review-spec
```

## 6. 기술 계획 생성

```
/spec-to-plan 백엔드에 Python FastAPI 사용
```

## 7. 작업 생성

```
/plan-to-tasks
```

## 8. 구현

```
/implement-tasks
```

## 프로젝트 구조

초기화 후:

```
my-project/
+-- .codexspec/
|   +-- memory/
|   |   +-- constitution.md
|   +-- specs/
|   |   +-- {feature-id}/
|   |       +-- spec.md
|   |       +-- plan.md
|   |       +-- tasks.md
|   +-- scripts/
+-- .claude/
|   +-- commands/
+-- CLAUDE.md
```

## 다음 단계

[전체 워크플로우 가이드](../user-guide/workflow.md)
