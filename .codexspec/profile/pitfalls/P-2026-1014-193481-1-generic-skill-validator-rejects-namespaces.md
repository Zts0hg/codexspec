### P-2026-1014-193481-1: Generic skill naming validators reject CodexSpec namespaces

- claim: Before changing a CodexSpec skill name to satisfy a generic validator, compare the validator with the project's native renderer and reproduce the check on the unchanged baseline.
- type: pitfall
- scope/when: creating or updating CodexSpec skills while using an external generic skill validator
- root-cause: The generic skill-creator validator accepts only lowercase letters, digits and hyphens; CodexSpec intentionally renders `name: codexspec:{command_name}`. Its colon rejection therefore occurs before and after a body-only change.
- workaround: Keep the established command identity. Run `python -B -m internal.maintainer_doc_skills --check` for repository documentation skills and `python -B internal/command_template_fragments.py --check-distribution` for distributed templates. Compare the generic validator's exact result against a temporary copy of the baseline skill; disclose its naming incompatibility instead of claiming that check passed or renaming commands solely to appease it.
- lesson: A generic validator's schema may differ from the consuming runtime's established contract. Establish that difference with baseline evidence and run the project's applicable checks before attributing the failure to a new edit.
- evidence.facts: `src/codexspec/integrations/codex.py` renders `name: codexspec:{command_name}`. The installed skill-creator `scripts/quick_validate.py` checks `^[a-z0-9-]+$`. Both the baseline and updated documentation translator returned "Name 'codexspec:translate-docs' should be hyphen-case (lowercase letters, digits, and hyphens only)"; repository skill/distribution checks passed.
- evidence.state: Outcome verified against baseline e35e6be295cf42a931df4b3d8dc405aa3b9f7f93 and the feature worktree for 2026-1014-193481. This records an external validator's observed limitation, not a runtime schema change or a substitute for behavioral assessment. No separate human endorsement.
- provenance: distill during documentation skill maintenance, 2026-10-14, derivation: inferred, confidence: high
- status: candidate
