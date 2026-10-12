### P-2026-1011-105126-1: File installers must check destination type before copying

- claim: A grouped file installer must establish that each existing destination is a regular file before preserving it or starting copies; containment validation alone does not establish that contract.
- type: pitfall
- scope/when: installing groups of files with a generic path validator that also supports directory destinations, especially before an exists-based preserve branch
- root-cause: `validate_write_path` deliberately accepts directories at the final path for its generic callers. A file installer that treats `target.exists()` as proof of a file silently skips occupied directories without force; with force, it fails after earlier copies.
- workaround: In the installer's existing all-destination preflight, call `validate_write_path(project, target)`, then reject `target.exists() and not target.is_file()` with `AutomationError("unsafe_write_path", ...)`. Complete preflight before copying any file. Preserve regular-file edits and unrelated extensions; do not remove an occupied directory or change the generic validator's directory support.
- lesson: Match a reused validator's actual guarantees to the caller's required object type before relying on existence for preservation or replacement.
- evidence.facts: Before the fix, `install_review_standards` returned 25 of 26 copies with a directory at `index.md` in nonforced mode; forced mode raised `IsADirectoryError` after 10 copies. Five regression cases failed before the fix and passed after it; the 60-test installation/configuration/maintenance set passed. See `src/codexspec/review_standards.py` and `tests/test_review_standards.py::test_d05_nonfile_destination_preflight_preserves_group` / `test_d06_init_reports_nonfile_standard_destination_before_copy`.
- evidence.state: Outcome verified in feature `2026-1011-105126-review-code-standards`; the generic validator continues to support directory destinations. The inferred lesson has not been separately endorsed by a human.
- provenance: distill near-moment during implement-tasks repair, 2026-10-12, derivation: inferred, confidence: high
- status: candidate
