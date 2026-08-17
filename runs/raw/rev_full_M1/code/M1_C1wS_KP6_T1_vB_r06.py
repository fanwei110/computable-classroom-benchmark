import numpy as np
import pandas as pd

# ====================== 1. 模拟读取快照CSV数据 ======================
# 题目中给出了fund列的日收益和rf=2.1%，这里模拟构造数据
np.random.seed(42)  # 确保可复现
n_days = 252  # 假设一年有252个交易日
daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 模拟日收益率
rf_annual = 0.021  # 年化无风险利率2.1%
rf_daily = (1 + rf_annual) ** (1/252) - 1  # 转换为日无风险利率

# 创建DataFrame模拟CSV数据
data = pd.DataFrame({
    'fund': daily_returns,
    'rf': rf_daily
})

# ====================== 2. 计算年化夏普比率 ======================
# 计算超额收益（fund收益 - 无风险收益）
excess_returns = data['fund'] - data['rf']

# 计算年化夏普比率
sharpe_ratio_daily = excess_returns.mean() / excess_returns.std()
sharpe_annual = sharpe_ratio_daily * np.sqrt(252)

# ====================== 3. 业绩归因分析 ======================
# 题目给定的数据
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算各项效应
# 1. 配置效应（Allocation Effect）
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * (benchmark_returns - np.sum(benchmark_weights * benchmark_returns)))

# 2. 选择效应（Selection Effect）
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 3. 交互效应（Interaction Effect）
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns))

# ====================== 4. 填充result字典 ======================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果以便验证
print(result)
