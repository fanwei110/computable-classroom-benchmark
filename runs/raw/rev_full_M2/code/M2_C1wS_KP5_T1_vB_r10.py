import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

# 设定参数
position_value = 1_850_000  # 仓位185万人民币
annual_vol = 0.218  # 年化波动率21.8%
confidence_95 = 0.95  # 95%置信水平
confidence_99 = 0.99  # 99%置信水平
trading_days = 252  # 假设一年252个交易日

# 步骤1: 将年化波动率换算到一日期限
daily_vol = annual_vol / np.sqrt(trading_days)

# 步骤2: 对两个置信水平计算正态分布分位数
z_score_95 = stats.norm.ppf(1 - confidence_95)  # 95%置信水平的分位数
z_score_99 = stats.norm.ppf(1 - confidence_99)  # 99%置信水平的分位数

# 步骤3: 计算VaR
# 95%置信水平，一天期限
var_95_1d_percent = z_score_95 * daily_vol
var_95_1d = position_value * abs(var_95_1d_percent)

# 99%置信水平，十天期限（使用平方根时间法则缩放）
var_99_10d_percent = z_score_99 * daily_vol * np.sqrt(10)
var_99_10d = position_value * abs(var_99_10d_percent)

# 创建结果字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 输出结果
print("参数法VaR计算结果：")
print(f"95%置信水平，一天VaR: ¥{result['var_95_1d']:,.2f}")
print(f"99%置信水平，十天VaR: ¥{result['var_99_10d']:,.2f}")

# 可选：显示计算过程
print(f"\n计算细节：")
print(f"日波动率: {daily_vol:.4%}")
print(f"95%置信水平z分数: {z_score_95:.4f}")
print(f"99%置信水平z分数: {z_score_99:.4f}")
print(f"95%一天损失百分比: {var_95_1d_percent:.4%}")
print(f"99%十天损失百分比: {var_99_10d_percent:.4%}")

# 可视化VaR分布
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# 95%一天VaR的分布
x1 = np.linspace(-4, 4, 1000)
y1 = stats.norm.pdf(x1)
ax1.plot(x1, y1, 'b-', label='日收益分布')
ax1.axvline(x=z_score_95, color='r', linestyle='--', label=f'95% VaR: ¥{var_95_1d:,.0f}')
ax1.fill_between(x1[x1 <= z_score_95], y1[x1 <= z_score_95], alpha=0.3, color='red')
ax1.set_title('95% Confidence Level - 1 Day VaR')
ax1.set_xlabel('Standard Deviations')
ax1.set_ylabel('Probability Density')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 99%十天VaR的分布
x2 = np.linspace(-4, 4, 1000)
y2 = stats.norm.pdf(x2)
ax2.plot(x2, y2, 'b-', label='10日收益分布')
ax2.axvline(x=z_score_99, color='r', linestyle='--', label=f'99% VaR: ¥{var_99_10d:,.0f}')
ax2.fill_between(x2[x2 <= z_score_99], y2[x2 <= z_score_99], alpha=0.3, color='red')
ax2.set_title('99% Confidence Level - 10 Day VaR')
ax2.set_xlabel('Standard Deviations')
ax2.set_ylabel('Probability Density')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 验证result字典
print(f"\n最终结果字典: {result}")
