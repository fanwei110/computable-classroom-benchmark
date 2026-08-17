# Artifact Card — FinEdu-CodeGen

## What this artifact is
The full reproducibility package for the paper: task specs, oracles, prompts,
the format-neutral judge, all generation/execution logs, the error-coding
pipeline, and the analysis + figure scripts. Every number in the paper is
regenerable from released logs by `scripts/reproduce_main_results.sh`.

## Components
- **Judge** (`harness/judge.py`): executes each generation as a script, reads a
  `result` dict, compares to the oracle with mixed absolute/relative tolerance.
  Validated on 41 adversarial cases (21 format-hostile-but-correct, 20 planted
  errors) — `harness/run_validation.py`.
- **Oracles** (`reference_impl/`): 6 reference implementations; dual-path verified
  (`verify_dual.py`, 52/52).
- **Coding** (`analysis/mechanical_coder.py`, `ai_coders.py`, `finalize_coding.py`):
  deterministic classifier + two heterogeneous LLM coders + adjudicator; blinded.
- **Stats** (`analysis/{journal_revision_stats,redteam_verify,l2_stats,bootstrap_ci,mixed_logit}.py`):
  cluster-bootstrap CIs, GEE + mixed-effects, equivalence (TOST), leave-one-task-out,
  wild-cluster bootstrap.
- **Figures** (`figures/*.py`, `analysis/rebuild_figures.py`).

## Environment
Python 3.10+; deps in `requirements.txt`; container in `environment/Dockerfile`.

## How to run
`bash scripts/reproduce_main_results.sh` (from the Zenodo archive). Regenerating
raw generations needs `OPENROUTER_API_KEY` (env var; never committed).

## Models used (as tools, not evaluated as subjects)
Evaluated models M1-M3 (see `config/models.yaml`, snapshot 2026-06-11). A fourth
model generated persona phrasings; two further models did secondary error coding
and two did figure rating — all disclosed. Correctness itself is judged only
against oracles, never by a model.

## Out-of-scope uses
Not a general finance-LLM leaderboard; not a claim about student learning; model
rankings are deployment-environment-specific and time-bounded (models drift).
