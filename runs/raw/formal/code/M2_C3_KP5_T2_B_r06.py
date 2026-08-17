import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------- 配置 ----------
csv_path = 'data/market_snapshot_v1.csv'   # 文件路径
position = 1_000_000                        # 头寸 100 万
conf_level = 0.95                           # 置信度 95%（可调）
output_fig = 'hist_var_plot.png'            # 图片文件名
# ------------------------

# 1. 读取数据
df = pd.read_csv(csv_path)
returns = df['fund'].dropna()               # 去除缺失值

# 2. 计算损益序列
pnl = position * returns.values

# 3. 历史法 VaR（左尾分位数，正损失金额）
var_cutoff = (1 - conf_level) * 100          # 分位数，如 5%
var_threshold = np.percentile(pnl, var_cutoff)
hist_var = -var_threshold                    # 正损失金额（若分位数为负，取反）

# 4. 绘制损益直方图并标记 VaR 线
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=100, color='steelblue', edgecolor='white', alpha=0.7, label='Daily P&L')
plt.axvline(var_threshold, color='red', linestyle='--', linewidth=2,
            label=f'{conf_level*100:.0f}% 1-Day VaR = {hist_var:,.2f}')
plt.xlabel('Profit & Loss')
plt.ylabel('Frequency')
plt.title('Historical VaR - P&L Distribution')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(output_fig, dpi=150)
plt.close()

# 5. 结果字典
result = {
    'hist_var_95_1d': round(hist_var, 2),
    'figure_path': os.path.abspath(output_fig)
}

print(result)
