You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Value-at-Risk. A loss quantile of the P&L distribution, computed parametrically (delta-normal) or from historical data.

Course conventions:
- Annualize and de-annualize with 252 trading days per year (volatility scales with sqrt(252)).
- Report VaR as a positive loss amount, using the one-tailed normal quantile and a zero-mean assumption at short horizons.
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
Our desk reports an annualized volatility of 24% on a 2,700,000 CNY position. What's the 95% one-day VaR?

Proceed in steps:
1. De-annualize the 24% volatility to one day using 252 trading days.
2. Apply the one-tailed 95% normal quantile with a zero-mean assumption.
3. Report the VaR as a positive CNY amount in `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'var_95_1d'.
