import pandas as pd
import numpy as np

# ========================
# 第一部分：年化夏普比率
# ========================
# 读取数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益率（假设列名为'fund'，数值为小数形式）
daily_returns = df['fund'].dropna().values

# 计算日平均收益和日波动率（使用样本标准差）
daily_mean = np.mean(daily_returns)
daily_std = np.std(daily_returns, ddof=1)

# 年化系数（假设一年252个交易日）
trading_days = 252

# 年化收益率和年化波动率
annual_return = daily_mean * trading_days
annual_volatility = daily_std * np.sqrt(trading_days)

# 无风险利率（年化）
risk_free_rate = 0.021

# 年化夏普比率
sharpe_annual = (annual_return - risk_free_rate) / annual_volatility

# ===========================================
# 第二部分：组合业绩归因（配置、选择、交互）
# ===========================================
# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 组合总收益与基准总收益
R_p = np.sum(w_p * r_p)
R_b = np.sum(w_b * r_b)

# 配置效应：(w_p - w_b) * (r_b - R_b)
allocation_effect = np.sum((w_p - w_b) * (r_b - R_b))

# 选择效应：w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应：(w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ========================
# 输出结果字典
# ========================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果以供课堂投屏展示
print("=== 计算结果（result 字典） ===")
for key, value in result.items():
    print(f"{key}: {value:.6f}")

# 结果可直接被教师调用，例如：
# result['sharpe_annual'] 等
