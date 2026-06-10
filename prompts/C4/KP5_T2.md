You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Value-at-Risk. A loss quantile of the P&L distribution, computed parametrically (delta-normal) or from historical data.

Course conventions:
- Historical VaR is the linearly interpolated empirical percentile (numpy default) of the P&L distribution.
- Report VaR as a positive loss amount, using the one-tailed normal quantile and a zero-mean assumption at short horizons.
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
Load the daily return series in column "fund" of the course data snapshot (CSV path given in the prompt). For a 1,000,000 CNY position, draw a histogram of the daily P&L distribution and mark the 95% one-day historical VaR with a labeled vertical line; the confidence level should be an adjustable parameter. Save the figure to the path given by the output contract. Also report the 95% one-day historical VaR as a positive CNY amount, computed as the linearly interpolated empirical percentile (numpy default) of the P&L distribution.

The course data snapshot is at data/market_snapshot_v1.csv (CSV).

Proceed in steps:
1. Load the snapshot CSV and form the daily P&L of the position.
2. Compute the 95% historical VaR as the linearly interpolated empirical percentile (numpy default), reported as a positive CNY amount.
3. Draw the histogram with a labeled VaR line; parameterize the confidence level.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'hist_var_95_1d', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
