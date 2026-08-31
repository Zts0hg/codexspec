# Confirmed Requirements: blueprint-auto-dev

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0829-2159yg`
**Status**: Confirmed
**Last Confirmed**: 2026-08-30

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Develop confirmed blueprint requirements without user intervention

- **Status**: confirmed
- **Statement**: After a blueprint requirement is confirmed, `auto-dev` MUST autonomously advance it
  through requirements, specification, design, planning, task generation, implementation, testing,
  code review, and review-driven repair. It MUST NOT request user decisions during normal execution.
- **Rationale**: All decisions that require product-owner input are resolved while preparing the
  blueprint, so development can proceed without manual handoffs.
- **User Evidence**: "到了auto-dev阶段，完全可以自主推进"
- **Confirmed At**: 2026-08-29

### NEED-002: Build new blueprint requirements in product context

- **Status**: confirmed
- **Statement**: The `blueprint` command MUST use the same interactive requirements discovery and
  explicit confirmation approach as `specify`, but MUST append the resulting confirmed requirements
  content to `.codexspec/blueprint.md` with `pending` status instead of creating a feature directory
  or starting development. Users MUST be able to repeat this process. While discussing a new
  requirement, `blueprint` MUST consider relevant implemented features under `.codexspec/specs/`
  and every existing blueprint requirement, including pending work, so the new requirement remains
  consistent with the product's implementation and planned evolution.
- **Rationale**: New product ideas naturally build on previously implemented and previously planned
  functionality.
- **User Evidence**: "在blueprint阶段会结合之前的实现和之前整理的待实现功能进行新功能的blueprint讨论"
- **Confirmed At**: 2026-08-29

### NEED-003: Operate on the shared blueprint from any checkout

- **Status**: confirmed
- **Statement**: When invoked from any checkout of the repository, both `blueprint` and `auto-dev`
  MUST locate and operate on the same dedicated branch, worktree, and
  `.codexspec/blueprint.md` instead of creating or modifying a blueprint copy in the caller's
  checkout.
- **Rationale**: A single physical blueprint file lets both commands observe current development
  states without synchronizing copies across branches.
- **User Evidence**: The user confirmed that both commands share one dedicated branch, worktree,
  and `blueprint.md` while running concurrently.
- **Confirmed At**: 2026-08-29

### NEED-004: Continue with requirements appended during the current run

- **Status**: confirmed
- **Statement**: After completing one requirement, `auto-dev` MUST re-read the shared
  `blueprint.md` and process the first requirement whose `Development Status` is `pending`. It MUST
  continue this cycle until a fresh read finds no pending requirement. Requirements appended while
  `auto-dev` is running therefore join the same run in document order.
- **Rationale**: Users can continue planning while automatic development is running, and newly
  confirmed work should enter the existing development sequence without restarting the command.
- **User Evidence**: "采用‘每完成一个需求就重新读取 blueprint，直到没有 pending 需求才结束’"
- **Confirmed At**: 2026-08-29

### NEED-006: Run repeated autonomous Requirements-First SDD chains

- **Status**: confirmed
- **Statement**: For each iteration, `auto-dev` MUST re-read `blueprint.md` and select the first
  requirements content block whose `Development Status` is `pending`. All blocks in blueprint are
  already confirmed; there is no unconfirmed block and no independent `requirements.md` file at
  this point. `auto-dev` MUST create the feature directory named from the block's permanent Feature
  ID and feature name, extract the selected block's content after its three blueprint-managed
  lines, write that content as the new feature's `requirements.md`, and autonomously run the
  existing Requirements-First SDD sequence and pass gates through specification, design,
  implementation planning, task generation, implementation, testing, code review, and
  review-driven repair. After completion, it repeats from a fresh read of blueprint.
- **Rationale**: `auto-dev` is the continuous multi-requirement form of the existing single-feature
  SDD workflow with automatic stage advancement.
- **User Evidence**: "auto-dev就是 连续多次的 requirements first sdd + auto_next 的流程。"
- **Confirmed At**: 2026-08-30

### NEED-007: Resume an interrupted in-progress requirement

- **Status**: confirmed
- **Statement**: When `auto-dev` starts and `blueprint.md` contains an `in_progress` requirement,
  it MUST resume that requirement before selecting any `pending` requirement. It MUST read the
  recorded `Feature Directory`, inspect the existing SDD documents, code changes, and verification
  results, and continue from the first unfinished or no-longer-passing stage. It MUST NOT change the
  requirement back to `pending` or create a new feature directory. After the resumed requirement
  reaches `completed`, `auto-dev` MUST continue with the first pending requirement in document
  order.
- **Rationale**: An unexpected process termination must not discard completed development work or
  cause the same requirement to be initialized twice.
- **User Evidence**: "下一次运行时应当先读取其 Feature Directory，根据已有 SDD 文档、代码和检查结果继续未完成的阶段；完成后再处理第一个 pending 需求。"
- **Confirmed At**: 2026-08-30

### NEED-008: Preserve unfinished work when an SDD stage cannot pass

- **Status**: confirmed
- **Statement**: When an SDD stage or code review does not pass, `auto-dev` MUST first revise,
  repair, and re-run the applicable checks autonomously under the existing workflow's progress and
  retry rules. If the existing stopping conditions are reached, including repeated unsuccessful
  repairs, consecutive rounds without substantive progress, or persistent unavailable verification,
  `auto-dev` MUST stop the current run without asking the user, leave the requirement
  `in_progress`, preserve its Feature Directory, SDD documents, code, and check evidence, and MUST
  NOT start a later pending requirement. The next invocation MUST resume this requirement under
  NEED-007.
- **Rationale**: Automatic development cannot report completion without satisfying the existing
  pass conditions, but an unsuccessful run also must not discard work or require another blueprint
  development state.
- **User Evidence**: Explicitly confirmed autonomous repair followed by stop-and-resume behavior
  when the existing SDD stopping conditions are reached.
- **Confirmed At**: 2026-08-30

### NEED-009: Support repeated integration without rebuilding the fixed branch

- **Status**: confirmed
- **Statement**: Developers or their general-purpose agents MUST be able to integrate the dedicated
  branch into the default branch at any selected committed point. After such an integration,
  `auto-dev` MUST keep using the existing fixed branch and worktree rather than rebuilding them.
  Once the latest default branch has been synchronized back into the fixed branch, a later PR or MR
  file diff MUST contain only changes for requirements whose code is not already present in the
  target default branch.
- **Rationale**: Continuous automatic development should survive repeated delivery checkpoints
  without replaying already integrated code during later reviews.
- **User Evidence**: "只要 code changes / file change 只包含其他尚未合并的需求，不影响code review即可。"
- **Confirmed At**: 2026-08-30

### NEED-010: Show the shared blueprint from the CLI

- **Status**: confirmed
- **Statement**: CodexSpec MUST provide a read-only `codexspec show-blueprint` CLI command. Starting
  from the current project, it MUST verify that the current location belongs to a Git repository,
  that the fixed `codexspec/auto-dev` branch exists, that
  `worktree-for-codexspec-auto-dev` exists and uses that branch, and that its
  `.codexspec/blueprint.md` exists. When every check passes, it MUST write the complete blueprint
  content directly to standard output. When a check fails, it MUST write a specific diagnostic to
  standard error and return a non-zero exit status.
- **Rationale**: Developers need a direct terminal command for inspecting the one current blueprint
  without locating the external worktree manually.
- **User Evidence**: Explicitly confirmed the `show-blueprint` command name and proposed discovery,
  validation, output, and failure behavior.
- **Confirmed At**: 2026-08-30

### NEED-005: Let an agent split completed requirements into delivery branches

- **Status**: superseded
- **Replaced By**: OUT-003
- **Statement**: Before final integration, a developer MUST be able to ask an agent to select one or
  more completed requirements, analyze the dedicated branch's Git history, create the requested
  target branches, and cherry-pick each requirement's implementation commits in their existing Git
  order. The developer MUST NOT need to collect or order commit hashes manually.
- **Rationale**: The dedicated branch supports continuous development, while agent-driven splitting
  lets teams integrate completed requirements in separate batches.
- **User Evidence**: "开发者需要拆分合并时，也不是他们手动拆分，而是他们驱动agent来进行拆分和commit分析和cheery pick"
- **Confirmed At**: 2026-08-30

## Constraints

### CON-001: Resolve user-owned decisions before automatic development

- **Status**: confirmed
- **Statement**: Blueprint discovery MUST resolve every product direction, option, constraint, and
  detail that requires a user decision before the requirement can be marked ready for `auto-dev`.
- **User Evidence**: "所有需要用户决定的方向、选型和细节都要在blueprint阶段确定下来"

### CON-002: Restrict changes by development status

- **Status**: confirmed
- **Statement**: The `blueprint` command MAY modify, delete, or reorder only requirements whose
  `Development Status` is `pending`. Requirements marked `in_progress` or `completed` MUST remain
  visible for context but MUST NOT be modified, deleted, or moved by `blueprint`.
- **User Evidence**: The user explicitly agreed that pending requirements remain editable while
  in-progress and completed requirements are read-only.

### CON-003: Protect every concurrent blueprint modification

- **Status**: confirmed
- **Statement**: `blueprint` and `auto-dev` MAY run concurrently, but every operation that reads a
  requirement state and modifies `blueprint.md` MUST be serialized against other blueprint
  modifications. After gaining exclusive modification access, the command MUST re-read and
  revalidate the current document before writing so it cannot overwrite another command's update.
- **User Evidence**: "两个命令可以同时运行，但共享同一个专用 branch、worktree 和 blueprint.md，并对每次 blueprint 修改进行并发保护。"

### CON-004: Develop only one requirement at a time

- **Status**: confirmed
- **Statement**: `auto-dev` MUST develop requirements sequentially. It MUST complete the current
  in-progress requirement before starting the next pending requirement in blueprint document order.
  Concurrent blueprint-only commits MAY appear between the current requirement's implementation
  commits without changing that implementation order.
- **User Evidence**: The user provided the expected linear history: multiple commits for requirement
  1 with blueprint commits interleaved, followed by requirement 2 commits, then later requirements.

### CON-005: Serialize Git writes in the shared worktree

- **Status**: confirmed
- **Statement**: Blueprint document mutations MAY be prepared while automatic development runs,
  but operations that mutate Git state in the dedicated worktree, including staging, committing,
  and merging, MUST be serialized. A blueprint write or commit MUST wait while a main-branch merge
  or another Git write is active, and feature commits MUST stage only their intended paths.
- **User Evidence**: Confirmed as part of the fixed-worktree synchronization proposal.

### CON-006: Use the complete feature directory name

- **Status**: confirmed
- **Statement**: A feature directory name MUST combine the permanent Feature ID and the normalized
  feature name as `<feature-id>-<feature-name>`. For example, Feature ID `2026-0813-1143el` and
  feature name `release-notes` MUST use
  `.codexspec/specs/2026-0813-1143el-release-notes/`; a directory named only from the Feature ID is
  invalid. The blueprint `Feature Directory` field MUST store this complete project-relative path.
- **User Evidence**: "feature 目录名是 feature id + feature name，比如
  \"2026-0813-1143el-release-notes\""

### CON-007: Allow only one auto-dev run per repository

- **Status**: confirmed
- **Statement**: Only one `auto-dev` process MAY run for a repository at a time. It MUST hold an
  exclusive run lock for its complete invocation. A second `auto-dev` invocation MUST detect the
  active process, report that automatic development is already running, and exit immediately
  instead of waiting or developing in parallel. The run lock MUST release automatically when its
  owning process exits, including unexpected termination. This run lock MUST NOT prevent
  `blueprint` from running concurrently under the separate short-lived blueprint modification
  lock.
- **User Evidence**: Explicitly confirmed the proposed one-active-`auto-dev` behavior and automatic
  lock release.

### CON-008: Keep show-blueprint read-only and lock-free

- **Status**: confirmed
- **Statement**: `codexspec show-blueprint` MUST NOT create or modify a branch, worktree, or file;
  MUST NOT fetch or merge Git history; and MUST NOT acquire the blueprint modification lock or any
  separate read lock. It MUST output the complete `.codexspec/blueprint.md` snapshot visible when
  it reads the file. Blueprint helper writes MUST use atomic file replacement so a concurrent
  lock-free reader observes either the complete previous file or the complete replacement file,
  never partially written content.
- **User Evidence**: "确认删除CLI命令 show-blueprint 的读取锁设计。"

## Decisions

### DEC-001: Keep three development states in the blueprint

- **Status**: confirmed
- **Decision**: Each requirement stored in `blueprint.md` MUST include a document-level
  `Development Status` field with exactly three values: `pending`, `in_progress`, and
  `completed`. It MUST also include a `Feature Directory` field that records the corresponding
  `.codexspec/specs/<feature-id>-<feature-name>/` directory after development starts.
- **Alternatives Rejected**: Removing the requirement from `blueprint.md` when development starts;
  adding separate `blocked`, `failed`, `paused`, or `retrying` blueprint states.
- **Reason**: The three states are sufficient to distinguish work that has not started, work with
  an existing feature directory, and work that has completed. Stage-specific review and failure
  results remain in the feature's own SDD artifacts rather than being duplicated in the blueprint.
- **User Evidence**: "同意保留三个最基本的开发状态，并且同意增加 Feature Directory 来关联到对应的 feature id 目录"
- **Confirmed At**: 2026-08-29

### DEC-002: Resolve unspecified implementation details autonomously

- **Status**: confirmed
- **Decision**: When `auto-dev` encounters uncertainty, it MUST inspect the applicable task, plan,
  design, specification, and confirmed requirements in that order, without contradicting a higher
  level document. If the confirmed requirements do not specify the detail and the choice does not
  change product intent, `auto-dev` MUST choose an established software engineering best practice
  and continue without asking the user.
- **Alternatives Rejected**: Asking the user to decide normal design or implementation details
  during `auto-dev`.
- **Reason**: The blueprint phase is the user decision boundary; later SDD stages translate that
  confirmed intent into an implementation and validate it autonomously.
- **User Evidence**: "所有不确定的内容可以层层回溯到requirements进行确认，如果没有提及则应该自行选择一个软件开发工程的最佳实践"
- **Confirmed At**: 2026-08-29

### DEC-003: Develop requirements in blueprint document order

- **Status**: confirmed
- **Decision**: The order of requirement sections in `blueprint.md` MUST be the implementation
  order. `auto-dev` MUST process pending requirements in that order and MUST NOT assign separate
  priorities, infer a different order, or reorder requirements dynamically.
- **Alternatives Rejected**: Adding a `Priority` field; allowing `auto-dev` to calculate or change
  the implementation order.
- **Reason**: Each newly appended requirement is discussed in the context of earlier implemented
  and planned functionality. Any prerequisite requirement or order adjustment belongs in the
  blueprint phase and is represented by moving the complete requirement sections in the document.
- **User Evidence**: "auto-dev跟blueprint命令应该遵守 需求在文档中的顺序就是实现顺序 的约定"
- **Confirmed At**: 2026-08-29

### DEC-004: Use one dedicated branch and worktree as the blueprint location

- **Status**: confirmed
- **Decision**: The project MUST use one fixed, dedicated branch and worktree as the location of
  `blueprint.md` and all automatic development work. The two commands MAY execute concurrently
  against that worktree; they MUST NOT require the caller's current checkout to switch branches.
- **Alternatives Rejected**: Maintaining independent blueprint copies on the caller's branch;
  preventing `blueprint` from running for the entire duration of `auto-dev`.
- **Reason**: A shared worktree provides immediate visibility of current states while still
  allowing users to continue planning pending requirements during automatic development.
- **User Evidence**: The user explicitly confirmed the shared dedicated branch/worktree model and
  per-modification concurrency protection.
- **Confirmed At**: 2026-08-29

### DEC-005: Assign the permanent Feature ID during blueprint discovery

- **Status**: confirmed
- **Decision**: When `blueprint` confirms and appends a requirement, it MUST assign the requirement
  its permanent `Feature ID`. The ID MUST remain unchanged when a pending requirement is edited,
  renamed, or moved. Agent-to-helper operations MUST use this ID as the only requirement locator,
  and `auto-dev` MUST reuse it as the prefix of the corresponding
  `<feature-id>-<feature-name>` feature directory name.
- **Alternatives Rejected**: Locating requirements by mutable titles or document positions; adding
  a separate blueprint-specific identifier.
- **Reason**: One stable identifier lets concurrent operations target the correct requirement after
  document edits and avoids maintaining duplicate identity systems.
- **User Evidence**: Explicitly confirmed using the `Feature ID` generated during blueprint work as
  the permanent and unique requirement identifier.
- **Confirmed At**: 2026-08-30

### DEC-006: Use a versioned JSON contract between the agent and helper

- **Status**: superseded
- **Replaced By**: DEC-007
- **Decision**: Every agent-to-helper request MUST be a JSON object containing
  `protocol_version`, `operation`, `feature_id`, `expected_blueprint_hash`, and an
  operation-specific `payload`. The helper MUST locate the dedicated blueprint itself and MUST NOT
  accept an arbitrary blueprint path. Every response MUST be versioned JSON with one of four
  results: `applied`, `conflict`, `rejected`, or `invalid_request`, plus the affected `feature_id`,
  applicable document hashes, and structured error details when the operation is not applied.
- **Alternatives Rejected**: Passing an entire replacement `blueprint.md`; accepting an unrestricted
  patch or arbitrary target path as the helper contract.
- **Reason**: A versioned, operation-specific contract is machine-validated, concurrency-aware, and
  prevents the helper from becoming a general-purpose file writer.
- **User Evidence**: Explicitly confirmed the proposed versioned JSON request and response format.
- **Confirmed At**: 2026-08-30

### DEC-007: Use operation-specific JSON for blueprint document changes

- **Status**: confirmed
- **Decision**: Agent-to-helper requests MUST use versioned, operation-specific JSON. Every request
  MUST contain `protocol_version`, `operation`, `expected_blueprint_hash`, and a strictly validated
  `payload`. Requests that modify an existing requirement MUST also contain its permanent
  `feature_id`; `append_requirement` MUST omit that field because the helper generates and returns
  the new `Feature ID` while holding exclusive modification access. The helper MUST locate the
  dedicated blueprint itself and MUST NOT accept an arbitrary target path.
- **Document Operations**:
  - `append_requirement`: append one complete new requirements content block; payload contains
    `feature_name` and `requirements_markdown`; the helper generates and inserts its `Feature ID`.
  - `replace_pending_requirement`: replace the complete requirements content of an existing pending
    block while preserving its `Feature ID`; this one operation covers additions, deletions, and
    edits inside that content.
  - `delete_pending_requirement`: delete one complete pending requirements block; payload is an
    empty object.
  - `move_pending_requirement`: move one complete pending requirements block; payload identifies
    the new position and the existing requirement used as the position reference.
- **Response**: The helper MUST return versioned JSON with `applied`, `conflict`, `rejected`, or
  `invalid_request`, the generated or targeted `feature_id` when available, applicable document
  hashes, and structured error details when no change is applied.
- **Alternatives Rejected**: Requiring a `Feature ID` before append; separate operations for editing
  individual entries inside a requirements content block; accepting a whole-blueprint replacement,
  unrestricted patch, or arbitrary target path.
- **Reason**: The contract distinguishes creating a document from targeting an existing document,
  while letting the agent own requirement content and the helper enforce identity, status, ordering,
  concurrency, and safe file replacement.
- **User Evidence**: Explicitly confirmed the four document operations and full-document replacement
  for internal edits after clarifying when a `Feature ID` exists.
- **Confirmed At**: 2026-08-30

### DEC-008: Separate agent-authored requirements from helper-managed metadata

- **Status**: confirmed
- **Decision**: The `append_requirement` payload MUST contain exactly `feature_name` and
  `requirements_markdown`. The agent-authored Markdown MUST omit `Feature ID`, `Development Status`,
  and `Feature Directory`. While holding exclusive modification access, the helper MUST generate
  and insert the permanent `Feature ID`, initialize `Development Status` to `pending`, initialize
  `Feature Directory` to `not-created`, and insert the separator between blueprint entries.
  When `auto-dev` creates the feature's `requirements.md`, it MUST copy the generated `Feature ID`
  and requirements content but MUST omit the blueprint-only `Development Status` and
  `Feature Directory` fields.
- **Alternatives Rejected**: Requiring the agent to supply a generated-ID placeholder; allowing the
  agent to set helper-managed development metadata; copying blueprint-only state into the feature's
  requirements record.
- **Reason**: The agent owns requirement meaning and wording, while the helper owns identity,
  development state, placement, and concurrency-sensitive file structure.
- **User Evidence**: Explicitly confirmed the proposed field ownership for append and feature-copy
  behavior.
- **Confirmed At**: 2026-08-30

### DEC-009: Use exact payload shapes for pending-document changes

- **Status**: confirmed
- **Decision**: The remaining pending-document operations MUST use exact payload objects and MUST
  reject missing, extra, or conditionally invalid fields:
  - `replace_pending_requirement` MUST contain exactly `feature_name` and `requirements_markdown`.
    The helper MUST preserve the existing `Feature ID`, `pending` status, and `not-created` feature
    directory, and MUST reject helper-managed metadata in the agent-authored Markdown.
  - `delete_pending_requirement` MUST use an empty payload object because the top-level
    `feature_id` already identifies the complete document to remove.
  - `move_pending_requirement` MUST use either `{"position": "first_pending"}`,
    `{"position": "last_pending"}`, or an object whose `position` is `before` or `after` and whose
    `reference_feature_id` names the position reference. A reference ID is required only for
    `before` and `after`. Both the moved and reference requirements MUST be `pending`.
- **Alternatives Rejected**: Partial Markdown patches; optional or nullable position references;
  moving pending requirements relative to in-progress or completed requirements.
- **Reason**: Exact operation shapes keep document updates predictable and let the helper validate
  each permitted change without interpreting free-form instructions.
- **User Evidence**: Explicitly confirmed all three proposed payload structures and validation
  rules.
- **Confirmed At**: 2026-08-30

### DEC-010: Use one update_status operation for development state changes

- **Status**: confirmed
- **Decision**: The helper contract MUST provide one `update_status` operation rather than separate
  start and completion operations. Its payload MUST contain `expected_status` and `new_status`.
  For `pending` to `in_progress`, it MUST also contain `feature_directory`; for `in_progress` to
  `completed`, it MUST omit `feature_directory` and preserve the value already recorded.
- **Allowed Transitions**: Only `pending` to `in_progress` and `in_progress` to `completed` are
  valid. The helper MUST reject every other transition, reject a current status that differs from
  `expected_status`, require the feature directory to be under `.codexspec/specs/` and have the
  exact `<feature-id>-<feature-name>` directory name represented by the current requirements block,
  and reject unknown or conditionally invalid fields.
- **Alternatives Rejected**: Separate `start_requirement` and `complete_requirement` operations;
  an unrestricted status setter.
- **Reason**: Status changes are one operation with two explicitly validated forms. Keeping the
  operation name visible in the complete request avoids confusing a payload with a standalone
  command.
- **User Evidence**: Explicitly confirmed the corrected `update_status` request shapes.
- **Confirmed At**: 2026-08-30

### DEC-011: Return one of four strictly separated helper results

- **Status**: confirmed
- **Decision**: Helper responses MUST be versioned JSON and MUST classify each request in this
  order: malformed or schema-invalid input as `invalid_request`; stale file hash or changed
  expected state as `conflict`; a structurally valid request that violates a blueprint rule as
  `rejected`; otherwise a successfully persisted change as `applied`.
- **Applied Response**: MUST include `protocol_version`, `result`, `operation`, `feature_id`,
  `previous_blueprint_hash`, `blueprint_hash`, and operation-specific `data`. Delete success uses an
  empty `data` object.
- **Conflict Response**: MUST include `protocol_version`, `result`, `operation`, `feature_id`, the
  current `blueprint_hash`, and `error`.
- **Rejected Response**: MUST include `protocol_version`, `result`, `operation`, `feature_id`, the
  current `blueprint_hash`, and `error`. This result covers valid requests that cannot legally be
  applied, such as changing a non-pending document, using an invalid move reference, requesting an
  unsupported state transition, or supplying a mismatched feature directory.
- **Invalid Request Response**: MUST include `protocol_version`, `result`, and `error`, but MUST omit
  top-level `operation`, `feature_id`, and `blueprint_hash` because blueprint processing has not
  begun. This result covers malformed JSON, unsupported protocol versions, missing required fields,
  wrong field types, conditionally invalid fields, and unexpected fields.
- **Error Object**: Every non-applied response MUST contain `error.code`, `error.message`, and
  `error.details`. `details` MUST be an empty object when there is no additional information and
  MUST NOT be `null`.
- **Alternatives Rejected**: Treating all failures as one generic error; accepting malformed input
  as a business-rule rejection; returning optional fields with `null` values.
- **Reason**: The fixed classification tells the agent whether to correct its request, re-read and
  retry, stop because an operation is forbidden, or continue after a successful write.
- **User Evidence**: Explicitly confirmed the complete response structures, examples, and result
  classification order.
- **Confirmed At**: 2026-08-30

### DEC-012: Store blueprint entries as prefixed requirements content blocks

- **Status**: confirmed
- **Decision**: `blueprint.md` MUST consist only of confirmed requirements content blocks separated
  by an independent line containing `---`. After trimming a block, its first three field lines MUST
  be `Feature ID`, `Development Status`, and `Feature Directory` in that order. The remaining
  Markdown is the requirements content and MUST be directly writable as the feature directory's
  newly created `requirements.md` without content transformation. The `blueprint` agent MUST ensure
  that content has the complete organization produced by `specify` before asking the helper to
  persist it.
- **Feature ID Duplication**: The blueprint-managed first line and the embedded requirements
  content MUST each contain the same `Feature ID`. The helper MUST generate both values during
  append and MUST reject a replacement or parsed block when the two values differ.
- **Parsing Rule**: The helper MUST normalize supported line endings and treat only an independent
  `---` line between blocks as a separator. Requirements content MUST NOT contain an independent
  `---` line internally. No free-form content may appear between requirements blocks. After the
  three managed fields, the helper MUST treat every remaining line as requirements content and
  MUST NOT require or interpret a document title, heading, section name, or other content keyword.
- **Extraction Rule**: `auto-dev` MUST remove the first three blueprint-managed field lines from the
  selected block, trim the remaining Markdown, and write it directly as `requirements.md`.
- **Alternatives Rejected**: Removing the embedded `Feature ID` and reconstructing the requirements
  content during extraction; allowing arbitrary prose between blocks or the reserved separator
  inside requirements content.
- **Reason**: The fixed three-line prefix keeps blueprint parsing and status updates mechanical,
  while the embedded document remains byte-for-byte compatible with the existing SDD workflow
  after trimming.
- **User Evidence**: Explicitly confirmed the three-field prefix, direct requirements extraction,
  duplicated matching `Feature ID`, independent-line separator rule, and that requirements content
  begins immediately after the fixed three fields without keyword-based detection.
- **Confirmed At**: 2026-08-30

### DEC-013: Identify implementation commits by Conventional Commit scope

- **Status**: confirmed
- **Decision**: Each implementation commit created by `auto-dev` MUST use Conventional Commits and
  MUST set its scope to the requirement's exact `Feature ID`, for example
  `feat(2026-0830-1030ab): add authentication service`. The commit type and description MAY reflect
  the specific change. Every successfully applied blueprint document change MUST be committed to
  the dedicated branch as a blueprint-only commit. Such commits MUST not use a feature ID as their
  scope and MUST contain only `.codexspec/blueprint.md` changes.
- **Alternatives Rejected**: Squashing each requirement into one commit; storing a duplicate ordered
  commit-hash list in blueprint; requiring developers to identify and order hashes manually.
- **Reason**: Git already records commit order. A stable feature scope lets an agent select the
  implementation commits for a requirement while excluding interleaved blueprint-only commits.
- **User Evidence**: "auto-dev 创建的实现提交可以从 feat(xxx module): description 变为
  feat(feature-id): description 之类的格式"
- **Confirmed At**: 2026-08-30

### DEC-014: Use one fixed integration branch and external worktree

- **Status**: confirmed
- **Decision**: Both commands MUST use the fixed local branch `codexspec/auto-dev` and a dedicated
  external worktree whose basename is `worktree-for-codexspec-auto-dev`. The worktree MUST be placed
  in a repository-specific location outside the main checkout, such as
  `<main-repository-path>-worktrees/worktree-for-codexspec-auto-dev`. Neither command may switch the
  dedicated worktree to a per-requirement branch or create per-requirement worktrees.
- **Creation Rule**: When the fixed branch and worktree do not exist, the command MUST identify the
  repository's default branch and attempt to fetch its configured remote when one exists. It MUST
  compare the locally available local and remote-tracking default-branch commits by ancestry rather
  than commit time. If one contains the other, initialize from the descendant. If they have
  diverged, initialize the fixed branch and merge both committed histories. Uncommitted changes in
  the main checkout MUST NOT be included.
- **Synchronization Rule**: Before starting the first pending requirement and before every later
  pending requirement, `auto-dev` MUST attempt to fetch the remote default branch when configured
  and merge any locally available new committed history from both the local and remote-tracking
  default branches into the fixed branch. A fetch failure MUST NOT stop the run; `auto-dev` MUST
  proceed on the assumption that the remote has no newly available commits. The failure MUST NOT
  disable later fetch attempts: `auto-dev` MUST try again at the next synchronization point before
  another pending requirement in the same run, and on a later invocation. It MUST re-establish the
  repository's required green verification baseline before marking the next requirement
  `in_progress`.
- **Conflict Rule**: If synchronization produces merge conflicts, `auto-dev` MUST resolve them
  autonomously and run the project's required checks. If it cannot resolve the conflicts or restore
  a passing verification baseline, it MUST abort that merge and stop the run. The next requirement
  MUST remain `pending`, and the next invocation MUST retry synchronization without introducing a
  separate blueprint status.
- **History Rule**: Synchronization MUST use merge and MUST NOT rebase the fixed branch, so existing
  implementation commit hashes and concurrent blueprint history are not rewritten.
- **Alternatives Rejected**: Choosing a baseline by commit timestamp; creating the fixed branch from
  the caller's arbitrary current branch; rebasing before each requirement; switching the fixed
  worktree to one branch per requirement; creating temporary requirement worktrees.
- **Reason**: One stable branch and physical blueprint keep planning state current, while merging the
  evolving default branch before each requirement prevents later automatic work from being built on
  a stale locally available codebase. Temporary remote unavailability does not prevent local
  autonomous development, while an unresolved merge cannot become the next requirement's baseline.
- **User Evidence**: Explicitly confirmed the analyzed fixed-branch, fixed-external-worktree, and
  merge-before-each-requirement proposal.
- **Confirmed At**: 2026-08-30

### DEC-015: Make auto-dev automation independent of workflow.auto_next

- **Status**: confirmed
- **Decision**: Invoking `auto-dev` MUST itself enable automatic stage advancement for the entire
  run. The command MUST reuse the existing auto-next stage order and pass conditions, but MUST NOT
  depend on, modify, enable, or disable `workflow.auto_next` in `.codexspec/config.yml`.
- **Compatibility**: The existing configuration continues to control only direct invocations of the
  ordinary single-feature SDD commands. Its value MUST neither prevent nor duplicate advancement
  owned by `auto-dev`.
- **Alternatives Rejected**: Requiring `workflow.auto_next: true`; automatically editing the fixed
  branch's configuration; refusing to run when the global option is false.
- **Reason**: Calling `auto-dev` is the user's explicit opt-in to continuous autonomous development,
  while the global setting must retain its existing behavior for ordinary command use.
- **User Evidence**: "auto-dev 与 workflow.auto_next 无关，auto-dev 复用 auto-next 的流程和通过条件，但它的自动执行由命令本身启用，不依赖全局配置。"
- **Confirmed At**: 2026-08-30

### DEC-016: Store blueprint.md under .codexspec in the dedicated worktree

- **Status**: confirmed
- **Decision**: The only blueprint document used by either command MUST be
  `.codexspec/blueprint.md` inside `worktree-for-codexspec-auto-dev`. Both commands MUST resolve the
  dedicated worktree first and then read or modify that file. They MUST NOT use a file at the same
  relative path in the checkout from which the command was invoked.
- **Alternatives Rejected**: Storing `blueprint.md` at the repository root; resolving the document
  relative to the caller's current checkout.
- **Reason**: A fixed path inside the shared worktree prevents branch-local blueprint copies and
  gives concurrent planning and development one current document.
- **User Evidence**: "使用专用 worktree 内的：.codexspec/blueprint.md"
- **Confirmed At**: 2026-08-30

### DEC-017: Use blueprint and auto-dev as the final command names

- **Status**: confirmed
- **Decision**: The two public command names MUST be `blueprint` and `auto-dev`. `blueprint` owns
  interactive requirements preparation and ordered blueprint maintenance; `auto-dev` owns
  continuous autonomous development from that blueprint.
- **Alternatives Rejected**: Renaming `blueprint` to `roadmap` or `backlog`; renaming `auto-dev` to
  `develop-blueprint`.
- **Reason**: The selected names distinguish planning from execution without reducing the document
  to a high-level roadmap or an ordinary task backlog, and without making the execution command
  unnecessarily long.
- **User Evidence**: "将 blueprint 和 auto-dev 作为最终命令名"
- **Confirmed At**: 2026-08-30

### DEC-018: Judge repeated integration by file differences, not a clean commit list

- **Status**: confirmed
- **Decision**: After changes from the fixed branch enter the default branch, `auto-dev` MUST merge
  the latest default-branch history back into the fixed branch at the next required synchronization
  point and continue without rebase or branch reconstruction. This rule applies whether integration
  used a merge commit, fast-forward, squash merge, rebase merge, or cherry-pick. A later PR or MR
  MAY list earlier fixed-branch commits whose hashes are not present in the default branch, but its
  code or file changes MUST exclude code already present in the target branch.
- **Clarification**: If only some requirements were integrated, a later PR or MR created directly
  from the fixed branch will include every remaining code change not present in the target branch,
  not only the most recently developed requirement.
- **Alternatives Rejected**: Rebuilding or rebasing the fixed branch after every integration;
  requiring every project to preserve original commit ancestry when merging.
- **Reason**: Squash, rebase, and cherry-pick create different commit hashes even when the resulting
  code is already present. Merging the target branch back provides a current file-diff base while
  preserving the fixed branch's development history.
- **User Evidence**: Explicitly accepted earlier commits remaining in the PR or MR commit list as
  long as code and file changes contain only requirements not yet integrated and code review is not
  affected.
- **Confirmed At**: 2026-08-30

## Out of Scope

### OUT-001: No requirements discovery during auto-dev

- **Status**: confirmed
- **Statement**: `auto-dev` MUST NOT perform interactive requirements discovery or pause between
  normal SDD stages for user confirmation.
- **Reason**: Requirements selected by `auto-dev` have already completed blueprint discovery.
- **User Evidence**: The user explicitly confirmed that `auto-dev` can proceed fully autonomously
  after all user-owned decisions are made during the blueprint phase.

### OUT-004: No additional blueprint status for an unsuccessful run

- **Status**: confirmed
- **Statement**: A stage or review result such as `BLOCKED`, `FAIL`, or `INCONCLUSIVE` MUST NOT be
  added to the allowed blueprint `Development Status` values. These values MAY remain in the
  applicable stage or review output while the blueprint requirement remains `in_progress`.
- **Reason**: Blueprint tracks only whether development has not started, is unfinished, or is
  completed; detailed results remain with the feature's SDD evidence.
- **User Evidence**: Explicitly confirmed that review failure results do not become blueprint
  development states.

### OUT-002: No automatic priority or dependency scheduling

- **Status**: confirmed
- **Statement**: This feature MUST NOT add priority-based scheduling or automatic dependency-based
  reordering to `auto-dev`.
- **Reason**: Users resolve prerequisites and reorder pending requirements during blueprint work.
- **User Evidence**: "如果有需要调整待实现需求，或者前置需求的情况，也是应该在blueprint阶段就完成"

### OUT-003: No dedicated branch-splitting or cherry-pick workflow

- **Status**: confirmed
- **Statement**: This feature MUST NOT add a command, `auto-dev` mode, or prescribed workflow for
  analyzing implementation commits, creating delivery branches, or performing cherry-picks.
- **Reason**: A general-purpose agent can perform those Git operations from the feature-scoped
  commit history. This feature only makes the relevant commits identifiable.
- **User Evidence**: "不增加命令。这个完全由普通通用的agent就可以完成得很好，不是我们本次需求覆盖范围和需要考虑的内容。"
- **Confirmed At**: 2026-08-30

## Open Questions

*None.*

## Superseded Entries

`DEC-006` and `NEED-005` remain in their original sections with `Status: superseded` and links to
their replacements.

## Confirmation Log

### Session 2026-08-29

- **Summary Presented**: Keep only `pending`, `in_progress`, and `completed` as blueprint-level
  development states. Use `Feature Directory` to associate an active or completed requirement
  with its dedicated feature directory. Leave stage-specific stop and failure results in the
  feature's own SDD artifacts.
- **User Confirmation**: Explicitly agreed to the three states and the `Feature Directory` field.
- **Entries Confirmed**: DEC-001

### Session 2026-08-29 - Autonomous development

- **Summary Presented**: `auto-dev` receives only confirmed blueprint requirements, makes design
  and implementation decisions autonomously within those requirements, repairs review findings,
  and does not request user decisions during normal execution.
- **User Confirmation**: Explicitly confirmed and clarified that every user-owned direction,
  option, and detail is decided during blueprint discovery. Unspecified implementation details use
  established software engineering best practices.
- **Entries Confirmed**: NEED-001, CON-001, DEC-002, OUT-001

### Session 2026-08-29 - Blueprint ordering

- **Summary Presented**: Use the order of requirement sections in `blueprint.md` as the automatic
  implementation order instead of adding a separate priority field.
- **User Confirmation**: Explicitly confirmed that blueprint discussion handles prerequisites and
  reordering, and that `auto-dev` follows document order without changing it.
- **Entries Confirmed**: NEED-002, DEC-003, OUT-002

### Session 2026-08-29 - Shared worktree concurrency

- **Summary Presented**: Let `blueprint` and `auto-dev` run concurrently against the same dedicated
  branch, worktree, and physical `blueprint.md`, while protecting each document modification from
  concurrent writes. Permit changes only to pending requirements.
- **User Confirmation**: Explicitly confirmed the shared worktree and per-modification concurrency
  protection model, after agreeing to status-based editing restrictions.
- **Entries Confirmed**: NEED-003, CON-002, CON-003, DEC-004

### Session 2026-08-29 - Live queue refresh

- **Summary Presented**: Re-read `blueprint.md` after each completed requirement and continue with
  the first pending requirement, including work appended during the current `auto-dev` run, until
  no pending requirement remains.
- **User Confirmation**: Explicitly selected this behavior.
- **Entries Confirmed**: NEED-004

### Session 2026-08-30 - Stable requirement identity

- **Summary Presented**: Assign a permanent `Feature ID` when a requirement is appended to
  `blueprint.md`; use it for every agent-to-helper operation and later reuse it in the feature
  directory instead of introducing a second identifier.
- **User Confirmation**: Explicitly confirmed.
- **Entries Confirmed**: DEC-005

### Session 2026-08-30 - Agent-helper base contract

- **Summary Presented**: Exchange versioned JSON containing an operation, permanent `Feature ID`,
  expected blueprint hash, and operation-specific payload; return a structured applied, conflict,
  rejected, or invalid-request result. Do not accept an arbitrary blueprint path or whole-file
  replacement.
- **User Confirmation**: Explicitly confirmed and requested a more precise payload schema.
- **Entries Confirmed**: DEC-006

### Session 2026-08-30 - Blueprint content-block operations

- **Summary Presented**: Separate appending a new requirements content block from replacing,
  deleting, or moving an existing pending block. Let the helper generate the `Feature ID` during
  append; require that ID for operations on existing blocks; handle all edits inside a pending
  block as one complete Markdown replacement.
- **User Confirmation**: Explicitly confirmed.
- **Entries Confirmed**: DEC-007
- **Entries Superseded**: DEC-006

### Session 2026-08-30 - Append field ownership

- **Summary Presented**: Let the agent provide only `feature_name` and confirmed requirements
  Markdown. Let the helper generate identity and blueprint-only state, insert entry separators, and
  exclude blueprint-only fields when creating the feature requirements record.
- **User Confirmation**: Explicitly confirmed.
- **Entries Confirmed**: DEC-008

### Session 2026-08-30 - Pending-document payloads

- **Summary Presented**: Use the same agent-authored fields for replacing a pending document, an
  empty payload for deleting it, and one of four exact destination forms for moving it among other
  pending documents. Reject extra fields and invalid status or reference combinations.
- **User Confirmation**: Explicitly confirmed.
- **Entries Confirmed**: DEC-009

### Session 2026-08-30 - Status update payloads

- **Summary Presented**: Use one `update_status` operation. Require a feature directory when moving
  from pending to in progress, preserve and omit that field when moving from in progress to
  completed, and reject all other transitions.
- **User Confirmation**: Explicitly confirmed after correcting the earlier unexplained proposal of
  separate start and completion operations.
- **Entries Confirmed**: DEC-010

### Session 2026-08-30 - Helper response contract

- **Summary Presented**: Return one of `invalid_request`, `conflict`, `rejected`, or `applied` using
  fixed response fields. Distinguish invalid JSON or schema from stale state, and distinguish both
  from a valid operation forbidden by blueprint rules.
- **User Confirmation**: Explicitly confirmed after reviewing concrete rejected and invalid-request
  examples.
- **Entries Confirmed**: DEC-011

### Session 2026-08-30 - Blueprint file format

- **Summary Presented**: Separate confirmed requirements content blocks with an independent `---`
  line. Prefix each block with three helper-managed fields, then preserve content that can be
  written directly as a new `requirements.md` and whose embedded `Feature ID` matches the prefix ID.
- **User Confirmation**: Explicitly confirmed, including the intentional duplicated `Feature ID`.
- **Entries Confirmed**: DEC-012

### Session 2026-08-30 - Commit identity and agent-driven splitting

- **Summary Presented**: Preserve each requirement's natural multi-commit history, allow
  blueprint-only commits to interleave, identify implementation commits by feature ID rather than
  storing a hash list, and keep each requirement's Git order.
- **User Confirmation**: Confirmed Conventional Commit scopes based on `Feature ID` and clarified
  that an agent, not the developer, analyzes commits, creates branches, and performs cherry-picks.
- **Entries Confirmed**: NEED-005, CON-004, DEC-013

### Session 2026-08-30 - Exclude delivery-branch automation

- **Summary Presented**: Choose whether a normal agent request or a new `auto-dev` mode performs
  branch splitting and cherry-picks.
- **User Confirmation**: Explicitly excluded the operation from this feature. A general-purpose
  agent can use the identifiable Git history without a CodexSpec command or prescribed workflow.
- **Entries Confirmed**: OUT-003
- **Entries Superseded**: NEED-005

### Session 2026-08-30 - Fixed branch and default-branch synchronization

- **Summary Presented**: Use fixed branch `codexspec/auto-dev` and an external worktree named
  `worktree-for-codexspec-auto-dev`; initialize from ancestry-aware local and remote default-branch
  history; merge both when diverged; fetch and merge before every requirement; never rebase or
  switch to per-requirement branches; serialize Git writes.
- **User Confirmation**: Explicitly confirmed the complete proposal.
- **Entries Confirmed**: CON-005, DEC-014

### Session 2026-08-30 - Auto-dev stage advancement

- **Summary Presented**: Treat `auto-dev` invocation as run-local opt-in to the existing auto-next
  sequence and pass gates without requiring or modifying `workflow.auto_next`.
- **User Confirmation**: Explicitly confirmed and defined `auto-dev` as repeated Requirements-First
  SDD plus automatic stage advancement across multiple blueprint requirements.
- **Entries Confirmed**: NEED-006, DEC-015

### Session 2026-08-30 - Feature directory naming

- **Summary Presented**: Treat the Feature ID as only the stable prefix of a feature directory
  name. Create and record the complete `.codexspec/specs/<feature-id>-<feature-name>/` path.
- **User Confirmation**: Explicitly clarified the required directory format with
  `2026-0813-1143el-release-notes` as the example.
- **Entries Confirmed**: CON-006

### Session 2026-08-30 - Interrupted-run recovery

- **Summary Presented**: On the next invocation, resume an existing `in_progress` requirement from
  its recorded feature directory and current SDD state before processing pending work. Preserve the
  status and directory instead of initializing the requirement again.
- **User Confirmation**: Explicitly confirmed the complete recovery behavior.
- **Entries Confirmed**: NEED-007

### Session 2026-08-30 - Default-branch synchronization failures

- **Summary Presented**: Continue automatic development with locally available branch information
  when no remote exists or a configured remote cannot be fetched. Resolve merge conflicts
  autonomously; if conflict resolution or the required checks cannot succeed, abort the merge, stop
  the run, and leave the next requirement pending for a later retry.
- **User Confirmation**: Explicitly selected continued development after fetch failure and stopping
  only when a merge cannot be resolved into a passing state.
- **Entries Confirmed**: DEC-014

### Session 2026-08-30 - Blueprint document location

- **Summary Presented**: Use `.codexspec/blueprint.md` inside the fixed dedicated worktree as the
  single blueprint document, regardless of the checkout from which either command is invoked.
- **User Confirmation**: Explicitly selected the proposed path.
- **Entries Confirmed**: NEED-003, DEC-016

### Session 2026-08-30 - Single active auto-dev run

- **Summary Presented**: Hold one repository-wide run lock for the complete `auto-dev` invocation,
  reject a second concurrent invocation immediately, continue allowing concurrent blueprint work,
  and release the run lock automatically when the process exits.
- **User Confirmation**: Explicitly confirmed.
- **Entries Confirmed**: CON-007

### Session 2026-08-30 - Final command names

- **Summary Presented**: Keep `blueprint` and `auto-dev` as the public command names after comparing
  them with `roadmap`, `backlog`, and `develop-blueprint`.
- **User Confirmation**: Explicitly selected `blueprint` and `auto-dev` as final.
- **Entries Confirmed**: DEC-017

### Session 2026-08-30 - Unsuccessful autonomous run

- **Summary Presented**: Repair and re-check autonomously, but stop without claiming completion
  when existing SDD progress or retry limits are reached. Preserve the in-progress feature and
  resume it on the next invocation without adding failed or blocked blueprint states.
- **User Confirmation**: Explicitly confirmed.
- **Entries Confirmed**: NEED-008, OUT-004

### Session 2026-08-30 - Retry remote fetch before each requirement

- **Summary Presented**: Choose whether one fetch failure suppresses later fetches in the same
  `auto-dev` run or whether every requirement keeps its independent pre-development synchronization
  attempt.
- **User Confirmation**: Explicitly required another fetch attempt before requirement 2 and every
  later requirement; a repeated fetch failure still does not stop development.
- **Entries Confirmed**: DEC-014

### Session 2026-08-30 - Repeated default-branch integration

- **Summary Presented**: Keep the fixed branch after any merge strategy, synchronize the resulting
  default branch back into it, and require later PR or MR file differences to exclude code already
  integrated. Accept that squash, rebase, or cherry-pick can leave older commits visible in the
  commit list because their hashes differ.
- **User Confirmation**: Explicitly accepted an older commit list provided that code and file
  changes contain only requirements not yet integrated and therefore do not interfere with review.
- **Entries Confirmed**: NEED-009, DEC-018

### Session 2026-08-30 - Read-only blueprint CLI

- **Summary Presented**: Add `codexspec show-blueprint` to locate and validate the fixed branch,
  dedicated worktree, and shared blueprint from the current Git project, then print the complete
  file or return a specific error. Keep the command read-only and fetch-free.
- **User Confirmation**: Explicitly confirmed the command name and behavior.
- **Entries Confirmed**: NEED-010

### Session 2026-08-30 - Lock-free blueprint display

- **Summary Presented**: Remove the CLI read lock and make helper-side atomic file replacement
  responsible for ensuring readers never observe partial blueprint content.
- **User Confirmation**: Explicitly confirmed removing the `show-blueprint` read-lock design.
- **Entries Confirmed**: CON-008

### Session 2026-08-30 - Final discovery confirmation

- **Summary Presented**: Confirm the complete `blueprint`, `auto-dev`, shared worktree, helper
  protocol, synchronization, recovery, repeated integration, and `show-blueprint` requirements,
  with no remaining open question or unconfirmed AI assumption.
- **User Confirmation**: Explicitly confirmed the final requirements summary.
- **Entries Confirmed**: NEED-001 through NEED-004, NEED-006 through NEED-010; CON-001 through
  CON-008; DEC-001 through DEC-005, DEC-007 through DEC-018; OUT-001 through OUT-004
- **Entries Superseded**: NEED-005, DEC-006

### Session 2026-08-30 - Requirements content parsing boundary

- **Summary Presented**: Parse each blueprint block solely from its fixed first three managed field
  lines and treat every following line as requirements content. Do not detect requirements content
  from `# Requirements:`, any other heading, or any section keyword.
- **User Confirmation**: Explicitly corrected the keyword-based interpretation and restated that
  all content after the fixed three lines is the requirements document.
- **Entries Confirmed**: DEC-012
