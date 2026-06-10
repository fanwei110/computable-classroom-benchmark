You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: risk-adjusted performance. The Sharpe ratio relates excess return to total risk; performance attribution decomposes active return into allocation, selection, and interaction effects.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
Load the daily return series in column "fund" of the course data snapshot. With an annual risk-free rate of 2.1%, draw the rolling 60-day annualized Sharpe ratio over time, with the window length adjustable. Also report the Sharpe value of the final 60-day window.

The course data snapshot is at data/market_snapshot_v1.csv (CSV).

Proceed in steps:
1. Load the snapshot CSV; account for the risk-free rate.
2. Compute the rolling 60-day annualized Sharpe ratio, window adjustable.
3. Report the final window's value; draw the series over time.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'rolling_sharpe_last', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
