## Con-2026-0812-14054p-1: Inject rendered managed blocks with a `re.sub` function replacement

- claim: When injecting a rendered managed block into a file via `re.sub`, pass a **function** replacement (e.g. `lambda _m: block`), never a string, so backslashes / `\g<...>` sequences in the block are not interpreted and cannot corrupt the output.
- type: convention
- scope/when: idempotently upserting a bounded managed block into a context/markdown file with `re.sub` in `src/codexspec/`
- evidence.facts: `src/codexspec/profile.py` uses `pattern.sub(lambda _match: block, existing)`; the isolated reviewer flagged this as correctly sidestepping "the exact class of `re.sub` corruption bug". The pre-existing `integrations/codex.py` skills-block upsert uses a **string** replacement (`pattern.sub(section.strip(), existing)`), which is the latent form to avoid.
- evidence.state: observed at feature 2026-0812-14054p-profile-consumption, base commit 8e69f51; verified by idempotency/non-destruction tests passing.
- provenance: distill @implement-tasks, 2026-08-12, derivation: inferred
- status: candidate
