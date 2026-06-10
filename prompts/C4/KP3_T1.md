You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: bond pricing with duration and convexity. Price is the discounted cashflow sum; duration and convexity measure its sensitivity to yield changes.

Course conventions:
- Bond yields are quoted with annual compounding; modified duration = Macaulay / (1+y); convexity = sum[t(t+1)CF_t/(1+y)^(t+2)] / P, in years squared.
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).

Task:
A bullet bond has face value 100, a 4.6% annual coupon (paid once a year), 7 years to maturity, and trades at a yield to maturity of 5.3% (annual compounding), valued at a coupon date. Compute the price, the Macaulay duration (years), the modified duration (years), and the convexity (in years squared, defined as sum[t(t+1)CF_t/(1+y)^(t+2)]/P).

Proceed in steps:
1. Discount the annual coupons and face at the annually-compounded yield to price the bond.
2. Compute the Macaulay duration; divide by (1+y) for the modified duration.
3. Compute the convexity as sum[t(t+1)CF/(1+y)^(t+2)]/P, in years squared.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'price', 'macaulay_duration_years', 'modified_duration_years', 'convexity'.
