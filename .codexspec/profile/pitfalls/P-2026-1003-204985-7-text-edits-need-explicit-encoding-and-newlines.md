### P-2026-1003-204985-7: Text edits need explicit encoding and newline handling

- claim: Portable text readers must select the file's encoding, and surgical editors must preserve newline bytes through both reading and writing.
- type: pitfall
- scope/when: reading UTF-8 templates, preserving configuration formatting, or passing byte-sensitive text to subprocesses
- root-cause: Path.read_text without encoding uses the platform codec, which can be cp1252 on Windows. Even with UTF-8 selected, universal-newline reading converts CRLF to LF; writing the resulting string as bytes cannot restore the original line endings. Subprocess text-mode stdin also translates LF to CRLF on Windows even when encoding="utf-8" is explicit, so Git can hash different bytes from those later written to disk.
- workaround: Specify encoding="utf-8" for template reads. For byte-preserving edits, decode read_bytes explicitly, apply source-index edits to that unnormalized text, and use the original newline style for inserted lines. For subprocess stdin whose bytes affect hashes or messages, encode explicitly and use binary pipes, then decode output separately. Preserve Git metadata such as MERGE_HEAD with byte I/O. Test LF and CRLF bytes directly on every platform, including Unicode comments and exact-byte toggle round trips.
- lesson: Explicit encoding and newline preservation solve separate problems; binary writing alone does not make a text round trip byte-preserving.
- evidence.facts: Both Windows Python jobs in CI run 37136180339 failed two template reads with UnicodeDecodeError and two configuration round trips with a dirty Git status. Four explicit CRLF tests reproduced the formatting defect on macOS; all eight LF/CRLF cases passed after preserving newline bytes. CI run 38104143348 reproduced the subprocess case on Windows Python 3.11 and 3.12; real Git with emulated Windows text transport reproduced the prepared/published tree mismatch on macOS. The seven tests in tests/test_git_transport.py passed after using binary stdin and explicit UTF-8 fixture output.
- evidence.state: Verified during features 2026-1003-204985 and 2026-1010-21225w CI investigations. Related write-side behavior is documented in P-2026-0902-054178-3.
- provenance: distill during PR CI investigation, 2026-10-04, extended 2026-10-11; derivation: inferred; confidence: high
- status: candidate
