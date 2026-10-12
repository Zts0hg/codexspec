### P-2026-1011-105126-3: Plugin root changes must cover every component path

- claim: When changing a plugin package root, revalidate explicit component discovery and every plugin-root-relative runtime/resource reference together.
- type: pitfall
- scope/when: changing marketplace source roots, component paths, or plugin resource layout
- root-cause: A root-relative helper reference and an implicit hook location can remain valid in the old component directory while becoming unavailable under a repository-level plugin root.
- workaround: Declare the contained command and hook paths; resolve runtime and review-resource references from that same root. Exercise startup and standalone runtime behavior from a plugin cache outside the consuming project, without requiring the CLI.
- lesson: Moving a package root changes the meaning of every relative path, including paths declared by another feature.
- evidence.facts: Integrating the shared review tree with the existing commit plugin produced two expected regression failures: the documented helper path did not exist in the declared root and the command contract retained the old path. After the command reference and explicit hook declaration were synchronized, 118 targeted integration checks passed, including CLI-free guarded commits and SessionStart behavior.
- evidence.state: Outcome verified during feature 2026-1011-105126-review-code-standards integration. The generalized lesson has not been separately endorsed by a human.
- provenance: distill during PR preparation, 2026-10-12; derivation: inferred; confidence: high
- status: candidate
