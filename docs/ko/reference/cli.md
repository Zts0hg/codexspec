# CLI 참조

## 명령

### `codexspec init`

새 CodexSpec 프로젝트를 초기화합니다.

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**인자:**

| 인자 | 설명 |
|----------|-------------|
| `PROJECT_NAME` | 새 프로젝트 디렉토리의 이름 |

**옵션:**

| 옵션 | 단축 | 설명 |
|--------|-------|-------------|
| `--here` | `-h` | 현재 디렉토리에서 초기화 |
| `--ai` | `-a` | 사용할 AI 어시스턴트 (기본값: claude) |
| `--lang` | `-l` | 출력 언어 (예: en, zh-CN, ja) |
| `--force` | `-f` | 기존 파일 덮어쓰기 강제 |
| `--no-git` | | git 초기화 건너뛰기 |
| `--debug` | `-d` | 디버그 출력 활성화 |

**예제:**

```bash
# 새 프로젝트 생성
codexspec init my-project

# 현재 디렉토리에서 초기화
codexspec init . --ai claude

# 중국어 출력으로
codexspec init my-project --lang zh-CN
```

---

### `codexspec check`

설치된 도구를 확인합니다.

```bash
codexspec check
```

---

### `codexspec version`

버전 정보를 표시합니다.

```bash
codexspec version
```

---

### `codexspec config`

프로젝트 구성을 보거나 수정합니다.

```bash
codexspec config [OPTIONS]
```

**옵션:**

| 옵션 | 단축 | 설명 |
|--------|-------|-------------|
| `--set-lang` | `-l` | 출력 언어 설정 |
| `--list-langs` | | 지원되는 모든 언어 나열 |
