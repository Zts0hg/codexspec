### Con-2026-1011-105126-1: Keep valued switches consistent across commands

- claim: When adding a switch that accepts an explicit value, use `on/off` as the canonical spelling in help, documentation, examples, and automated invocations. Accept the same value aliases as existing switches: `on/true/1/yes` and `off/false/0/no`, with consistent case and whitespace handling. Represent the resulting state as a boolean in YAML configuration and internal data. Keep this convention separate from each switch's default and omitted-argument behavior, which its own contract defines.
- type: convention
- scope/when: adding or revising CodexSpec switch parameters that take values, including workflow commands and their automated handoffs
- evidence.facts: “我希望对于开关参数，能够尽可能在参数值上一致，让用户使用时更加清晰方便”; “同意” in response to documenting `on/off`, accepting existing aliases, and using boolean YAML/internal state.
- evidence.state: Confirmed during requirements discovery for feature 2026-1011-105126-review-code-standards. Existing `--auto-next`, `--auto-distill`, and `--worktrees` documentation and parsing in `src/codexspec/__init__.py` match the convention. The new feature's switch is specified in DEC-009 of its requirements and managed through the existing `codexspec config` entry point; the implemented setter passed all value-alias, YAML-boolean, formatting-preservation and routed-CLI checks in tests/test_config_auto_maintenance.py. The full suite passed with 2071 tests and 54 platform skips.
- provenance: distill near the switch-value confirmation in specify, 2026-10-11, source feature: 2026-1011-105126-review-code-standards, derivation: explicit, confidence: high; outcome updated by distill during implement-tasks, 2026-10-11
- status: vetted
