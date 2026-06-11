# Stage-2 Run Log Schema (defined at stage 1, frozen)

All 2,160 generations are archived as JSON Lines, one file per
model x condition: `runs/raw/{model}_{condition}.jsonl` (gitignored until
release packaging; released in full with the benchmark).

Each line:

```json
{
  "run_id": "M1_C1_KP5_T3_A1_r03",
  "timestamp_utc": "2026-06-20T03:14:15Z",
  "model": "M1",
  "model_version": "<exact API model id>",
  "api_snapshot_date": "YYYY-MM-DD",
  "condition": "C1",
  "task_id": "KP5_T3",
  "phrasing_variant": "A1",        // C1/C3: teacher+variant; C2/C4: "canonical"
  "repetition": 3,
  "prompt": "<full prompt text sent>",
  "prompt_sha256": "...",
  "decoding": {"temperature": 0.0, "top_p": 1.0},   // from config, locked
  "completion": "<full model output>",
  "extracted_code": "<code block extracted or empty>",
  "exec": {"ok": true, "error_type": null, "stdout": "...", "stderr": "..."},
  "result_extracted": {"var_95_1d": 67143.19},
  "judge": {
    "bucket": "correct",
    "tier": "strict",
    "behavior": "answer",
    "needs_review": false,
    "details": {}
  },
  "latency_ms": {"api": 8230, "exec": 1450, "total": 9680},
  "manual_review": null,           // filled in stage 3 where needs_review
  "error_class": null,             // filled by blinded double coding, stage 3
  "declared": null                 // filled by blinded double coding, stage 3
}
```

Rules:
- `prompt` is stored verbatim; nothing is normalized.
- `latency_ms.total` is wall-clock from prompt submission to executed
  output (the paper's latency metric).
- Code extraction rule: among python-tagged fenced blocks, the first that
  defines `result` (else the first python-tagged block); if none, untagged
  fenced blocks that look like Python under the same preference; if none,
  a bare-code completion is tried whole. The raw completion is always kept.
  (Implementation aligned to this rule 2026-06-11 - DEVIATIONS.md #5.)
- One retry on transport errors only (HTTP failure, timeout at the API
  layer); model-content failures are never retried.
- The judge verdict is written by harness/judge.py at run time; manual
  fields stay null until stage 3 and are never overwritten silently.
