You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: bond pricing with duration and convexity. Price is the discounted cashflow sum; duration and convexity measure its sensitivity to yield changes.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
For the bond with face 100, 4.6% coupon, 7 years to maturity, and current yield 5.3%, draw the exact price-yield curve for yields from 2% to 9% and overlay the duration-based approximations around the current yield, with a legend. Make the yield shift adjustable. Also report the exact price if the yield rises by 100 basis points and the duration-based estimate of the relative price change for that move.

Proceed in steps:
1. Price the bond on a yield grid from 2% to 9% for the exact curve.
2. Overlay the duration-based approximations around 5.3%.
3. Report the exact price at +100bp and the duration-based estimate of the relative change.
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'price_at_up100bp', 'dur_approx_change_up100bp', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
