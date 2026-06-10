# Error-Coding Manual (Codebook) — frozen at preregistration

Scope: every generation that fails numerical correctness or visualization
adequacy receives exactly ONE **primary** error class. Multi-error detail is
retained in the released logs. Orthogonally, every convention-relevant
generation is coded **declared vs. silent**.

## 1. The four primary classes — operational criteria

**Code (CD).** The generation does not execute (syntax error, runtime
exception, timeout), or fails for programming reasons unrelated to finance
(shape mismatch, library misuse, wrong variable wiring). *All non-executable
generations are coded CD, without exception.* Format failures (executes but
violates the output contract) are NOT coded here — they sit in a separate
manual-review category and are reported separately.

**Conventional (CV).** The generation implements a *correct model* under a
*wrong or unintended convention*: annualization factor (252/250/365),
day-count, discrete vs. continuous compounding, payment frequency, percent
vs. decimal units, sign convention, ddof, percentile interpolation,
weight-order mapping, risk-free conversion rule, attribution scheme variant.

**Conceptual (CN).** The generation applies the wrong model, formula, or
definition: a quantity that no recognized convention choice would produce.

**Visualization (VZ).** Computation is correct but the figure is misleading,
incomplete, or absent (wrong objects, unlabeled axes that change meaning,
missing required curve/marker, file never produced).

## 2. The mechanical CV/CN criterion (decisive rule)

> Identify, from the code, the convention set the generation actually used.
> Re-evaluate its outputs under THAT convention (i.e., against reference
> values recomputed with the same inputs but the generation's convention).
> If the outputs are then correct, the error is **Conventional**.
> Otherwise it is **Conceptual**.

A "convention" for this purpose is any choice listed in
`conventions/course_conventions.md` (binding or defensible-alternative
lists) or any variant with standing in mainstream textbooks/market practice.
A choice with no such standing is not a convention; failing under it is CN.

Precedence when several things are wrong at once:
1. Not executable → CD (always).
2. Executable, numeric wrong → apply the mechanical criterion to the FULL
   set of failed keys: if one coherent convention swap fixes all failed
   keys → CV; if any failed key survives every coherent convention swap → CN.
3. Numeric correct, figure inadequate → VZ.

## 3. Declared vs. silent (orthogonal coding)

A convention is *declared* iff it is stated in **commentary**: natural-
language text around the code, code comments or docstrings, or string
values inside `result`. The mere appearance of a number (e.g., `sqrt(365)`)
in executable code is NOT a declaration. Declaring convention A while
implementing convention B is coded *silent* with a `declared_mismatch` flag
(and scores `wrong` at the T3 tier).

## 4. Boundary exemplars (12)

| # | Case (sample where available) | Class | Reasoning under the mechanical criterion |
|---|---|---|---|
| 1 | De-annualizes vol by sqrt(365) silently (p01) | CV | correct under the 365-day convention |
| 2 | VaR reported negative (p02) | CV | sign convention; magnitude correct |
| 3 | Outputs percent where decimals intended (p03) | CV | unit convention; rescaling fixes all keys |
| 4 | Sharpe with 250-day annualization (p04) | CV | recognized (Chinese-textbook) convention |
| 5 | ddof=0 population std (p05) | CV | recognized estimator convention |
| 6 | Macaulay value under the modified-duration key (p06) | CN | no convention renders Macaulay = modified at y>0; definitional misuse |
| 7 | Two-tailed z (1.96) for 95% one-tailed VaR (p09) | CN | "two-tailed VaR" has no standing; misunderstands the VaR definition |
| 8 | Correlation matrix used as covariance (p11) | CN | not a convention; modeling error |
| 9 | Annual bond treated as semiannual payer (p16) | CV | payment-frequency convention swap renders all keys correct (note: still *wrong* here because the task pins annual) |
| 10 | Convexity without the (1+y)^2 divisor (p17) | CV | recognized definitional variant of convexity |
| 11 | Sharpe ignoring the stated risk-free rate (p19) | CV | "gross Sharpe" has textbook standing; mechanical test passes under rf=0. Coded CV with `ignored_given_data` flag; scores `wrong` at the T3 tier because ignoring stated data is never defensible |
| 12 | Declares 365, implements 250 (p18) | CV | convention error by the mechanical test; coded silent + `declared_mismatch`; T3 tier `wrong` |

Drill note: the 20 planted adversarial samples
(`harness/adversarial/planted/` + `expected.yaml: planted_class`) are the
calibration set. Before stage-3 coding, both coders independently classify
all 20; discuss any disagreement against this manual; target agreement
20/20 before touching real failures.

## 5. Blinding and reliability protocol

1. Strip every failed generation of its prompt and condition metadata;
   present code + commentary only, in randomized order (fixed seed recorded).
2. Two coders code the full failure sample independently (primary class +
   declared/silent).
3. Report Cohen's kappa for the error coding itself. Threshold: kappa >= 0.7
   acceptable; 0.6-0.7 report with caution; < 0.6 → recalibrate this manual
   on the drill set and recode everything (preregistered rule, Appendix X.4).
4. Disagreements resolved by discussion; resolution log released.

## 6. Freeze rule

This manual is frozen at the preregistration commit. If any criterion must
change after the first generation is collected, the change and its reason
are disclosed in the paper (no silent edits).
