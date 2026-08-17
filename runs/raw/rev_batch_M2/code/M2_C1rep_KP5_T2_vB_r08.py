import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取数据，fund列已经是日收益（题目指明）
df = pd.read_csv('data/market_snapshot_v1.csv')
returns = df['fund'].dropna()  # 剔除缺失值

# 2. 头寸100万，损益序列
position = 1_000_000
pnl = position * returns

# 3. 历史模拟法计算95%一日VaR（置信度可调）
alpha = 0.95  # 置信度，可调
var_percentile = np.percentile(pnl, 100 * (1 - alpha))
hist_var_95_1d = -var_percentile  # VaR用正数表示损失

# 4. 绘制损益直方图并标注VaR线
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7, color='skyblue')
plt.axvline(x=var_percentile, color='red', linestyle='--', linewidth=2,
            label=f'95% 1-Day VaR: {hist_var_95_1d:,.2f}')
plt.xlabel('P&L')
plt.ylabel('Frequency')
plt.title('Historical P&L Distribution (1-Day, 95% VaR)')
plt.legend()
plt.tight_layout()

# 5. 保存图片
figure_path = 'hist_var_plot.png'
plt.savefig(figure_path)
plt.close()

# 6. 输出结果字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

# 打印以便查看
print(result)
