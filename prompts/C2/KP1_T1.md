You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Markowitz mean-variance portfolio theory. Portfolio variance is w' Sigma w; the minimum-variance portfolio minimizes it subject to full investment; the efficient frontier traces minimal volatility for each target return.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
Three risky assets have annualized volatilities 18.7%, 24.3%, and 31.2%; correlations corr(1,2)=0.21, corr(1,3)=-0.13, corr(2,3)=0.37. Short sales are allowed and the portfolio is fully invested. Compute the weights of the global minimum-variance portfolio and its annualized volatility.

Proceed in steps:
1. Build the covariance matrix from volatilities and correlations.
2. Solve for the minimum-variance weights (closed form or solver), normalized to sum to 1.
3. Compute the portfolio volatility as the square root of w' Sigma w.
4. Populate `result` with the required keys.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'mvp_weights', 'mvp_vol_annual'.
