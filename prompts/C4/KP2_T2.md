You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: the CAPM and the security market line. Expected return is a linear function of beta; deviations from the line are alphas.

Course conventions:
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
With a risk-free rate of 2.3% and an expected market return of 9.4% per year, draw the security market line for betas from 0 to 2. Plot stocks X (beta 0.62, expected return 8.1%), Y (beta 1.18, expected return 13.1%), and Z (beta 1.51, expected return 9.9%) as labeled points so it is visible which lie above or below the line. The figure should be parameterized so the risk-free rate and market return can be changed. Save the figure to the path given by the output contract. Also report the slope of the SML (the market risk premium) and the CAPM expected return at beta 1.27. Decimals.

Proceed in steps:
1. Draw the SML over betas 0 to 2 and plot the three labeled points.
2. Parameterize the risk-free rate and market return.
3. Report the slope and the expected return at beta 1.27, in decimals.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'sml_slope', 'er_at_beta_127', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
