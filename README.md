# FinEdu-CodeGen: a benchmark for concept-to-code generation in securities-investment education

Companion benchmark for *"Can LLMs Teach Finance Live? Benchmarking
Concept-to-Code Generation for a Generative-Inquiry Securities Investment
Classroom"* (submitted to IEEE TALE 2026). It measures whether LLMs can
generate numerically correct, pedagogically usable Python for the canonical
models of an investments course, under four prompting conditions crossing
*convention information* x *structural scaffolding* (2x2).

## Layout

```
conventions/   course computational conventions (frozen; defines "strict")
tasks/         18 task specs (6 knowledge points x T1 computation /
               T2 visualization / T3 scenario probe), YAML
tasks/answers/ reference values + T3 conditional answer sets (generated,
               committed, dual-path verified)
reference_impl/  reference implementations + build_answers.py +
               verify_dual.py (52 checks, two independent paths, <=1e-8)
data/          frozen market snapshot (seed 20260610, SHA256 recorded)
harness/       automated judge + 40-sample adversarial validation suite
               (20 correct-but-format-hostile must pass; 20 planted errors
               must fail into the right bucket) - currently 40/40
prompts/       frozen C2/C4 prompt sets (18 each), convention header,
               C1/C3 external-phrasing collection template + assembler,
               zero-leak checker for C2, alignment log
codebook.md    error-coding manual (4 classes, mechanical CV/CN criterion,
               12 boundary exemplars, blinding protocol)
analysis/      preregistered analysis plan + cluster-bootstrap CI and
               mixed-logit scripts
config/        model/decoding configuration template (locked before stage 2)
runs/          run-log schema (raw logs released with the benchmark)
figures/       Fig. 1 architecture diagram (vector PDF)
```

## Reproduce the stage-1 validation

```bash
python tasks/validate_tasks.py            # 18/18 schema checks
python data/make_snapshot.py              # byte-identical regeneration
python reference_impl/build_answers.py    # answers + distinguishability
python reference_impl/verify_dual.py      # 52/52 dual-path checks
python prompts/generate_prompts.py        # regenerate C2/C4 (frozen output)
python prompts/check_c2_no_leak.py        # 18/18 zero convention leaks
python harness/run_validation.py          # 40/40 adversarial acceptance
```

Requirements: Python 3.10+, numpy, scipy, pandas, matplotlib, pyyaml, mpmath.

## Preregistration

See [PREREGISTRATION.md](PREREGISTRATION.md). The initial commit of this
repository constitutes the preregistration: task specs, conditional answer
sets, judging harness + acceptance results, codebook, frozen prompts,
hypotheses, and analysis plan, all committed before any model generation
was collected.

## Status

Stage 1 (infrastructure + preregistration): complete, pending two external
inputs - the C1/C3 instructor phrasings (collection template in prompts/)
and the locked model/decoding config. Stage 2 (2,160 generations) must not
start before both are frozen.
