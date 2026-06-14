# Review Follow-up Fixes Design

## Scope

Resolve four consistency defects found by reviewing the current branch against
`main`: implementation-stage feature resolution, requirements metadata
initialization, localized workflow documentation, and PowerShell creation
output.

## Implementation Command Contract

- `implement-tasks` resolves an explicit tasks file or feature directory first.
- Without an explicit path, it matches the current timestamp-format branch.
- If resolution is missing or ambiguous, it asks the user to select a feature.
- It never selects the latest workspace.
- It reads `requirements.md`, `spec.md`, `plan.md`, `tasks.md`, and the
  constitution.
- When `requirements.md` is absent, it uses legacy spec-only mode and states
  that original-discussion fidelity cannot be verified.

## Requirements Metadata

- Bash and PowerShell creation scripts replace `[FEATURE NAME]` with the
  normalized ASCII short name.
- They replace `[feature-id]` with the generated timestamp feature ID.
- `[DATE]` and `[DATE/TIME]` remain placeholders until the first confirmed
  requirements update because creation is not confirmation.
- Fallback requirements content follows the same metadata contract.

## PowerShell Output

- Creation output includes `BRANCH_NAME`, `REQUIREMENTS_FILE`, `FEATURE_ID`,
  and `HAS_GIT`.
- `SPEC_FILE` is removed because `spec.md` does not exist at creation time.
- Tests assert that returned paths identify files created by the command.

## Localized Documentation

Update German, Spanish, French, Japanese, Korean, and Brazilian Portuguese
user guides and workflow pages so they state:

- `specify` creates a workspace and persists confirmed `requirements.md`.
- `generate-spec` reads the selected requirements record rather than relying
  on prior-session context.
- `clarify` updates requirements first, then synchronizes the spec.
- The workflow includes `requirements.md` as the authoritative first artifact.

The update is limited to statements affected by this branch; it does not
rewrite unrelated translated content.

## Testing

- Add contract tests for `implement-tasks` resolution and authority.
- Add Bash and PowerShell creation tests for initialized metadata.
- Change PowerShell output tests to reject `SPEC_FILE`.
- Add localized-document assertions covering the new workflow.
- Run the complete test suite and platform-available syntax checks.
