import os
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# Helper: try to load fund daily returns, else generate deterministic data
# ----------------------------------------------------------------------
def load_fund_returns(filepath='fund.csv', seed=42, n_days=252):
    """Load 'fund' column from CSV, or generate synthetic data if missing."""
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        if 'fund' in df.columns:
            return df['fund'].values
        else:
            raise ValueError("CSV file must contain a 'fund' column.")
    # Synthetic data with fixed seed for reproducibility
    rng = np.random.default_rng(seed)
    # Daily mean ~0.0004 (10% annual), daily vol ~0.01 (15.87% annual)
    daily_returns = rng.normal(loc=0.0004, scale=0.01, size=n_days)
    return daily_returns

# ----------------------------------------------------------------------
# 1. Annualised Sharpe ratio
# ----------------------------------------------------------------------
fund_returns = load_fund_returns()
rf_annual = 0.021
rf_daily = rf_annual / 252  # simple daily rate

excess_daily = fund_returns - rf_daily
mean_excess_daily = np.mean(excess_daily)
std_excess_daily = np.std(excess_daily, ddof=1)   # sample std

sharpe_annual = np.sqrt(252) * mean_excess_daily / std_excess_daily

# ----------------------------------------------------------------------
# 2. Brinson attribution: allocation, selection, interaction
# ----------------------------------------------------------------------
w_p = np.array([0.45, 0.35, 0.20])   # portfolio weights
r_p = np.array([0.083, 0.021, -0.014])  # portfolio sector returns
w_b = np.array([0.40, 0.40, 0.20])   # benchmark weights
r_b = np.array([0.067, 0.034, -0.009]) # benchmark sector returns

# Total benchmark return
R_b = np.dot(w_b, r_b)

# Allocation effect: sum[(w_p - w_b) * (r_b - R_b)]
allocation_effect = np.sum((w_p - w_b) * (r_b - R_b))

# Selection effect: sum[w_b * (r_p - r_b)]
selection_effect = np.sum(w_b * (r_p - r_b))

# Interaction effect: sum[(w_p - w_b) * (r_p - r_b)]
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ----------------------------------------------------------------------
# Store results
# ----------------------------------------------------------------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# Output contract: print the result dictionary
if __name__ == '__main__':
    print(result)

