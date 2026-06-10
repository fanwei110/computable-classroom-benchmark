You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: risk-adjusted performance. The Sharpe ratio relates excess return to total risk; performance attribution decomposes active return into allocation, selection, and interaction effects.

Course conventions:
- Annualize and de-annualize with 252 trading days per year (volatility scales with sqrt(252)).
- Use the sample standard deviation (ddof = 1).
- Convert annual rates to shorter periods by simple division (annual/12 monthly, annual/252 daily).
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
Load the daily return series in column "fund" of the course data snapshot (CSV path given in the prompt). With an annual risk-free rate of 2.1% (daily = annual/252), draw the rolling 60-trading-day annualized Sharpe ratio over time (ddof=1, 252-day annualization), with the window length as an adjustable parameter. Save the figure to the path given by the output contract. Also report the Sharpe value of the final (most recent) 60-day window.

The course data snapshot is at data/market_snapshot_v1.csv (CSV).

Proceed in steps:
1. Load the snapshot CSV; use a daily risk-free rate of annual/252.
2. Compute the rolling 60-day Sharpe (ddof=1), annualized by sqrt(252), window adjustable.
3. Report the final window's value as a decimal; draw the series over time.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'rolling_sharpe_last', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
