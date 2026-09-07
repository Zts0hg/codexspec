### P-2026-0902-054178-3: `Path.write_text` translates LF to CRLF on Windows and breaks byte-pinned copies

- claim: Copying a file through `read_text`/`write_text` silently converts LF to CRLF on Windows (`newline=None` translates to `os.linesep`); copy byte-pinned files in binary mode.
- type: pitfall
- scope/when: any file copy or install step that must preserve exact bytes, especially after a line-ending policy (`.gitattributes`) pins worktrees to LF
- root-cause: `read_text`/`write_text` use universal-newline text mode; `write_text` with the default `newline=None` translates every `\n` to `os.linesep`, so an LF source becomes CRLF once written on Windows. Pinning the worktree to LF (`.gitattributes`: `* text=auto eol=lf`) exposed the pre-existing text-mode copy in `codexspec init`: the source script became LF in the worktree while the installed copy gained CRLF, failing a byte-equality test.
- workaround: copy in binary mode — `dest_file.write_bytes(src_file.read_bytes())` (or `shutil.copyfile`). Applied in `src/codexspec/__init__.py` for the `.sh`/`.ps1` helper scripts. Reserve text mode for cases where newline translation is actually intended.
- lesson: a line-ending policy at one layer shifts byte-fidelity obligations onto every layer that touches those bytes; when introducing one, audit all copy/IO call sites for text-vs-binary mode instead of trusting previously green tests — the old tests were green only because both sides were CRLF together.
- evidence.facts: windows-latest CI failed `test_init_preserves_review_context_resolver_content` with `assert b'#!/usr/bin/...exit 0\r\n' == b'#!/usr/bin/...exit 0\n'`; after the binary-copy fix, a fresh `codexspec init` produced a helper script byte-identical to its source.
- evidence.state: confirmed at feature 2026-0902-054178 rollout (commit 950d898, released in v0.7.15); init smoke test byte-equal and windows legs green in run 34040200566. Still valid.
- provenance: distill @release v0.7.15, 2026-09-07, derivation: inferred, confidence: high
- status: candidate
