You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: bond pricing with duration and convexity. Price is the discounted cashflow sum; duration and convexity measure its sensitivity to yield changes.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
A bullet bond has face value 100, a 4.6% coupon, 7 years to maturity, and trades at a yield to maturity of 5.3%. Compute the price, the Macaulay duration, the modified duration, and the convexity.

Proceed in steps:
1. Discount the cashflows at the quoted yield to price the bond.
2. Compute the Macaulay duration and the modified duration.
3. Compute the convexity.
4. Populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'price', 'macaulay_duration_years', 'modified_duration_years', 'convexity'.
