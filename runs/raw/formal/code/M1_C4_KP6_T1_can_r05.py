import numpy as np
import pandas as pd

# 第一部分：计算年化夏普比率
# 读取数据
data_path = 'data/market_snapshot_v1.csv'
market_data = pd.read_csv(data_path)

# 提取基金日收益率
fund_returns_daily = market_data['fund'].dropna().values

# 无风险利率（年化2.1%，日化=2.1%/252）
risk_free_rate_annual = 0.021
risk_free_rate_daily = risk_free_rate_annual / 252

# 计算超额收益（日收益 - 日无风险利率）
excess_returns_daily = fund_returns_daily - risk_free_rate_daily

# 计算样本标准差（ddof=1）
std_excess_daily = np.std(excess_returns_daily, ddof=1)

# 年化夏普比率（均值 / 标准差 * sqrt(252)）
sharpe_annual = np.mean(excess_returns_daily) / std_excess_daily * np.sqrt(252)

# 第二部分：Brinson-Hood-Beebower业绩归因
# 组合和基准的权重与收益
weights_portfolio = np.array([0.45, 0.35, 0.20])
weights_benchmark = np.array([0.40, 0.40, 0.20])
returns_portfolio = np.array([0.083, 0.021, -0.014])
returns_benchmark = np.array([0.067, 0.034, -0.009])

# 计算配置效应：Σ(w_p - w_b) * r_b
allocation_effect = np.sum((weights_portfolio - weights_benchmark) * returns_benchmark)

# 计算选择效应：Σw_b * (r_p - r_b)
selection_effect = np.sum(weights_benchmark * (returns_portfolio - returns_benchmark))

# 计算交互效应：Σ(w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((weights_portfolio - weights_benchmark) * (returns_portfolio - returns_benchmark))

# 存储结果
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（供课堂展示）
print(result)
