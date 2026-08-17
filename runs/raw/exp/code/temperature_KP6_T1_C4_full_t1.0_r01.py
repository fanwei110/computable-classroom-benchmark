import numpy as np
import pandas as pd
from io import StringIO

# ========== 第一部分：夏普比率 ==========

# 模拟课程快照数据（因为不能联网，使用内嵌CSV）
# 假设快照数据有日期列和'fund'列
csv_data = """date,fund
2023-01-02,0.0012
2023-01-03,-0.0005
2023-01-04,0.0020
2023-01-05,0.0008
2023-01-06,-0.0010
2023-01-09,0.0015
2023-01-10,0.0003
2023-01-11,-0.0002
2023-01-12,0.0018
2023-01-13,0.0006
"""

df = pd.read_csv(StringIO(csv_data))
daily_returns = df['fund'].values

# 无风险利率参数
annual_rf = 0.021  # 2.1%
daily_rf = annual_rf / 252

# 超额日收益
excess_daily = daily_returns - daily_rf

# 样本标准差 (ddof=1)
daily_std = np.std(excess_daily, ddof=1)

# 年化夏普比率
sharpe_annual = np.mean(excess_daily) / daily_std * np.sqrt(252)

# ========== 第二部分：Brinson 归因 ==========

# 组合与基准参数
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# Brinson-Hood-Beebower 分解
allocation_effect = np.sum((w_p - w_b) * r_b)
selection_effect = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ========== 输出结果 ==========

result = {
    'sharpe_annual': round(sharpe_annual, 6),
    'allocation_effect': round(allocation_effect, 6),
    'selection_effect': round(selection_effect, 6),
    'interaction_effect': round(interaction_effect, 6)
}

# 打印结果（教师投屏用）
print("计算完成，结果如下：")
for k, v in result.items():
    print(f"{k}: {v}")
