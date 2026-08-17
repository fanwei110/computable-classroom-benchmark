import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取数据
data = pd.read_csv('data/market_snapshot_v1.csv')
returns = data['fund'].pct_change().dropna()  # 日收益率

# 计算损益（头寸100万）
position = 1_000_000
pnl = returns * position

# 计算95%置信度1日VaR
confidence_level = 0.95
var_95_1d = -np.percentile(pnl, 100 * (1 - confidence_level))

# 绘制直方图
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, color='blue', edgecolor='black')

# 添加VaR标根线
plt.axvline(x=-var_95_1d, color='red', linestyle='--', label=f'95% 1-day VaR: {var_95_1d:,.2f}')

plt.title('Profit & Loss Distribution with Historical VaR')
plt.xlabel('P&L (RMB)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_path = 'hist_var_plot.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'hist_var_95_1d': var_95_1d,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
