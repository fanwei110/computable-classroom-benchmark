import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------- 加载与计算 --------------------
file_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(file_path)

# 提取 fund 列日收益（小数形式）
returns = df['fund'].dropna().values

# 头寸
position = 1_000_000  # 100万元

# 每日损益序列
pnl = position * returns

# 可调节的置信水平（此处设定为 95%）
confidence = 0.95
percentile = (1 - confidence) * 100  # 5% 分位数

# 历史 VaR（正数损失，按样本分位数计算）
var_cutoff = np.percentile(pnl, percentile)   # 损益的分位数（负数或正数）
var_amount = -var_cutoff   # 损失报告为正数

# 将 VaR 值保留两位小数
var_95_1d = round(var_amount, 2)

# -------------------- 绘图 --------------------
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='skyblue', edgecolor='white', alpha=0.7, density=True)
plt.axvline(var_cutoff, color='red', linestyle='--', linewidth=2,
            label=f'{int(confidence*100)}% 1‑Day Historical VaR: ¥{var_95_1d:,.2f}')
plt.xlabel('Daily P&L (¥)')
plt.ylabel('Frequency')
plt.title(f'Daily P&L Distribution (100万元 Fund) - Historical VaR')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图像
figure_dir = 'output'
os.makedirs(figure_dir, exist_ok=True)
fig_path = os.path.join(figure_dir, 'historical_var_fund.png')
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# -------------------- 结果字典 --------------------
result = {
    'hist_var_95_1d': var_95_1d,    # 例如 12345.67
    'figure_path': fig_path         # 'output/historical_var_fund.png'
}

print(result)
