# review-code Evaluation Runner

This directory contains development-only fixtures for exercising the
`review-code` defect-gate protocol against synthetic repositories.

Normal CI uses the canned adapter through `tests/test_review_code_eval.py`.
Live evaluation is opt-in and requires an already authenticated supported host:

```bash
python tests/evals/review_code/run_eval.py \
  --cases tests/evals/review_code/cases \
  --host codex \
  --record .codexspec/specs/2026-0713-2221gs-review-code-reliability/review-code-eval-results.json
```

Records contain host, case, verdict, profile, finding-count, and expectation
outcomes only. They do not store prompts, credentials, or model output.
