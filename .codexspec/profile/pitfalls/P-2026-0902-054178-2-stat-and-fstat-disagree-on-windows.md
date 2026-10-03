### P-2026-0902-054178-2: `os.stat(path)` and `os.fstat(fd)` disagree on Windows for the same untouched file

- claim: File-stability checks that compare a full stat signature across acquisition sources (path-stat vs fstat) fail on every read on Windows; compare only mode and size across sources, and full signatures only within the same source.
- type: pitfall
- scope/when: TOCTOU/stability checks that compare `os.stat(path)` against `os.fstat(fd)` (before/after open) on cross-platform code
- root-cause: on Windows, `os.stat(path)` and `os.fstat(fd)` can report different `st_dev`, `st_ino`, and timestamp values for the same untouched file, because the two calls query the filesystem through different Win32 paths; strict equality of a full signature therefore fails on every read, independent of any actual mutation.
- workaround: split the comparison into two tiers — cross-source checks compare only `(st_mode, st_size)`, which both sources report consistently; same-source pairs (path-stat before vs after, fstat before vs after) compare the full signature (dev, ino, mode, size, mtime_ns, ctime_ns) and still catch real mid-read mutations. Applied in `internal/command_template_fragments.py::_read_stable_file_snapshot` (`_stat_identity` + same-source signature pairs).
- lesson: stat fields are not a portable identity key across acquisition sources; each OS fills them through different APIs. When CI is the only Windows executor, such portability defects surface only after merge — pre-verify by reasoning about field semantics per platform, and treat the first windows-latest run of new low-level file code as part of the change.
- evidence.facts: windows-latest CI (Python 3.11 and 3.12) failed 50+ tests with `FragmentError: one.md: file changed while being opened` although no file changed (GitHub run 34027731861); after the mode+size cross-source fix, all windows legs passed (run 34040200566).
- evidence.state: confirmed at feature 2026-0902-054178 rollout (commit 8cd043e, released in v0.7.15); windows legs green in run 34040200566. Still valid.
- provenance: distill @release v0.7.15, 2026-09-07, derivation: inferred, confidence: high
- status: candidate
