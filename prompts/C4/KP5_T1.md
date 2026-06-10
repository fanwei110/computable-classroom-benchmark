You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Value-at-Risk. A loss quantile of the P&L distribution, computed parametrically (delta-normal) or from historical data.

Course conventions:
- Annualize and de-annualize with 252 trading days per year (volatility scales with sqrt(252)).
- Report VaR as a positive loss amount, using the one-tailed normal quantile and a zero-mean assumption at short horizons.
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
A position is worth 1,850,000 CNY and its annualized return volatility is 21.8%. Under the delta-normal (parametric) model with zero mean, compute (i) the 95% one-day VaR and (ii) the 99% ten-day VaR (square-root-of-time scaling from one day). Course conventions: de-annualize by sqrt(252); one-tailed z; report VaR as positive CNY loss amounts.

Proceed in steps:
1. De-annualize the volatility to one day using 252 trading days.
2. Use the one-tailed normal quantiles (95% and 99%) with a zero-mean assumption.
3. Scale the ten-day VaR by sqrt(10); report both as positive CNY amounts.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'var_95_1d', 'var_99_10d'.
