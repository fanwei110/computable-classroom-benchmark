You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Value-at-Risk. A loss quantile of the P&L distribution, computed parametrically (delta-normal) or from historical data.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
Load the daily return series in column "fund" of the course data snapshot. For a 1,000,000 CNY position, draw a histogram of the daily P&L distribution and mark the 95% one-day historical VaR with a labeled vertical line; make the confidence level adjustable. Also report the 95% one-day historical VaR in CNY.

The course data snapshot is at data/market_snapshot_v1.csv (CSV).

Proceed in steps:
1. Load the snapshot CSV and form the daily P&L of the position.
2. Compute the 95% historical VaR from the empirical distribution, in CNY.
3. Draw the histogram with a labeled VaR line; parameterize the confidence level.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'hist_var_95_1d', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
