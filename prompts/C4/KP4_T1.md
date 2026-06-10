You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Black-Scholes pricing of European options and the Greeks. Price, delta, and vega follow from the closed-form solution.

Course conventions:
- The option risk-free rate is continuously compounded; vega is quoted per unit of volatility (dC/dsigma).
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
A European call on a non-dividend-paying stock: spot 103.7, strike 97.5, implied volatility 27.6% (annualized), risk-free rate 4.3% per year with continuous compounding, time to expiry 0.58 years. Compute the Black-Scholes call price, the call delta, and the vega quoted per unit of volatility (dC/dsigma). Decimals.

Proceed in steps:
1. Compute d1 and d2 with the continuously compounded rate.
2. Price the call and compute delta = N(d1).
3. Compute vega per unit of volatility (dC/dsigma), in decimals.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'call_price', 'call_delta', 'call_vega'.
