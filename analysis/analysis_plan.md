# Statistical Analysis Plan (preregistered, frozen)

## Design

4 prompting conditions (C1 improvised; C2 structured-generic; C3
convention-informed; C4 CKU-templated) x 3 models x 18 tasks x 10
repetitions = 2,160 generations. Factorization: conv = {C3, C4},
struct = {C2, C4}.

## Outcomes

Primary: numerical correctness (strict tier for T3). Secondary:
executability; defensible-tier correctness (T3); visualization adequacy
(T2, human-rated); task-level reliability (all 10 repetitions correct);
latency (descriptive).

## Confirmatory hypotheses (registered before any generation)

- **H1**: numerical correctness is higher under C4 than C1.
- **H2**: convention information has a positive main effect -
  C3 > C1 and C4 > C2.

Test: mixed-effects logistic regression, correct ~ conv + struct +
conv:struct + model, random intercept by task (analysis/mixed_logit.py);
GEE with task clusters as robustness. Inference threshold alpha = 0.05 on
the conv and struct main effects (H1 read from the C4-C1 contrast).

Falsifiable directional predictions (registered):
- conv main effect > struct main effect, with no strong interaction;
- T3 is the weakest task type in C1 (both tiers) and shows the largest
  C4-C1 gain.
If the data contradict these, the paper reports the contradiction (the
pre-written alternative-narrative branches are used; no silent rewriting).

## Interval estimates

All proportions carry 95% cluster-bootstrap CIs over tasks
(analysis/bootstrap_ci.py; B = 10,000; seed = 20260610).

## Exploratory (descriptive only, no tests)

Model ordering; between-model spread compression C1 vs C4 (with ceiling
caveat); task-type breakdown; error-class distribution; declaration rate;
clarifying-question count; latency distribution.

## Error coding

Per codebook.md: blinded, double-coded, kappa reported; mechanical CV/CN
criterion; declared/silent coded orthogonally.
