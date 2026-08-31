## S-2026-0829-2159yg-1: Before blaming the environment, diff the probe's arguments against the code's

- claim: when a syscall-level failure reproduces in both the code and your manual probes, verify the probe uses byte-identical flags and arguments before building an environment-failure theory.
- type: strategy
- scope/when: debugging syscall/library failures that seem intermittent or environment-dependent
- trigger: a failure (e.g. EBADF/EINVAL from a syscall) shows up in the code AND in your own reproduction probes, occasionally succeeding — an "environment problem" theory starts forming.
- action: print the exact arguments both the code and the probe pass (flag values included, e.g. `flags=4` vs `flags=6`) and diff them; also check whether each probe that "contradicts" another actually differs in one argument. Fix the code if the code is wrong; only then treat the remainder as environmental.
- evidence.facts: during feature 2026-0829-2159yg, a `LOCK_NB`-without-`LOCK_EX` flock bug produced deterministic EBADF; probes repeating the same flag mistake failed identically while differently-flagged probes succeeded, producing an elaborate false "host has intermittent flock phases" theory (launchd-spawned children were even tested) before the one-argument diff ended it.
- evidence.state: confirmed at feature 2026-0829-2159yg-blueprint-auto-dev; commit f96d87a. Related: [[P-2026-0829-2159yg-1]].
- provenance: distill @pr (auto), 2026-08-31, derivation: inferred, confidence: high
- status: candidate
