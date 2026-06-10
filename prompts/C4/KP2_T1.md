You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: the CAPM and the security market line. Expected return is a linear function of beta; deviations from the line are alphas.

Course conventions:
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
The risk-free rate is 2.3% per year and the expected market return is 9.4% per year. Stocks X, Y, Z have betas 0.62, 1.18, and 1.51. Compute the CAPM expected annual return of each stock. Stock Y actually returned 13.1% over the year; compute its alpha relative to the CAPM prediction. Decimals.

Proceed in steps:
1. Apply the CAPM line E[Ri] = rf + beta (E[Rm] - rf) to each beta, in decimals.
2. Compute the alpha of stock Y against its CAPM prediction.
3. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'er_x', 'er_y', 'er_z', 'alpha_y'.
