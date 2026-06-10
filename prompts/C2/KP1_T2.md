You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Markowitz mean-variance portfolio theory. Portfolio variance is w' Sigma w; the minimum-variance portfolio minimizes it subject to full investment; the efficient frontier traces minimal volatility for each target return.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
Two risky assets have expected annual returns 7.1% and 12.4% and annualized volatilities 16.3% and 28.9%. Draw the mean-variance frontier (volatility on x, expected return on y) for correlations 0.15, 0.45, and 0.75 on one axes, marking the minimum-variance portfolio on each curve; short sales allowed, fully invested. Also report, for correlation 0.45, the annualized volatility of the minimum-variance portfolio and the minimum annualized volatility at a target expected return of 10%.

Proceed in steps:
1. For each correlation, build the covariance matrix and trace the frontier over portfolio weights.
2. Mark the minimum-variance portfolio on each curve; label curves in a legend.
3. For correlation 0.45, compute the two required volatilities.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'mvp_vol_at_rho45', 'frontier_vol_at_target', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
