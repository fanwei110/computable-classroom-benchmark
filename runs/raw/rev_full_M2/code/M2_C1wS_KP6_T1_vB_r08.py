import numpy as np
import pandas as pd

# ------------------------------------------------------------
# 1. 读取快照 CSV，计算年化夏普比率
#    假设 CSV 文件名为 'snapshot.csv'，其中包含列 'fund_daily_return'
#    无风险利率年化 2.1%，折算为日度：rf_daily = 0.021 / 252
#    超额收益 = fund_daily_return - rf_daily
#    年化夏普比率 = sqrt(252) * mean(超额收益) / std(超额收益)
# ------------------------------------------------------------

rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

try:
    df = pd.read_csv('snapshot.csv')
    fund_ret = df['fund_daily_return'].values
    excess_ret = fund_ret - rf_daily
    sharpe_annual = np.sqrt(trading_days) * excess_ret.mean() / excess_ret.std()
except Exception as e:
    # 若文件不存在或列名不匹配，此处会抛出异常；教学场景下请确保文件正确。
    raise RuntimeError(f"读取 snapshot.csv 失败: {e}")

# ------------------------------------------------------------
# 2. Brinson 业绩归因
#    组合权重与收益
#    基准权重与收益
# ------------------------------------------------------------
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益

w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 配置效应 = Σ (w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ------------------------------------------------------------
# 3. 填充输出字典 result
# ------------------------------------------------------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果供投屏查看
print(result)
