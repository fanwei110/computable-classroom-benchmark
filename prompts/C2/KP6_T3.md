You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: risk-adjusted performance. The Sharpe ratio relates excess return to total risk; performance attribution decomposes active return into allocation, selection, and interaction effects.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
Take the fund returns in our course data file - the "fund" column. With the risk-free rate at 2.1%, what was the fund's annualized Sharpe ratio over the whole sample?

The course data snapshot is at data/market_snapshot_v1.csv (CSV).

Proceed in steps:
1. Load the snapshot CSV; account for the 2.1% risk-free rate.
2. Compute the full-sample annualized Sharpe ratio.
3. Report it in `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'sharpe_annual'.
