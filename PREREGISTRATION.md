# Preregistration

This document, together with the files it references, is frozen at this
repository's initial commit, **before any model generation was collected**.
The commit hash and timestamp serve as the registration record (mirrored to
OSF on public release).

## 1. The registered bundle (five pieces)

1. **Task specifications + conditional reference answers**:
   `tasks/*.yaml` (18 tasks; parameters deliberately perturbed away from
   textbook values), `tasks/answers/answers.json` (reference values; six T3
   conditional answer sets enumerating defensible (convention, value) pairs,
   each pair pairwise distinguishable beyond the summed tolerance bands).
2. **Judging harness**: `harness/judge.py` (+ `_exec_module.py`) -
   format-neutral output-contract reading (zero text parsing), mixed
   tolerance |x-x*| <= max(tau_abs, tau_rel|x*|) with tau_rel = 1e-4
   (1e-3 for optimization tasks), objective-value comparison for weight
   vectors, T3 three-tier scoring (strict / defensible-with-declaration /
   wrong), clarifying-question behavior category, format failures reported
   separately. **Adversarial acceptance: 40/40**
   (`harness/validation_report.md`; 20 correct-but-format-hostile judged
   correct, 20 planted errors judged wrong and archived to the right
   bucket).
3. **Error-coding manual**: `codebook.md` - four primary classes with
   operational criteria, the mechanical convention-swap criterion, 12
   boundary exemplars, blinding and double-coding protocol with a kappa
   threshold (recalibrate-and-recode below 0.6).
4. **Hypotheses** (confirmatory, falsifiable):
   - **H1**: numerical correctness under C4 (CKU-templated) exceeds C1
     (improvised zero-shot).
   - **H2**: convention information has a positive main effect:
     C3 > C1 and C4 > C2.
   Registered directional predictions (their failure is reported, not
   repaired): the convention main effect exceeds the structure main effect
   with no strong interaction; T3 is the weakest task type in C1 and gains
   most from templating.
5. **Analysis plan**: `analysis/analysis_plan.md` - mixed-effects logistic
   regression with task random effects (GEE robustness check) for H1/H2;
   cluster-bootstrap 95% CIs over tasks for all proportions; everything
   else exploratory and descriptive.

## 2. Freeze rules

- The harness, tolerances, codebook, course conventions, and the C2/C4
  prompt sets are frozen as of this commit. Any later change is disclosed
  in the paper with its reason; nothing is silently edited.
- T3 conditional answer sets may be **extended** after data collection
  (never edited) if a generation uses an unenumerated but defensible
  convention; every extension is disclosed (scenario-1 rule).
- Decoding parameters, model identities, and snapshot dates are locked in
  `config/models.template.yaml` -> `config/models.yaml` before stage 2;
  stage 2 refuses to run while `locked: false`.

## 3. Pending external inputs (registered as pending, scenario-4 rule)

- **C1/C3 improvised phrasings**: 2 variants per task, authored by two
  instructors not involved in designing the templates, harness, or
  reference answers, before seeing any model output
  (`prompts/C1_C3_collection_template.md`). They will be added in a
  follow-up commit and frozen; **stage 2 must not start before that
  commit**. C3 = the identical phrasing + the one-line convention header
  (`prompts/convention_header.txt`); all conditions carry the same
  output contract.
- **Model selection and classroom decoding parameters**: filled by the
  authors into the config and locked before stage 2.

## 4. Repository hygiene

No draft manuscript, no expected or simulated result figures, and no
anticipated numbers exist anywhere in this repository's history. The full
raw logs of all 2,160 generations (prompt, completion, stdout, judge
verdict, latency) will be archived per `runs/schema.md` and released with
the benchmark.
