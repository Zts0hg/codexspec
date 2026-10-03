### P-2026-1003-204985-7: Text edits need explicit encoding and newline handling

- claim: Portable text readers must select the file's encoding, and surgical editors must preserve newline bytes through both reading and writing.
- type: pitfall
- scope/when: reading UTF-8 templates or modifying configuration while preserving unrelated formatting
- root-cause: Path.read_text without encoding uses the platform codec, which can be cp1252 on Windows. Even with UTF-8 selected, universal-newline reading converts CRLF to LF; writing the resulting string as bytes cannot restore the original line endings.
- workaround: Specify encoding="utf-8" for template reads. For byte-preserving edits, decode read_bytes explicitly, apply source-index edits to that unnormalized text, and use the original newline style for inserted lines. Test LF and CRLF bytes directly on every platform, including Unicode comments and exact-byte toggle round trips.
- lesson: Explicit encoding and newline preservation solve separate problems; binary writing alone does not make a text round trip byte-preserving.
- evidence.facts: Both Windows Python jobs in CI run 37136180339 failed two template reads with UnicodeDecodeError and two configuration round trips with a dirty Git status. Four explicit CRLF tests reproduced the formatting defect on macOS; all eight LF/CRLF cases passed after preserving newline bytes.
- evidence.state: Verified during feature 2026-1003-204985 CI investigation. Related write-side behavior is documented in P-2026-0902-054178-3.
- provenance: distill during PR CI investigation, 2026-10-04; derivation: inferred; confidence: high
- status: candidate
