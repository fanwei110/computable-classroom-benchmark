import pandas as pd
import numpy as np

# 1. 读取快照 CSV，假定文件名为 "snap.csv"，其中包含 "fund" 列（日收益率，小数形式）
df = pd.read_csv("snap.csv")

# 无风险利率：年化 2.1%
rf_annual = 0.021
rf_daily = rf_annual / 252   # 算术转换，与常见处理一致

# 2. 计算年化夏普比率
daily_excess = df["fund"] - rf_daily
mean_excess = daily_excess.mean()
std_excess = daily_excess.std()
sharpe_annual = (mean_excess / std_excess) * np.sqrt(252)

# 3. 业绩归因：配置效应、选择效应、交互效应
# 组合权重与收益（小数）
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与收益（小数）
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

allocation_effect = np.sum((w_p - w_b) * r_b)
selection_effect   = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# 4. 填充结果字典
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print(result)
