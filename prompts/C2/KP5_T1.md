You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Value-at-Risk. A loss quantile of the P&L distribution, computed parametrically (delta-normal) or from historical data.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
A position is worth 1,850,000 CNY and its annualized return volatility is 21.8%. Under the delta-normal (parametric) model, compute (i) the 95% one-day VaR and (ii) the 99% ten-day VaR.

Proceed in steps:
1. Convert the annualized volatility to the one-day horizon in a suitable way.
2. Apply the normal quantiles for the two confidence levels.
3. Scale to the ten-day horizon appropriately; report both VaR amounts in CNY.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'var_95_1d', 'var_99_10d'.
