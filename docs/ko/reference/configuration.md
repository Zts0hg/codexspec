<a id="configuration-and-internationalization"></a>

# 설정과 국제화

설정은 `.codexspec/config.yml`에 저장합니다. 템플릿은 영어로 유지하지만,
에이전트는 설정된 언어로 대화와 산출물을 작성합니다.
표준 언어 코드는 13개입니다: `en`, `zh-CN`, `zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `it`, `ar`, `hi`.
포르투갈어 CLI 코드는 `pt`이며, 현지화된 문서와 번역 카탈로그는 `pt-BR`을 사용합니다.

<a id="language-dimensions"></a>

## 언어별 설정

| 구분 | 설정 키 | 초기화 시 | 나중에 설정 | 적용 대상 |
|-----------|------------|-------------------|-----------|----------|
| 출력·기본 언어 | `language.output` | `--lang` | `config --set-lang` | 다른 언어 설정이 없을 때 사용할 기본 언어 |
| 대화 | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | 대화와 CLI 출력 |
| 문서 | `language.document` | `--document-lang` | `config --set-document-lang` | 요구사항, 명세서, 설계, 계획, 태스크 |
| 커밋 | `language.commit` | `--commit-lang` | `config --set-commit-lang` | 커밋 메시지와 Git 워크플로우에서 생성하는 텍스트 |

각 언어 설정은 독립적으로 `language.output`, 그다음 `en`을 기본값으로 사용합니다.
`language.templates`는 `en`으로 유지합니다.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

첫 TTY 초기화에서는 `--lang` 또는 세 가지 개별 언어 옵션을 모두 지정하지 않으면 기본 언어를 선택하라는 메시지가 표시됩니다.
`--force`는 다른 초기화 확인을 자동 승인하지만 이 언어 선택은 생략하지 않습니다.
비 TTY 초기화에서는 기본적으로 영어를 사용합니다. 재초기화할 때도 명시적으로 설정하지 않은 언어 키는 유지합니다.

<a id="workflow-and-review-settings"></a>

## 워크플로우와 리뷰 설정

| 설정 | 기본값 | 동작 | CLI 제어 |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | 통과한 일반 SDD 단계에서 다음 단계로 진행 | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | 마무리 작업 성공 후 사용자와의 대화 없이 지식 추출 | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | 자동 수정 중 검증된 유지보수 개선을 점진적으로 적용 | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | 일반 기능과 독립적인 유지보수 작업을 별도 worktree로 격리 | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | 프로젝트의 운영 범위 밖에서 발생하는 지적을 누가 판단할지 지정 | `config --decided-by reviewer\|ask` |

불리언 CLI 스위치는 대소문자를 구분하지 않고 `on/true/1/yes`와 `off/false/0/no`를 받으며, 앞뒤 공백도 허용합니다.
값을 지정하지 않고 사용하면 대상 체크아웃의 현재 값을 전환합니다. YAML에는 불리언 값으로 저장합니다.

`review.decided_by: reviewer`에서는 리뷰어가 결함으로 인정할지 판단합니다.
`ask`에서는 운영 범위 밖의 발생 조건을 사용자 판단을 기다리는 시나리오로 처리합니다.
사용자는 수정할지 해당 시나리오를 제외할지 한 번 결정하며, 확정된 결정은 이후 라운드에서도 사용할 수 있도록 보존합니다.
판단을 기다리는 항목이 있으면 완료할 수 없습니다. 한 번의 `review-code` 실행에 한해 `--decided-by`로 설정된 모드를 재정의할 수 있습니다.

설정을 쓸 때도 worktree 작업 위치 선택 규칙을 따릅니다.
main 체크아웃에서 독립적인 변경을 요청하면 유지보수 worktree에 기록하며, main에서 적용 중인 설정이 즉시 바뀌지는 않습니다.
기능 worktree 안에서 변경한 설정은 그곳에서 적용됩니다.

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

<details>
<summary>설정 예시</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

언어와 설정의 자세한 동작은 [설정](configuration.md)과 [국제화](../user-guide/i18n.md)를 참고하세요.
