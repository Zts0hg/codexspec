# Commands

CodexSpec のスラッシュコマンドのリファレンスです。これらのコマンドは Claude Code のチャットインターフェースで呼び出します。

ワークフローのパターンや各コマンドを使うタイミングについては [Workflow](workflow.md) を、CLI コマンドについては [CLI](../reference/cli.md) を参照してください。

## Quick Reference

README のカタログと対応するよう、カテゴリ別にグループ化しています。各グループ内ではワークフロー順に並んでいます。

### Core Workflow Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:constitution` | プロジェクト憲法を作成・更新し、アーティファクト間の整合性を検証します |
| `/codexspec:specify` | 対話を通じて要件を明確化・確認し、`requirements.md` に保存します |
| `/codexspec:generate-spec` | 明確化された要件から `spec.md` を生成します（★ 自動レビュー付き） |
| `/codexspec:spec-to-plan` | 仕様書を技術的な実装計画に変換します（★ 自動レビュー付き） |
| `/codexspec:plan-to-tasks` | 計画を追跡可能で検証可能なタスクに分割します（★ 自動レビュー付き） |
| `/codexspec:implement-tasks` | タスクを条件付き TDD ワークフローで実行します |

### Review Commands (Quality Gates)

| Command | Purpose |
|---------|---------|
| `/codexspec:review-spec` | 仕様書の完全性と品質を検証します |
| `/codexspec:review-plan` | 技術計画の実現可能性と整合性をレビューします |
| `/codexspec:review-tasks` | タスクのカバレッジ、順序、実現可能性を検証します |

### Enhancement Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:config` | プロジェクト設定を対話的に管理します（作成/参照/変更/リセット） |
| `/codexspec:clarify` | 既存の仕様書をスキャンして曖昧さを検出します（4 カテゴリ、最大 5 問） |
| `/codexspec:analyze` | アーティファクト間の整合性分析を行います（読み取り専用、重大度ベース） |
| `/codexspec:checklist` | 要件品質のチェックリストを生成します |
| `/codexspec:tasks-to-issues` | タスクを GitHub Issues に変換します |

### Git Workflow Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:commit-staged` | ステージ済み変更からコミットメッセージを生成します（セッションコンテキスト対応） |
| `/codexspec:pr` | git diff から PR/MR の説明を生成します（プラットフォームを自動検出） |

### Code Review Commands

| Command | Purpose |
|---------|---------|
| `/codexspec:review-code` | 任意の言語のコードをレビューします（慣用的表現の明確さ、正確性、堅牢性、アーキテクチャ） |
| `/codexspec:review-python-code` | Python コードをレビューします（PEP 8、型安全性、堅牢性、憲法整合性） |
| `/codexspec:review-react-code` | React/TypeScript コードをレビューします（コンポーネントアーキテクチャ、Hooks 規則、状態、パフォーマンス） |

### Fast Track

| Command | Purpose |
|---------|---------|
| `/codexspec:quick` | 小さな変更向けに要件ファーストの SDD フローを合理化して実行します |

---

## Command Categories

### Core Workflow Commands

Requirements-First SDD の主要なワークフローを担うコマンド群です：Constitution → 確認された要件 → Specification → Plan → Tasks → Implementation。ここでは確認された要件が最優先の権威となります。Confirmation Gate で明示的に確認されるまで、チェーン上のいかなる事項も確定しません。

### Review Commands (Quality Gates)

各ワークフロー段階のアーティファクトを、**エビデンスに基づくレビュー** 契約の下で検証するコマンド群です。すべての欠陥は具体的な `Evidence`、`Location`、`Mismatch`、`Impact`、`Remediation` を含まなければなりません。設計に関する助言（アドバイザリ）は別枠で報告され、ステータスを変更したり自動的な修正をトリガーすることはありません。検証された欠陥は最大 2 ラウンドまで修正して再レビューできます。助言は最後まで任意です。

### Enhancement Commands

反復的な洗練、アーティファクト間の検証、設定、プロジェクト管理ツールとの統合を行うコマンド群です。

### Git Workflow Commands

完成した作業を共有可能なアーティファクトに変換するコマンド群です。ステージ済み diff からのコミットメッセージと、ブランチ差分からの構造化された PR/MR 説明を生成します。

### Code Review Commands

ソースコード（任意言語、Python 専用、React/TypeScript 専用）を、慣用的表現の明確さ、正確性、堅牢性、アーキテクチャ、憲法整合性の観点からレビューするコマンド群です。発見事項はアーティファクトレビューと同じ重大度規律を採用しています。CRITICAL/HIGH の指摘は具体的エビデンスを引用し、LOW の提案は助言扱いです。

### Fast Track

小さく境界が明確な変更に対して、要件ファーストの SDD フローをエンドツーエンドで合理化して実行するコマンドです。

---

## Command Reference

### `/codexspec:constitution`

プロジェクト憲法を作成または更新します。憲法はアーキテクチャの原則、技術スタック、コード標準、ガバナンス規則を定義し、その後のすべての開発意思決定を導きます。

**Syntax:**

```
/codexspec:constitution [principles description]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `principles description` | No | 取り込む原則の説明（指定がない場合はプロンプトで尋ねられます） |

**What it does:**

- `.codexspec/memory/constitution.md` が存在しない場合は作成します
- 既存の憲法に新しい原則を反映して更新します
- テンプレートとのアーティファクト間整合性を検証します
- 変更点と影響を受けるファイルを示す Sync Impact Report を生成します
- 依存テンプレートに対する憲法適合性レビューを実施します

**What it creates:**

```
.codexspec/
└── memory/
    └── constitution.md    # プロジェクトガバナンス文書
```

**Example:**

```text
You: /codexspec:constitution Focus on code quality, testing standards, and clean architecture

AI:  Creating constitution...

     ✓ Created .codexspec/memory/constitution.md
     Version: 1.0.0

     Sync Impact Report:
     - plan-template-*.md: ✅ aligned
     - spec-template-*.md: ✅ aligned
     - tasks-template-*.md: ✅ aligned

     Core Principles:
     1. Code Quality First
     2. Test-Driven Development
     3. Clean Architecture

     Suggested commit: docs: create constitution v1.0.0
```

**Tips:**

- プロジェクトの早期に原則を定義すると、意思決定の一貫性が保たれます
- 技術面とプロセス面の両方の原則を盛り込みます
- 主要な機能開発を始める前に憲法を見直します
- 憲法の変更はアーティファクト間検証をトリガーします

---

### `/codexspec:specify`

対話型の Q&A を通じて要件を明確化し、得られた要約を確認したうえで、後のセッションに向けて保存します。

**Syntax:**

```
/codexspec:specify [your idea or requirement]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `your idea or requirement` | No | 構築したいものの初期説明（指定がない場合はプロンプトで尋ねられます） |

**What it does:**

- あなたのアイデアを理解するための明確化質問を投げかけます
- 想定していなかったエッジケースを探ります
- 対話を通じて高品質な要件を共同で作り上げます
- 技術的な実装ではなく「何を」「なぜ」に焦点を当てます
- 確認されたニーズ、制約、決定、対象外事項、未解決質問に安定した ID を割り当てます
- ユーザーの根拠と確認ログを記録します
- 機能ワークスペースと `requirements.md` を作成します

**What it creates:**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

確認された項目だけが権威ある要件になります。未解決の質問は明示的に未解決のまま残されます。これが要件に対する Confirmation Gate であり、最終的な要約を明示的に確認するまでは何も確定しません。

**Example:**

```text
You: /codexspec:specify I want to build a task management app

AI:  Great! Let me help you clarify the requirements.

     First, who are the target users for this app?
     - Individual professionals
     - Small teams
     - Enterprise organizations
     - All of the above

You: Small teams, mainly software development teams

AI:  Got it. For small dev teams:
     - Do you need real-time collaboration features?
     - Should tasks support sub-tasks or just flat lists?
     - Any integration requirements (GitHub, Slack, etc.)?

You: Real-time is important. Sub-tasks yes. GitHub integration would be nice.

AI:  [Continues exploring requirements...]

     Summary of clarified requirements:
     - Target: Small dev teams (5-20 people)
     - Core: Tasks with sub-tasks, real-time updates
     - Integration: GitHub (optional)
     - Priority: Real-time collaboration > Sub-tasks > GitHub

     Ready to generate the spec document?
     Use /codexspec:generate-spec to create spec.md
```

**Tips:**

- 初期の要件探索に活用します
- 完璧にまとめようと気にする必要はありません。洗練は反復的に進めます
- AI が前提を置いたと感じたら質問を投げかけます
- spec を生成する前に要約を確認します

---

### `/codexspec:generate-spec`

明確化された要件から `spec.md` を生成します。このコマンドは「要件コンパイラ」として機能し、明確化された要件を構造化された仕様書に変換します。

**Syntax:**

```
/codexspec:generate-spec
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| Feature path | No | 機能ディレクトリ、`requirements.md`、対象の `spec.md` のいずれかを明示的に指定します。解釈が曖昧な場合に必要です |

**What it does:**

- 選択した機能ワークスペースから確認された要件を読み取ります
- `spec.md` のみを含むレガシーワークスペースもサポートします（追跡可能性に関する警告付き）
- 包括的な `spec.md` を生成します。内容は以下のとおりです:
  - 機能の概要と目標
  - 受け入れ基準付きのユーザーストーリー
  - 機能要件（REQ-XXX 形式）
  - 非機能要件（NFR-XXX 形式）
  - エッジケースとその取り扱い
  - 対象外事項
- 要件 ID に遡る `Sources` 参照を付加します
- 権威の衝突を推測で解決せず、ユーザーの確認のために停止します
- 自動的にレビューを行い、エビデンスに基づく欠陥は最大 2 ラウンドまで修復する可能性があります

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**Example:**

```text
You: /codexspec:generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec:review-spec
     - Or proceed to /codexspec:spec-to-plan
```

**Tips:**

- `/codexspec:specify` で要件を明確化してから実行します
- 次に進む前に生成された spec をレビューします
- 品質検証には `/codexspec:review-spec` を使います
- わずかな調整であれば spec.md を直接編集します

---

### `/codexspec:clarify`

既存の仕様書をスキャンして曖昧さと抜けを検出します。初期の spec 作成後、反復的に洗練する際に使います。

**Syntax:**

```
/codexspec:clarify [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | spec ファイルのパス（指定がない場合は自動検出されます） |

**What it does:**

- 絞り込んだ曖昧さカテゴリを使って要件と spec をスキャンします
- 的を絞った明確化質問を投げかけます（最大 5 問）
- ユーザー確認後にまず `requirements.md` を更新し、その後 `spec.md` を同期します
- review-spec の指摘があればそれらも統合します

**Ambiguity Categories:**

| Category | What it Detects |
|----------|-----------------|
| **Completeness Gaps** | セクションの欠落、空の内容、受け入れ基準の不在 |
| **Specificity Issues** | 曖昧な表現（"fast"、"scalable" など）、未定義の制約 |
| **Behavioral Clarity** | エラー処理の抜け、未定義の状態遷移 |
| **Measurability Problems** | 計測基準のない非機能要件 |

**Example:**

```text
You: /codexspec:clarify

AI:  Scanning spec.md for ambiguities...

     Found issues in 3 categories.

     ## Question 1/5: Specificity

     **Context**: NFR-001 states "System should respond quickly"

     **Question**: What is the target response time?

     | Option | Description | Impact |
     |--------|-------------|--------|
     | A | < 100ms for all operations | High performance requirement |
     | B | < 500ms for reads, < 1s for writes | Balanced approach |
     | Custom | Provide a different answer | - |

     **Recommendation**: Option B - balanced for typical web app

You: B

AI:  ✓ Updated NFR-001: Response time < 500ms reads, < 1s writes
     Added to Clarifications section in spec.md
```

**Tips:**

- spec.md は存在するものの洗練が必要なときに使います
- `/codexspec:review-spec` の指摘を統合します
- 1 セッションあたり最大 5 問です
- 複雑な仕様書では複数回実行します

---

### `/codexspec:spec-to-plan`

機能の仕様書を技術的な実装計画に変換します。ここでは機能を **どのように** 構築するかを定義します。

**Syntax:**

```
/codexspec:spec-to-plan [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | spec ファイルのパス（指定がない場合は `.codexspec/specs/` から自動検出されます） |

**What it does:**

- 仕様書と憲法を読み取ります
- 確認された要件とリポジトリの制約によって必要な技術的詳細だけを盛り込みます
- 該当する憲法ルールを確認しますが、任意の慣習を機能要件としては扱いません
- 仕様書の要件への `Covers` リンクを追加します
- 技術的な決定とその根拠を文書化します
- 決定が確認された意図を変える場合は停止します

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # 技術的な実装計画
```

**Example:**

```text
You: /codexspec:spec-to-plan Use Python FastAPI for backend, React for frontend, PostgreSQL for database

AI:  Generating technical plan...

     Constitutionality Review:
     ✓ Clean Architecture: Modular design with clear boundaries
     ✓ TDD: Test-first approach enforced in phases
     ✓ Code Quality: Linting and type hints required

     Architecture:
     - Backend: FastAPI with layered architecture
     - Frontend: React with component structure
     - Database: PostgreSQL with migration strategy

     Module Dependency Graph:
     ┌─────────────┐
     │    API      │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Services   │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │    Data     │
     └─────────────┘

     ✓ Created plan.md
     5 Implementation Phases defined
```

**Tips:**

- spec をレビューして安定させてから実行します
- 該当する憲法ルールは必須ですが、無関係なテンプレート慣習は必須ではありません
- プロジェクトの種類に応じて関連するセクションを盛り込みます
- タスクに進む前に計画をレビューします

---

### `/codexspec:plan-to-tasks`

技術計画を実行可能なタスクに分割し、明示的なカバレッジと検証可能な成果物を設定します。

**Syntax:**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `paths` | No | spec と plan のパス（指定がない場合は自動検出されます） |

**What it does:**

- 検証可能な成果物を 1 つ持つタスクを作成します。1 つのタスクが密接に関連する複数ファイルを扱うこともあります
- 計画、憲法、確認されたニーズ、リスクによってテストファーストが要求される場合にのみ、その順序を採用します
- 真に独立している場合にのみタスクに `[P]` を付与します
- 各タスクの正確なファイルパスを指定します
- 計画や要件 ID への `Covers` リンクを追加します

**What it creates:**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # タスク分割
```

**Task Structure:**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**Example:**

```text
You: /codexspec:plan-to-tasks

AI:  Breaking down plan into tasks...

     ✓ Created tasks.md
     Total: 24 tasks
     Parallelizable: 8 tasks (33%)

     Phase 1: Foundation (4 tasks)
     Phase 2: Core Implementation - TDD (10 tasks)
     Phase 3: Integration (4 tasks)
     Phase 4: Interface Layer (3 tasks)
     Phase 5: Testing & Documentation (3 tasks)

     Execution Order:
     Phase 1 → [Phase 2 tasks in parallel groups] → Phase 3 → Phase 4 → Phase 5

     Checkpoints defined at each phase boundary.
```

**Tips:**

- 各タスクは検証可能な 1 つの成果物を生み出すべきで、密接に関連するファイルを扱っても構いません
- テストタスクが実装より先になるのはテストファーストが要求される場合のみです
- `[P]` は真に独立して並列化可能なタスクを示します
- 実装に入る前に依存関係をレビューします

---

### `/codexspec:implement-tasks`

条件付き TDD ワークフローで実装タスクを実行します。タスクリストを体系的に進めます。

**Syntax:**

```
/codexspec:implement-tasks [tasks_path]
/codexspec:implement-tasks [spec_path plan_path tasks_path]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `tasks_path` | No | tasks.md のパス（指定がない場合は自動検出されます） |
| `spec_path plan_path tasks_path` | No | 3 つの文書のパスを明示的に指定します |

**File Resolution:**

- **引数なし**: `.codexspec/specs/` から自動検出します
- **引数 1 つ**: `tasks.md` のパスとみなし、それ以外は同じディレクトリから推論します
- **引数 3 つ**: spec.md、plan.md、tasks.md への明示的なパスです

**What it does:**

- tasks.md を読み込み、未完了のタスクを特定します
- コードタスクに TDD ワークフローを適用します:
  - **Red**: まず失敗するテストを書きます
  - **Green**: テストを通るように実装します
  - **Verify**: すべてのテストを実行します
  - **Refactor**: テストを通したまま改善します
- テスト不可能なタスク（ドキュメント、設定）は直接実装します
- 進捗に合わせてタスクのチェックボックスを更新します
- ブロッカーが発生した場合は issues.md に記録します

**TDD Workflow for Code Tasks:**

```
Red → Green → Verify → Refactor → Mark Complete
```

**Direct Implementation for Non-Testable:**

- ドキュメントファイル
- 設定ファイル
- 静的アセット
- インフラファイル

**Example:**

```text
You: /codexspec:implement-tasks

AI:  Starting implementation...

     Loading context:
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     Tech Stack: Python 3.11+ / FastAPI / PostgreSQL / pytest

     Working on Task 1.1: Setup Project Structure
     ✓ Created src/taskman/__init__.py
     ✓ Created pyproject.toml
     [x] Task 1.1 Complete

     Working on Task 2.1: Write Tests for Task Entity [P]
     ✓ Created tests/test_task.py
     Running tests... 5 passed (all expected failures)
     [x] Task 2.1 Complete

     Working on Task 2.2: Implement Task Entity
     ✓ Created src/taskman/models/task.py
     Running tests... 5 passed
     [x] Task 2.2 Complete

     ...
```

**Tips:**

- 途中で中断しても続きから再開できます
- ブロッカーは issues.md に記録されます
- 意義のあるタスクやフェーズの節目でコミットされます
- 検証を済ませてから `/codexspec:review-tasks` を先に実行してください

---

### `/codexspec:review-spec`

仕様書を、確認された要件との整合性および仕様書自身の内部品質の両面から検証します。

**Syntax:**

```
/codexspec:review-spec [path_to_spec.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_spec.md` | No | spec ファイルのパス（指定がない場合は自動検出されます） |

**What it does:**

- 確認された `requirements.md` の各項目に対する忠実性を確認します
- 内部的一貫性、明確さ、検証可能性を確認します
- 権威ある内容が必要とする場合に限り、テンプレートセクションの欠落を欠陥として扱います
- 各欠陥に `Evidence`、`Location`、`Mismatch`、`Impact`、`Remediation` を含めることを要求します
- `Risk Advisories / Design Opportunities` を欠陥と分けて報告します
- ステータスと、分類された指摘から導出される互換性スコアを生成します

**Shared review contract:**

| Category | Meaning |
|----------|---------|
| Fidelity defect | 権威あるソースと衝突する、あるいは権威あるソースを漏らしているもの |
| Intrinsic defect | 内部的に矛盾している、実行不可能、または検証不可能なもの |
| Advisory | 現時点で欠陥のエビデンスを伴わない、任意の改善提案 |

ステータスは `PASS`、`PASS_WITH_WARNINGS`、`NEEDS_REVISION`、`BLOCKED` のいずれかです。助言はステータスやスコアを変更しません。

**Example:**

```text
You: /codexspec:review-spec

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning SPEC-001
     Evidence: CON-002 requires a measurable response-time limit.
     Location: spec.md, REQ-006
     Mismatch: "Respond quickly" has no measurable threshold.
     Impact: Acceptance cannot be verified.
     Remediation: Ask the user to confirm a threshold, update requirements.md,
                  then synchronize REQ-006.

     Risk Advisories / Design Opportunities:
     - None
```

**Tips:**

- `/codexspec:spec-to-plan` の前に実行します
- `BLOCKED` と `NEEDS_REVISION` は先に進める準備ができていない合図とみなします
- 助言を要件に昇格させないようにします
- 修正後にもう一度実行します

---

### `/codexspec:review-plan`

技術的な実装計画を、忠実性、実現可能性、技術的決定の妥当性の観点からレビューします。

**Syntax:**

```
/codexspec:review-plan [path_to_plan.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_plan.md` | No | plan ファイルのパス（指定がない場合は自動検出されます） |

**What it does:**

- `Covers` リンクと、仕様書の必要なカバレッジを検証します
- 該当する憲法ルールとリポジトリの事実を確認します
- 具体的なコストや衝突を生む場合に限り、根拠のない複雑さを指摘します
- 各欠陥にエビデンス欄を必須とし、同じ根本原因を持つ指摘はマージします
- 任意のアーキテクチャ改善は助言として報告します
- 共通のステータス・互換性スコア契約を使用します

**Example:**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**Tips:**

- `/codexspec:plan-to-tasks` の前に実行します
- エビデンスに基づく欠陥はタスク生成の前に解消します
- 投機的なアーキテクチャのアイデアは助言セクションに留めます
- 技術スタックがチームのスキルに合致しているか確認します

---

### `/codexspec:review-tasks`

タスク分割を、カバレッジ、検証可能な成果物、正しい順序付け、実現可能な依存関係の観点から検証します。

**Syntax:**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path_to_tasks.md` | No | tasks ファイルのパス（指定がない場合は自動検出されます） |

**What it does:**

- すべての必要な計画項目と要件がタスクでカバーされているか確認します
- 権威あるソースが要求する場合にのみ、テストファーストの順序付けを検証します
- 各タスクが確認可能な 1 つの成果物を持つことを検証します
- 依存関係を検証します（循環なし、正しい順序）
- 並列化マーカーをレビューします
- ファイルパスを検証します
- 各欠陥にエビデンス欄を必須とします
- 任意のプロセス改善は助言として報告します
- 共通のステータス・互換性スコア契約を使用します

**Example:**

```text
You: /codexspec:review-tasks

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning TASK-001
     Evidence: Task 2.5 declares a dependency on Task 2.4.
     Location: tasks.md, Task 2.5
     Mismatch: Task 2.5 is also marked [P].
     Impact: Parallel execution can start before its prerequisite completes.
     Remediation: Remove [P] or remove the dependency if the plan proves independence.
```

**Tips:**

- `/codexspec:implement-tasks` の前に実行します
- テスト順序に関する指摘は、権威あるソースがテストを要求している場合にのみ欠陥になります
- 並列化マーカーが正確か確認します
- ファイルパスがプロジェクト構造と一致するか確認します

---

### `/codexspec:analyze`

requirements.md、spec.md、plan.md、tasks.md にまたがる、非破壊的な整合性分析を実行します。権威の衝突、トレーサビリティの抜け、重複、カバレッジの欠落を特定します。

**Syntax:**

```
/codexspec:analyze
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| None | - | 現在の機能のアーティファクトを分析します |

**What it does:**

- アーティファクト間の重複を検出します
- 計測可能な基準を欠く曖昧さを特定します
- 記述が不十分な項目を検出します
- 憲法との整合性を確認します
- 要件からタスクへのカバレッジをマッピングします
- 用語や順序の不整合を報告します

**Severity Levels:**

| Level | Definition |
|-------|------------|
| **CRITICAL** | 憲法違反、中核アーティファクトの欠落、カバレッジ皆無 |
| **HIGH** | 重複・衝突する要件、曖昧なセキュリティ属性 |
| **MEDIUM** | 用語の揺れ、非機能要件のカバレッジ欠如 |
| **LOW** | スタイル・表現の改善 |

**Example:**

```text
You: /codexspec:analyze

AI:  Analyzing artifacts...

     # Specification Analysis Report

     ## Coverage Summary
     | Requirement Key | Has Task? | Task IDs |
     |-----------------|-----------|----------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | None |

     ## Issues Found

     | ID | Category | Severity | Summary |
     |----|----------|----------|---------|
     | A1 | Coverage | CRITICAL | REQ-003 has no task coverage |
     | A2 | Duplication | HIGH | REQ-005 and REQ-008 overlap |
     | A3 | Ambiguity | MEDIUM | NFR-002 "secure" not defined |

     ## Metrics
     - Total Requirements: 12
     - Total Tasks: 24
     - Coverage: 92% (11/12 requirements)
     - Critical Issues: 1

     ## Next Actions
     1. Add tasks for REQ-003 (CRITICAL)
     2. Consider merging REQ-005 and REQ-008
     3. Define "secure" in NFR-002

     Resolve CRITICAL issues before /codexspec:implement-tasks
```

**Tips:**

- `/codexspec:plan-to-tasks` の後、実装の前に実行します
- CRITICAL の指摘は実装をブロックすべきです
- 読み取り専用の分析であり、ファイルは変更されません
- 指摘をアーティファクトの品質向上に活用します

---

### `/codexspec:checklist`

要件の完全性、明確さ、一貫性を検証するための品質チェックリストを生成します。これは「要件記述のためのユニットテスト」のようなものです。

**Syntax:**

```
/codexspec:checklist [focus_area]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `focus_area` | No | ドメインの焦点（例: "ux"、"api"、"security"、"performance"） |

**What it does:**

- 品質の次元ごとに整理されたチェックリストを生成します
- `FEATURE_DIR/checklists/` ディレクトリにチェックリストを作成します
- 項目は実装のテストではなく、要件の品質に焦点を当てます

**Quality Dimensions:**

- **Requirement Completeness**: 必要な要件がすべて揃っているか?
- **Requirement Clarity**: 要件は具体的で曖昧さがないか?
- **Requirement Consistency**: 要件同士に衝突はないか?
- **Acceptance Criteria Quality**: 成功基準は計測可能か?
- **Scenario Coverage**: すべてのフローやケースが扱われているか?
- **Edge Case Coverage**: 境界条件が定義されているか?
- **Non-Functional Requirements**: パフォーマンス、セキュリティ、アクセシビリティは明記されているか?
- **Dependencies & Assumptions**: それらは文書化されているか?

**Example Checklist Types:**

- `ux.md` - 視覚的階層、インタラクション状態、アクセシビリティ
- `api.md` - エラー形式、レート制限、認証
- `security.md` - データ保護、脅威モデル、侵害対応
- `performance.md` - メトリクス、負荷条件、劣化

**Example:**

```text
You: /codexspec:checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

     ## Security Requirements Quality Checklist

     ### Authentication Requirements
     - [ ] CHK001 - Are authentication requirements defined for all protected endpoints? [Completeness]
     - [ ] CHK002 - Is password complexity explicitly specified? [Clarity]
     - [ ] CHK003 - Are session timeout requirements quantified? [Measurability]

     ### Data Protection
     - [ ] CHK004 - Are data encryption requirements specified at rest? [Completeness]
     - [ ] CHK005 - Are data encryption requirements specified in transit? [Completeness]
     - [ ] CHK006 - Is PII handling explicitly documented? [Clarity]

     Total: 15 items across 4 categories
```

**Tips:**

- チェックリストは実装の正しさではなく要件の品質を検証します
- 要件のレビューや改善に活用します
- 焦点を絞った検証のためにドメイン別のチェックリストを作成します
- 技術計画に進む前に実行します

---

### `/codexspec:tasks-to-issues`

`tasks.md` のタスクを GitHub Issues に変換し、プロジェクトの追跡と協業に役立てます。

**Syntax:**

```
/codexspec:tasks-to-issues
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| None | - | 現在の機能の全タスクを変換します |

**What it does:**

- タスク ID、説明、依存関係、ファイルパスを解析します
- 構造化された本文を持つ GitHub Issue を作成します
- タスク種別（セットアップ、実装、テスト、ドキュメント）に基づいてラベルを付与します
- Issue 間で依存関係をリンクします
- 作成した Issue を URL 付きで報告します

**Prerequisites:**

- GitHub リモートを持つ Git リポジトリ
- GitHub CLI (`gh`) がインストール済みで認証済みであること
- `tasks.md` ファイルが存在すること

**Example:**

```text
You: /codexspec:tasks-to-issues

AI:  Converting tasks to GitHub issues...

     Repository: github.com/example/taskman

     Creating issues:
     ✓ #42: Task 1.1 - Setup Project Structure (setup)
     ✓ #43: Task 2.1 - Write Tests for Task Entity (testing)
     ✓ #44: Task 2.2 - Implement Task Entity (implementation)
     ...

     Summary:
     - Issues created: 24
     - Labels applied: setup(4), implementation(12), testing(5), documentation(3)
     - Dependencies linked: 18

     View issues: https://github.com/example/taskman/issues
```

**Tips:**

- GitHub CLI の認証が必要です（`gh auth login`）
- GitHub リポジトリでのみ動作します
- リポジトリのデフォルト設定で Issue を作成します
- 実行前に重複がないか確認します

---

### `/codexspec:commit-staged`

ステージ済みの git 変更をもとに、セッションのコンテキストを理解した上で Conventional Commits に準拠したコミットメッセージを生成します。

**Syntax:**

```
/codexspec:commit-staged [-p]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `-p` | No | プレビューモード。コミットせずにメッセージだけを表示します |

**What it does:**

- `git diff --staged` を実行してステージ済みの変更を取得します
- 変更内容とセッションコンテキストを分析して意図を把握します
- Conventional Commits の仕様に従います
- 実行モード（デフォルト）では、メッセージ生成後に直接コミットします
- プレビューモード（`-p`）では、コミットせずにメッセージだけを表示します
- ステージ済み変更がない場合はエラーを報告します

**Example:**

```text
You: /codexspec:commit-staged

AI:  Analyzing staged changes...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Generated commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Executing commit...

     ✓ Committed: def5678
```

**Preview Mode Example:**

```text
You: /codexspec:commit-staged -p

AI:  Preview mode - no commit will be executed

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow
```

**Tips:**

- 事前に `git add` で変更をステージします
- ステージされた内容だけを解析し、Git の 2 段階コミットワークフローを尊重します
- 意味のあるコミットメッセージのためにセッションコンテキストを考慮します
- コミット前に確認するには `-p` フラグを使います
- デフォルトで Conventional Commits の仕様に従います

---

### `/codexspec:review-code`

任意の言語のコードを、慣用的表現の明確さ、正確性、堅牢性、アーキテクチャ、憲法整合性の観点からレビューします。

**Syntax:**

```
/codexspec:review-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | レビュー対象のソースファイルまたはディレクトリを 1 つ以上（スペース区切り）。省略時は `src/` |

**What it does:**

- 拡張子から主要言語を検出し、複数言語が混在する対象では言語別のパスを実行します
- 設定が存在する場合に静的解析ツールを実行します（`ruff`/`mypy`、`eslint`/`tsc`、`go vet`/`gofmt`、`cargo check`/`cargo clippy`、`shellcheck`）。ない場合は妥当にスキップし、カバレッジ低下を報告します
- 4 つの次元を採点します: 慣用的表現の明確さと簡潔さ、正確性と明示的契約、実行時の堅牢性とリソース規律、アーキテクチャと設計の完全性
- 検出したフレームワーク向けの必須サブセクションを挿入します（例: React の場合は Hooks Compliance、Rust の場合は Ownership & Borrowing、Go の場合は Goroutine & Context Discipline、C/C++ の場合は Memory & Lifetime Safety、Shell の場合は Execution Safety）
- `.codexspec/memory/constitution.md` が存在する場合は指摘をそれと照合します。ない場合は憲法軸を除外し、その重みを再配分します
- 指摘を重大度で分類します: CRITICAL、HIGH、MEDIUM、LOW（LOW の提案は合計 5 点の減点上限付き）

**Example:**

```text
You: /codexspec:review-code src/

AI:  # Code Review Report

     ## Summary
     - Overall Status: Needs Work
     - Quality Score: 78/100
     - Detected Language: Python

     ## Static Analysis Results
     | Tool   | Status | Issues | Details                |
     |--------|--------|--------|------------------------|
     | ruff   | Warn   | 3      | Unused imports, line length |
     | mypy   | Pass   | 0      | No type errors         |

     ## Detailed Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/auth/service.py:42 - bare `except Exception:` swallows the original cause
       Impact: Original error context is lost during debugging.
       Suggestion: narrow the exception and re-raise with `raise ... from err`.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/auth/service.py:120 - manual loop where a comprehension suffices

     ## Recommendations
     1. Priority 1: Fix CODE-001 before merge.
     2. Priority 2: Apply LOW suggestions opportunistically.
```

**Tips:**

- 複数のパスを渡すことで範囲を絞ってレビューできます。例: `src/ tests/`
- スコアはあくまで助言です。CRITICAL/HIGH の指摘が実行すべきシグナルです
- Python のみ、または React のみのプロジェクトでは、より深い言語特有のチェックができる `/codexspec:review-python-code` や `/codexspec:review-react-code` を使うのが望ましいです
- 修正後に再実行してスコアの回復を確認します（CRITICAL/HIGH が解消されれば 95 以上を期待できます）

---

### `/codexspec:review-python-code`

Python コードを、PEP 8 準拠、型安全性、エンジニアリングの堅牢性、憲法整合性の観点からレビューします。

**Syntax:**

```
/codexspec:review-python-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | レビュー対象の Python ファイルまたはディレクトリを 1 つ以上（スペース区切り）。省略時は `src/` |

**What it does:**

- PEP 8 / リント結果として `ruff check` を、型チェック結果として `mypy` を実行します
- Python 固有の 4 つの次元をレビューします: Pythonic と KISS の原則、型安全性と明示性、エンジニアリングの堅牢性、憲法整合性
- 型注釈の完全性、広すぎる例外処理、`raise ... from err` によるコンテキスト保存を確認します
- リソース管理（`with` コンテキストマネージャ）、async/await の正確性、構造化 `logging` の規律を検証します
- `.codexspec/memory/constitution.md` の MUST/SHOULD 原則が存在する場合は指摘をそれと照合します
- 指摘を重大度で分類します: CRITICAL（憲法 MUST 違反、ロジックバグ、セキュリティ脆弱性）、HIGH（型安全性の欠如、ruff/mypy エラー、リソースリーク）、MEDIUM（設計/リファクタの機会、注釈の欠落）、LOW（可読性、Pythonic な表現）

**Example:**

```text
You: /codexspec:review-python-code src/codexspec/

AI:  # Python Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | ruff  | Pass   | 0      |
     | mypy  | Pass   | 0      |

     ## Findings
     ### Warnings (HIGH)
     - [ ] [CODE-002] src/codexspec/__init__.py:218 - public function missing return type annotation
       Suggestion: add the return type and verify with mypy.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/codexspec/cli.py:140 - use `pathlib.Path` instead of `os.path` string concatenation
```

**Tips:**

- 対象が Python のみで PEP 8 / 型安全性の深さが欲しい場合は `/codexspec:review-code` の代わりに使います
- 完全なカバレッジのためには `ruff` と `mypy` が対象プロジェクトにインストール・設定されている必要があります。ない場合はカバレッジ低下を報告します
- 憲法の MUST 原則は採点対象です。憲法がない場合は、言語に依存しないメタ原則（テスト容易性、簡潔性）が適用されます

---

### `/codexspec:review-react-code`

React/TypeScript コードを、コンポーネントアーキテクチャ、Hooks 規則、状態管理、パフォーマンス、憲法整合性の観点からレビューします。

**Syntax:**

```
/codexspec:review-react-code [path...]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `path...` | No | レビュー対象の React/TypeScript ファイルまたはディレクトリを 1 つ以上（スペース区切り、`.tsx`、`.ts`、`.jsx`、`.js` を想定）。省略時は `src/` |

**What it does:**

- ESLint 設定が存在する場合は `npx eslint` を、`tsconfig.json` が存在する場合は `npx tsc --noEmit` を実行します
- React 固有の 4 つの次元をレビューします: コンポーネントの原子性と単一責任、Hooks 規則と副作用管理、状態管理とデータフロー、パフォーマンスと堅牢性
- `useEffect` の依存配列が網羅的かを検証し、導出値を `state` として保持する誤用を検出し、不要なエフェクトにフラグを立てます
- 古いクロージャのリスク、エフェクトのクリーンアップ欠如、プロップドリリング、メモ化されていないコストの高いレンダリング、ローディング/エラー状態の欠落を確認します
- `.codexspec/memory/constitution.md` が存在する場合は指摘をそれと照合します
- 指摘を重大度で分類します: CRITICAL（Hooks 規則違反、競合状態）、HIGH（クリーンアップの欠落、未処理の Promise リジェクト）、MEDIUM（リファクタ候補）、LOW（可読性）

**Example:**

```text
You: /codexspec:review-react-code src/components/

AI:  # React Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | eslint| Warn   | 2      |
     | tsc   | Pass   | 0      |

     ## Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/components/UserProfile.tsx:38 - `useEffect` missing `userId` in dependency array
       Impact: stale closure fetches the wrong user after navigation.
       Suggestion: add `userId` to the dependency array or extract to a custom hook.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/components/Button.tsx:12 - extract derived value instead of `useState`
```

**Tips:**

- 対象が React/TypeScript のみで Hooks / コンポーネントアーキテクチャの深さが欲しい場合は `/codexspec:review-code` の代わりに使います
- 完全なカバレッジのためには ESLint と `tsconfig.json` が存在する必要があります。ない場合はカバレッジ低下を報告します
- React の指摘はベースとなる TypeScript チェックの上に重ねられるため、型安全性の問題も検出されます

---

### `/codexspec:quick`

小さな変更向けに、要件ファーストの SDD フローを合理化して実行します。

**Syntax:**

```
/codexspec:quick [describe a small requirement]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `describe a small requirement` | No | 小さく境界が明確な変更の短い説明（指定がない場合はプロンプトで尋ねられます） |

**What it does:**

- スコープ（触れるファイル、モジュールの広がり、新規依存、未解決のプロダクト決定）を評価し、変更が広範あるいは複数の独立した成果物を持つ場合は標準フローを推奨します
- `/codexspec:specify` と同じタイムスタンプ規約で機能ワークスペースと `requirements.md` を作成します
- 実装に実質的な影響を与える曖昧さだけを解消し、簡潔な確認済み要約（`NEED-*`、関連する `CON-*`/`DEC-*`、`OUT-*`、未解決の `OPEN-*`）を提示します
- Confirmation Gate で止まります。要約を確認するまでは何も生成しません
- 新しい機能ディレクトリに対して生成コマンドを連鎖させます: `/codexspec:generate-spec`、`/codexspec:spec-to-plan`、`/codexspec:plan-to-tasks`、`/codexspec:implement-tasks`
- 各生成コマンド自身の自動レビューループに委ねます。レビューが新たなプロダクトやアーキテクチャの決定を必要とする場合は一時停止してユーザーに尋ねます
- 機能ディレクトリ、アーティファクトのパス、レビュー結果、実装の検証結果、未解決の助言は別個に報告します

**What it creates:**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**Example:**

```text
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → spec-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**Tips:**

- Quick は本当に小さく単一の成果物を持つ変更のためにとっておきます。そうでなければ `/codexspec:specify` と標準フローを走らせます
- 確認は依然として必須です。Quick は自動化を進めるためにプロダクトの決定を推測することはありません
- いずれかの生成レビューが `NEEDS_REVISION`/`BLOCKED` を返した場合、Quick は停止して制御をユーザーに戻します

---

### `/codexspec:pr`

git diff から、構造化された GitHub Pull Request / GitLab Merge Request の説明を生成します。オプションで `spec.md` を統合し、SDD で追跡可能なコンテキストを盛り込むことができます。

**Syntax:**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--target-branch <branch>` | No | 比較対象のブランチ（デフォルト: `origin/main`） |
| `--sections <list>` | No | `summary, changes, testing, verify, checklist, notes` のカンマ区切り部分集合（デフォルト: `all`） |
| `--spec <id-or-path>` | No | 任意の spec 統合: 機能 ID（例: `2025-0321-1430k7-auth`、`.codexspec/specs/` 配下で解決）、または明示的な `path/to/spec.md`。省略時は git のみから生成します |
| `--output <file>` | No | 説明を端末ではなくファイルに保存します |

**What it does:**

- ターゲットブランチに対して git コンテキスト（現在のブランチ、リモート URL、先行コミット数、ファイル変更、完全な diff、コミットメッセージ）を収集します
- リモート URL からプラットフォームを自動検出します: GitHub → "Pull Request"、GitLab → "Merge Request"、その他/なし → GitHub の用語をデフォルトとし警告を出します
- `.codexspec/memory/constitution.md` が存在する場合は読み込み、ドキュメント/コードレビューの基準に説明を合わせます
- 説明の言語は `language.commit`（次に `language.output`、次に英語）を尊重します。技術用語（API、JWT、PR、MR）は適宜英語のまま残します
- `--spec` が指定された場合は、spec.md からユーザーストーリーと要件を取り出した Context セクションを追加します。それ以外は diff のみから生成します
- `--sections` に従ってセクションを出力します（Summary、Changes、Testing、Verification Steps、Pre-merge Checklist、Notes / Breaking Changes）

**Example:**

```text
You: /codexspec:pr --spec 2026-0613-1200ab-task-management

AI:  Generating Pull Request description...

     Platform: GitHub (github.com/example/taskman)
     Branch:   feature/task-management  →  origin/main
     Commits:  8 ahead

     ## Pull Request: Task management for small dev teams

     ### Context
     - User stories and REQ-* pulled from spec.md

     ### Summary
     - Adds task CRUD, sub-tasks, and real-time updates

     ### Changes
     - src/taskman/models/task.py (new)
     - src/taskman/api/tasks.py (new)
     - ...

     ### Verification Steps
     1. `uv run pytest`
     2. `uv run codexspec check`
```

**Tips:**

- 形式化された仕様書を持たない小さなバグ修正や変更では `--spec` を省略します
- `/codexspec:commit-staged` と組み合わせれば、同じ作業からコミットメッセージと PR 説明をまとめて生成できます
- このコマンドのエンドツーエンドの実例（spec.md のコンテキストをどう組み込むかを含む）は [PR description generator case study](../case-studies/case-study-pr-description-generator.md) を参照してください

---

### `/codexspec:config`

プロジェクト設定を対話的に管理します（作成/参照/変更/リセット）。これは `codexspec config` CLI のスラッシュコマンド版であり、Plugin Marketplace 経由でインストールした環境に適しています。

**Syntax:**

```
/codexspec:config [--view]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--view` | No | 現在の設定を変更せずに表示します。引数なしの場合は対話型管理メニューを開きます |

**What it does:**

- `.codexspec/config.yml` のみを対象とします
- `--view`（またはメニューの "View current config"）はファイルを読みやすい形式で表示します。存在しない場合は "Configuration Not Found" と報告します
- 設定が存在する場合の対話モードでは View、Modify、Reset to defaults、Cancel を提供します
- 設定が存在しない場合は作成フローを走らせ、`output` だけの最小設定を書き出します（interaction/document/commit は `output`、次に `en` に解決されるため、`output` だけのファイルでも完全に機能します）
- 各言語の次元（output、interaction、document、commit）を個別に設定でき、`auto_next` などのワークフローオプションも切り替えられます

**What it creates/edits:**

```
.codexspec/config.yml
```

**Example:**

```text
You: /codexspec:config

AI:  ## Configuration Manager

     Configuration file found at .codexspec/config.yml.
     What would you like to do?
     - View current config
     - Modify config
     - Reset to defaults
     - Cancel

You: Modify config

AI:  Select a dimension to change:
     - Output language (base)
     - Interaction language
     - Document language
     - Commit-message language
     - workflow.auto_next

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**Tips:**

- 何かを変更する前に `/codexspec:config --view` で現在の状態を確認します
- 新規作成やリセット時には `output` だけを書き出します。`output` と異なる値にしたい場合にのみ `interaction`/`document` を設定します
- 端末でスクリプト的に変更する場合は `codexspec config` CLI（`--set-lang`、`--set-interaction-lang`、`--set-document-lang`、`--set-commit-lang`、`--auto-next`）を使うのが適しています

---

## Workflow Overview

```text
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

各レビューは人間によるチェックポイントです。エビデンスに基づく指摘を用いて忠実性と本質的な品質を検証します。設計に関する助言は別枠であり、進行をブロックすることはありません。検証された欠陥は最大 2 ラウンドまで修正して再レビューできます。

---

## Troubleshooting

### "Feature directory not found"

コマンドが機能ディレクトリを見つけられませんでした。

**Solutions:**

- まず `codexspec init` を実行してプロジェクトを初期化します
- `.codexspec/specs/` ディレクトリが存在するか確認します
- 正しいプロジェクトディレクトリにいるか確認します
- 複数の候補がある場合は、機能ディレクトリやアーティファクトのパスを明示的に渡します

### "No spec.md found"

仕様書ファイルがまだ存在しません。

**Solutions:**

- まず `/codexspec:specify` を実行して要件を明確化します
- その後 `/codexspec:generate-spec` を実行して spec.md を作成します

### "Constitution not found"

プロジェクト憲法が存在しません。

**Solutions:**

- `/codexspec:constitution` を実行して作成します
- 憲法は任意ですが、意思決定の一貫性のために推奨されます

### "Tasks file not found"

タスク分割が存在しません。

**Solutions:**

- まず `/codexspec:spec-to-plan` を実行済みであることを確認します
- その後 `/codexspec:plan-to-tasks` を実行して tasks.md を作成します

### "GitHub CLI not authenticated"

`/codexspec:tasks-to-issues` コマンドは GitHub 認証が必要です。

**Solutions:**

- GitHub CLI をインストールします: `brew install gh`（macOS）または同等のコマンド
- 認証します: `gh auth login`
- 確認します: `gh auth status`

---

## Next Steps

- [Workflow](workflow.md) - よくあるパターンと各コマンドを使うタイミング
- [CLI](../reference/cli.md) - プロジェクト初期化のためのターミナルコマンド
