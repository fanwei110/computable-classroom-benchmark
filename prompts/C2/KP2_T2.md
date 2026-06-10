You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: the CAPM and the security market line. Expected return is a linear function of beta; deviations from the line are alphas.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
With a risk-free rate of 2.3% and an expected market return of 9.4% per year, draw the security market line for betas 0 to 2 and plot stocks X (beta 0.62, return 8.1%), Y (beta 1.18, return 13.1%), and Z (beta 1.51, return 9.9%) as labeled points. Make the risk-free rate and market return adjustable. Also report the slope of the SML and the CAPM expected return at beta 1.27.

Proceed in steps:
1. Draw the SML over betas 0 to 2 and plot the three labeled points.
2. Parameterize the risk-free rate and market return.
3. Report the slope and the expected return at beta 1.27.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'sml_slope', 'er_at_beta_127', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
