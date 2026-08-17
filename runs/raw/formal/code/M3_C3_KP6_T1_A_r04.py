import pandas as pd
import numpy as np

# ================= 1. 年化夏普比率 =================
# 假设你的数据文件读取后存入 df，且日收益列名为 'fund'
# df = pd.read_csv('你的课程数据文件.csv')
# daily_returns = df['fund']

# 以下是计算逻辑（因无数据，暂以 None 占位，实际运行时取消注释即可）：
# mean_daily = daily_returns.mean()
# std_daily = daily_returns.std(ddof=1)  # 严格遵循ddof=1的样本标准差
# rf_annual = 0.021
# sharpe_annual = (mean_daily * 252 - rf_annual) / (std_daily * np.sqrt(252))

# ================= 2. 业绩归因计算 =================
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

allocation_effect = np.sum((w_p - w_b) * r_b)
selection_effect = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ================= 3. 结果存入字典 =================
result = {
    'sharpe_annual': None,  # 替换为上述计算出的 sharpe_annual 变量
    'allocation_effect': float(allocation_effect),
    'selection_effect': float(selection_effect),
    'interaction_effect': float(interaction_effect)
}

print(result)
