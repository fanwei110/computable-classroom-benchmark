import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
file_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(file_path)

# 计算fund列的日收益率 (假设fund列为基金净值)
df['daily_return'] = df['fund'].pct_change()
returns = df['daily_return'].dropna()

# 设定头寸和可调的置信水平
position = 1000000  # 100万元
confidence_level = 0.95  # 置信水平，可在此处调整

# 计算日损益 (PnL)
pnl = returns * position

# 历史模拟法计算VaR：取损益序列的 (1 - 置信水平) 分位数，取负值表示损失
hist_var_95_1d = -np.percentile(pnl, (1 - confidence_level) * 100)

# 绘制日损益直方图
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

# 标出95%一日历史VaR线 (在直方图中，VaR对应的损失是负数，即 -hist_var_95_1d)
plt.axvline(x=-hist_var_95_1d, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1-day Historical VaR: {hist_var_95_1d:.2f} 元')

plt.title('日损益分布直方图及历史VaR')
plt.xlabel('日损益 (元)')
plt.ylabel('频数')
plt.legend()
plt.grid(axis='y', alpha=0.5)

# 保存图片
figure_path = 'pnl_var_histogram.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 按照输出契约构建结果字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

print(f"计算完成！95%一日历史VaR为: {hist_var_95_1d:.2f} 元")
print(f"图片已保存至: {figure_path}")
