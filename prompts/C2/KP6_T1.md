You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: risk-adjusted performance. The Sharpe ratio relates excess return to total risk; performance attribution decomposes active return into allocation, selection, and interaction effects.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
Part 1: load the daily return series in column "fund" of the course data snapshot; with an annual risk-free rate of 2.1%, compute the annualized Sharpe ratio. Part 2: a portfolio and its benchmark have three sectors - portfolio weights [0.45, 0.35, 0.20] with sector returns [0.083, 0.021, -0.014]; benchmark weights [0.40, 0.40, 0.20] with sector returns [0.067, 0.034, -0.009]. Compute the allocation, selection, and interaction effects.

The course data snapshot is at data/market_snapshot_v1.csv (CSV).

Proceed in steps:
1. Load the snapshot CSV; account for the risk-free rate in the fund returns.
2. Compute the annualized Sharpe ratio.
3. Compute the allocation, selection, and interaction effects.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'sharpe_annual', 'allocation_effect', 'selection_effect', 'interaction_effect'.
