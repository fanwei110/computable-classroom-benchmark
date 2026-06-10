# Course Computational Conventions (Frozen at Preregistration)

These are the binding conventions of the securities-investment course. Every reference
answer, every CKU template (C4), and the single-line convention header (C3) derive from
this document. The *strict* tier of T3 scoring means "matches these conventions."

## The Convention Header (verbatim, used in condition C3)

> Conventions: use 252 trading days per year for all annualization and de-annualization;
> quote bond yields with annual compounding; quote option risk-free rates with continuous
> compounding; express all rates, returns, volatilities, and weights as decimals (0.05 = 5%);
> report VaR as a positive loss amount; use the sample standard deviation (ddof = 1).

## Binding conventions, itemized

| # | ID | Convention | Where it binds |
|---|----|-----------|----------------|
| 1 | `ann_252` | Annualization factor = 252 trading days. Volatility scales by sqrt(252), mean returns by 252. De-annualization of an annualized volatility to one day divides by sqrt(252). | KP5 (VaR), KP6 (Sharpe), KP1 (when daily data given) |
| 2 | `bond_annual_comp` | Bond yields are quoted with annual compounding; coupons as stated in the task (annual unless said otherwise). Modified duration = Macaulay / (1 + y). Convexity = sum[t(t+1)CF_t/(1+y)^(t+2)] / P (in years^2). | KP3 |
| 3 | `opt_cont_comp` | Option-pricing risk-free rates are continuously compounded; Black–Scholes in its standard continuous form. Vega is quoted per unit of volatility (dC/dsigma), not per percentage point. | KP4 |
| 4 | `decimal_units` | All rates, returns, vols, weights are decimals. 24% volatility enters as 0.24; outputs likewise. | all KPs |
| 5 | `var_positive` | VaR is reported as a positive loss magnitude in currency units. 95% one-day parametric VaR = V * z(0.95) * sigma_daily, z(0.95) = Phi^-1(0.95) ≈ 1.6449 (one-tailed), zero-mean assumption at the one-day horizon. | KP5 |
| 6 | `ddof_1` | Standard deviations of return series use the sample estimator (ddof = 1). | KP5, KP6 |
| 7 | `rf_simple_split` | Converting an annual rate to a shorter period uses simple division (annual/12 for monthly, annual/252 for daily) unless the task says otherwise. | KP2 (T3), KP6 |
| 8 | `hist_var_linear` | Historical VaR = linearly interpolated empirical percentile of the P&L distribution (numpy default interpolation). | KP5 (T2) |
| 9 | `first_named_first` | When a portfolio is described as "a 60/40 portfolio of A and B", weights map to assets in the order named (60% in A). | KP1 (T3) |
| 10 | `duration_firstorder` | The course's taught rule of thumb for rate moves: dP/P ≈ −D_mod × dy (first order). Convexity is added only when the task asks for it. | KP3 (T3) |
| 11 | `attr_bhb` | Performance attribution uses Brinson–Hood–Beebower with a separate interaction term: allocation = Σ(w_p−w_b)r_b; selection = Σ w_b(r_p−r_b); interaction = Σ(w_p−w_b)(r_p−r_b). | KP6 |

## Defensible alternatives (for T3 conditional answer sets)

A convention is *defensible* if it appears in mainstream textbooks or market practice and a
reasonable instructor could intend it. The enumerated defensible alternatives, by convention:

- `ann_252`: 250 trading days (common in Chinese textbooks); 365 calendar days (defensible
  only where the volatility being de-annualized could plausibly be calendar-annualized,
  i.e., KP5 T3; **not** defensible for annualizing trading-day return series in KP6).
- `rf_simple_split`: geometric conversion (1+r)^(1/12)−1.
- `first_named_first`: the reverse weight order (40/60).
- `duration_firstorder`: duration+convexity second-order approximation; full exact repricing.
- `opt_cont_comp` (vega): vega per percentage point (dC/dsigma × 0.01); for a 1pp vol-bump
  question, exact repricing vs. vega×0.01 are both defensible (strict = exact repricing).
- KP6 Sharpe: ddof = 0 (population std) and 250-day annualization are defensible if
  declared; silently ignoring a risk-free rate that the task states is **not** defensible.

Anything not listed here is *not* defensible (e.g., z = 1.96 for a 95% one-tailed VaR is a
conceptual error, not an alternative convention). Per the preregistration disclosure rule:
after data collection the answer sets may only be *extended* (never edited) and any
extension must be disclosed in the paper.

## Note on the paper draft

The example header in draft §IV.C mentioned "ACT/360 day count"; no benchmark task leaves
accrued interest or day-count unpinned (bond tasks are quoted at coupon dates), so the
frozen header above replaces day-count with the conventions that actually bind. The draft
text will be updated to quote this header verbatim at the data-fill stage.
