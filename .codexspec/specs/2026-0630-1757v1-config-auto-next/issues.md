# Implementation Issues — config-auto-next

## Issue: PLD-1 `flag_value` mechanism infeasible in Click 8.3 (R1 materialized)

- **Task**: T003 (also affects PLD-1 in plan.md)
- **Error**: Click 8.3.1 no longer honors `flag_value` for a *bare* optional-value
  option — `codexspec config --auto-next` (no value) errors with
  `"Option '--auto-next' requires an argument."` instead of yielding the flag
  value. Verified with both pure Click 8.3.1 and Typer 0.24.1. The `=`-form
  (`--auto-next=off`) still works.
- **Impact**: The plan's planned mechanism (PLD-1: `is_flag=False,
  flag_value=SENTINEL`) cannot deliver the confirmed bare-toggle UX
  (`codexspec config --auto-next`).
- **Attempted**:
  1. `typer.Option(None, "--auto-next", is_flag=False, flag_value=SENTINEL)` —
     bare errors (Click 8.3 limitation).
  2. Pure-Click equivalent — same error (confirms it is Click, not Typer).
- **Workaround Found**: Bare `--auto-next` is rewritten to
  `--auto-next=<sentinel>` by `_normalize_auto_next_argv()` in `main()` before
  Click parses. The `config` handler still treats the sentinel as a toggle, and
  explicit values (`on/off`, `=off`, etc.) pass through unchanged. End-to-end
  smoke confirmed: bare toggles both directions; explicit on/off/yes/=off work;
  invalid → exit 1 + file unchanged; no-project → exit 1; `--help` lists it.
- **Caveat / testability**: `CliRunner.invoke(app, ...)` bypasses `sys.argv`, so
  the bare-toggle path is exercised via subprocess (real `main()` entry) in the
  test suite rather than CliRunner. Explicit-value, invalid, and no-project
  cases ARE covered via CliRunner.
- **Status**: Workaround Found
- **Product impact**: None — confirmed behavior (bare toggle + explicit) is
  preserved unchanged; only the implementation mechanism differs from PLD-1.
  This is a plan-level mechanism change, not a product decision; no user
  confirmation required per the stop-conditions (behavior/scope unchanged).
