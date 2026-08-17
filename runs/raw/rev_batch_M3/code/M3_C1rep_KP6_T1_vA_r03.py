import numpy as np
import pandas as pd

# =============== 问题 1 计算逻辑 ===============
# df = pd.read_csv('课程数据文件.csv') # 请替换为实际文件读取方式
# daily_returns = df['fund']
# rf_daily = (1 + 0.021) ** (1/252) - 1
# excess_returns = daily_returns - rf_daily
# sharpe_annual = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)

# =============== 问题 2 计算结果 ===============
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

allocation_effect = float(np.sum((w_p - w_b) * r_b))
selection_effect = float(np.sum(w_b * (r_p - r_b)))
interaction_effect = float(np.sum((w_p - w_b) * (r_p - r_b)))

# =============== 输出字典 ===============
result = {
    'sharpe_annual': None,  # 需将此替换为上述问题1计算得出的 sharpe_annual 数值
    'allocation_effect': 0.00165,
    'selection_effect': 0.0002,
    'interaction_effect': 0.00145
}
