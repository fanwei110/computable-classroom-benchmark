You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Markowitz mean-variance portfolio theory. Portfolio variance is w' Sigma w; the minimum-variance portfolio minimizes it subject to full investment; the efficient frontier traces minimal volatility for each target return.

Course conventions:
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
Two risky assets have expected annual returns 7.1% and 12.4% and annualized volatilities 16.3% and 28.9%. Produce a figure that draws the mean-variance frontier (volatility on x, expected return on y) for correlations 0.15, 0.45, and 0.75 on the same axes, marking the global minimum-variance portfolio on each curve. Short sales allowed, fully invested. Save the figure to the path given by the output contract. Also report, for correlation 0.45: the annualized volatility of the global minimum-variance portfolio, and the minimum annualized volatility achievable at a target expected return of 10%. Decimals throughout.

Proceed in steps:
1. For each correlation, build the covariance matrix and trace the frontier over portfolio weights.
2. Mark the minimum-variance portfolio on each curve; label curves in a legend.
3. For correlation 0.45, compute the two required volatilities as decimals.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'mvp_vol_at_rho45', 'frontier_vol_at_target', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
