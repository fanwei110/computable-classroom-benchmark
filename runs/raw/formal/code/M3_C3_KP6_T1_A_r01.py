import pandas as pd
import numpy as np

# ================= 第一问：计算年化夏普比率 =================
# 注：因缺少实际课程数据文件，以下为计算逻辑代码
# df = pd.read_csv('课程数据文件.csv') 
# daily_returns = df['fund']
# rf_daily = 0.021 / 252
# excess_returns = daily_returns - rf_daily
# sharpe_annual = (excess_returns.mean() / daily_returns.std(ddof=1)) * np.sqrt(252)
sharpe_annual = None  # 无数据文件暂设为 None

# ================= 第二问：业绩归因计算 =================
wp = np.array([0.45, 0.35, 0.20])
rp = np.array([0.083, 0.021, -0.014])
wb = np.array([0.40, 0.40, 0.20])
rb = np.array([0.067, 0.034, -0.009])

allocation_effect = np.sum((wp - wb) * rb)
selection_effect = np.sum(wb * (rp - rb))
interaction_effect = np.sum((wp - wb) * (rp - rb))

# ================= 输出契约 =================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': float(allocation_effect),
    'selection_effect': float(selection_effect),
    'interaction_effect': float(interaction_effect)
}

print(result)
