# FinEdu-CodeGen: a reliability benchmark for live LLM-generated computational finance code

Companion artifact for the article *"Structure Before Convention: A Pre-Registered
Reliability Benchmark and Two-Layer Deployment Architecture for Classroom
LLM-Generated Financial Code"* (target: IEEE Access). It measures whether LLMs can
generate numerically correct, pedagogically usable Python for the canonical
models of a securities-investment course, under four prompting conditions
crossing *convention information* x *structural scaffolding* (2x2).

## Artifact identification
- **Reproduces:** every number in the article — the 2x2 headline grid (Table II),
  the outcome reconciliation (Table III), the post-hoc wording x framing
  factorial (Table IV), by-task results (Table V), the system specification
  (Table VI), the full inferential appendix (Table VII), the 2x2 heatmap
  (Fig. 2), the error distribution (Fig. 3), and every robustness statistic
  (task-cluster bootstrap intervals, leave-one-task-out ranges, a task-level
  Rademacher sign-flip test, GEE and provider-adjusted GEE, and the
  mixed-effects variational-Bayes fit).
- **Scale:** 6 knowledge points x 3 task types x 4 conditions x 3 models x 10
  repetitions = 2,160 pre-registered generations, plus a disclosed post-hoc
  factorial completion of the same size (2,160) and 600 real-instructor
  validation generations.
- **Version:** 1.0.0 · **License:** code MIT, data CC BY 4.0 · **Archive:** deposited on Zenodo (DOI cited in the article)
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
runs/            run-log schema, results_formal.csv, and the complete raw logs
                 of every generation (runs/raw/, stored byte-for-byte)
coding/          codebook + deterministic/AI/blinded error coding materials
analysis/        preregistered analysis plan + all stats & figure scripts
figures/         Fig. 1-4 sources and vector PDFs (architecture, 2x2 heatmap,
                 error mix, latency)
config/          model/decoding config (locked before stage 2; key via env var)
docs/            dataset card, artifact card, generated 18-task audit index
PREREGISTRATION.md, DEVIATIONS.md, codebook.md
```

## Hardware & software requirements
- Python 3.10+ (tested 3.11); no GPU required. ~4 GB RAM is ample.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy,
  statsmodels, matplotlib, pyyaml, mpmath, requests, openpyxl). Container:
  `environment/Dockerfile`.
- Regenerating raw generations/coding calls the OpenRouter API and needs
  `export OPENROUTER_API_KEY=...` (never committed).

## Reproduce the main results
Everything needed is in this repository; no separate download is required.
```bash
pip install -r requirements.txt
bash scripts/reproduce_main_results.sh
```
The script calls the numerical, validation, audit, and figure stages in
sequence; no single analysis file produces every reported result. Then compare
the printed numbers with Tables II-VII and the abstract.

## Reproduce the stage-1 validation
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
generation. See `PREREGISTRATION.md`; all eleven later deviations are disclosed
in `DEVIATIONS.md`, including the post-hoc factorial completion (#11).

## Known limitations
- Enabling-layer study: no student subjects or learning-outcome data.
- Model rankings are procurement-contingent (region-available models) and
  time-bounded (model drift); the released judge allows re-measurement, and the
  byte-identical replays in `runs/raw/` document one such drift check directly.
- The pre-registered "structure" contrast identifies a deployable bundle rather
  than a pure atomic manipulation; the disclosed post-hoc cells (Creg, C1wS)
  separate its wording and framing components.
- Error-class proportions rest on coding whose reliability is limited: automated
  coding reaches kappa=0.49 over 686 items (0.34 on the C1 subset), and two human
  coders reach kappa=0.03 (AC1=0.32, raw agreement 45.1%) on the public 266-item
  C1 subset. Substantive claims are therefore anchored to the deterministic
  (kappa-immune) mechanical categories.

## Status
Stages 1-3 complete: infrastructure and preregistration; 2,160 pre-registered
generations plus a disclosed post-hoc factorial completion (2,160) and 600
real-instructor validation generations; coding, adjudication, and analysis
locked. Human error-coding validation by two independent coders is complete: it
confirmed that the conventional/conceptual distinction is not reliably
human-codable, so the paper makes no error-share claim and anchors to the
deterministic (kappa-immune) floor.

## Contact
Ping Guo (corresponding author) — guopingapple@haut.edu.cn, School of Foreign
Languages, Henan University of Technology; Wei Fan — vincentfan@whu.edu.cn,
Business School, Zhengzhou University.
