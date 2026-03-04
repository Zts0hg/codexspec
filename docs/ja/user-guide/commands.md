# コマンド

これは CodexSpec のスラッシュコマンドのリファレンスです。これらのコマンドは Claude Code のチャットインターフェースで呼び出されます。

各コマンドをいつ使用するかについては、[ワークフロー](workflow.md) を参照してください。CLI コマンドについては、[CLI](../reference/cli.md) を参照してください。

## クイックリファレンス

| コマンド | 目的 |
|---------|---------|
| `/codexspec.constitution` | プロジェクト憲法を作成または更新（クロスアーティファクト検証付き） |
| `/codexspec.specify` | インタラクティブな Q&A で要件を明確化 |
| `/codexspec.generate-spec` | 明確化された要件から spec.md ドキュメントを生成 |
| `/codexspec.clarify` | 既存の仕様をスキャンして曖昧さを発見（反復的な改善） |
| `/codexspec.spec-to-plan` | 仕様を技術実装計画に変換 |
| `/codexspec.plan-to-tasks` | 計画をアトミックで TDD 適用のタスクに分解 |
| `/codexspec.implement-tasks` | 条件付き TDD ワークフローでタスクを実行 |
| `/codexspec.review-spec` | 仕様の完全性と品質を検証 |
| `/codexspec.review-plan` | 技術計画の実現可能性と整合性をレビュー |
| `/codexspec.review-tasks` | タスク分解の TDD 準拠を検証 |
| `/codexspec.analyze` | クロスアーティファクト一貫性分析（読み取り専用） |
| `/codexspec.checklist` | 要件品質チェックリストを生成 |
| `/codexspec.tasks-to-issues` | タスクを GitHub issues に変換 |
| `/codexspec.commit` | セッションコンテキスト付きの Conventional Commits メッセージを生成 |
| `/codexspec.commit-staged` | ステージングされた変更からコミットメッセージを生成 |

---

## コマンドカテゴリ

### コアワークフローコマンド

主要な SDD ワークフロー用のコマンド: 憲法 → 仕様 → 計画 → タスク → 実装。

### レビューコマンド（品質ゲート）

各ワークフロー段階でアーティファクトを検証するコマンド。**次の段階に進む前に推奨されます。**

### 拡張コマンド

反復的な改善、クロスアーティファクト検証、プロジェクト管理統合用のコマンド。

---

## コマンドリファレンス

### `/codexspec.constitution`

プロジェクト憲法を作成または更新します。憲法は、すべての後続の開発決定を導くアーキテクチャ原則、技術スタック、コード標準、ガバナンスルールを定義します。

**構文:**
```
/codexspec.constitution [principles description]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `principles description` | いいえ | 含める原則の説明（指定されていない場合はプロンプトが表示されます） |

**動作:**
- 存在しない場合、`.codexspec/memory/constitution.md` を作成
- 既存の憲法を新しい原則で更新
- テンプレートとのクロスアーティファクト一貫性を検証
- 変更と影響を受けるファイルを示す同期影響レポートを生成
- 依存テンプレートの憲法準拠レビューを含む

**作成されるもの:**
```
.codexspec/
└── memory/
    └── constitution.md    # プロジェクトガバナンスドキュメント
```

**例:**
```text
You: /codexspec.constitution Focus on code quality, testing standards, and clean architecture

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

**ヒント:**
- プロジェクトの早い段階で原則を定義し、一貫した意思決定を行う
- 技術的およびプロセス的な原則の両方を含める
- 主要な機能開発の前に憲法をレビューする
- 憲法の変更はクロスアーティファクト検証をトリガーする

---

### `/codexspec.specify`

インタラクティブな Q&A で要件を明確化します。このコマンドは初期アイデアを探索し、ファイルは作成しません。完全な制御権はユーザーが保持します。

**構文:**
```
/codexspec.specify [your idea or requirement]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `your idea or requirement` | いいえ | 構築したいものの初期説明（指定されていない場合はプロンプトが表示されます） |

**動作:**
- アイデアを理解するための明確化質問を行う
- 考慮していないかもしれないエッジケースを探索
- 対話を通じて高品質な要件を共創
- "何を" と "なぜ" に焦点を当て、技術実装には焦点を当てない
- **ファイルを生成しない** - ドキュメントを作成するタイミングはユーザーが決定

**作成されないもの:**
- このコマンド中にファイルは作成されない
- 要件はユーザーが承認するまで会話に残る

**例:**
```text
You: /codexspec.specify I want to build a task management app

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
     Use /codexspec.generate-spec to create spec.md
```

**ヒント:**
- 初期要件探索に使用
- 完全であることを気にしない - 改善は反復的
- AI が仮定をした場合は質問する
- spec を生成する前にサマリーをレビューする

---

### `/codexspec.generate-spec`

明確化された要件から `spec.md` ドキュメントを生成します。このコマンドは「要件コンパイラ」として機能し、明確化された要件を構造化された仕様に変換します。

**構文:**
```
/codexspec.generate-spec
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| なし | - | 前の `/codexspec.specify` セッションからのコンテキストを使用 |

**動作:**
- `.codexspec/specs/{NNN}-{feature-name}/` ディレクトリを作成
- 包括的な `spec.md` を生成:
  - 機能概要とゴール
  - 受け入れ基準付きのユーザーストーリー
  - 機能要件 (REQ-XXX 形式)
  - 非機能要件 (NFR-XXX 形式)
  - エッジケースと対応アプローチ
  - スコープ外の項目

**作成されるもの:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── spec.md
```

**例:**
```text
You: /codexspec.generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/001-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec.review-spec
     - Or proceed to /codexspec.spec-to-plan
```

**ヒント:**
- `/codexspec.specify` で要件が明確化された後に実行
- 進む前に生成された spec をレビュー
- 品質検証に `/codexspec.review-spec` を使用
- 軽微な調整が必要な場合は spec.md を直接編集

---

### `/codexspec.clarify`

既存の仕様をスキャンして曖昧さとギャップを発見します。初期 spec 作成後の反復的な改善に使用します。

**構文:**
```
/codexspec.clarify [path_to_spec.md]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_spec.md` | いいえ | spec ファイルへのパス（指定されていない場合は自動検出） |

**動作:**
- 4 つの焦点を絞った曖昧さカテゴリで spec をスキャン
- 的を絞った明確化質問を行う（最大 5 つ）
- 明確化の回答で spec.md を更新
- 利用可能な場合は review-spec の発見事項を統合

**曖昧さカテゴリ:**

| カテゴリ | 検出内容 |
|----------|-----------------|
| **完全性のギャップ** | 欠落セクション、空のコンテンツ、不在の受け入れ基準 |
| **具体性の問題** | 曖昧な用語（"fast"、"scalable"）、未定義の制約 |
| **振る舞いの明確さ** | エラー処理のギャップ、未定義の状態遷移 |
| **測定可能性の問題** | メトリクスのない非機能要件 |

**例:**
```text
You: /codexspec.clarify

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

**ヒント:**
- spec.md が存在するが改善が必要な場合に使用
- `/codexspec.review-spec` の発見事項を統合
- セッションあたり最大 5 つの質問
- 複雑な仕様には複数回実行

---

### `/codexspec.spec-to-plan`

機能仕様を技術実装計画に変換します。ここでは機能が **どのように** 構築されるかを定義します。

**構文:**
```
/codexspec.spec-to-plan [path_to_spec.md]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_spec.md` | いいえ | spec ファイルへのパス（指定されていない場合は `.codexspec/specs/` から自動検出） |

**動作:**
- 仕様と憲法を読み込む
- バージョン制約付きで技術スタックを定義
- 憲法準拠レビューを実行（憲法が存在する場合は必須）
- モジュール依存グラフ付きのアーキテクチャを作成
- 理由付きで技術決定を文書化
- 実装フェーズを計画

**作成されるもの:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── plan.md    # 技術実装計画
```

**例:**
```text
You: /codexspec.spec-to-plan Use Python FastAPI for backend, React for frontend, PostgreSQL for database

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

**ヒント:**
- spec がレビューされ安定した後に実行
- 憲法が存在する場合、憲法準拠レビューは必須
- プロジェクトタイプに基づいて関連セクションを含める
- タスクに進む前に計画をレビュー

---

### `/codexspec.plan-to-tasks`

技術計画を TDD 適用のアトミックで実行可能なタスクに分解します。

**構文:**
```
/codexspec.plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `paths` | いいえ | spec と plan へのパス（指定されていない場合は自動検出） |

**動作:**
- アトミックなタスクを作成（タスクごとに 1 つのプライマリファイル）
- TDD を適用: テストタスクは実装タスクに先行
- `[P]` で並列化可能なタスクをマーク
- 各タスクの正確なファイルパスを指定
- フェーズチェックポイントを定義

**作成されるもの:**
```
.codexspec/
└── specs/
    └── 001-task-management/
        └── tasks.md    # タスク分解
```

**タスク構造:**
```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**例:**
```text
You: /codexspec.plan-to-tasks

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

**ヒント:**
- 各タスクは 1 つのプライマリファイルのみを扱うべき
- テストタスクは常に実装タスクに先行
- `[P]` は真に独立した並列化可能なタスクをマーク
- 実装前に依存関係をレビュー

---

### `/codexspec.implement-tasks`

条件付き TDD ワークフローで実装タスクを実行します。タスクリストを体系的に処理します。

**構文:**
```
/codexspec.implement-tasks [tasks_path]
/codexspec.implement-tasks [spec_path plan_path tasks_path]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `tasks_path` | いいえ | tasks.md へのパス（指定されていない場合は自動検出） |
| `spec_path plan_path tasks_path` | いいえ | 3 つのドキュメントへの明示的なパス |

**ファイル解決:**
- **引数なし**: `.codexspec/specs/` から自動検出
- **1 つの引数**: `tasks.md` パスとして扱い、他は同じディレクトリから推論
- **3 つの引数**: spec.md、plan.md、tasks.md への明示的なパス

**動作:**
- tasks.md を読み込み、未完了タスクを特定
- コードタスクに TDD ワークフローを適用:
  - **Red**: 最初に失敗するテストを書く
  - **Green**: テストに合格するよう実装
  - **Verify**: すべてのテストを実行
  - **Refactor**: テストを緑に保ちながら改善
- テスト不可能なタスク（ドキュメント、設定）は直接実装
- 進行に伴いタスクのチェックボックスを更新
- ブロッカーが発生した場合は issues.md に記録

**コードタスクの TDD ワークフロー:**
```
Red → Green → Verify → Refactor → Mark Complete
```

**テスト不可能なタスクの直接実装:**
- ドキュメントファイル
- 設定ファイル
- 静的アセット
- インフラファイル

**例:**
```text
You: /codexspec.implement-tasks

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

**ヒント:**
- 中断された場合は途中から再開可能
- ブロッカーは issues.md に記録
- 重要なタスク/フェーズ後にコミット
- 最初に `/codexspec.review-tasks` を実行して検証

---

### `/codexspec.review-spec`

仕様の完全性、明確さ、一貫性、技術計画への準備状況を検証します。

**構文:**
```
/codexspec.review-spec [path_to_spec.md]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_spec.md` | いいえ | spec ファイルへのパス（指定されていない場合は自動検出） |

**動作:**
- すべての必須セクションの完全性をチェック
- 明確さと具体性を評価
- 内部一貫性を検証
- 要件のテスト可能性を評価
- 憲法整合性をチェック
- スコア付きレビューレポートを生成

**レビュー次元:**

| 次元 | 重み | 検証内容 |
|-----------|--------|-------------------|
| 完全性 | 25% | すべてのセクションが存在し、実質的 |
| 明確さ | 25% | 曖昧な表現なし、単一の解釈 |
| 一貫性 | 20% | 内部矛盾なし |
| テスト可能性 | 20% | 要件が検証可能 |
| 憲法整合性 | 10% | プロジェクト原則に整合 |

**例:**
```text
You: /codexspec.review-spec

AI:  Reviewing specification...

     # Specification Review Report

     ## Summary
     - **Overall Status**: ⚠️ Needs Work
     - **Quality Score**: 72/100
     - **Readiness**: Needs Revision

     ## Section Analysis
     | Section | Status | Completeness | Quality |
     |---------|--------|--------------|---------|
     | Overview | ✅ | 100% | High |
     | Goals | ✅ | 100% | High |
     | User Stories | ⚠️ | 80% | Medium |
     | Functional Requirements | ✅ | 100% | High |
     | Non-Functional Requirements | ⚠️ | 50% | Medium |
     | Edge Cases | ❌ | 0% | N/A |

     ## Critical Issues (Must Fix)
     - [SPEC-001]: Edge Cases section is empty
       - Impact: May miss important failure scenarios
       - Suggestion: Document at least 3-5 edge cases

     ## Warnings (Should Fix)
     - [SPEC-002]: NFR-001 uses vague term "fast"
       - Impact: Cannot verify without metrics
       - Suggestion: Specify concrete response time

     ## Recommendations
     1. Add Edge Cases section with handling approaches
     2. Quantify non-functional requirements
     3. Add acceptance criteria to User Story 3

     Available follow-up:
     - /codexspec.clarify - to address ambiguities
     - /codexspec.spec-to-plan - if issues resolved
```

**ヒント:**
- `/codexspec.spec-to-plan` の前に実行
- 進む前に重要な問題に対処
- 警告はブロックしないがリスクを示す
- 修正後に再実行

---

### `/codexspec.review-plan`

技術実装計画の実現可能性、アーキテクチャ品質、仕様との整合性をレビューします。

**構文:**
```
/codexspec.review-plan [path_to_plan.md]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_plan.md` | いいえ | plan ファイルへのパス（指定されていない場合は自動検出） |

**動作:**
- 仕様要件が計画でカバーされていることを検証
- 技術スタックの選択を評価
- アーキテクチャ決定を評価
- 実装フェーズを検証
- 憲法整合性をチェック
- スコア付きレビューレポートを生成

**レビュー次元:**

| 次元 | 重み | 検証内容 |
|-----------|--------|-------------------|
| 仕様整合性 | 30% | すべての要件に実装がある |
| 技術スタック | 15% | 適切な技術選択 |
| アーキテクチャ品質 | 25% | 健全な設計とパターン |
| フェーズ計画 | 15% | 論理的で現実的なフェーズ |
| 憲法整合性 | 15% | プロジェクト原則に従う |

**例:**
```text
You: /codexspec.review-plan

AI:  Reviewing technical plan...

     # Plan Review Report

     ## Summary
     - **Overall Status**: ✅ Pass
     - **Quality Score**: 85/100
     - **Readiness**: Ready for Task Breakdown

     ## Spec Alignment
     | Requirement | Coverage | Status |
     |-------------|----------|--------|
     | REQ-001 to REQ-012 | ✅ Full | All covered |
     | US-001 to US-004 | ✅ Full | All covered |
     | NFR-001 to NFR-003 | ⚠️ Partial | Caching not detailed |

     ## Architecture Review
     Strengths:
     - Clean separation of concerns
     - Well-defined module boundaries
     - Appropriate design patterns

     Concerns:
     - Missing error handling strategy documentation

     ## Constitution Alignment
     | Principle | Compliance |
     |-----------|------------|
     | Clean Architecture | ✅ |
     | TDD | ✅ |
     | Code Quality | ✅ |

     Ready for /codexspec.plan-to-tasks
```

**ヒント:**
- `/codexspec.plan-to-tasks` の前に実行
- 重要な問題は解決すべき
- アーキテクチャの問題を早期に発見するために使用
- 技術スタックがチームのスキルに合っているか確認

---

### `/codexspec.review-tasks`

タスク分解の完全性、TDD 準拠、正しい順序、適切な依存関係を検証します。

**構文:**
```
/codexspec.review-tasks [path_to_tasks.md]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_tasks.md` | いいえ | tasks ファイルへのパス（指定されていない場合は自動検出） |

**動作:**
- すべての計画項目にタスクカバレッジがあるかチェック
- TDD 準拠を検証（テストが実装に先行）
- タスク粒度を検証（アトミック、単一ファイルフォーカス）
- 依存関係を検証（サイクルなし、正しい順序）
- 並列化マーカーをレビュー
- ファイルパスを検証

**レビュー次元:**

| 次元 | 重み | 検証内容 |
|-----------|--------|-------------------|
| 計画カバレッジ | 30% | すべての計画項目にタスクがある |
| TDD 準拠 | 25% | テストファーストワークフローが適用 |
| 依存関係と順序 | 20% | 正しい依存関係、サイクルなし |
| タスク粒度 | 15% | アトミック、適切なスコープ |
| 並列化とファイル | 10% | 正しいマーカーとパス |

**例:**
```text
You: /codexspec.review-tasks

AI:  Reviewing task breakdown...

     # Tasks Review Report

     ## Summary
     - **Overall Status**: ⚠️ Needs Work
     - **Quality Score**: 78/100
     - **Total Tasks**: 24
     - **Parallelizable**: 8 (33%)

     ## TDD Compliance
     | Component | Test Task | Test Before Impl | Status |
     |-----------|-----------|------------------|--------|
     | Task Entity | ✅ | ✅ | ✅ |
     | User Entity | ✅ | ✅ | ✅ |
     | TaskService | ❌ Missing | N/A | ❌ |

     ## TDD Violations
     - [TDD-001]: TaskService missing test task

     ## Dependency Issues
     - [DEP-001]: Task 2.5 marked [P] but depends on 2.4

     ## Recommendations
     1. Add test task for TaskService before implementation
     2. Fix parallelization marker on Task 2.5

     Fix issues before /codexspec.implement-tasks
```

**ヒント:**
- `/codexspec.implement-tasks` の前に実行
- TDD 違反はコード品質にとって重要
- 並列化マーカーが正確かチェック
- ファイルパスがプロジェクト構造と一致するか確認

---

### `/codexspec.analyze`

spec.md、plan.md、tasks.md にわたる非破壊的なクロスアーティファクト一貫性分析を実行します。不一致、重複、カバレッジギャップを特定します。

**構文:**
```
/codexspec.analyze
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| なし | - | 現在の機能のアーティファクトを分析 |

**動作:**
- アーティファクト間の重複を検出
- 測定可能な基準が欠けている曖昧さを特定
- 仕様不足の項目を発見
- 憲法整合性をチェック
- 要件カバレッジをタスクにマッピング
- 用語と順序の一貫性の問題をレポート

**重大度レベル:**

| レベル | 定義 |
|-------|------------|
| **CRITICAL** | 憲法違反、コアアーティファクトの欠落、ゼロカバレッジ |
| **HIGH** | 重複/競合する要件、曖昧なセキュリティ属性 |
| **MEDIUM** | 用語のずれ、非機能カバレッジの欠落 |
| **LOW** | スタイル/表現の改善 |

**例:**
```text
You: /codexspec.analyze

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

     Resolve CRITICAL issues before /codexspec.implement-tasks
```

**ヒント:**
- `/codexspec.plan-to-tasks` 後、実装前に実行
- CRITICAL 問題は実装をブロックすべき
- 読み取り専用分析 - ファイルは変更されない
- 発見事項を使用してアーティファクト品質を改善

---

### `/codexspec.checklist`

要件の完全性、明確さ、一貫性を検証するための品質チェックリストを生成します。これらは「要件記述のための単体テスト」です。

**構文:**
```
/codexspec.checklist [focus_area]
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `focus_area` | いいえ | ドメインフォーカス（例: "ux"、"api"、"security"、"performance"） |

**動作:**
- 品質次元で整理されたチェックリストを生成
- `FEATURE_DIR/checklists/` ディレクトリにチェックリストを作成
- 項目は実装テストではなく要件品質に焦点

**品質次元:**
- **要件完全性**: 必要な要件がすべて存在するか？
- **要件明確さ**: 要件は具体的で曖昧さがないか？
- **要件一貫性**: 要件は競合なく整合しているか？
- **受け入れ基準品質**: 成功基準は測定可能か？
- **シナリオカバレッジ**: すべてのフロー/ケースが扱われているか？
- **エッジケースカバレッジ**: 境界条件が定義されているか？
- **非機能要件**: パフォーマンス、セキュリティ、アクセシビリティが指定されているか？
- **依存関係と前提**: 文書化されているか？

**チェックリストタイプの例:**
- `ux.md` - 視覚階層、インタラクション状態、アクセシビリティ
- `api.md` - エラー形式、レート制限、認証
- `security.md` - データ保護、脅威モデル、侵害対応
- `performance.md` - メトリクス、負荷条件、劣化

**例:**
```text
You: /codexspec.checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/001-task-management/checklists/security.md

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

**ヒント:**
- チェックリストは実装の正確性ではなく要件品質を検証
- 要件レビューと改善に使用
- 的を絞った検証のためにドメイン固有のチェックリストを作成
- 技術計画に進む前に実行

---

### `/codexspec.tasks-to-issues`

`tasks.md` からタスクを GitHub issues に変換し、プロジェクト追跡とコラボレーションを行います。

**構文:**
```
/codexspec.tasks-to-issues
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| なし | - | 現在の機能からすべてのタスクを変換 |

**動作:**
- タスク ID、説明、依存関係、ファイルパスを解析
- 構造化された本文で GitHub issues を作成
- タスクタイプに基づいてラベルを追加（setup、implementation、testing、documentation）
- issues 間の依存関係をリンク
- URL 付きで作成された issues をレポート

**前提条件:**
- GitHub リモートを持つ Git リポジトリ
- GitHub CLI (`gh`) がインストールされ、認証済み
- `tasks.md` ファイルが存在

**例:**
```text
You: /codexspec.tasks-to-issues

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

**ヒント:**
- GitHub CLI 認証が必要（`gh auth login`）
- GitHub リポジトリでのみ動作
- リポジトリのデフォルト設定で issues を作成
- 実行前に重複をチェック

---

### `/codexspec.commit`

git ステータスとセッションコンテキストに基づいて Conventional Commits 準拠のコミットメッセージを生成します。このコマンドはコンテキスト認識であり、異なる git 状態を処理します。

**構文:**
```
/codexspec.commit
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| なし | - | 現在の git 状態とセッションコンテキストを分析 |

**動作:**
- git コンテキストを収集（ブランチ、ステータス、ステージング/未ステージング変更）
- 意図理解のためにセッション会話履歴を分析
- git 状態に基づいて優先ロジックに従う:
  - **ステージングされた変更が存在**: ステージングされた変更のみからコミットメッセージを生成
  - **ステージングなし、未ステージング変更あり**: ステージングリマインダー付きでコミットメッセージを提案
  - **変更なし**: クリーンな作業ディレクトリをレポート
- Conventional Commits 準拠のメッセージを生成
- コミット実行前にユーザーに確認

**Git 状態処理:**

| 状態 | 動作 |
|-------|----------|
| ステージングされた変更 | メッセージ生成、確認、コミット |
| 未ステージングのみ | メッセージ提案、ステージングリマインダー、すべてステージングするか確認 |
| クリーン | "No changes detected" をレポート |

**例:**
```text
You: /codexspec.commit

AI:  Analyzing git context...

     Branch: feature/add-auth
     Staged: 2 files
     Unstaged: 3 files

     Suggested commit message:
     feat(auth): add JWT authentication module

     - Implement token generation and validation
     - Add middleware for protected routes
     - Include unit tests for auth service

     Confirm commit? (y/n)

You: y

AI:  ✓ Committed: abc1234
```

**ヒント:**
- `/codexspec.commit-staged` より柔軟 - 様々な git 状態を処理
- 意味のあるコミットメッセージのためにセッションコンテキストを考慮
- コミット前に常に確認
- 未ステージング変更の場合、最初にステージングするよう明確なリマインダーを提供

---

### `/codexspec.commit-staged`

ステージングされた git 変更のみに基づいて Conventional Commits 準拠のコミットメッセージを生成します。これは、すでに変更をステージングしている場合のシンプルで焦点を絞ったコマンドです。

**構文:**
```
/codexspec.commit-staged
```

**引数:**
| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| なし | - | ステージングされた変更のみを分析 |

**動作:**
- `git diff --staged` を実行してステージングされた変更を取得
- 変更を分析してコミットメッセージを生成
- Conventional Commits 仕様に従う
- コミット前にユーザーに確認
- ステージングされた変更がない場合はエラーをレポート

**例:**
```text
You: /codexspec.commit-staged

AI:  Analyzing staged changes...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Suggested commit message:
     feat(auth): implement token refresh logic

     - Add refresh token generation
     - Include token expiration handling
     - Add tests for refresh flow

     Confirm commit? (y/n)

You: y

AI:  ✓ Committed: def5678
```

**ヒント:**
- 最初に `git add` で変更をステージング
- ステージングされたコンテンツのみを分析 - 未ステージングは無視
- コミットしたいものがわかっている場合、`/codexspec.commit` よりシンプル
- よりコンテキスト認識のあるメッセージには `/codexspec.commit` を使用

---

## ワークフロー概要

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec Human-AI Collaboration Workflow              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Define project principles                         │
│         │                         with cross-artifact validation         │
│         ▼                                                                │
│  2. Specify  ───────►  Interactive Q&A to clarify requirements           │
│         │               (no file created - human control)                │
│         ▼                                                                │
│  3. Generate Spec  ─►  Create spec.md document                           │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 1: /codexspec.review-spec ★                        ║   │
│  ║  Validate: Completeness, Clarity, Testability, Constitution       ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  Resolve ambiguities (iterative)                   │
│         │               4 targeted categories, max 5 questions           │
│         ▼                                                                │
│  5. Spec to Plan  ──►  Create technical plan with:                       │
│         │               • Constitutionality review (MANDATORY)           │
│         │               • Module dependency graph                        │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 2: /codexspec.review-plan ★                        ║   │
│  ║  Validate: Spec Alignment, Architecture, Tech Stack, Phases        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  Generate atomic tasks with:                       │
│         │               • TDD enforcement (tests before impl)            │
│         │               • Parallel markers [P]                           │
│         │               • File path specifications                       │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 3: /codexspec.review-tasks ★                       ║   │
│  ║  Validate: Coverage, TDD Compliance, Dependencies, Granularity     ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  Cross-artifact consistency check                  │
│         │               Detect gaps, duplications, constitution issues   │
│         ▼                                                                │
│  8. Implement  ─────►  Execute with conditional TDD workflow             │
│                          Code: Test-first | Docs/Config: Direct          │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**重要ポイント**: 各レビューゲート (★) は、より多くの時間を投資する前に AI 出力を検証する **人間のチェックポイント** です。これらのゲートをスキップすると、多くの場合、コストのかかる手戻りが発生します。

---

## トラブルシューティング

### "Feature directory not found"

コマンドが機能ディレクトリを見つけられませんでした。

**解決策:**
- 最初に `codexspec init` を実行してプロジェクトを初期化
- `.codexspec/specs/` ディレクトリが存在するかチェック
- 正しいプロジェクトディレクトリにいることを確認

### "No spec.md found"

仕様ファイルがまだ存在しません。

**解決策:**
- 最初に `/codexspec.specify` を実行して要件を明確化
- 次に `/codexspec.generate-spec` を実行して spec.md を作成

### "Constitution not found"

プロジェクト憲法が存在しません。

**解決策:**
- `/codexspec.constitution` を実行して作成
- 憲法はオプションですが、一貫した決定のために推奨

### "Tasks file not found"

タスク分解が存在しません。

**解決策:**
- 最初に `/codexspec.spec-to-plan` を実行したことを確認
- 次に `/codexspec.plan-to-tasks` を実行して tasks.md を作成

### "GitHub CLI not authenticated"

`/codexspec.tasks-to-issues` コマンドには GitHub 認証が必要です。

**解決策:**
- GitHub CLI をインストール: `brew install gh` (macOS) または同等のコマンド
- 認証: `gh auth login`
- 確認: `gh auth status`

---

## 次のステップ

- [ワークフロー](workflow.md) - 一般的なパターンと各コマンドをいつ使用するか
- [CLI](../reference/cli.md) - プロジェクト初期化用の端末コマンド
