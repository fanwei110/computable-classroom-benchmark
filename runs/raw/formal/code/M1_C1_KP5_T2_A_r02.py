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

# 计算历史VaR
historical_pnl = returns * position  # 日损益
var_95_1d = -np.percentile(historical_pnl, 100 * (1 - confidence_level))

# 绘制直方图
plt.figure(figsize=(10, 6))
plt.hist(historical_pnl, bins=50, alpha=0.75, color='blue', edgecolor='black')
plt.axvline(x=-var_95_1d, color='red', linestyle='--', label=f'{confidence_level*100:.0f}% 1-day Historical VaR')
plt.title('Daily P&L Distribution with Historical VaR')
plt.xlabel('Daily P&L (RMB)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
os.makedirs('output', exist_ok=True)
figure_path = 'output/historical_var_plot.png'
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'hist_var_95_1d': var_95_1d,
    'figure_path': figure_path
}

print(result)
