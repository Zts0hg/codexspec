<a id="available-commands"></a>

# 利用可能なコマンド

CLI には 6 つの公開コマンドがあります。エージェント連携では 28 コマンドを配布します。
Claude では `/codexspec:<name>`、Codex では `$codexspec:<name>` で呼び出します。
以下の表は、読みやすさのため Claude の表記で統一しています。

<a id="cli-commands"></a>

## CLI コマンド

| コマンド | 目的 |
|---------|---------|
| `codexspec init` | Claude、Codex、または両方に合わせてプロジェクトを初期化・更新 |
| `codexspec check` | インストール済みのツールと依存関係を確認 |
| `codexspec version` | バージョンとシステム情報を表示 |
| `codexspec config` | プロジェクト設定を表示・変更 |
| `codexspec list-commands` | 利用可能なエージェントコマンドをカテゴリ別に表示 |
| `codexspec show-blueprint` | 共有 worktree のブループリントを変更せずに出力 |

<a id="core-workflow-commands"></a>

## 基本ワークフローコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:constitution` | プロジェクト原則を作成・更新し、成果物間の整合性を検証 |
| `/codexspec:specify` | 機能要件を話し合い、確認して保存 |
| `/codexspec:blueprint` | ブループリントの確認済み・保留中の要件を準備・管理 |
| `/codexspec:generate-spec` | 確認済み要件から追跡可能な仕様書を作成し、自動レビュー |
| `/codexspec:spec-to-design` | アーキテクチャ、コンポーネント、インターフェース、判断を定義し、自動レビュー |
| `/codexspec:design-to-plan` | 実装のフェーズ、順序、検証を計画し、自動レビュー |
| `/codexspec:plan-to-tasks` | 上位成果物の内容を網羅する検証可能なタスクを作成し、自動レビューと分析 |
| `/codexspec:implement-tasks` | タスクを実行し、結果を検証してレビュー・修正 |
| `/codexspec:auto-dev` | 確認済みブループリント要件をドキュメントの順に自律開発 |

<a id="artifact-review-commands"></a>

## 成果物レビューコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:review-spec` | 仕様書の忠実度と内部品質を確認 |
| `/codexspec:review-design` | 設計の忠実度、実現可能性、計画に進める状態かを確認 |
| `/codexspec:review-plan` | 計画の忠実度、実現可能性、実装に進める状態かを確認 |
| `/codexspec:review-tasks` | タスクの忠実度、依存関係、実行可能性、検証を確認 |

<a id="requirements-existing-code-and-debugging"></a>

## 要件、既存コード、デバッグ

| コマンド | 目的 |
|---------|---------|
| `/codexspec:clarify` | 要件の曖昧さを解消し、仕様書より先に要件を更新 |
| `/codexspec:analyze` | 一連の成果物の追跡可能性を確認し、下位成果物を上位の判断基準に合わせて修正 |
| `/codexspec:checklist` | 要件品質のチェックリストを生成 |
| `/codexspec:tasks-to-issues` | 既存のタスクを、実行に移せる GitHub Issue に変換 |
| `/codexspec:debug` | 修正前に根本原因を調査 |
| `/codexspec:reverse-spec` | 既存アーキテクチャの調査、モジュール成果物の草案作成、または基準との差異の報告 |

<a id="project-knowledge-commands"></a>

## プロジェクト知識コマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:distill` | 再利用可能な知識を記録、またはローカルワークスペースで候補をレビュー |
| `/codexspec:evolve` | 承認済み知識をもとに、上流への貢献に向けた草案を作成 |
| `/codexspec:onboard` | 既存コードから慣行の候補と、根拠のある制約を初期登録 |

<a id="git-and-code-review-commands"></a>

## Git とコードレビューのコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:commit-staged` | ステージ済み変更からメッセージを生成し、プレビューまたは許可を得たコミットを実行 |
| `/codexspec:pr` | 構造化された PR/MR の説明を生成 |
| `/codexspec:release-notes` | 変更履歴のエントリを更新し、Git 履歴からリリース本文を生成 |
| `/codexspec:review-code` | 選択した変更を欠陥ゲートとしてレビュー。パスの品質評価には `--audit` を使用 |

<a id="utility-commands"></a>

## ユーティリティコマンド

| コマンド | 目的 |
|---------|---------|
| `/codexspec:config` | 対話形式でプロジェクト設定を作成・表示・変更・リセット |
| `/codexspec:quick` | 小さな変更に対し、簡潔な要件優先 SDD ワークフローを実行 |

旧 Python／React レビューはプラグインの互換性維持用であり、インストールされる 28 コマンドには含まれません。言語やフレームワークに応じた基準を読み込む `review-code` を使い、パス単位の評価には `--audit` を指定してください。

## コマンドリファレンス

### `/codexspec:constitution`

プロジェクト憲法を作成または更新します。憲法はアーキテクチャの原則、技術スタック、コード標準、ガバナンス規則を定義し、その後のすべての開発意思決定を導きます。

**構文：**

```
/codexspec:constitution [principles description]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `principles description` | いいえ | 取り込む原則の説明（指定がない場合はプロンプトで尋ねられます） |

**処理内容：**

- `.codexspec/memory/constitution.md` が存在しない場合は作成します
- 既存の憲法に新しい原則を反映して更新します
- テンプレートとのアーティファクト間整合性を検証します
- 変更点と影響を受けるファイルを示す Sync Impact Report を生成します
- 依存テンプレートに対する憲法適合性レビューを実施します

**生成するファイル：**

```
.codexspec/
└── memory/
    └── constitution.md    # Project governance document
```

**例：**

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

**使い方のポイント：**

- プロジェクトの早期に原則を定義すると、意思決定の一貫性が保たれます
- 技術面とプロセス面の両方の原則を盛り込みます
- 主要な機能開発を始める前に憲法を見直します
- 憲法の変更はアーティファクト間検証をトリガーします

---

### `/codexspec:specify`

対話型の Q&A を通じて要件を明確化し、得られた要約を確認したうえで、後のセッションに向けて保存します。

**構文：**

```
/codexspec:specify [your idea or requirement]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `your idea or requirement` | いいえ | 構築したいものの初期説明（指定がない場合はプロンプトで尋ねられます） |

**処理内容：**

- あなたのアイデアを理解するための明確化質問を投げかけます
- 想定していなかったエッジケースを探ります
- 対話を通じて高品質な要件を共同で作り上げます
- 技術的な実装ではなく「何を」「なぜ」に焦点を当てます
- 確認されたニーズ、制約、決定、対象外事項、未解決質問に安定した ID を割り当てます
- ユーザーの根拠と確認ログを記録します
- 機能ワークスペースと `requirements.md` を作成します

**生成するファイル：**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

確認された項目だけが権威ある要件になります。未解決の質問は明示的に未解決のまま残されます。これが要件に対する Confirmation Gate であり、最終的な要約を明示的に確認するまでは何も確定しません。

**例：**

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

**使い方のポイント：**

- 初期の要件探索に活用します
- 完璧にまとめようと気にする必要はありません。洗練は反復的に進めます
- AI が前提を置いたと感じたら質問を投げかけます
- spec を生成する前に要約を確認します

---

### `/codexspec:blueprint`

開発前に複数の確認済み要件を準備するには `blueprint`、そのキューを開発するには `auto-dev` を使います。

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

ブループリントの要件検討では、ユーザーが決めるべき方向性、選択、制約を解決してから要件をキューに入れます。
共有の `.codexspec/blueprint.md` では、`pending`、`in_progress`、`completed` の状態を使います。
保留中の要件は追加、置換、削除、並べ替えができます。進行中と完了済みの項目は、ブループリントの管理操作では読み取り専用です。

Auto-dev はドキュメントに記載された順に開発し、進行中の機能があれば、別の機能を始める前に再開します。
機能が完了するたびにキューを読み直すため、新たに追加された保留中の作業もその実行で処理できます。
確認済み要件の範囲内で SDD の各ステージ、実装、検証、レビュー、修正を行います。
`auto-dev` を呼び出すと、`workflow.auto_next` の値にかかわらず自動化が有効になります。この設定自体は変更しません。

両コマンドは、ブランチ `codexspec/auto-dev` の `worktree-for-codexspec-auto-dev` を共有します。
共通の所有権管理と書き込み保護のもとで同時に操作できますが、要件の開発はそのワークスペースで順次行います。
確認済み要件から決められない製品上の判断が必要になると、通常の自律実行中には質問せず、根拠を示して停止します。

現在の共有ブループリントを変更せずに確認するには、次を実行します。

```bash
codexspec show-blueprint
```

---

### `/codexspec:generate-spec`

確認済み要件から追跡可能な仕様書を作成し、自動レビューを実行します。

**構文：**

```
/codexspec:generate-spec
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| 機能のパス | いいえ | 機能ディレクトリ、`requirements.md`、対象の `spec.md` のいずれかを明示的に指定します。解釈が曖昧な場合に必要です |

**処理内容：**

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
- 上位の判断根拠の食い違いを推測で解決せず、ユーザーの確認のために停止します
- 自動的にレビューを行い、エビデンスに基づく欠陥は最大 2 ラウンドまで修復する可能性があります

**生成するファイル：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**例：**

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
     - Or proceed to /codexspec:spec-to-design
```

---

### `/codexspec:spec-to-design`

確認済みの `requirements.md` と `spec.md`、プロジェクト原則、関連するリポジトリの事実を読みます。コンポーネント、インターフェース、データフロー、代替案、判断を上流の要件に結び付けた `design.md` を作成し、`review-design` を自動実行します。確認済みの意図が変わる選択や、ユーザーの新たな判断が必要な場合は停止します。

```text
/codexspec:spec-to-design <feature-dir>
```

---

### `/codexspec:design-to-plan`

確認済みの設計を実装計画に変換します。先に `spec-to-design` を実行し、アーキテクチャ、コンポーネント、インターフェース、技術選定を定義します。

```text
/codexspec:design-to-plan [design.md | spec.md | feature-directory]
```

`requirements.md`、`spec.md`、`design.md`、プロジェクト憲章を読み、実装フェーズ、順序、検証方法を計画します。システムを再設計せず、設計を参照します。各計画コンポーネントには `Covers: REQ-xxx; Design: <design component>` を記載します。

`plan.md` を生成して `review-plan` を実行します。`auto_next` が有効な場合、レビュー合格後に `plan-to-tasks` に進みます。確認済みの意図を変更する判断にはユーザーの確認が必要です。明示的なパスを優先し、次に現在の機能ブランチを使用します。機能が一意に決まらない場合は選択を求めます。`design.md` のない旧機能では、従来どおり `spec.md` から計画できます。

---

### `/codexspec:plan-to-tasks`

技術計画を実行可能なタスクに分割し、明示的なカバレッジと検証可能な成果物を設定します。

**構文：**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `paths` | いいえ | spec と plan のパス（指定がない場合は自動検出されます） |

**処理内容：**

- 検証可能な成果物を 1 つ持つタスクを作成します。1 つのタスクが密接に関連する複数ファイルを扱うこともあります
- 計画、憲法、確認されたニーズ、リスクによってテストファーストが要求される場合にのみ、その順序を採用します
- 真に独立している場合にのみタスクに `[P]` を付与します
- 各タスクの正確なファイルパスを指定します
- 計画や要件 ID への `Covers` リンクを追加します

**生成するファイル：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # Task breakdown
```

**タスクの構造：**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**例：**

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

**使い方のポイント：**

- 各タスクは検証可能な 1 つの成果物を生み出すべきで、密接に関連するファイルを扱っても構いません
- テストタスクが実装より先になるのはテストファーストが要求される場合のみです
- `[P]` は真に独立して並列化可能なタスクを示します
- 実装に入る前に依存関係をレビューします

タスク作成後に `review-tasks` を実行します。結果が `PASS` または `PASS_WITH_WARNINGS` なら `analyze` を 1 回実行します。この分析は追加の完了ゲートにはなりません。タスクは確認済み要件、仕様、設計、計画を網羅します。

---

### `/codexspec:implement-tasks`

タスクを実行し、結果を検証してレビュー・修正.

```text
/codexspec:implement-tasks <feature-dir>
```

4 つの成果物レビュアー `review-spec`、`review-design`、`review-plan`、`review-tasks` は、忠実度、網羅性、実現可能性、内部品質を確認します。
生成後に自動実行され、手動でも呼び出せます。レポートでは、検証済みの欠陥と、合否に影響しないリスクの助言や設計上の改善案を分けて報告し、適合度スコアも示します。

`review-code` は、選択した変更を対象とする独立した欠陥ゲートと、コード全体の明示的な品質評価を提供します。

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

デフォルトでは機能ブランチの差分全体をレビューします。コミット済み、ステージ済み、未ステージ、Git の無視対象でない未追跡の変更がすべて含まれます。
コミット済み、未コミット、単一コミットのいずれかを明示的に選ぶこともできます。
`--feature` は要件の文脈を追加しますが、Git の対象範囲は狭めません。
`--audit` は指定されたパスを評価し、完了判定ではなく、助言としての評価表を作成します。

レビューでは `.codexspec/review-code/` から共通基準を読み込み、関連する動作の観点や、言語・フレームワークごとのチェックを選びます。
指摘には、具体的な根拠、実際に発生し得る条件、選択した変更に起因すること、影響の説明が必要です。
レビュアーはファイルを編集せず、欠陥と根拠のある保守提案を報告します。修正を行う呼び出し元は、それらを独立して検証します。

実装では、コードのタスクはテストを先に書いて進め、ドキュメントや設定は直接変更して適切なチェックを行います。
修正後の差分レビューでは、影響を受けていない範囲の確認結果を再利用できます。
最終的な受け入れには、新たに行う機能全体のレビューで `PASS` を得ること、対象範囲の確認と検証が完了すること、
認定された P0–P3 の欠陥が 1 件も残っていないことが必要です。根拠のある保守提案は別に報告します。

`workflow.auto_maintenance` のデフォルトは **true** です。
修正を行う呼び出し元が、検証済みで互換性を保つ保守改善も適用するかを、この設定で制御します。
無効にしても提案は報告され、欠陥の修正や必須チェックは免除されません。
ステージの自動進行とは独立した設定で、`implement-tasks` の引数ではありません。

根本原因を先に調べるデバッグには、次のコマンドを使います。

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug は、調査 → パターン分析 → 単一仮説の検証 → 失敗するテストを先に書いて修正、の順に進みます。
実装中の修正が行き詰まった場合、単純ではない動作上の欠陥について原因を追う必要がある場合、
同じ種類の根本原因がレビューの複数ラウンドで再発した場合に、この手順へ移ります。
修正が 3 回失敗したら、アーキテクチャを再検討します。

要件の明確さ、完全性、一貫性を評価するには、`checklist` を使います。

```text
/codexspec:checklist Check the authentication requirements for completeness
```

レビュー対象の選び方、引数、詳しい手順は、[コマンドリファレンス](commands.md)を参照してください。

---

### `/codexspec:auto-dev`

確認済みブループリント要件をドキュメントの順に自律開発.

参照 [`blueprint`](#codexspecblueprint).

```text
/codexspec:auto-dev
```

---

### `/codexspec:review-spec`

仕様書を、確認された要件との整合性および仕様書自身の内部品質の両面から検証します。

**構文：**

```
/codexspec:review-spec [path_to_spec.md]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_spec.md` | いいえ | spec ファイルのパス（指定がない場合は自動検出されます） |

**処理内容：**

- 確認された `requirements.md` の各項目に対する忠実性を確認します
- 内部的一貫性、明確さ、検証可能性を確認します
- 権威ある内容が必要とする場合に限り、テンプレートセクションの欠落を欠陥として扱います
- 各欠陥に `Evidence`、`Location`、`Mismatch`、`Impact`、`Remediation` を含めることを要求します
- `Risk Advisories / Design Opportunities` を欠陥と分けて報告します
- ステータスと、分類された指摘から導出される互換性スコアを生成します

**共通のレビュー規則：**

| 分類 | 意味 |
|----------|---------|
| 上位の根拠との不一致 | 上位の判断根拠と矛盾する、または必要な内容を網羅していないもの |
| 内部的な欠陥 | 内部的に矛盾している、実行不可能、または検証不可能なもの |
| 助言 | 現時点で欠陥のエビデンスを伴わない、任意の改善提案 |

ステータスは `PASS`、`PASS_WITH_WARNINGS`、`NEEDS_REVISION`、`BLOCKED` のいずれかです。助言はステータスやスコアを変更しません。

**例：**

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

**使い方のポイント：**

- `/codexspec:spec-to-design` の前に実行します
- `BLOCKED` と `NEEDS_REVISION` は先に進める準備ができていない合図とみなします
- 助言を要件に昇格させないようにします
- 修正後にもう一度実行します

---

### `/codexspec:review-design`

確認済みの要件と仕様に照らして `design.md` の忠実性、実現可能性、計画に進める状態かを確認します。根拠のある欠陥と任意の設計改善を分けて報告し、他の成果物レビューと同じ状態および修正回数の制限を適用します。

```text
/codexspec:review-design <feature-dir>
```

---

### `/codexspec:review-plan`

技術的な実装計画を、忠実性、実現可能性、技術的決定の妥当性の観点からレビューします。

**構文：**

```
/codexspec:review-plan [path_to_plan.md]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_plan.md` | いいえ | plan ファイルのパス（指定がない場合は自動検出されます） |

**処理内容：**

- `Covers` リンクと、仕様書の必要なカバレッジを検証します
- 該当する憲法ルールとリポジトリの事実を確認します
- 具体的なコストや衝突を生む場合に限り、根拠のない複雑さを指摘します
- 各欠陥にエビデンス欄を必須とし、同じ根本原因を持つ指摘はマージします
- 任意のアーキテクチャ改善は助言として報告します
- 共通のステータス・互換性スコア契約を使用します

**例：**

```text
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**使い方のポイント：**

- `/codexspec:plan-to-tasks` の前に実行します
- エビデンスに基づく欠陥はタスク生成の前に解消します
- 投機的なアーキテクチャのアイデアは助言セクションに留めます
- 技術スタックがチームのスキルに合致しているか確認します

計画は確認済みの `design.md` を実装するもので、アーキテクチャの選択をやり直すものではありません。レビューでは要件の網羅性に加え、計画から設計への参照も確認します。

---

### `/codexspec:review-tasks`

タスク分割を、カバレッジ、検証可能な成果物、正しい順序付け、実現可能な依存関係の観点から検証します。

**構文：**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_tasks.md` | いいえ | tasks ファイルのパス（指定がない場合は自動検出されます） |

**処理内容：**

- すべての必要な計画項目と要件がタスクでカバーされているか確認します
- 権威あるソースが要求する場合にのみ、テストファーストの順序付けを検証します
- 各タスクが確認可能な 1 つの成果物を持つことを検証します
- 依存関係を検証します（循環なし、正しい順序）
- 並列化マーカーをレビューします
- ファイルパスを検証します
- 各欠陥にエビデンス欄を必須とします
- 任意のプロセス改善は助言として報告します
- 共通のステータス・互換性スコア契約を使用します

**例：**

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

**使い方のポイント：**

- `/codexspec:implement-tasks` の前に実行します
- テスト順序に関する指摘は、権威あるソースがテストを要求している場合にのみ欠陥になります
- 並列化マーカーが正確か確認します
- ファイルパスがプロジェクト構造と一致するか確認します

---

### `/codexspec:clarify`

既存の仕様書をスキャンして曖昧さと抜けを検出します。初期の spec 作成後、反復的に洗練する際に使います。

**構文：**

```
/codexspec:clarify [path_to_spec.md]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path_to_spec.md` | いいえ | spec ファイルのパス（指定がない場合は自動検出されます） |

**処理内容：**

- 絞り込んだ曖昧さカテゴリを使って要件と spec をスキャンします
- 的を絞った明確化質問を投げかけます（最大 5 問）
- ユーザー確認後にまず `requirements.md` を更新し、その後 `spec.md` を同期します
- review-spec の指摘があればそれらも統合します

**曖昧さの分類：**

| 分類 | 確認する内容 |
|----------|-----------------|
| **情報の不足** | セクションの欠落、空の内容、受け入れ基準の不在 |
| **具体性の不足** | 曖昧な表現（"fast"、"scalable" など）、未定義の制約 |
| **振る舞いの明確さ** | エラー処理の抜け、未定義の状態遷移 |
| **測定可能性の問題** | 計測基準のない非機能要件 |

**例：**

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

**使い方のポイント：**

- spec.md は存在するものの洗練が必要なときに使います
- `/codexspec:review-spec` の指摘を統合します
- 1 回の実行につき最大 5 問です
- 複雑な仕様書では必要に応じて繰り返し実行します

---

### `/codexspec:analyze`

- **specify** は要件の検討を開始、または再開します。要件サマリーが正式な判断基準になるのは、明示的な確認を得た場合だけです。
- **clarify** は既存の要件や仕様の曖昧さを解消します。1 回の実行で 4 つのカテゴリにわたり、最大 5 つの質問をします。
  まず `requirements.md` を更新し、その後 `spec.md` を同期します。
- **analyze** は要件 → 仕様 → 設計 → 計画 → タスクの流れ全体を確認します。
  上位の判断基準から修正内容が一意に決まる場合は、下位成果物を自動で修正します。`requirements.md` は一切編集しません。
  未解決の指摘は報告します。タスクレビューの合格後に自動実行されますが、情報提供を目的としており、実装の合否は判定しません。

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

過去の機能に `requirements.md` がない場合は `spec.md` から分析し、元の議論の証拠がないことを明示したうえで、成果物を変更せずに結果だけを報告します。過去の `design.md` がなくても分析は続行できます。

---

### `/codexspec:checklist`

要件の完全性、明確さ、一貫性を検証するための品質チェックリストを生成します。これは「要件記述のためのユニットテスト」のようなものです。

**構文：**

```
/codexspec:checklist [focus_area]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `focus_area` | いいえ | ドメインの焦点（例: "ux"、"api"、"security"、"performance"） |

**処理内容：**

- 品質の観点ごとに整理されたチェックリストを生成します
- `FEATURE_DIR/checklists/` ディレクトリにチェックリストを作成します
- 項目は実装のテストではなく、要件の品質に焦点を当てます

**品質の観点：**

- **要件の網羅性**: 必要な要件がすべて揃っているか?
- **要件の明確さ**: 要件は具体的で曖昧さがないか?
- **要件の一貫性**: 要件同士に衝突はないか?
- **受け入れ基準の品質**: 成功基準は計測可能か?
- **シナリオの網羅性**: すべてのフローやケースが扱われているか?
- **境界ケースの網羅性**: 境界条件が定義されているか?
- **非機能要件**: パフォーマンス、セキュリティ、アクセシビリティは明記されているか?
- **依存関係と前提**: それらは文書化されているか?

**チェックリストの種類の例：**

- `ux.md` - 視覚的階層、インタラクション状態、アクセシビリティ
- `api.md` - エラー形式、レート制限、認証
- `security.md` - データ保護、脅威モデル、侵害対応
- `performance.md` - メトリクス、負荷条件、劣化

**例：**

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

**使い方のポイント：**

- チェックリストは実装の正しさではなく要件の品質を検証します
- 要件のレビューや改善に活用します
- 焦点を絞った検証のためにドメイン別のチェックリストを作成します
- 技術計画に進む前に実行します

---

### `/codexspec:tasks-to-issues`

`tasks.md` のタスクを GitHub Issues に変換し、プロジェクトの追跡と協業に役立てます。

**構文：**

```
/codexspec:tasks-to-issues
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| なし | - | 現在の機能の全タスクを変換します |

**処理内容：**

- タスク ID、説明、依存関係、ファイルパスを解析します
- 構造化された本文を持つ GitHub Issue を作成します
- タスク種別（セットアップ、実装、テスト、ドキュメント）に基づいてラベルを付与します
- Issue 間で依存関係をリンクします
- 作成した Issue を URL 付きで報告します

**前提条件：**

- GitHub リモートを持つ Git リポジトリ
- GitHub CLI (`gh`) がインストール済みで認証済みであること
- `tasks.md` ファイルが存在すること

**例：**

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

**使い方のポイント：**

- GitHub CLI の認証が必要です（`gh auth login`）
- GitHub リポジトリでのみ動作します
- リポジトリのデフォルト設定で Issue を作成します
- 実行前に重複がないか確認します

issue を作成する前に、リモートと照合して対象リポジトリを確認し、明示的な許可を得ます。タスク一覧の生成だけで公開が許可されたことにはなりません。

---

### `/codexspec:debug`

修正前に根本原因を調査.

参照 [ワークフロー](workflow.md#review-and-debugging).

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

---

### `/codexspec:reverse-spec`

既存コードに対しては、目的に応じて 2 つのコマンドを使い分けます。

| コマンド | 用途 | 出力と操作範囲 |
|---------|-----------|-----------------|
| `onboard [path]` | 既存のコードベースから再利用可能なプロジェクト知識を初期登録 | 慣行の候補と、根拠に基づいて範囲を絞った制約をプロファイルに記録。コードは読み取り専用 |
| `reverse-spec [path]` | 既存アーキテクチャの理解、または確認済みの意図とコードの比較 | 成果物の草案または差異レポート。コードは読み取り専用 |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard は観察できるコードから慣行を推論し、明示的な禁止事項がある場合にだけ制約を提案します。
慣行の候補はローカルで直ちに有効になります。制約の候補は、セッション内で保存・編集・破棄を決める必要があります。
既存の知識は保持します。初回のコードスキャンをもとに、過去の判断理由や、実際に経験したかどうか分からない落とし穴を作り出すことはありません。

Reverse-spec には 3 つのモードがあります。

- **概要**：パス未指定、またはリポジトリルートを指定した場合。調査するモジュールを選ぶために、アーキテクチャの要点を記した `design.md` と `slices.md` を作成します。
- **生成**：確認済みの基準がないモジュールパスを指定した場合。`spec.md`、`design.md`、未確定・推論段階の要件を草案として作成します。
- **照合**：確認済みの基準があるモジュールを指定した場合。`reconcile.md` を作成し、
  確認済みの仕様・設計に照らして、文書化されていない動作、未実装の仕様、意味の不一致を報告します。意図については要件を判断基準にします。

推論から作成された草案は、人による確認を経て初めて基準として使えます。
照合では、コードの修正、ドキュメントの更新、意図の判断のいずれを進めるべきかを提案しますが、自動では適用しません。

---

### `/codexspec:distill`

複数の機能で再利用できる知識を `.codexspec/profile/` に取り込み、保留中の候補を Markdown ファイルを手で編集せずにレビューします。

**構文：**

```text
/codexspec:distill [interaction segment]
/codexspec:distill review
```

**手動レビュー：**

- `/codexspec:distill review`、または抽出する新しい内容がない直接呼び出しは、`127.0.0.1` からのみ配信されるオフラインの HTML ページを開きます。ヘッダーにはこのセッションが書き込むプロジェクトディレクトリ名が表示され、並べて開いた 2 つのレビューを見分けられます。
- ページは構造化された改訂、承認、破棄、保留、統合、ステージ済み決定の完全な一覧、そして明示的な**すべて適用**に対応します。改訂と統合は、同じ操作をステージする前に最終的な Markdown の正確なプレビューを表示しなければなりません。決定の操作を使う前に、各レコードが 3 つのプレビュー状態のどれにあるか（プレビュー未実行／現在の編集内容と一致／プレビュー後に編集が変更）をページが示します。
- レコードファイルを削除する操作はすべて、その結果を明示する 2 度目の確認を求めます。破棄は適用時に削除されるファイルを、統合は削除されるメンバーレコードの件数を、下書きの破棄は失われるステージ済み決定の件数を示します。
- レコードが `vetted` になるには、人の承認と結果に基づく検証の根拠の両方が必要です。承認を選ぶ前に、保存済みの根拠がその要件を既に満たしているかどうかをページが示します。
- キューは決定内容でレコードをグループ化し、保留中のうち何件が既に片付いたかを示します。決定をステージすると次の未決定レコードへ進みます。ヘッダーのスイッチでこれを無効にできます。
- ページはキーボードで操作できます。`?` でキー一覧を表示します。バッチの適用、セッションの中止、下書きの破棄を単一キーで行うことはできません。
- ステージ済みの決定は、Git から除外された復旧可能なプロジェクト下書きに保持されます。書き込み可能なレビューはプロジェクトごとに 1 つだけです。
- 構造的に壊れた下書きは対処方法が分かる診断とともに保持され、明示的な破棄操作によってのみ削除されます。
- 適用時にソースハッシュを再確認し、いずれかのレコードが変化していればバッチ全体を拒否します。同時編集を上書きすることはなく、部分的な成功を報告することもありません。
- ページのアセットはすべて CodexSpec に同梱されます。CDN、リモートモデル呼び出し、テレメトリは一切使いません。
- ブラウザーを開けない場合、コマンドはトークンで保護されたローカル URL を出力します。ブラウザーが適さないときは明示的なテキストモードを要求してください。検証と書き込み経路は同じです。

自動 distill は非対話・非ブロッキングのままです。ページを開くことも、テキストレビューを開始することも、保存済み下書きを待つこともありません。

---

### `/codexspec:evolve`

`evolve` は、承認済み知識のうちプロジェクト外でも役立つものだけを選び、コマンド・スキルの草案を作成します。
push や、人によるレビューを受けるための貢献 PR の作成前に、明示的な承認を得ます。

```text
/codexspec:evolve
```

---

### `/codexspec:onboard`

既存コードから慣行の候補と、根拠のある制約を初期登録.

参照 [`reverse-spec`](#codexspecreverse-spec).

```text
/codexspec:onboard src/
```

---

### `/codexspec:commit-staged`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** はステージング領域の内容そのものを分析し、Conventional Commits のメッセージを生成します。
  `-p` では、コミットせずにプレビューできます。ファイルの選択とステージングは、呼び出し元のワークフローが行います。
  許可を得て実行する場合は、保護された実行環境で、コミットする内容が分析対象と一致することを再確認します。
  エージェントのコミットガイダンスは通常の会話、SDD、blueprint、auto-dev にも適用されます。
  コマンドが利用可能であるだけでは、その呼び出しにも、コミットの許可にもなりません。
- **pr** は差分をもとに、構造化された GitHub PR または GitLab MR の説明を生成します。
  `--spec` を指定すると、`spec.md` のファイルパス、またはそのファイルを指す機能ディレクトリ名やプレフィックスから、機能の文脈を追加できます。
  デフォルトでは、ホスティングプラットフォームで使うためのテキストを出力します。
- **release-notes** は Git 履歴から、Keep a Changelog のエントリとリリース本文を作成します。
  デフォルトのセクションは `[Unreleased]` で、`--version` を指定すると、そのラベルを使います。
  ステージング、コミット、バージョン更新、タグ付け、公開、リリース作成は行いません。
- **tasks-to-issues** は既存のタスクから、依存関係と受け入れ基準を含む GitHub Issue を作成します。
  認証済みの GitHub CLI が必要です。Issue のリポジトリが、設定済みのリモートと一致することも検証します。

コミットのプレビューと、許可を得て現在のチェックアウトで行うコミットには、Python 3.11+ と Git が必要です。
実行環境は CLI で初期化したプロジェクトにインストールされ、Claude プラグインにも同梱されます。
エージェントが作成する、内容の変更を伴うマージでも、ステージ済み内容の分析を行います。
履歴だけをつなぐマージでは、ツリーと親を検証しながら Git のデフォルトメッセージを維持します。
fast-forward はコミットを作成しません。

共通ヘルパー `.codexspec/scripts/commit-staged-helper.py`（またはプラグイン同梱版）には Python 3.11+ と Git が必要です。LLM を呼び出さず、Git hooks を維持し、分析後にステージ済み内容が変わっていればコミットを拒否します。一度限りの初期化でもこのランタイムは配置されますが、ワークスペースのルーティング、blueprint、auto-dev には引き続き CLI が必要です。

---

### `/codexspec:pr`

git diff から、構造化された GitHub Pull Request / GitLab Merge Request の説明を生成します。オプションで `spec.md` を統合し、SDD で追跡可能なコンテキストを盛り込むことができます。

**構文：**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `--target-branch <branch>` | いいえ | 比較対象のブランチ（デフォルト: `origin/main`） |
| `--sections <list>` | いいえ | `summary, changes, testing, verify, checklist, notes` のカンマ区切り部分集合（デフォルト: `all`） |
| `--spec <id-or-path>` | いいえ | 任意の spec 統合: 機能 ID（例: `2025-0321-1430k7-auth`、`.codexspec/specs/` 配下で解決）、または明示的な `path/to/spec.md`。省略時は git のみから生成します |
| `--output <file>` | いいえ | 説明を端末ではなくファイルに保存します |

**処理内容：**

- ターゲットブランチに対して git コンテキスト（現在のブランチ、リモート URL、先行コミット数、ファイル変更、完全な diff、コミットメッセージ）を収集します
- リモート URL からプラットフォームを自動検出します: GitHub → "Pull Request"、GitLab → "Merge Request"、その他/なし → GitHub の用語をデフォルトとし警告を出します
- `.codexspec/memory/constitution.md` が存在する場合は読み込み、ドキュメント/コードレビューの基準に説明を合わせます
- 説明の言語は `language.commit`（次に `language.output`、次に英語）を尊重します。技術用語（API、JWT、PR、MR）は適宜英語のまま残します
- `--spec` が指定された場合は、spec.md からユーザーストーリーと要件を取り出した Context セクションを追加します。それ以外は diff のみから生成します
- `--sections` に従ってセクションを出力します（Summary、Changes、Testing、Verification Steps、Pre-merge Checklist、Notes / Breaking Changes）

**例：**

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

**使い方のポイント：**

- 形式化された仕様書を持たない小さなバグ修正や変更では `--spec` を省略します
- `/codexspec:commit-staged` と組み合わせれば、同じ作業からコミットメッセージと PR 説明をまとめて生成できます
- このコマンドのエンドツーエンドの実例（spec.md のコンテキストをどう組み込むかを含む）は [PR description generator case study](../case-studies/case-study-pr-description-generator.md) を参照してください

---

### `/codexspec:release-notes`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** はステージング領域の内容そのものを分析し、Conventional Commits のメッセージを生成します。
  `-p` では、コミットせずにプレビューできます。ファイルの選択とステージングは、呼び出し元のワークフローが行います。
  許可を得て実行する場合は、保護された実行環境で、コミットする内容が分析対象と一致することを再確認します。
  エージェントのコミットガイダンスは通常の会話、SDD、blueprint、auto-dev にも適用されます。
  コマンドが利用可能であるだけでは、その呼び出しにも、コミットの許可にもなりません。
- **pr** は差分をもとに、構造化された GitHub PR または GitLab MR の説明を生成します。
  `--spec` を指定すると、`spec.md` のファイルパス、またはそのファイルを指す機能ディレクトリ名やプレフィックスから、機能の文脈を追加できます。
  デフォルトでは、ホスティングプラットフォームで使うためのテキストを出力します。
- **release-notes** は Git 履歴から、Keep a Changelog のエントリとリリース本文を作成します。
  デフォルトのセクションは `[Unreleased]` で、`--version` を指定すると、そのラベルを使います。
  ステージング、コミット、バージョン更新、タグ付け、公開、リリース作成は行いません。
- **tasks-to-issues** は既存のタスクから、依存関係と受け入れ基準を含む GitHub Issue を作成します。
  認証済みの GitHub CLI が必要です。Issue のリポジトリが、設定済みのリモートと一致することも検証します。

コミットのプレビューと、許可を得て現在のチェックアウトで行うコミットには、Python 3.11+ と Git が必要です。
実行環境は CLI で初期化したプロジェクトにインストールされ、Claude プラグインにも同梱されます。
エージェントが作成する、内容の変更を伴うマージでも、ステージ済み内容の分析を行います。
履歴だけをつなぐマージでは、ツリーと親を検証しながら Git のデフォルトメッセージを維持します。
fast-forward はコミットを作成しません。

#### リリースノートのオプション

| コマンド | リファレンス |
|---|---|
| `--version <X.Y.Z>` | 指定されたバージョンラベル。未指定時は `[Unreleased]` |
| `--from <ref>` | 開始参照。未指定時は直近の到達可能なタグ、特定可能な変更履歴のバージョン、全履歴の順に使用 |
| `--to <ref>` | 終了参照。既定値は `HEAD` |
| `--output <file>` | リリース本文の出力先。未指定時はターミナル |
| `--spec <feature>` | 任意の機能コンテキスト。機能を解決できない場合は報告し、Git 情報だけで続行 |

---

### `/codexspec:review-code`

選択した Git 変更を、マージ前の厳格な欠陥ゲートとしてレビューします。デフォルト対象は機能の完全な差分です。明示的なセレクターでコミット済み、未コミット、または単一コミットの証拠を選べますが、パスフィルターは受け付けません。

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**既定のレビュー方式：**

- デフォルトは広範な品質スコアカードではなく、変更範囲の欠陥ゲートです。
- 位置引数としてパスを指定することはできません。助言的なパス単位の品質評価には `--audit` を明示してください。

**欠陥ゲートの構文：**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code [--committed] --incremental-from <fingerprint> [--feature <feature-dir>]
```

すべての欠陥ゲート形式で `--decided-by reviewer|ask` を指定でき、その実行に限り `review.decided_by` を上書きします。

<!-- REVIEW-CODE-SYSTEM-CONTRACT -->
<!-- REVIEW-CODE-VARIANT-SEARCH -->
<!-- REVIEW-CODE-NEUTRAL-HANDOFF -->

ゲートは対象内の全成果物を棚卸しし、適用要件を評価して Scope、System Contract、Behavior、Risk、Verification の 5 パスをこの順で実行します。根拠のあるモジュール間契約と意味単位のレビューパーティションを記録し、検証済みで反復可能な根本原因ごとに、ラウンド終了前に境界を限定した関連箇所の検索を行います。6 つのレポートセクションの後に、`schema_version: "3"` を使用する機械可読な `<review-code-result>` 結果ブロック が 1 つ続きます。この 結果ブロック には対象識別子、カバレッジ、修正後に再確認する客観的な義務が含まれます。呼び出し側はこの中立な義務を新しい完全レビューに渡しますが、修正理由や以前の正しさの結論は渡しません。判定は `PASS`、`FAIL`、`INCONCLUSIVE` のいずれかです。P0-P3 の指摘はすべて `FAIL`、必須証拠またはカバレッジの不足は `INCONCLUSIVE` です。

**増分ラウンド。** 修正後は `--incremental-from <fingerprint>` で、その結果以降に変わった部分だけを再レビューします。対象は変更されたファイル、それらが関わるレビューパーティションと契約、そして引き継がれた義務です。変更がなく影響も受けないファイルは以前のカバレッジを再利用しますが、レビュアーは他の場所で見つけた欠陥も通常どおり報告します。増分の `PASS` で機能が完了することはありません。`implement-tasks` は最初に完全レビューを行い、修正のたびに増分レビューを行い、最終受け入れとして新しい完全レビューをもう一度行います。レビュー記録はリポジトリ外のユーザーキャッシュディレクトリ (`~/.cache/codexspec/review/` または `%LOCALAPPDATA%\codexspec\review\`) に書き込まれ、会話にはレポートと 結果ブロック だけが表示されます。

**判定モード。** `.codexspec/config.yml` の `review.decided_by` は、トリガーがプロジェクトの実際の利用状況の外にある指摘 (プロジェクトが決して受け取らない入力など) を誰が判断するかを決めます。既定の `reviewer` では、レビューはこれまでとまったく同じように動作します。`ask` にすると、レビューはその項目を理由に失敗とせず、保留中のシナリオ判断として報告します。`implement-tasks` は一度だけ、修正するか、そのシナリオを対象外として受け入れるかを尋ねます。回答は確定済みの `CON` または `OUT` エントリとして `requirements.md` に記録され、以降のラウンドでは再び指摘されません。

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — all required review and verification completed with no findings.
```

**適用する基準と保守提案。** 各レビューは共通ルールと選択したモードを読み、7 つの観点を評価したうえで、実際の振る舞い・契約・依存関係に必要な詳細だけを読み込みます。追跡中に見つかった未変更の依存コードも言語・フレームワーク別チェックを有効にできます。保守提案には現在の問題を示す証拠と、既存の振る舞いを保つ局所的な改善が必要です。仮想的な将来の複雑さやスタイルの数値基準だけでは修正を正当化できません。欠陥結果はバージョン 3 を維持し、同じ対象フィンガープリントに結び付いたバージョン 1 の `<review-code-maintenance>` で提案を別途報告します。単独レビューは報告のみ行い、`implement-tasks` が `workflow.auto_maintenance`（既定 `true`）に従って検証・適用します。実質的な進展がある間は修正を続け、既存の停止条件にも従います。固定の回数上限はなく、最終的な受け入れには新たな完全レビューが必要です。

真偽値を取る CLI スイッチは、大文字・小文字を区別せず、`on/true/1/yes` と `off/false/0/no` を受け付けます。前後の空白も許容されます。
値を指定せずに使うと、書き込み先チェックアウトの現在値を切り替えます。YAML には真偽値として保存します。

`codexspec init` は Claude Code と Codex 共通のレビュー資源を `.codexspec/review-code/` に配置します。`--force` は配布資源を更新し、別パスの拡張ファイルを保持します。CLI のインストールだけではプロジェクトファイルを作りません。プラグインのみの場合、プロジェクトに資源ツリーがなければ、ホストが解決したプラグインルートから同じ資源を読みます。

<!-- REVIEW-CODE-AUDIT -->

#### パス単位の品質評価

明示的な audit モードでは、現在のファイル内容全体を対象に言語の慣習に沿った分かりやすさ、正確性、堅牢性、アーキテクチャ、憲法整合性を評価します。このスコアカードは助言用であり、`implement-tasks` の完了条件にはなりません。

**構文：**

```
/codexspec:review-code --audit [paths...]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `path...` | いいえ | レビュー対象のソースファイルまたはディレクトリを 1 つ以上（スペース区切り）。省略時は `src/` |

**処理内容：**

- 拡張子から主要言語を検出し、複数言語が混在する対象では言語別のパスを実行します
- 設定が存在する場合に静的解析ツールを実行します（`ruff`/`mypy`、`eslint`/`tsc`、`go vet`/`gofmt`、`cargo check`/`cargo clippy`、`shellcheck`）。ない場合は妥当にスキップし、カバレッジ低下を報告します
- 4 つの観点を採点します: 言語の慣習に沿った明確さと簡潔さ、正確性と明示的契約、実行時の堅牢性とリソース管理、アーキテクチャと設計の完全性
- 検出したフレームワーク向けの必須サブセクションを挿入します（例: React の場合は Hooks Compliance、Rust の場合は Ownership & Borrowing、Go の場合は Goroutine & Context Discipline、C/C++ の場合は Memory & Lifetime Safety、Shell の場合は Execution Safety）
- `.codexspec/memory/constitution.md` が存在する場合は指摘をそれと照合します。ない場合は憲法軸を除外し、その重みを再配分します
- 指摘を重大度で分類します: CRITICAL、HIGH、MEDIUM、LOW（LOW の提案は合計 5 点の減点上限付き）

**例：**

```text
You: /codexspec:review-code --audit src/

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

**使い方のポイント：**

- 複数のパスを渡すことで範囲を絞ってレビューできます。例: `src/ tests/`
- スコアは参考情報です。CRITICAL/HIGH の指摘をもとに対応を判断します

---

### `/codexspec:config`

プロジェクト設定を対話的に管理します（作成/参照/変更/リセット）。これは `codexspec config` CLI のスラッシュコマンド版であり、Plugin Marketplace 経由でインストールした環境に適しています。

**構文：**

```
/codexspec:config [--view]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `--view` | いいえ | 現在の設定を変更せずに表示します。引数なしの場合は対話型管理メニューを開きます |

**処理内容：**

- `.codexspec/config.yml` のみを対象とします
- `--view`（またはメニューの "View current config"）はファイルを読みやすい形式で表示します。存在しない場合は "Configuration Not Found" と報告します
- 設定が存在する場合の対話モードでは View、Modify、Reset to defaults、Cancel を提供します
- 設定が存在しない場合は作成フローを走らせ、`output` だけの最小設定を書き出します（interaction/document/commit は `output`、次に `en` に解決されるため、`output` だけのファイルでも完全に機能します）
- 各言語の次元（output、interaction、document、commit）を個別に設定でき、`auto_next` などのワークフローオプションも切り替えられます

**作成・編集するファイル：**

```
.codexspec/config.yml
```

**例：**

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
     - workflow.auto_distill
     - workflow.auto_maintenance
     - workflow.worktrees (default on; checkout-local)
     - review.decided_by

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**使い方のポイント：**

- 何かを変更する前に `/codexspec:config --view` で現在の状態を確認します
- 新規作成やリセット時には `output` だけを書き出します。`output` と異なる値にしたい場合にのみ `interaction`/`document` を設定します
- 端末でスクリプト的に変更する場合は `codexspec config` CLI（`--set-lang`、`--set-interaction-lang`、`--set-document-lang`、`--set-commit-lang`、`--auto-next`）を使うのが適しています

対話メニューでは `workflow.auto_distill`、`workflow.auto_maintenance`、`workflow.worktrees`、`review.decided_by` も管理できます。設定変更は、各チェックアウトで個別に有効になる worktree のルーティング規則に従います。

---

### `/codexspec:quick`

小規模な変更に向けた、簡略版の要件優先 SDD フローを実行します。

**構文：**

```
/codexspec:quick [describe a small requirement]
```

**引数：**

| 引数 | 必須 | 説明 |
|----------|----------|-------------|
| `describe a small requirement` | いいえ | 小さく境界が明確な変更の短い説明（指定がない場合はプロンプトで尋ねられます） |

**処理内容：**

- スコープ（触れるファイル、モジュールの広がり、新規依存、未解決のプロダクト決定）を評価し、変更が広範あるいは複数の独立した成果物を持つ場合は標準フローを推奨します
- `/codexspec:specify` と同じタイムスタンプ規約で機能ワークスペースと `requirements.md` を作成します
- 実装に実質的な影響を与える曖昧さだけを解消し、簡潔な確認済み要約（`NEED-*`、関連する `CON-*`/`DEC-*`、`OUT-*`、未解決の `OPEN-*`）を提示します
- Confirmation Gate で止まります。要約を確認するまでは何も生成しません
- 新しい機能ディレクトリに対して生成コマンドを連鎖させます: `/codexspec:generate-spec`、`/codexspec:design-to-plan`、`/codexspec:plan-to-tasks`、`/codexspec:implement-tasks`
- 各生成コマンド自身の自動レビューループに委ねます。レビューが新たなプロダクトやアーキテクチャの決定を必要とする場合は一時停止してユーザーに尋ねます
- 機能ディレクトリ、アーティファクトのパス、レビュー結果、実装の検証結果、未解決の助言は別個に報告します

**生成するファイル：**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**例：**

```text
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → design-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**使い方のポイント：**

- Quick は本当に小さく単一の成果物を持つ変更のためにとっておきます。そうでなければ `/codexspec:specify` と標準フローを走らせます
- 確認は依然として必須です。Quick は自動化を進めるためにプロダクトの決定を推測することはありません
- いずれかの生成レビューが `NEEDS_REVISION`/`BLOCKED` を返した場合、Quick は停止して制御をユーザーに戻します

---
