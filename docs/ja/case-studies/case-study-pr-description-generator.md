# CodexSpec の使用事例: プロジェクトに PR 記述生成機能を追加する

> 過去の事例：以下の会話、途中の判断、コマンド順序、レビュー点数は当時のワークフローの記録であり、現在のコマンド仕様ではありません。現在の標準フローには独立した設計段階と `review-design` があり、`clarify` は確認済み要件を先に更新してから仕様に反映します。[現在のワークフロー](../user-guide/workflow.md)と [PR コマンドのリファレンス](../user-guide/commands.md#codexspecpr)を参照してください。

> このドキュメントは、CodexSpec プロジェクト自体に新機能を追加するために CodexSpec ツールチェーンを使った完全なプロセスを記録したもので、Spec-Driven Development (SDD) の実践例を示しています。

## 概要

**対象となる機能**: `/codexspec:pr` コマンドの追加。構造化された GitHub PR / GitLab MR の説明を生成します。(公開済みコマンドのユーザー向け概要は、[README の `/codexspec:pr` の項目](https://github.com/Zts0hg/codexspec/blob/main/README.md) を参照してください。)

**開発フロー**: `specify → generate-spec → review-spec → clarify → design-to-plan`

**主な特徴**: 開発の途中で要件の問題が浮上し、`clarify` コマンドで修正された点です。これは SDD の柔軟性を示しています。CodexSpec の **Confirmation Gate** の具体例でもあり、あなたが明示的に確認するまでは何も確定せず、一度受け入れられた意思決定も clarify のチェックポイントで再検討されて覆すことができます。

---

## ステージ 1: 初期要件の明確化 (`/codexspec:specify`)

### 初期のユーザー入力

```
I want to add a feature to the project: a new Git-related command that generates accurate, detailed, and standards-compliant GitHub PR descriptions (or MR descriptions, for GitLab). Below are two PR commands I have used in other projects, provided for reference.

[Reference Example 1 - Structured Description]
Now, acting as a project maintainer, based on all the work we have done so far, write a clear Pull Request description for this submission.
The PR description should be aimed at the other reviewers on the team and include the following sections:
1. Context
2. Implementation
3. Testing
4. How to Verify

[Reference Example 2 - Simple Description]
Based on the code diff between the current branch and origin/main, use Markdown to produce a Merge Request title and description that comply with Git conventions. (Describe in Chinese.)
```

### 明確化のプロセス

**Q1: 出力言語**

- 選択肢: プロジェクト設定に従う / 中国語 / 自動検出
- **ユーザーの選択**: プロジェクト設定に従う (現在: en)

**Q2: プラットフォームサポート**

- 選択肢: GitHub と GitLab の両方をサポート / GitHub のみ / プラットフォームを自動検出
- **ユーザーの選択**: プラットフォームを自動検出

**Q3: PR 説明の内容**

- 選択肢: 詳細な構造化説明 / 簡潔な説明 / カスタマイズ可能なテンプレート
- **ユーザーの選択**: 詳細な構造化説明 (推奨)

**Q4: 起動条件**

- 選択肢: 現在のブランチと origin/main / 未 push のコミット / 設定可能なターゲットブランチ
- **ユーザーの選択**: 設定可能なターゲットブランチ

**Q5: spec のソース**

- 選択肢: spec.md を優先 / Git 情報のみ / すべてのソースを統合
- **ユーザーの選択**: すべてのソースを統合 (推奨)

**Q6: 名前付け**

- 選択肢: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **ユーザーの選択**: codexspec.pr (推奨)

**Q7: spec が見つからない場合の扱い**

- 選択肢: 生成を続行し Context をスキップ / 先に spec 作成を促す / 警告しつつ継続
- **ユーザーの選択**: 生成を続行し Context をスキップ

**Q8: 出力方法**

- 選択肢: ターミナル出力 / ファイルに保存 / ターミナル + 任意でファイル
- **ユーザーの選択**: ターミナル + 任意でファイル (推奨)

**Q9: デフォルトのセクション**

- 選択肢: Context, Implementation, Testing, How to Verify (すべて選択)
- **ユーザーの選択**: 4 セクションすべて

**Q10: コマンドのパラメータ**

- **ユーザーの選択**: すべてのパラメータは任意
  - `--target-branch`: デフォルトは origin/main
  - `--output`: 指定がない場合はターミナル出力のみ
  - `--sections`: 指定がない場合はデフォルトに従う
  - `--no-spec`: spec.md の検索をスキップ

### 言語設定の修正

**ユーザーからのフィードバック**: 言語の挙動は `/commit-staged` コマンドに合わせるべき。すなわち、まず `config.yml` の `language.commit` を優先し、`language.commit` が未設定の場合にのみ `language.output` にフォールバックする。

**更新後の要件サマリ**:

```
Language priority: language.commit > language.output > English (default)
```

---

## ステージ 2: 仕様書ドキュメントの生成 (`/codexspec:generate-spec`)

### 生成されたドキュメントの構造

生成された `spec.md` は次のセクションを含みます。

- **概要**: 機能の概要
- **目標**: 4 つの目標
- **ユーザーストーリー**: 受け入れ基準を伴う 4 つのユーザーストーリー
- **機能要件**: 8 つの要件 (REQ-001 から REQ-008)
- **コマンドパラメータ**: 4 つのパラメータ定義
- **非機能要件**: 3 つの要件 (パフォーマンス、互換性、エラー処理)
- **受け入れ基準 (テストケース)**: 10 のテストケース
- **エッジケース**: 6 つのエッジケース
- **出力フォーマットの例**: GitHub PR と GitLab MR の例
- **対象外**: 明示的に除外した機能
- **依存関係**: 依存関係
- **関連コマンド**: 関連コマンド

### 主要な要件の抜粋

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## ステージ 3: 仕様のレビュー (`/codexspec:review-spec`)

### レビュー結果

- **総合ステータス**: ✅ Pass
- **品質スコア**: 92/100
- **準備状態**: 計画対応可

### 検出された問題

**警告 (対応推奨)**:

1. **SPEC-001**: テストファイル検出のロジックが明示的に指定されていない
2. **SPEC-002**: 複数の spec.md が存在する場合「最終更新日時」で選ぶと不正確になりうる

**提案 (あると嬉しい)**:

1. `--title` パラメータの追加を検討する
2. 出力フォーマットの検証要件を追加する
3. GitHub Enterprise の URL パターンのサポートを検討する

### レビューレポートの場所

`.codexspec/specs/2026-0613-1200ab-pr-description-generator/review-spec.md`

これは **証拠に基づくレビュー** です。上記の警告と提案はそれぞれ spec 内の具体的で特定可能なギャップに紐付き、助言項目 (あると嬉しい) は受け入れ判断に影響せず、自動変更もトリガーしません。

---

## ステージ 4: 要件の明確化と調整 (`/codexspec:clarify`) ― 重要な転換点

### 発見された問題

**ユーザーからのフィードバック**:
> spec.md の使い方に問題があることに気づきました。たとえば、ユーザーが非常に小さな変更を行う場合は、CodexSpec の標準フロー (specify → plan → tasks → implement) をたどらず、対話や Claude Code の組み込み plan モードで直接変更を行い、変更が終わったあとに別途 CodexSpec コマンドを呼び出して標準準拠の PR 説明を生成したくなります。このとき、デフォルトで「最終更新日時の spec.md」を選ぶと、今回の変更と無関係な過去の spec.md の内容を引き込んでしまうかもしれません。

これはまさに **Confirmation Gate** の実例です。先の意思決定 (「デフォルトで最終更新日時の spec.md を使う」) は記録されていましたが、覆せないという意味での確定はしていませんでした。ユーザーが現実の利用パターンという新情報とともに clarify のチェックポイントで再検討し、一度受け入れられたデフォルトは覆りました。

### 明確化 Q&A のプロセス

**Q1: spec の選択戦略**

**コンテキスト**: 現在の EC-004 は「複数の spec.md → 最終更新日時のものを使用」としている。しかし、ユーザーが SDD フローに従わず小さな変更を行った場合、最新の spec.md は今回の変更と無関係な可能性がある。

| 選択肢 | 説明 |
|--------|-------------|
| A | ユーザーが明示的に `--spec` を渡さない限り、デフォルトでは spec.md を使わない |
| B | ブランチ名で一致させる |
| C | ユーザーに選択を促す |
| D | ファイル変更で一致させる |

**ユーザーの選択**: 選択肢 A
**理由**: 誤参照を避けるため。`--spec` パラメータにより、SDD 連携を望むユーザーが明示的にオプトインできる。

---

**Q2: spec のコンテンツ抽出戦略**

**コンテキスト**: ユーザーが `--spec` を渡した場合、spec.md の構造が不完全だとどうするか?

| 選択肢 | 説明 |
|--------|-------------|
| A | ベストエフォートで抽出し、欠落セクションはスキップ |
| B | 警告し Context をスキップ |
| C | 完全な構造を要求し、そうでなければエラーにする |

**ユーザーの選択**: 選択肢 A
**理由**: spec のフォーマット問題でワークフローを止めないため。

---

**Q3: テストファイルの検出**

**コンテキスト**: Testing セクションはどのようにテストファイルを検出すべきか?

| 選択肢 | 説明 |
|--------|-------------|
| A | 一般的なディレクトリパターン (tests/, test/) |
| B | 言語非依存のヒューリスティクス (ディレクトリ + ファイル名パターン) |
| C | 能動的な検出は行わず、コミットメッセージからのみ推論 |

**ユーザーの選択**: 選択肢 B
**理由**: 様々な言語の多様なプロジェクト構造をカバーできるため。

---

**Q4: PR タイトルの生成**

**コンテキスト**: PR のタイトルはどのように生成すべきか?

| 選択肢 | 説明 |
|--------|-------------|
| A | ブランチ名のパースを優先 |
| B | 最初のコミットメッセージを優先 |
| C | 統合 (git diff + ブランチ名 + コミットメッセージ) |

**ユーザーの選択**: 選択肢 C
**理由**: 最初のコミットは変更の一部しか表しておらず、ブランチ名は強い命名規律を前提とする。参照できる git 情報とコード変更が豊富にある場合、統合的に分析する方がより正確。

---

**Q5: 検証コマンドの生成**

**コンテキスト**: 「How to Verify」セクションは検証コマンドをどう生成すべきか?

| 選択肢 | 説明 |
|--------|-------------|
| A | 汎用テンプレート |
| B | プロジェクト検出 (pyproject.toml → pytest, package.json → npm test) |
| C | コミットメッセージから推論 |

**ユーザーの選択**: 選択肢 B
**理由**: プロジェクト検出の方が実用的な検証コマンドを生成できるため。

---

### 明確化セッションのサマリ

| 質問 | 決定 | 影響 |
|----------|----------|--------|
| spec の選択戦略 | `--spec` でオプトイン | REQ-007, EC-004, パラメータ表 |
| spec のコンテンツ抽出 | ベストエフォートで抽出 | REQ-005b, EC-004c |
| テストファイル検出 | 言語非依存のヒューリスティクス | REQ-006b |
| PR タイトルの生成 | 統合的分析 | REQ-008a |
| 検証コマンドの生成 | プロジェクトファイル検出 | REQ-010 |

### 主要な変更: パラメータロジックの反転

```
Original design: --no-spec (skip spec)
New design:      --spec (enable spec, opt-in)
```

この変更は、本事例で Confirmation Gate が働いたことを最も明確に示しています。当初は spec をデフォルトで使い、不要な場合に `--no-spec` で無効にする方針でした。しかし、ユーザーがその方針では支障をきたす実際のワークフローを示したため、方針を見直し、明示的に指定した場合だけ spec を使う方式へ変更して再確認しました。

---

## ステージ 5: 技術実装計画 (`/codexspec:design-to-plan`)

### 計画の概要

**実装アプローチ**: Markdown テンプレートファイル (`/codexspec:commit-staged` と一貫)

**新規依存関係なし** ― 機能はスラッシュコマンドのテンプレートで提供され、Python コードは不要です。

### 技術的意思決定のサマリ

| 決定 | 選択 | 理由 |
|----------|--------|--------|
| 実装アプローチ | Markdown テンプレート | 既存コマンドと一貫、保守が容易 |
| 言語優先順位 | commit > output > en | `/commit-staged` と一貫 |
| プラットフォーム検出 | リモート URL のパース | シンプルで信頼性が高い |
| spec 連携 | オプトイン (`--spec`) | 誤参照を回避 |
| コンテンツ抽出 | ベストエフォート | ワークフローを止めない |
| テスト検出 | ディレクトリ + ファイル名パターン | 言語非依存 |
| タイトル生成 | 統合的分析 | 最も正確 |
| コマンド検出 | プロジェクトファイル検出 | より実用的 |
| 出力モード | ターミナル優先、任意でファイル | 柔軟 |

### 実装フェーズ

1. **フェーズ 1**: テンプレート作成 (YAML frontmatter、言語設定、Git コンテキスト)
2. **フェーズ 2**: コア機能 (Spec 連携、テスト検出、コマンド検出、タイトル生成)
3. **フェーズ 3**: エッジケース対応
4. **フェーズ 4**: テスト
5. **フェーズ 5**: ドキュメントの更新

### ファイル一覧

**作成**:

- `templates/commands/pr.md`

**修正**:

- `CLAUDE.md` - コマンドの説明を追加
- `README.md` - コマンドを一覧に追加

**テスト**:

- `tests/test_pr_template.py`

---

## 完全なフロー図

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CodexSpec SDD Development Flow                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:specify                                                     │
│  ├─ Clarify requirements through Q&A                                    │
│  ├─ User provides reference examples                                    │
│  └─ 10 questions covering language, platform, content, parameters, etc. │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:generate-spec                                               │
│  ├─ Generate a complete spec.md                                         │
│  ├─ 4 user stories, 8 functional requirements, 10 test cases            │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/spec.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:review-spec                                                 │
│  ├─ Quality score: 92/100                                               │
│  ├─ Found 2 warnings (test-file discovery, multi-spec handling)         │
│  └─ Status: Pass, can proceed to planning                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:clarify  (Critical adjustment)                              │
│  ├─ User surfaces a real-world usage issue                              │
│  ├─ 5 clarification questions, all answered                             │
│  ├─ Key change: --no-spec → --spec (opt-in)                             │
│  └─ Added 5 requirements (REQ-005b, 006b, 008a, 010, updated 007)       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:design-to-plan                                                │
│  ├─ Update the technical implementation plan                            │
│  ├─ 9 technical decisions, including 5 new ones                         │
│  ├─ 5 implementation phases                                             │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/plan.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Subsequent steps (not completed in this session)                       │
│  ├─ /codexspec:review-plan - Validate plan quality                      │
│  ├─ /codexspec:plan-to-tasks - Break down into executable tasks         │
│  └─ /codexspec:implement-tasks - Execute the implementation             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 主な学び

### 1. clarify ステージの価値

この事例は `clarify` コマンドの極めて重要な役割を示しています。

- **ユーザーが使用中に現実の問題を発見** ― 小規模な変更の場面で spec.md を誤用するリスク
- **明確化の Q&A を通じて設計上の欠陥を解決** ― 自動検出からオプトインへの移行
- **要件変更が体系的に記録される** ― すべての変更は spec.md の Clarifications セクションに保存

### 2. SDD フローの柔軟性

- 線形なフローではなく、どの段階でも戻って調整できる
- `clarify` は `review-spec` のあと、`design-to-plan` の前に挿入できる
- 仕様書ドキュメントも技術計画も、変更を反映して更新される

### 3. パラメータ設計の進化

```
Initial design:
  --no-spec: skip spec.md (used by default)

Final design:
  --spec: enable spec.md (not used by default)
```

この変更は「デフォルトで SDD ワークフロー」から「非 SDD ワークフローもサポート」への設計上のシフトを反映しており、ツールをより汎用的にしています。

### 4. ドキュメントの出力

| ステージ | 出力ファイル | 内容 |
|-------|-------------|---------|
| generate-spec | spec.md | 完全な仕様書ドキュメント |
| review-spec | review-spec.md | 品質レビューレポート |
| clarify | (spec.md を更新) | 明確化の記録と要件の更新 |
| design-to-plan | plan.md | 技術実装計画 |

---

## 付録: コマンドクイックリファレンス

```bash
# 1. Initial requirement clarification
/codexspec:specify

# 2. Generate the specification document
/codexspec:generate-spec

# 3. Review the specification quality
/codexspec:review-spec

# 4. Clarify/adjust requirements (optional; use when an issue is found)
/codexspec:clarify [issue description]

# 5. Generate the technical plan
/codexspec:design-to-plan

# 6. Review the plan quality (optional)
/codexspec:review-plan

# 7. Break down into tasks
/codexspec:plan-to-tasks

# 8. Execute the implementation
/codexspec:implement-tasks
```

---

*このドキュメントは CodexSpec SDD ワークフローで生成され、実際の開発の対話を記録したものです。*
