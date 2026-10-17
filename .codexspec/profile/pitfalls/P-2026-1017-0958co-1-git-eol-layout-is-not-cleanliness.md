### P-2026-1017-0958co-1: Git EOL layout is not proof of an unchanged file

- claim: A Git safety check must establish the repository's text-conversion policy before treating CRLF worktree bytes as equivalent to an LF blob.
- type: pitfall
- scope/when: comparing worktree bytes with Git blobs before overwriting, deleting, or otherwise accepting affected files
- root-cause: `git ls-files --eol` reports observed index/worktree line endings. The same `i/lf w/crlf` output appears for a clean checkout conversion and for an unstaged user edit when `core.autocrlf=false` or the path has `-text`.
- workaround: Read effective `text` and `eol` attributes with `git check-attr -z` and the applicable `core.autocrlf` setting before normalization. An explicit `-text` disables it; automatic conversion additionally requires Git to classify the content as text. Compare actual bytes with the committed blob independently of assume-unchanged/skip-worktree flags, and avoid invoking user-configured clean filters merely to perform the safety check.
- lesson: An observation about byte representation does not establish the policy that makes two representations equivalent; test both the allowed conversion and a visually identical dirty state.
- evidence.facts: Real-Git probes accepted and overwrote LF-to-CRLF local edits with normalization disabled. The 18 text/binary policy variants in `tests/test_installation_upgrade.py::test_t04_s02_s04_crlf_protection_follows_git_policy` now distinguish disabled conversion, automatic binary exclusion, and supported clean conversions, and refusal snapshots include directories and Git metadata.
- evidence.state: Reproduced and regression-verified in feature 2026-1017-0958co; 106 installation-focused tests passed. No native Windows execution is claimed.
- provenance: distill @implement-tasks, 2026-10-17; derivation: inferred; confidence: high
- status: candidate
