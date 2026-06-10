You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Black-Scholes pricing of European options and the Greeks. Price, delta, and vega follow from the closed-form solution.

Course conventions:
- The option risk-free rate is continuously compounded; vega is quoted per unit of volatility (dC/dsigma).
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
For the European call with strike 97.5, risk-free rate 4.3% per year (continuous compounding), and 0.58 years to expiry on a non-dividend stock, draw the call delta as a function of the spot price from 70 to 140, with three curves for implied volatilities 15%, 27.6%, and 40%, labeled in a legend. Volatility should be an adjustable parameter. Save the figure to the path given by the output contract. Also report the delta at spot 110 with volatility 27.6%. Decimals.

Proceed in steps:
1. Compute delta = N(d1) over the spot grid for each volatility (continuously compounded rate).
2. Draw the three labeled curves and parameterize the volatility.
3. Report the delta at spot 110 with volatility 27.6%, as a decimal.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'delta_at_s110', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
