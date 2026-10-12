### P-2026-1011-105126-2: Absence defaults must distinguish present unreadable links

- claim: A permissive default for a missing policy file must distinguish true absence from a present entry that cannot be read.
- type: pitfall
- scope/when: reading file-backed automation policy where absence enables optional actions
- root-cause: `Path.exists()` follows symbolic links, so a dangling or cyclic link returns false and can enter an absence-default branch. Boolean path queries can also suppress operating-system errors; they do not establish why a policy source cannot be read.
- workaround: Inspect the policy entry with `Path.lstat()`. Use the absence default only for `FileNotFoundError`; convert other status errors to the existing actionable configuration error. Then retain the strict read and schema validation. Preserve readable links and explicit stored booleans rather than adding an unrelated link prohibition.
- lesson: Establish the reason for missing filesystem information before applying a permissive policy default; a readable-value contract needs explicit error handling.
- evidence.facts: In `src/codexspec/review_maintenance.py`, the pre-repair `if not config.exists(): return True` enabled maintenance for both dangling and cyclic configuration links. `tests/test_config_auto_maintenance.py::test_p06_present_unreadable_link_refuses_policy` produced two expected failures before repair; the two readable-link cases passed. After the `lstat()` repair, the configuration, maintenance and standards set passed all 64 cases. See the tests and [Python's pathlib status-query documentation](https://docs.python.org/3/library/pathlib.html).
- evidence.state: Outcome verified in feature `2026-1011-105126-review-code-standards`; true absence still defaults true, readable linked policies retain their explicit value, and unreadable present entries raise the existing error. No change is implied for other readers with different contracts. The inferred lesson has not been separately endorsed by a human.
- provenance: distill near-moment during implement-tasks repair, 2026-10-12, derivation: inferred, confidence: high
- status: candidate
