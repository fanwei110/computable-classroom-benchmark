import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置置信度（可调）
confidence = 0.95

# 1. 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 2. 获取日收益率序列，假设 fund 列为小数形式的日收益率
returns = df['fund']

# 3. 计算头寸损益 (100万)
position = 1_000_000
pnl = position * returns  # 损益金额序列

# 4. 历史模拟法计算 VaR
# 损益左尾分位数（如5%分位数），取负号得到正 VaR 值
var_cutoff = np.percentile(pnl, 100 * (1 - confidence))
hist_var_95_1d = -var_cutoff

# 5. 绘制损益直方图并标注 VaR 线
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='skyblue', edgecolor='black', alpha=0.7, label='日损益分布')
plt.axvline(var_cutoff, color='red', linestyle='dashed', linewidth=2,
            label=f'{confidence*100:.0f}% 一日 VaR = {hist_var_95_1d:,.2f}')
plt.xlabel('损益（元）')
plt.ylabel('频次')
plt.title('历史模拟法 — 日损益分布与 VaR')
plt.legend()
plt.grid(True, alpha=0.3)

# 6. 保存图像
figure_path = 'hist_var_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 7. 输出字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': os.path.abspath(figure_path)
}

# 如果作为脚本运行，可以打印查看
print(result)
