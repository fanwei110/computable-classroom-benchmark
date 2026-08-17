# FinEdu-CodeGen: a reliability benchmark for live LLM-generated computational finance code

Companion artifact for the article *"Structure, Not Convention: A Pre-Registered
Reliability Benchmark and Two-Layer Deployment Architecture for Classroom
LLM-Generated Financial Code"* (target: IEEE Access). It measures whether LLMs can
generate numerically correct, pedagogically usable Python for the canonical
models of a securities-investment course, under four prompting conditions
crossing *convention information* x *structural scaffolding* (2x2).

## Artifact identification
- **Reproduces:** every number in the article — the 2x2 headline grid (Table II),
  by-task results (Table III), error distribution (Fig. 2), the 2x2 interaction
  (Fig. 3), and all robustness statistics (equivalence test, leave-one-task-out,
  wild-cluster bootstrap, task-level reliability).
- **Scale:** 6 knowledge points x 3 task types x 4 conditions x 3 models x 10
  repetitions = 2,160 generations.
- **Version:** 1.0.0 · **License:** code MIT, data CC BY 4.0 · **DOI:** [ZENODO_DOI]
- **Cite:** see `CITATION.cff`.

## Layout
```
conventions/     course computational conventions (frozen; defines "strict")
tasks/           18 task specs (6 KPs x T1 computation / T2 visualization /
                 T3 scenario probe), YAML; tasks/answers/ = oracle values +
                 T3 conditional answer sets (dual-path verified, <=1e-8)
reference_impl/  6 oracle implementations + verify_dual.py (52/52 checks)
data/            frozen market snapshot (seeded, SHA256 recorded)
prompts/         frozen C1-C4 prompt sets, convention header, zero-leak checker
harness/         format-neutral judge + 41-case adversarial suite (41/41)
runs/            run-log schema + results_formal.csv (2,160 rows); raw logs in
                 the Zenodo archive (gitignored here)
coding/          codebook + deterministic/AI/blinded error coding (Zenodo archive)
analysis/        preregistered analysis plan + all stats & figure scripts
figures/         Fig. 1-4 sources and vector PDFs (architecture, error mix,
                 2x2 heatmap, latency)
config/          model/decoding config (locked before stage 2; key via env var)
PREREGISTRATION.md, DEVIATIONS.md, codebook.md
```

## Hardware & software requirements
- Python 3.10+ (tested 3.11); no GPU required. ~4 GB RAM is ample.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy,
  statsmodels, matplotlib, pyyaml, mpmath, requests, openpyxl). Container:
  `environment/Dockerfile`.
- Regenerating raw generations/coding calls the OpenRouter API and needs
  `export OPENROUTER_API_KEY=...` (never committed).

## Reproduce the main results (from the Zenodo archive)
```bash
pip install -r requirements.txt
bash scripts/reproduce_main_results.sh   # journal_stats + redteam_stats + l2_stats + figures
```
Then compare the printed numbers with Tables II-III and the abstract.

## Reproduce the stage-1 validation (from the git repo)
```bash
python tasks/validate_tasks.py         # 18/18 schema checks
python data/make_snapshot.py           # byte-identical regeneration
python reference_impl/verify_dual.py   # 52/52 dual-path oracle checks
python harness/run_validation.py       # 41/41 adversarial acceptance
```

## Preregistration
The initial commit (`1184058`, 2026-06-11) is the preregistration: task specs,
conditional answer sets, judging harness + acceptance results, codebook, frozen
prompts, hypotheses, and analysis plan — all committed before any model
generation. See `PREREGISTRATION.md`; all later deviations are in `DEVIATIONS.md`.

## Known limitations
- Enabling-layer study: no student subjects or learning-outcome data.
- Model rankings are procurement-contingent (region-available models) and
  time-bounded (model drift); the released judge allows re-measurement.
- The "structure" factor is a deployable bundle, not a pure atomic manipulation.
- Error-class proportions rest on moderate inter-coder reliability (kappa=0.49);
  claims are anchored to the deterministic (kappa-immune) floor.

## Status
Stages 1-3 complete (infrastructure/preregistration; 2,160 generations; coding,
adjudication, and analysis locked). Human error-coding validation by two
independent coders is complete: it confirmed that the conventional/conceptual
distinction is not reliably human-codable (Cohen's kappa=0.03), so the paper
makes no error-share claim and anchors to the deterministic (kappa-immune) floor.

## Contact
Ping Guo (corresponding author) — guopingapple@haut.edu.cn, School of Foreign
Languages, Henan University of Technology; Wei Fan — vincentfan@whu.edu.cn,
Business School, Zhengzhou University.
