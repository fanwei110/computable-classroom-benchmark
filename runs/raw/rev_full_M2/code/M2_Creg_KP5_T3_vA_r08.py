import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# ================================
# Input parameters
# ================================
position_value = 2_700_000      # 头寸价值 (元)
annual_vol = 0.24               # 年化波动率
confidence_level = 0.95         # VaR 置信水平
trading_days = 252              # 年交易日数假设

# ================================
# Calculation
# ================================
# 日波动率 (假设收益率独立同分布且均值为零)
daily_vol = annual_vol / np.sqrt(trading_days)

# 标准正态分布下置信水平对应的分位数 (单尾)
# ppf 返回下分位数，对于 95% 即为 1.64485...
z_score = norm.ppf(confidence_level)

# 绝对金额 VaR (损失取正)
var_95_1d = position_value * daily_vol * z_score

# ================================
# Output
# ================================
result = {
    'var_95_1d': var_95_1d
}

# 打印结果，便于检查
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print(result)

# ================================
# 可选：可视化演示
# ================================
x = np.linspace(-4, 4, 500)
y = norm.pdf(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, label='标准正态分布')
ax.fill_between(x[x <= -z_score], norm.pdf(x[x <= -z_score]),
                alpha=0.4, color='red', label=f'VaR 左侧尾部 (α=0.05)')
ax.axvline(-z_score, color='red', linestyle='--')
ax.set_title('95% 一日 VaR 示意图')
ax.set_xlabel('标准化收益率')
ax.set_ylabel('概率密度')
ax.legend()
plt.tight_layout()
plt.savefig('var_plot.png')   # 保存图片
plt.close()
