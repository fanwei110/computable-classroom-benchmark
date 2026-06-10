# Prompt-Set Alignment & Design-Decision Log (frozen at preregistration)

Records every decision made while constructing the four-condition prompt set,
so the C2-vs-C4 contrast cleanly isolates *convention information* from
*structural scaffolding* (paper §IV.C; execution-plan scenario ②).

## 1. C2 ↔ C4 structural alignment

Both conditions share, section for section: role framing → concept card →
conventions/assumptions slot → task statement → numbered steps (identical
count per task) → code-quality instructions → output contract. Differences
are confined to the information content of the conventions slot, the task
statement variant, and convention words inside steps.

| Slot | C4 | C2 |
|---|---|---|
| Conventions slot | task-specific convention bullet list (from `conventions_binding`) | single neutral sentence: "choose appropriate, internally consistent computational assumptions" |
| Task statement (T1/T2) | fully convention-pinned YAML `description` | convention-stripped `NEUTRAL_STATEMENT` (same parameters) |
| Task statement (T3) | conversational `canonical_question` (identical in both) | same |
| Steps | convention-explicit (e.g., "de-annualize using 252 trading days") | same step, neutralized (e.g., "convert the volatility to the horizon in a suitable way") |

Verification: `check_c2_no_leak.py` scans all 18 C2 prompts against 29
forbidden patterns covering every binding and defensible convention;
current status: 18/18 clean.

## 2. Neutralization decisions (scenario ② instances)

- KP5 steps: "de-annualize using 252 trading days" → "convert the volatility
  to the horizon in a suitable way"; "one-tailed quantile, positive CNY loss"
  → "apply the normal quantile … report the VaR amounts in CNY".
- KP3 steps: "annual compounding", the convexity formula, and the
  first-order rule of thumb are removed; C2 says "compute the bond's
  interest-rate sensitivity … estimate the price impact".
- KP6 steps: "annual/252, ddof=1, sqrt(252), BHB formulas" → "account for the
  risk-free rate … compute the annualized Sharpe ratio / the three effects".
- KP1_T3 step 1: "map weights in the order named (60% in A)" → "decide how
  the 60/40 weights map to the two assets".
- Concept cards were stripped of two phrases that brushed against
  conventions: KP3 "first- and second-order sensitivities" → "sensitivity to
  yield changes"; KP6 "Brinson attribution" → "performance attribution".
- KP6_T2 neutral statement: "rolling 60-trading-day" → "rolling 60-day"
  (window length is task data; the *annualization basis* is the convention).
- False-positive resolved: "one percentage point" in KP4_T3's question is
  task data (the size of the vol bump), not the vega-quotation convention;
  the forbidden pattern was narrowed to "per percentage point".

## 3. Other frozen design decisions affecting the paper text

1. **Convention header** (C3) drops the draft §IV.C example's "ACT/360 day
   count" and instead enumerates the conventions that actually bind
   (252-day annualization, bond annual compounding, option continuous
   compounding, decimal units, positive VaR, ddof=1). No benchmark task
   leaves day count unpinned (bonds are valued at coupon dates). The draft
   §IV.C quotation must be updated to the frozen header at data-fill.
2. **KP2_T3 risk-free rate 3.1% → 4.7%**: at 3.1% the strict (rf/12) and
   defensible (geometric) answers were separated by less than the sum of
   their tolerance bands (1.5e-5 < 1.67e-5), making the tiers statistically
   indistinguishable; 4.7% restores a 2x margin. Decided before any model
   was queried; enforced in general by the pairwise-distinguishability
   assertion in `build_answers.py`.
3. **KP3_T3 phrasing**: removed "in percent" from the canonical question -
   it actively invited percent units while the contract expects decimals.
4. **T3 defensible sets exclude unit variants** (percent-vs-decimal): unit
   errors are coded as conventional errors, not defensible alternatives.
   Preregistered disclosure rule: after data collection the conditional
   answer sets may be EXTENDED (never edited) if a model uses an
   unenumerated but defensible convention; any extension is disclosed in
   the paper (scenario ①).
5. **Repetition split** (from §IV.C): C1/C3 use 2 frozen external phrasing
   variants × 5 repetitions; C2/C4 use 1 canonical prompt × 10 repetitions.
