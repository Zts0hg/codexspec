# Feature Name Validation Design

## Scope

Reject feature creation when the supplied short name contains no ASCII
alphanumeric characters after normalization. Document the feature naming
contract so timestamp-only resolution and random-suffix behavior are not
misread as compatibility or overwrite defects.

## Behavior

- Feature descriptions may use any language.
- The short name used in branch and workspace paths must normalize to a
  non-empty ASCII lowercase name containing letters, digits, and hyphens.
- Bash and PowerShell creation scripts validate the normalized suffix before
  creating a branch, directory, or `requirements.md`.
- Invalid input exits non-zero and tells the caller to provide an ASCII short
  name, with an example.
- Existing valid ASCII normalization behavior remains unchanged.

## Naming Contract

- Feature IDs always use `YYYY-MMDD-HHMMxx`, where `xx` is a two-character
  lowercase ASCII alphanumeric random suffix.
- Feature names and workspace directories always use
  `YYYY-MMDD-HHMMxx-short-name`.
- Sequential `NNN-name` identifiers are not part of the supported contract.
- "Legacy compatibility mode" refers only to reading an existing `spec.md`
  when `requirements.md` is absent. It does not include alternate directory
  naming formats.
- The full feature name, not the timestamp ID alone, is the workspace and
  branch identity. Independently created features may share a timestamp ID and
  coexist when their short names differ.
- Short-ID lookup is an optional convenience for a unique local match. It
  reports ambiguity instead of selecting or overwriting a workspace.

## Testing

- Add Bash and PowerShell regression tests using a CJK-only short name.
- Assert failure, the ASCII guidance, and absence of feature directories.
- Keep existing timestamp-format and valid short-name tests.
- Add contract assertions covering timestamp-only naming and the limited
  meaning of legacy compatibility.
