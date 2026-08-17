import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 计算fund列的日收益率
fund_returns = df['fund'].dropna()

# 计算日收益率（简单收益率）
daily_returns = fund_returns.values

# 设置头寸
position = 1_000_000  # 100万

# 计算损益（P&L）
pnl = position * daily_returns

# 定义VaR置信度（可调整）
confidence_level = 0.95

# 历史法计算VaR
var_95 = -np.percentile(pnl, (1 - confidence_level) * 100)

# 创建直方图
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制损益直方图
n, bins, patches = ax.hist(pnl, bins=50, edgecolor='black', alpha=0.7, color='skyblue')

# 标记VaR线
ax.axvline(x=-var_95, color='red', linestyle='--', linewidth=2, 
           label=f'95% 1-Day VaR: ${var_95:,.2f}')

# 设置标题和标签
ax.set_xlabel('Profit/Loss ($)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title(f'Historical VaR Analysis - Daily P&L Distribution\nPosition: ${position:,}', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# 保存图表
figure_path = 'hist_var_figure.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.show()

# 构建结果字典
result = {
    'hist_var_95_1d': var_95,
    'figure_path': os.path.abspath(figure_path)
}

print(f"95% 1-Day Historical VaR: ${var_95:,.2f}")
print(f"Figure saved at: {result['figure_path']}")
