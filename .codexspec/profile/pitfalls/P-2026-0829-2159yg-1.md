## P-2026-0829-2159yg-1: `flock(LOCK_NB)` without a lock type returns EBADF on macOS

- claim: `fcntl.flock` needs a lock type OR'd with `LOCK_NB`; `LOCK_NB` alone fails with EBADF, and legitimate contention returns EAGAIN instead.
- type: pitfall
- scope/when: implementing or debugging cross-process file locks in Python on macOS/Linux
- root-cause: `LOCK_NB` is a modifier flag, not a lock type; macOS's flock(2) rejects a request that names no lock mode (`LOCK_NB` alone) with EBADF, so the failure looks like a bad descriptor rather than contention.
- workaround: call `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)` for try-lock. When translating errors into domain outcomes, classify only `EAGAIN`/`EWOULDBLOCK`/`EACCES` as "busy"; every other errno (EBADF included) must fail closed with the raw error.
- lesson: a probe or test that repeats the code's own flag mistake reproduces the bug perfectly while looking like an environment failure — diff the probe's exact syscall arguments against the code's before theorizing about the environment.
- evidence.facts: non-blocking acquire in `src/codexspec/automation.py` FileLock used `LOCK_NB` alone; 6 ownership/CLI tests failed deterministically with "OSError: [Errno 9] Bad file descriptor"; after switching to `LOCK_EX | LOCK_NB` with an errno-busy classification, the full suite passed 1327/1327. Manual probes repeating the flag mistake intermittently "succeeded" (kernel-version-dependent undefined behavior), which masked the cause for hours.
- evidence.state: confirmed at feature 2026-0829-2159yg-blueprint-auto-dev; commit f96d87a. Still valid for macOS flock(2).
- provenance: distill @pr (auto), 2026-08-31, derivation: inferred, confidence: high
- status: candidate
