## D-2026-0812-14054p-1: distill record IDs are namespaced by the full source-feature id

- claim: distill record IDs MUST be namespaced by the distilling feature's full spec-dir id (`{YYYY-MMDD-HHMM}{rr}`, e.g. `P-2026-0812-14054p-1`), never bare sequential (`P-001`), so records produced on parallel feature branches never collide on id (and, with one-file-per-record, never on filename either) when merged. The full id (with date) also makes each record self-describing — the date reads recency/staleness, the feature id gives decision context and scope.
- type: decision
- scope/when: any record written to `.codexspec/profile/` by distill
- evidence.facts: "这似乎是暴露来 distill 另外一个设计缺陷，没有考虑到多人协作时不同特性分支产生的distill内容的编号冲突"; "按照 A 改成带 distill 来源特性 ID 的前缀"; "ID更希望保留类似\" P-2026-0812-14054p-1(feature-id + 局部序号)\"的名称，比较好识别日期和来源". Two feature branches (2026-0811-1418yq, 2026-0812-14054p) each distilled `P-001`/`Con-001`, which would collide on merge.
- evidence.state: decided and implemented at feature 2026-0812-14054p; distill.md record-format updated; existing records on both branches migrated. Mirrors the spec-dir timestamp+random naming that already prevents parallel-branch collisions. See [[D-2026-0812-14054p-2]] for the one-file-per-record store that uses this id as the filename.
- provenance: distill @implement-tasks, 2026-08-12, derivation: explicit
- status: candidate
