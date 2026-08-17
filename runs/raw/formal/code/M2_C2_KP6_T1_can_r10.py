import pandas as pd
import numpy as np

# ============================================================
# 1. 读取数据并计算年化夏普比率
# ============================================================
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_returns = df['fund']

# 若数据为百分比形式（如 2.0 代表 2%），自动转换为小数
if fund_returns.abs().median() > 0.1:
    fund_returns = fund_returns / 100.0

# 无风险利率设定（年化 2.1%，按 252 个交易日折算日化）
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 超额收益序列
excess_returns = fund_returns - rf_daily

# 年化夏普比率
sharpe_annual = (excess_returns.mean() / excess_returns.std()) * np.sqrt(trading_days)

# ============================================================
# 2. Brinson 业绩归因：配置效应、选择效应、交互效应
# ============================================================
# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应：Σ (w_p,i - w_b,i) * r_b,i
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应：Σ w_b,i * (r_p,i - r_b,i)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应：Σ (w_p,i - w_b,i) * (r_p,i - r_b,i)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# 可验证：总主动收益 = 配置 + 选择 + 交互
# total_active = np.sum(w_p * r_p) - np.sum(w_b * r_b)

# ============================================================
# 3. 结果输出
# ============================================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印供投屏展示
for key, value in result.items():
    print(f"{key}: {value:.6f}")
