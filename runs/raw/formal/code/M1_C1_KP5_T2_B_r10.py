import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取数据
data = pd.read_csv('data/market_snapshot_v1.csv')
returns = data['fund'].pct_change().dropna()  # 日收益率

# 参数设置
position = 1_000_000  # 头寸100万
confidence_level = 0.95  # 置信度95%

# 计算损益
pnl = returns * position

# 计算历史法VaR
var_95_1d = -np.percentile(pnl, 100 * (1 - confidence_level))

# 绘制直方图
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')
plt.axvline(x=-var_95_1d, color='red', linestyle='--', label=f'95% 1-day VaR: {var_95_1d:,.2f}元')
plt.title('Profit & Loss Distribution with Historical VaR')
plt.xlabel('Profit & Loss (CNY)')
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
