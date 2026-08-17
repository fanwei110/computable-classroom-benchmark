import numpy as np
import pandas as pd

# ==================== Part 1: Annualized Sharpe Ratio ====================

# Read CSV snapshot
df = pd.read_csv('data/market_snapshot_v1.csv')

# Extract fund daily returns
fund_returns = df['fund'].values

# Annual risk-free rate
rf_annual = 0.021

# Convert annual risk-free rate to daily (compound convention, 252 trading days)
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# Compute daily excess returns: fund return minus daily risk-free rate
excess_returns_daily = fund_returns - rf_daily

# Compute mean and standard deviation of daily excess returns
mean_excess_daily = np.mean(excess_returns_daily)
std_excess_daily = np.std(excess_returns_daily, ddof=1)  # sample std

# Annualized Sharpe ratio: daily Sharpe × sqrt(252)
sharpe_daily = mean_excess_daily / std_excess_daily
sharpe_annual = sharpe_daily * np.sqrt(252)

# ==================== Part 2: Brinson Attribution ====================

# Portfolio weights and sector returns
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# Benchmark weights and sector returns
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# Allocation effect: Σ (w_p - w_b) × r_b
#   Measures impact of overweighting/underweighting sectors vs benchmark,
#   evaluated at benchmark sector returns
allocation_effect = np.sum((w_p - w_b) * r_b)

# Selection effect: Σ w_b × (r_p - r_b)
#   Measures impact of superior/inferior sector-level returns vs benchmark,
#   evaluated at benchmark weights
selection_effect = np.sum(w_b * (r_p - r_b))

# Interaction effect: Σ (w_p - w_b) × (r_p - r_b)
#   Joint effect of simultaneously differing in weight and return
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ==================== Verification ====================
# Portfolio return
r_portfolio = np.sum(w_p * r_p)
# Benchmark return
r_benchmark = np.sum(w_b * r_b)
# Total active return should equal sum of three effects
active_return = r_portfolio - r_benchmark
total_effect = allocation_effect + selection_effect + interaction_effect
assert np.isclose(active_return, total_effect), \
    f"Brinson decomposition mismatch: {active_return} ≠ {total_effect}"

# ==================== Result Dictionary ====================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print("===== 结果 =====")
for k, v in result.items():
    print(f"{k}: {v}")

# Verification print
print(f"\n[验证] 组合收益: {r_portfolio:.6f}")
print(f"[验证] 基准收益: {r_benchmark:.6f}")
print(f"[验证] 主动收益: {active_return:.6f}")
print(f"[验证] 三效应之和: {total_effect:.6f}")
