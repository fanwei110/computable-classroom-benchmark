import pandas as pd
import numpy as np

# ----------------------------------------------------------------------
# 1. Read the daily fund returns
# ----------------------------------------------------------------------
# Assume CSV with column 'fund' containing daily returns (e.g., 0.001 for 0.1%)
df = pd.read_csv("data/market_snapshot_v1.csv")
fund_returns = df["fund"].dropna()  # remove any missing values

# ----------------------------------------------------------------------
# 2. Annualized Sharpe Ratio
# ----------------------------------------------------------------------
rf_annual = 0.021                 # annual risk‑free rate
trading_days = 252                # conventional number of trading days
rf_daily = rf_annual / trading_days

# Daily excess returns
excess_daily = fund_returns - rf_daily

# Annualized Sharpe: sqrt(252) * mean(daily excess) / std(daily excess)
# Sample standard deviation (ddof=1) is the market standard.
sharpe_annual = np.sqrt(trading_days) * excess_daily.mean() / excess_daily.std(ddof=1)

# ----------------------------------------------------------------------
# 3. Brinson performance attribution
# ----------------------------------------------------------------------
# Portfolio weights & returns for three sectors
wP = np.array([0.45, 0.35, 0.20])
rP = np.array([0.083, 0.021, -0.014])

# Benchmark weights & returns
wB = np.array([0.40, 0.40, 0.20])
rB = np.array([0.067, 0.034, -0.009])

# Allocation effect: (wP - wB) * rB
allocation_effect = np.sum((wP - wB) * rB)

# Selection effect: wB * (rP - rB)
selection_effect = np.sum(wB * (rP - rB))

# Interaction effect: (wP - wB) * (rP - rB)
interaction_effect = np.sum((wP - wB) * (rP - rB))

# ----------------------------------------------------------------------
# 4. Output dictionary
# ----------------------------------------------------------------------
result = {
    "sharpe_annual": float(sharpe_annual),
    "allocation_effect": float(allocation_effect),
    "selection_effect": float(selection_effect),
    "interaction_effect": float(interaction_effect),
}

# Display the results (for verification)
print(result)
