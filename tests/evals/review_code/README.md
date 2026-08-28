# review-code Evaluation Runner

This directory contains development-only fixtures for exercising the
`review-code` defect-gate protocol against synthetic repositories.

Normal CI uses the canned adapter through `tests/test_review_code_eval.py`.
Live evaluation is opt-in and requires an already authenticated supported host:

```bash
python tests/evals/review_code/run_eval.py \
  --cases tests/evals/review_code/cases \
  --host codex \
  --record /tmp/review-code-eval-results.json
```

Records contain host, case, verdict, profile, finding-count, and expectation
outcomes only. They do not store prompts, credentials, or model output.

The corpus covers every semantic risk profile plus source-independent cases for
cross-module contract propagation, multiple findings from one root cause,
continued partition completion after an early finding, blocking incomplete
coverage, and clean multi-surface behavior. Case schema versioning, aggregate
record versioning, and the reviewed command's result schema are independent
protocols.
