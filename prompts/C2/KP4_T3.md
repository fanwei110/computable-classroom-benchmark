You are the live coding assistant of a university securities-investment course. The instructor will run your code in front of the class, so it must be correct and self-contained.

Concept: Black-Scholes pricing of European options and the Greeks. Price, delta, and vega follow from the closed-form solution.

Assumptions:
- Choose appropriate, internally consistent computational assumptions wherever the task statement leaves a choice open.

Task:
Same call as before - spot 103.7, strike 97.5, vol 27.6%, rate 4.3%, 0.58 years left. If implied volatility goes up by one percentage point, how much does the call price rise?

Proceed in steps:
1. Work out how the call price responds to the one-point volatility move.
2. Report the price change in `result`.

Write one self-contained Python script. Use only numpy, scipy, pandas, and matplotlib. No internet access, no placeholder values, deterministic output, clear variable names.

Output contract: store all required outputs in a dictionary named `result` under exactly these keys: 'price_change'.
