import pandas as pd
import numpy as np

# ===== 第一问：计算年化夏普比率 =====
# 请将 'course_data.csv' 替换为您真实的课程数据文件名
try:
    df = pd.read_csv('course_data.csv')
    daily_returns = df['fund']
    
    rf_annual = 0.021
    rf_daily = rf_annual / 252  # 日无风险利率
    
    # 计算年化夏普比率
    mean_excess_daily = daily_returns.mean() - rf_daily
    std_daily = daily_returns.std()
    sharpe_annual = (mean_excess_daily / std_daily) * np.sqrt(252)
except Exception as e:
    print(f"数据文件读取失败，夏普比率暂设为None: {e}")
    sharpe_annual = None

# ===== 第二问：业绩归因计算 =====
W_p = np.array([0.45, 0.35, 0.20])
R_p = np.array([0.083, 0.021, -0.014])
W_b = np.array([0.40, 0.40, 0.20])
R_b = np.array([0.067, 0.034, -0.009])

allocation_effect = np.sum((W_p - W_b) * R_b)
selection_effect = np.sum(W_b * (R_p - R_b))
interaction_effect = np.sum((W_p - W_b) * (R_p - R_b))

# ===== 输出契约 =====
result = {
    'sharpe_annual': sharpe_annual,  # 若数据读取成功将为具体数值
    'allocation_effect': float(allocation_effect),
    'selection_effect': float(selection_effect),
    'interaction_effect': float(interaction_effect)
}

print(result)
