You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: risk-adjusted performance. The Sharpe ratio relates excess return to total risk; performance attribution decomposes active return into allocation, selection, and interaction effects.

Course conventions:
- Annualize and de-annualize with 252 trading days per year (volatility scales with sqrt(252)).
- Use the sample standard deviation (ddof = 1).
- Convert annual rates to shorter periods by simple division (annual/12 monthly, annual/252 daily).
- Attribution is Brinson-Hood-Beebower with a separate interaction term: allocation = sum (w_p - w_b) r_b; selection = sum w_b (r_p - r_b); interaction = sum (w_p-w_b)(r_p-r_b).
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
Part 1: Load the daily return series in column "fund" of the course data snapshot (CSV path given in the prompt). With an annual risk-free rate of 2.1% (converted to daily by dividing by 252), compute the annualized Sharpe ratio using the sample standard deviation (ddof=1) and a 252-day annualization. Part 2: A portfolio and its benchmark have three sectors. Portfolio weights [0.45, 0.35, 0.20] and sector returns [0.083, 0.021, -0.014]; benchmark weights [0.40, 0.40, 0.20] and sector returns [0.067, 0.034, -0.009]. Compute the Brinson-Hood-Beebower allocation, selection, and interaction effects (decimals).

The course data snapshot is at data/market_snapshot_v1.csv (CSV).

Proceed in steps:
1. Load the snapshot CSV; subtract the daily risk-free rate (annual/252) from the fund returns.
2. Compute the Sharpe ratio with the sample standard deviation (ddof=1), annualized by sqrt(252).
3. Compute the Brinson-Hood-Beebower allocation, selection, and interaction effects, in decimals.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'sharpe_annual', 'allocation_effect', 'selection_effect', 'interaction_effect'.
