import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置参数
confidence_level = 0.95  # 可调置信水平
position = 1_000_000  # 头寸100万元

# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')
returns = df['fund'].pct_change().dropna()  # 日收益率

# 计算日损益
daily_pnl = returns * position

# 计算历史VaR
var = -np.percentile(daily_pnl, 100 * (1 - confidence_level))

# 绘制直方图
plt.figure(figsize=(10, 6))
plt.hist(daily_pnl, bins=50, alpha=0.75, color='blue', edgecolor='black')

# 添加VaR线
plt.axvline(x=-var, color='red', linestyle='--', label=f'{confidence_level*100:.0f}% 1-day Historical VaR: {var:,.2f}')

plt.title('Daily P&L Distribution with Historical VaR')
plt.xlabel('Daily P&L (RMB)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_path = 'var_plot.png'
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'hist_var_95_1d': var,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
