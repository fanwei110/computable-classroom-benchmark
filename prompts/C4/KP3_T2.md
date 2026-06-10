You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: bond pricing with duration and convexity. Price is the discounted cashflow sum; duration and convexity measure its sensitivity to yield changes.

Course conventions:
- Bond yields are quoted with annual compounding; modified duration = Macaulay / (1+y); convexity = sum[t(t+1)CF_t/(1+y)^(t+2)] / P, in years squared.
- Express all rates, returns, volatilities, and weights as decimals (0.05 means 5%).
- For yield-shift estimates, the course rule of thumb is the first-order approximation dP/P = -D_mod * dy.

Task:
For the bond with face 100, 4.6% annual coupon, 7 years to maturity, and current yield 5.3% (annual compounding), draw the exact price-yield curve for yields from 2% to 9%, and overlay (i) the first-order modified-duration approximation and (ii) the duration-plus-convexity approximation around the current yield, with a legend distinguishing the three. The yield shift should be an adjustable parameter. Save the figure to the path given by the output contract. Also report the exact price if the yield rises by 100 basis points, and the first-order modified-duration estimate of the relative price change for that move (a decimal, negative for a fall).

Proceed in steps:
1. Price the bond on a yield grid from 2% to 9% (annual compounding) for the exact curve.
2. Overlay the first-order duration line and the duration-plus-convexity curve around 5.3%.
3. Report the exact price at +100bp and the first-order relative change (decimal, negative for a fall).
4. Save the figure and populate `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'price_at_up100bp', 'dur_approx_change_up100bp', 'figure_path'. Save the figure to a file and store its path under result['figure_path'].
