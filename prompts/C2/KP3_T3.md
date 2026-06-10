You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: bond pricing with duration and convexity. Price is the discounted cashflow sum; duration and convexity measure its sensitivity to yield changes.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
Take that 7-year bond we looked at - face 100, 4.6% annual coupon, yield 5.3%. If yields rise by 80 basis points, roughly how much does its price fall?

Proceed in steps:
1. Compute the bond's interest-rate sensitivity at the current yield.
2. Estimate the price impact of an 80 basis-point rise.
3. Report the size of the fall in `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'price_drop_pct'.
