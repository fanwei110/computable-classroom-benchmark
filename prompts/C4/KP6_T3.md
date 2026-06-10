You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: risk-adjusted performance. The Sharpe ratio relates excess return to total risk; performance attribution decomposes active return into allocation, selection, and interaction effects.

Course conventions:
- Annualize and de-annualize with 252 trading days per year (volatility scales with sqrt(252)).
- Use the sample standard deviation (ddof = 1).
- Convert annual rates to shorter periods by simple division (annual/12 monthly, annual/252 daily).
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
Take the fund returns in our course data file - the "fund" column. With the risk-free rate at 2.1%, what was the fund's annualized Sharpe ratio over the whole sample?

The course data snapshot is at data/market_snapshot_v1.csv (CSV).

Proceed in steps:
1. Load the snapshot CSV; subtract the daily risk-free rate (annual/252).
2. Compute the full-sample Sharpe with the sample standard deviation (ddof=1), annualized by sqrt(252).
3. Report it as a decimal in `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'sharpe_annual'.
