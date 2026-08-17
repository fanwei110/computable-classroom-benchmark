# Dataset Card — FinEdu-CodeGen

## Summary
A preregistered reliability benchmark for **live LLM-generated computational
finance code** in a securities-investment classroom. It crosses two prompt
factors in a 2x2 design — *convention information* x *structural scaffolding* —
over 6 knowledge points x 3 task types x 4 conditions x 3 models = **2,160
generations**, each scored format-neutrally against an analytic or solver oracle.

## Composition
- **Tasks** (`tasks/*.yaml`, 18): 6 knowledge points (mean-variance frontier,
  CAPM/SML, bond duration/convexity, Black-Scholes/Greeks, VaR, Sharpe/attribution)
  x {T1 computation, T2 visualization, T3 scenario probe}.
- **Reference answers** (`tasks/answers/answers.json`): oracle values + T3
  conditional answer sets (defensible (convention, value) pairs); dual-path verified.
- **Prompts** (`prompts/`): frozen C2/C4 templates, C1/C3 phrasings, convention header.
- **Generations** (`runs/`): 2,160 model outputs + execution/judge/latency logs.
- **Error coding** (`coding/`): deterministic labels + two blinded LLM coders +
  adjudication + ~140 blinded packets for human validation.
- **Market snapshot** (`data/market_snapshot_v1.csv`): frozen, seeded, SHA256-recorded.

## Collection & provenance
Generations produced via OpenRouter (API snapshot 2026-06-11), provider-default
decoding, Chinese prompts, pass@1. C1/C3 phrasings are LLM-persona-simulated (a
fourth, non-evaluated model), with a real-instructor validation subset (§V.D).
All post-registration deviations are logged in `DEVIATIONS.md`.

## Intended use
Measuring and comparing the numerical reliability of LLM-generated finance
teaching code; studying prompt-structure effects; a template for reliability
benchmarks in other correctness-verifiable domains.

## Out-of-scope / limitations
- No student subjects or learning-outcome data (enabling-layer study only).
- Model rankings are procurement-contingent (region-available models).
- Structure factor is a deployable *bundle*, not a pure atomic manipulation.
- Error-class proportions rest on moderate inter-coder reliability (kappa=0.49);
  anchor claims to the deterministic (kappa-immune) floor.

## License & citation
Data: **CC BY 4.0**. Code: MIT (see `LICENSE`). Cite via `CITATION.cff`.
