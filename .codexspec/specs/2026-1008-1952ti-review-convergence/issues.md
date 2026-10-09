# Issues

## Live-host verification limits

- **Tasks**: T024, T025.
- **Status**: Codex coordinated acceptance and schema-3 parsing checks are complete; detailed evidence and scope limits are recorded in [tasks.md](tasks.md#acceptance-evidence-2026-10-09).
- **Claude Code**: The optional live invocation timed out after 900 seconds. No Claude behavioral pass is claimed.
- **Codex CLI eval**: Both selected answers parse, but their verdicts are INCONCLUSIVE because the CLI read-only sandbox blocks required review operations. These case expectations do not pass; the separate coordinated Codex fixture reviews establish the recorded acceptance results.
- **Scenario input**: TS-24.3 uses the prescribed scripted accept input. Human interaction with the question UI is not verified.

## Resolved: live adapter mixed answer and diagnostic streams

- **Trigger**: A valid schema-3 answer on stdout plus repeated/example envelopes on stderr caused the parser to see multiple results.
- **Resolution**: Both live adapters return stdout only and reject nonzero host exits. Four red-green regression cases cover duplicated diagnostic envelopes and failed hosts supplying apparent success. Commit: `a37ce2b`.

## Historical review run

A prior schema-2 run stopped after eight complete reviews at the user's request. Its configuration-writer findings were repaired, but that run did not establish final acceptance. The resumed schema-3 run has an independent external ledger at `$HOME/.cache/codexspec/review/797fd308835574ea54a57974956066b8573c8b3d70922981ed7081842e60bc75/loops/2026-1008-1952ti.json`; prior rounds are not inherited as evidence or progress-guard state. The current feature verdict is recorded there and in its fingerprint-keyed result directory.
