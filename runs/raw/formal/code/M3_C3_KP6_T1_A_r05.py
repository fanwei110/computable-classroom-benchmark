import pandas as pd
import numpy as np

# ================= 第一问：年化夏普比率 =================
# 读取数据（请根据实际文件名和格式调整）
# df = pd.read_csv('课程数据文件.csv') 
# daily_returns = df['fund']

# 假设 daily_returns 已经获取，计算夏普比率的逻辑如下：
rf_annual = 0.021
# 债券收益率按年复利报价，日化无风险利率：
rf_daily = (1 + rf_annual) ** (1/252) - 1

# excess_returns = daily_returns - rf_daily
# mean_excess = excess_returns.mean()
# std_daily = daily_returns.std(ddof=1)  # 样本标准差 ddof=1
# sharpe_annual = (mean_excess / std_daily) * np.sqrt(252)

# 注：因未挂载数据文件，此处使用占位符，若运行请取消注释上方的读取与计算代码
sharpe_annual = None 

# ================= 第二问：业绩归因 =================
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

allocation_effect = np.sum((w_p - w_b) * r_b)
selection_effect = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ================= 输出契约 =================
result = {
    'sharpe_annual': sharpe_annual,  # 运行数据后替换为实际数值
    'allocation_effect': float(allocation_effect),
    'selection_effect': float(selection_effect),
    'interaction_effect': float(interaction_effect)
}

print(result)
