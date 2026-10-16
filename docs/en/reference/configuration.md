<a id="configuration-and-internationalization"></a>

# Configuration and Internationalization

Configuration lives in `.codexspec/config.yml`. Templates stay in English;
agents write interaction text and generated artifacts in the configured languages.
The 13 standard language codes are `en`, `zh-CN`, `zh-TW`, `ja`, `ko`,
`es`, `fr`, `de`, `pt`, `ru`, `it`, `ar`, and `hi`.
The Portuguese CLI code is `pt`; localized documentation and translation
catalogs use `pt-BR`.

<a id="language-dimensions"></a>

## Language Dimensions

| Dimension | Config key | At initialization | Set later | Controls |
|-----------|------------|-------------------|-----------|----------|
| Output/base | `language.output` | `--lang` | `config --set-lang` | Fallback for the other language dimensions |
| Interaction | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | Conversation and CLI output |
| Document | `language.document` | `--document-lang` | `config --set-document-lang` | Requirements, specifications, designs, plans, tasks |
| Commit | `language.commit` | `--commit-lang` | `config --set-commit-lang` | Commit messages and Git-delivery content |

Each specific language falls back independently to `language.output`, then `en`.
`language.templates` remains `en`.

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

First-time TTY initialization prompts for the base language unless you supply
`--lang` or all three specific language options. `--force` auto-confirms other
initialization prompts; it does not suppress this language selection.
Non-TTY initialization defaults to English. Re-initialization preserves language
keys you did not explicitly set.

<a id="workflow-and-review-settings"></a>

## Workflow and Review Settings

| Setting | Default | Effect | CLI control |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | Advance passing ordinary SDD stages | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | Non-interactive knowledge capture after successful wrap-up | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | Apply verified incremental maintenance during automatic repairs | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | Isolate ordinary features and standalone maintenance | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | Who decides findings triggered outside the project's operating context | `config --decided-by reviewer\|ask` |

Boolean CLI switches accept case-insensitive `on/true/1/yes` and
`off/false/0/no`, including surrounding whitespace. A bare boolean switch toggles
the destination checkout's current value; stored YAML values are booleans.

With `review.decided_by: reviewer`, the reviewer decides defect admission.
With `ask`, an out-of-context trigger becomes a pending scenario decision: the
user decides once whether to fix it or exclude that scenario, and the confirmed
decision is retained for later rounds. Pending decisions block completion.
A single `review-code` run can override the configured mode with `--decided-by`.

Configuration writes follow worktree routing. A standalone change from the main
checkout is made in the maintenance worktree and does not immediately change
main's effective setting; changes in a feature worktree take effect there.

<details>
<summary>CLI initialization options</summary>

| Option | Meaning |
|--------|---------|
| `PROJECT_NAME` | New directory name; use `.` for the current directory |
| `--here`, `-h` | Initialize the current directory |
| `--ai`, `-a` | `claude`, `codex`, or `both`; default `claude` |
| `--lang`, `-l` | Set the base output language |
| `--interaction-lang` | Set interaction language |
| `--document-lang` | Set document language |
| `--commit-lang` | Set commit-message language |
| `--force`, `-f` | Regenerate installed artifacts and auto-confirm migration/update/compliance prompts; preserve project-authored context and unrelated configuration |
| `--no-git` | Skip Git repository initialization |
| `--debug`, `-d` | Show detailed debug output |

</details>

<details>
<summary>CLI configuration options</summary>

| Option | Meaning |
|--------|---------|
| `--set-lang`, `-l` | Set the base output language |
| `--set-interaction-lang` | Set interaction language |
| `--set-document-lang` | Set document language |
| `--set-commit-lang`, `-c` | Set commit-message language |
| `--list-langs` | List supported language codes |
| `--auto-next` | Toggle/set automatic stage advancement |
| `--auto-distill` | Toggle/set automatic knowledge capture |
| `--auto-maintenance` | Toggle/set automatic incremental maintenance |
| `--worktrees` | Toggle/set checkout-local worktree isolation |
| `--decided-by` | Set `reviewer` or `ask` review decision mode |

</details>

<details>
<summary>Configuration example</summary>

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

See [Configuration](configuration.md) and
[Internationalization](../user-guide/i18n.md) for detailed language and
setting behavior.
