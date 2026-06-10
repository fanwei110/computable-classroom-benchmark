You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: the CAPM and the security market line. Expected return is a linear function of beta; deviations from the line are alphas.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
A stock has a beta of 1.42. Last month the market fell 5.8%, and the risk-free rate is 4.7% a year. What does CAPM say the stock's return should have been last month?

Proceed in steps:
1. Convert the annual risk-free rate to a monthly figure in a suitable way.
2. Apply the CAPM line at the monthly horizon.
3. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'capm_return_monthly'.
