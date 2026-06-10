"""Generate the frozen C2 (structured-generic) and C4 (CKU-templated) prompts.

Design (paper SIV.C):
  C4 = full CKU template: role framing + concept card + an explicit
       conventions block + task statement + step decomposition + code-quality
       instructions + the uniform output contract.
  C2 = the SAME scaffold, section for section and step for step, but with
       every piece of convention information replaced by a deliberately
       neutral counterpart ("in an appropriate, internally consistent way").
       C2 must contain ZERO financial conventions - verified by
       check_c2_no_leak.py against a forbidden-pattern list.

T3 tasks keep their conversational canonical question as the task statement
in both conditions (templating fixes conventions, not the phrasing).
C1/C3 are NOT generated here: C1 phrasings come from two external
instructors (see C1_C3_collection_template.md); make_c3.py assembles
C3 = C1 + convention header, and appends the output contract to both.
"""

from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[0].parent if (HERE.parent / "tasks").exists() else HERE.parent
TASKS = HERE.parent / "tasks"

ROLE = ("You are the live coding assistant of a university securities-investment "
        "course. The instructor will run your code in front of the class, so it "
        "must be correct and self-contained.")

CODE_QUALITY = ("Write one self-contained Python script. Use only numpy, scipy, "
                "pandas, and matplotlib. No internet access, no placeholder "
                "values, deterministic output, clear variable names.")

CONVENTION_HEADER = (
    "Conventions: use 252 trading days per year for all annualization and "
    "de-annualization; quote bond yields with annual compounding; quote option "
    "risk-free rates with continuous compounding; express all rates, returns, "
    "volatilities, and weights as decimals (0.05 = 5%); report VaR as a positive "
    "loss amount; use the sample standard deviation (ddof = 1).")

CONCEPT = {
    "KP1": "Concept: Markowitz mean-variance portfolio theory. Portfolio variance "
           "is w' Sigma w; the minimum-variance portfolio minimizes it subject to "
           "full investment; the efficient frontier traces minimal volatility "
           "for each target return.",
    "KP2": "Concept: the CAPM and the security market line. Expected return is a "
           "linear function of beta; deviations from the line are alphas.",
    "KP3": "Concept: bond pricing with duration and convexity. Price is the "
           "discounted cashflow sum; duration and convexity measure its "
           "sensitivity to yield changes.",
    "KP4": "Concept: Black-Scholes pricing of European options and the Greeks. "
           "Price, delta, and vega follow from the closed-form solution.",
    "KP5": "Concept: Value-at-Risk. A loss quantile of the P&L distribution, "
           "computed parametrically (delta-normal) or from historical data.",
    "KP6": "Concept: risk-adjusted performance. The Sharpe ratio relates excess "
           "return to total risk; performance attribution decomposes active "
           "return into allocation, selection, and interaction effects.",
}

# Conventions block lines for C4, keyed by binding id (course_conventions.md).
CONV_TEXT = {
    "ann_252": "Annualize and de-annualize with 252 trading days per year "
               "(volatility scales with sqrt(252)).",
    "bond_annual_comp": "Bond yields are quoted with annual compounding; "
                        "modified duration = Macaulay / (1+y); convexity = "
                        "sum[t(t+1)CF_t/(1+y)^(t+2)] / P, in years squared.",
    "opt_cont_comp": "The option risk-free rate is continuously compounded; "
                     "vega is quoted per unit of volatility (dC/dsigma).",
    "decimal_units": "Express all rates, returns, volatilities, and weights as "
                     "decimals (0.05 means 5%).",
    "var_positive": "Report VaR as a positive loss amount, using the one-tailed "
                    "normal quantile and a zero-mean assumption at short horizons.",
    "ddof_1": "Use the sample standard deviation (ddof = 1).",
    "rf_simple_split": "Convert annual rates to shorter periods by simple "
                       "division (annual/12 monthly, annual/252 daily).",
    "hist_var_linear": "Historical VaR is the linearly interpolated empirical "
                       "percentile (numpy default) of the P&L distribution.",
    "first_named_first": "Portfolio weights map to assets in the order named "
                         "(a 60/40 portfolio of A and B holds 60% in A).",
    "duration_firstorder": "For yield-shift estimates, the course rule of thumb "
                           "is the first-order approximation dP/P = -D_mod * dy.",
    "attr_bhb": "Attribution is Brinson-Hood-Beebower with a separate "
                "interaction term: allocation = sum (w_p - w_b) r_b; selection "
                "= sum w_b (r_p - r_b); interaction = sum (w_p-w_b)(r_p-r_b).",
}

# The C2 conventions section is a single neutral counterpart, identical for
# all tasks (same slot, zero information).
NEUTRAL_CONV = ("Choose appropriate, internally consistent computational "
                "assumptions wherever the task statement leaves a choice open.")

# Neutral task statements for C2 (convention words stripped; parameters kept).
NEUTRAL_STATEMENT = {
    "KP1_T1": "Three risky assets have annualized volatilities 18.7%, 24.3%, and "
              "31.2%; correlations corr(1,2)=0.21, corr(1,3)=-0.13, corr(2,3)=0.37. "
              "Short sales are allowed and the portfolio is fully invested. Compute "
              "the weights of the global minimum-variance portfolio and its "
              "annualized volatility.",
    "KP1_T2": "Two risky assets have expected annual returns 7.1% and 12.4% and "
              "annualized volatilities 16.3% and 28.9%. Draw the mean-variance "
              "frontier (volatility on x, expected return on y) for correlations "
              "0.15, 0.45, and 0.75 on one axes, marking the minimum-variance "
              "portfolio on each curve; short sales allowed, fully invested. Also "
              "report, for correlation 0.45, the annualized volatility of the "
              "minimum-variance portfolio and the minimum annualized volatility at "
              "a target expected return of 10%.",
    "KP2_T1": "The risk-free rate is 2.3% per year and the expected market return "
              "is 9.4% per year. Stocks X, Y, Z have betas 0.62, 1.18, 1.51. "
              "Compute each stock's CAPM expected annual return. Stock Y actually "
              "returned 13.1% over the year; compute its alpha.",
    "KP2_T2": "With a risk-free rate of 2.3% and an expected market return of 9.4% "
              "per year, draw the security market line for betas 0 to 2 and plot "
              "stocks X (beta 0.62, return 8.1%), Y (beta 1.18, return 13.1%), and "
              "Z (beta 1.51, return 9.9%) as labeled points. Make the risk-free "
              "rate and market return adjustable. Also report the slope of the SML "
              "and the CAPM expected return at beta 1.27.",
    "KP3_T1": "A bullet bond has face value 100, a 4.6% coupon, 7 years to "
              "maturity, and trades at a yield to maturity of 5.3%. Compute the "
              "price, the Macaulay duration, the modified duration, and the "
              "convexity.",
    "KP3_T2": "For the bond with face 100, 4.6% coupon, 7 years to maturity, and "
              "current yield 5.3%, draw the exact price-yield curve for yields "
              "from 2% to 9% and overlay the duration-based approximations around "
              "the current yield, with a legend. Make the yield shift adjustable. "
              "Also report the exact price if the yield rises by 100 basis points "
              "and the duration-based estimate of the relative price change for "
              "that move.",
    "KP4_T1": "A European call on a non-dividend-paying stock: spot 103.7, strike "
              "97.5, implied volatility 27.6% (annualized), risk-free rate 4.3% "
              "per year, 0.58 years to expiry. Compute the call price, the delta, "
              "and the vega.",
    "KP4_T2": "For the European call with strike 97.5, risk-free rate 4.3% per "
              "year, and 0.58 years to expiry on a non-dividend stock, draw the "
              "call delta against the spot price from 70 to 140 with three curves "
              "for implied volatilities 15%, 27.6%, and 40%, labeled in a legend; "
              "make volatility adjustable. Also report the delta at spot 110 with "
              "volatility 27.6%.",
    "KP5_T1": "A position is worth 1,850,000 CNY and its annualized return "
              "volatility is 21.8%. Under the delta-normal (parametric) model, "
              "compute (i) the 95% one-day VaR and (ii) the 99% ten-day VaR.",
    "KP5_T2": "Load the daily return series in column \"fund\" of the course data "
              "snapshot. For a 1,000,000 CNY position, draw a histogram of the "
              "daily P&L distribution and mark the 95% one-day historical VaR "
              "with a labeled vertical line; make the confidence level "
              "adjustable. Also report the 95% one-day historical VaR in CNY.",
    "KP6_T1": "Part 1: load the daily return series in column \"fund\" of the "
              "course data snapshot; with an annual risk-free rate of 2.1%, "
              "compute the annualized Sharpe ratio. Part 2: a portfolio and its "
              "benchmark have three sectors - portfolio weights [0.45, 0.35, "
              "0.20] with sector returns [0.083, 0.021, -0.014]; benchmark "
              "weights [0.40, 0.40, 0.20] with sector returns [0.067, 0.034, "
              "-0.009]. Compute the allocation, selection, and interaction "
              "effects.",
    "KP6_T2": "Load the daily return series in column \"fund\" of the course data "
              "snapshot. With an annual risk-free rate of 2.1%, draw the rolling "
              "60-day annualized Sharpe ratio over time, with the window length "
              "adjustable. Also report the Sharpe value of the final 60-day "
              "window.",
}

# Step decompositions: STEPS[task]["c4"] and ["c2"] are aligned 1:1.
STEPS = {
    "KP1_T1": {"c4": ["Build the covariance matrix from volatilities and correlations.",
                      "Solve for the minimum-variance weights (closed form or solver), normalized to sum to 1.",
                      "Compute the portfolio volatility as the square root of w' Sigma w, as a decimal.",
                      "Populate `result` with the required keys."],
               "c2": ["Build the covariance matrix from volatilities and correlations.",
                      "Solve for the minimum-variance weights (closed form or solver), normalized to sum to 1.",
                      "Compute the portfolio volatility as the square root of w' Sigma w.",
                      "Populate `result` with the required keys."]},
    "KP1_T2": {"c4": ["For each correlation, build the covariance matrix and trace the frontier over portfolio weights.",
                      "Mark the minimum-variance portfolio on each curve; label curves in a legend.",
                      "For correlation 0.45, compute the two required volatilities as decimals.",
                      "Save the figure and populate `result`."],
               "c2": ["For each correlation, build the covariance matrix and trace the frontier over portfolio weights.",
                      "Mark the minimum-variance portfolio on each curve; label curves in a legend.",
                      "For correlation 0.45, compute the two required volatilities.",
                      "Save the figure and populate `result`."]},
    "KP1_T3": {"c4": ["Map the 60/40 weights to the assets in the order named (60% in A).",
                      "Build the two covariance matrices (correlation 0.3 and 0.8).",
                      "Compute both portfolio volatilities as decimals.",
                      "Populate `result`."],
               "c2": ["Decide how the 60/40 weights map to the two assets.",
                      "Build the two covariance matrices (correlation 0.3 and 0.8).",
                      "Compute both portfolio volatilities.",
                      "Populate `result`."]},
    "KP2_T1": {"c4": ["Apply the CAPM line E[Ri] = rf + beta (E[Rm] - rf) to each beta, in decimals.",
                      "Compute the alpha of stock Y against its CAPM prediction.",
                      "Populate `result`."],
               "c2": ["Apply the CAPM line E[Ri] = rf + beta (E[Rm] - rf) to each beta.",
                      "Compute the alpha of stock Y against its CAPM prediction.",
                      "Populate `result`."]},
    "KP2_T2": {"c4": ["Draw the SML over betas 0 to 2 and plot the three labeled points.",
                      "Parameterize the risk-free rate and market return.",
                      "Report the slope and the expected return at beta 1.27, in decimals.",
                      "Save the figure and populate `result`."],
               "c2": ["Draw the SML over betas 0 to 2 and plot the three labeled points.",
                      "Parameterize the risk-free rate and market return.",
                      "Report the slope and the expected return at beta 1.27.",
                      "Save the figure and populate `result`."]},
    "KP2_T3": {"c4": ["Convert the annual risk-free rate to monthly by simple division (annual/12).",
                      "Apply the CAPM line at the monthly horizon, in decimals.",
                      "Populate `result`."],
               "c2": ["Convert the annual risk-free rate to a monthly figure in a suitable way.",
                      "Apply the CAPM line at the monthly horizon.",
                      "Populate `result`."]},
    "KP3_T1": {"c4": ["Discount the annual coupons and face at the annually-compounded yield to price the bond.",
                      "Compute the Macaulay duration; divide by (1+y) for the modified duration.",
                      "Compute the convexity as sum[t(t+1)CF/(1+y)^(t+2)]/P, in years squared.",
                      "Populate `result`."],
               "c2": ["Discount the cashflows at the quoted yield to price the bond.",
                      "Compute the Macaulay duration and the modified duration.",
                      "Compute the convexity.",
                      "Populate `result`."]},
    "KP3_T2": {"c4": ["Price the bond on a yield grid from 2% to 9% (annual compounding) for the exact curve.",
                      "Overlay the first-order duration line and the duration-plus-convexity curve around 5.3%.",
                      "Report the exact price at +100bp and the first-order relative change (decimal, negative for a fall).",
                      "Save the figure and populate `result`."],
               "c2": ["Price the bond on a yield grid from 2% to 9% for the exact curve.",
                      "Overlay the duration-based approximations around 5.3%.",
                      "Report the exact price at +100bp and the duration-based estimate of the relative change.",
                      "Save the figure and populate `result`."]},
    "KP3_T3": {"c4": ["Compute the modified duration at the current yield (annual compounding).",
                      "Apply the course rule of thumb dP/P = -D_mod * dy with dy = 0.008.",
                      "Report the magnitude of the fall as a positive decimal in `result`."],
               "c2": ["Compute the bond's interest-rate sensitivity at the current yield.",
                      "Estimate the price impact of an 80 basis-point rise.",
                      "Report the size of the fall in `result`."]},
    "KP4_T1": {"c4": ["Compute d1 and d2 with the continuously compounded rate.",
                      "Price the call and compute delta = N(d1).",
                      "Compute vega per unit of volatility (dC/dsigma), in decimals.",
                      "Populate `result`."],
               "c2": ["Compute d1 and d2.",
                      "Price the call and compute the delta.",
                      "Compute the vega.",
                      "Populate `result`."]},
    "KP4_T2": {"c4": ["Compute delta = N(d1) over the spot grid for each volatility (continuously compounded rate).",
                      "Draw the three labeled curves and parameterize the volatility.",
                      "Report the delta at spot 110 with volatility 27.6%, as a decimal.",
                      "Save the figure and populate `result`."],
               "c2": ["Compute the delta over the spot grid for each volatility.",
                      "Draw the three labeled curves and parameterize the volatility.",
                      "Report the delta at spot 110 with volatility 27.6%.",
                      "Save the figure and populate `result`."]},
    "KP4_T3": {"c4": ["Reprice the call exactly at volatility 28.6% and at 27.6% (continuously compounded rate).",
                      "Report the exact price difference in `result`."],
               "c2": ["Work out how the call price responds to the one-point volatility move.",
                      "Report the price change in `result`."]},
    "KP5_T1": {"c4": ["De-annualize the volatility to one day using 252 trading days.",
                      "Use the one-tailed normal quantiles (95% and 99%) with a zero-mean assumption.",
                      "Scale the ten-day VaR by sqrt(10); report both as positive CNY amounts.",
                      "Populate `result`."],
               "c2": ["Convert the annualized volatility to the one-day horizon in a suitable way.",
                      "Apply the normal quantiles for the two confidence levels.",
                      "Scale to the ten-day horizon appropriately; report both VaR amounts in CNY.",
                      "Populate `result`."]},
    "KP5_T2": {"c4": ["Load the snapshot CSV and form the daily P&L of the position.",
                      "Compute the 95% historical VaR as the linearly interpolated empirical percentile (numpy default), reported as a positive CNY amount.",
                      "Draw the histogram with a labeled VaR line; parameterize the confidence level.",
                      "Save the figure and populate `result`."],
               "c2": ["Load the snapshot CSV and form the daily P&L of the position.",
                      "Compute the 95% historical VaR from the empirical distribution, in CNY.",
                      "Draw the histogram with a labeled VaR line; parameterize the confidence level.",
                      "Save the figure and populate `result`."]},
    "KP5_T3": {"c4": ["De-annualize the 24% volatility to one day using 252 trading days.",
                      "Apply the one-tailed 95% normal quantile with a zero-mean assumption.",
                      "Report the VaR as a positive CNY amount in `result`."],
               "c2": ["Convert the 24% annualized volatility to the one-day horizon in a suitable way.",
                      "Apply the 95% normal quantile.",
                      "Report the VaR amount in `result`."]},
    "KP6_T1": {"c4": ["Load the snapshot CSV; subtract the daily risk-free rate (annual/252) from the fund returns.",
                      "Compute the Sharpe ratio with the sample standard deviation (ddof=1), annualized by sqrt(252).",
                      "Compute the Brinson-Hood-Beebower allocation, selection, and interaction effects, in decimals.",
                      "Populate `result`."],
               "c2": ["Load the snapshot CSV; account for the risk-free rate in the fund returns.",
                      "Compute the annualized Sharpe ratio.",
                      "Compute the allocation, selection, and interaction effects.",
                      "Populate `result`."]},
    "KP6_T2": {"c4": ["Load the snapshot CSV; use a daily risk-free rate of annual/252.",
                      "Compute the rolling 60-day Sharpe (ddof=1), annualized by sqrt(252), window adjustable.",
                      "Report the final window's value as a decimal; draw the series over time.",
                      "Save the figure and populate `result`."],
               "c2": ["Load the snapshot CSV; account for the risk-free rate.",
                      "Compute the rolling 60-day annualized Sharpe ratio, window adjustable.",
                      "Report the final window's value; draw the series over time.",
                      "Save the figure and populate `result`."]},
    "KP6_T3": {"c4": ["Load the snapshot CSV; subtract the daily risk-free rate (annual/252).",
                      "Compute the full-sample Sharpe with the sample standard deviation (ddof=1), annualized by sqrt(252).",
                      "Report it as a decimal in `result`."],
               "c2": ["Load the snapshot CSV; account for the 2.1% risk-free rate.",
                      "Compute the full-sample annualized Sharpe ratio.",
                      "Report it in `result`."]},
}


def output_contract(spec):
    keys = ", ".join(f"'{k}'" for k in spec["required_keys"])
    line = (f"Output contract: store all required outputs in a dictionary named "
            f"`result` under exactly these keys: {keys}.")
    if spec["figure_required"]:
        line += (" Save the figure to a file and store its path under "
                 "result['figure_path'].")
    return line


def data_note(spec):
    if spec["data_file"]:
        return f"The course data snapshot is at {spec['data_file']} (CSV)."
    return None


def build_prompt(spec, condition):
    kp = spec["id"].split("_")[0]
    is_t3 = spec["task_type"] == "T3"
    task_text = (spec["canonical_question"].strip() if is_t3
                 else (spec["description"].strip() if condition == "c4"
                       else NEUTRAL_STATEMENT[spec["id"]].strip()))
    conv_block = ("\n".join("- " + CONV_TEXT[c] for c in spec["conventions_binding"])
                  if condition == "c4" else "- " + NEUTRAL_CONV)
    steps = STEPS[spec["id"]][condition]
    parts = [ROLE, "", CONCEPT[kp], "",
             ("Course conventions:" if condition == "c4" else "Assumptions:"),
             conv_block, "", "Task:", task_text]
    note = data_note(spec)
    if note:
        parts += ["", note]
    parts += ["", "Proceed in steps:"]
    parts += [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    parts += ["", CODE_QUALITY, "", output_contract(spec)]
    return "\n".join(parts) + "\n"


def main():
    n = 0
    for f in sorted(TASKS.glob("KP*_T*.yaml")):
        spec = yaml.safe_load(f.read_text(encoding="utf-8"))
        for cond, folder in (("c2", "C2"), ("c4", "C4")):
            out = HERE / folder / f"{spec['id']}.md"
            out.write_text(build_prompt(spec, cond), encoding="utf-8")
            n += 1
    (HERE / "convention_header.txt").write_text(CONVENTION_HEADER + "\n", encoding="utf-8")
    print(f"wrote {n} prompts + convention_header.txt")


if __name__ == "__main__":
    main()
