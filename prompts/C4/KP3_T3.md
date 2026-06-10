You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: bond pricing with duration and convexity. Price is the discounted cashflow sum; duration and convexity measure its sensitivity to yield changes.

Course conventions:
- Bond yields are quoted with annual compounding; modified duration = Macaulay / (1+y); convexity = sum[t(t+1)CF_t/(1+y)^(t+2)] / P, in years squared.
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).
- For yield-shift estimates, the course rule of thumb is the first-order approximation dP/P = -D_mod * dy.

Task:
Take that 7-year bond we looked at - face 100, 4.6% annual coupon, yield 5.3%. If yields rise by 80 basis points, roughly how much does its price fall?

Proceed in steps:
1. Compute the modified duration at the current yield (annual compounding).
2. Apply the course rule of thumb dP/P = -D_mod * dy with dy = 0.008.
3. Report the magnitude of the fall as a positive decimal in `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'price_drop_pct'.
