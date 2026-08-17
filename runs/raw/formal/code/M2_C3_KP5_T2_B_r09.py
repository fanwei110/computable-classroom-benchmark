import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------
# 1. 读取数据（若为真实数据，请取消注释）
# df = pd.read_csv('data/market_snapshot_v1.csv')
# returns = df['fund']
# ------------------------------
# 模拟日收益率（小数形式）
np.random.seed(42)
n = 1000
returns = pd.Series(np.random.normal(0.0002, 0.015, n))  # 均值0.02%, 波动1.5%

# 头寸
position = 1_000_000  # 100万

# 每日损益
pnl = position * returns

# ------------------------------
# 2. 历史法 VaR（95% 一日）
confidence = 0.95
var_percentile = (1 - confidence) * 100  # 5

# 损益从小到大排序
sorted_pnl = np.sort(pnl)
# 5%分位的索引（使用线性插值）
var_loss = -np.percentile(sorted_pnl, var_percentile)  # 损失为正

# ------------------------------
# 3. 画直方图并标出 VaR
plt.figure(figsize=(8, 5))
plt.hist(pnl, bins=50, color='steelblue', edgecolor='white', alpha=0.8)
plt.axvline(-var_loss, color='red', linestyle='dashed', linewidth=2,
            label=f'95% 1-day VaR = {var_loss:,.2f}')
plt.title('Historical P&L Distribution (Fund)')
plt.xlabel('P&L')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()

# 保存图片
figure_path = 'var_histogram.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ------------------------------
# 4. 存结果
result = {
    'hist_var_95_1d': round(var_loss, 2),
    'figure_path': os.path.abspath(figure_path)
}

print(result)
