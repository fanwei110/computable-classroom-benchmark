You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Black-Scholes pricing of European options and the Greeks. Price, delta, and vega follow from the closed-form solution.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
A European call on a non-dividend-paying stock: spot 103.7, strike 97.5, implied volatility 27.6% (annualized), risk-free rate 4.3% per year, 0.58 years to expiry. Compute the call price, the delta, and the vega.

Proceed in steps:
1. Compute d1 and d2.
2. Price the call and compute the delta.
3. Compute the vega.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'call_price', 'call_delta', 'call_vega'.
