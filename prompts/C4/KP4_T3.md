You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Black-Scholes pricing of European options and the Greeks. Price, delta, and vega follow from the closed-form solution.

Course conventions:
- The option risk-free rate is continuously compounded; vega is quoted per unit of volatility (dC/dsigma).
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
Same call as before - spot 103.7, strike 97.5, vol 27.6%, rate 4.3%, 0.58 years left. If implied volatility goes up by one percentage point, how much does the call price rise?

Proceed in steps:
1. Reprice the call exactly at volatility 28.6% and at 27.6% (continuously compounded rate).
2. Report the exact price difference in `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'price_change'.
