You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Markowitz mean-variance portfolio theory. Portfolio variance is w' Sigma w; the minimum-variance portfolio minimizes it subject to full investment; the efficient frontier traces minimal volatility for each target return.

Course conventions:
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).
- Portfolio weights map to assets in the order named (a 60/40 portfolio of A and B holds 60% in A).

Task:
Asset A runs at about 18.4% annualized volatility and asset B at about 29.7%. If the correlation between them rises from 0.3 to 0.8, what happens to the volatility of a 60/40 portfolio of A and B?

Proceed in steps:
1. Map the 60/40 weights to the assets in the order named (60% in A).
2. Build the two covariance matrices (correlation 0.3 and 0.8).
3. Compute both portfolio volatilities as decimals.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'vol_before_annual', 'vol_after_annual'.
