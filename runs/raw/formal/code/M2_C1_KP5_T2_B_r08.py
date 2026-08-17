import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------- 参数设置 ----------------------------
position = 1_000_000          # 头寸 100 万
confidence = 0.95             # 置信度，可调（如改为 0.99）
# -----------------------------------------------------------------

# 1. 读取数据 & 计算损益
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_returns = df['fund'].dropna()          # 去除缺失值
pnl = position * fund_returns               # 日损益序列

# 2. 计算历史 VaR（损益分位数，左尾）
var_cutoff = np.percentile(pnl, 100 * (1 - confidence))   # 5% 分位数
var_value = -var_cutoff   # 转化为损失正值（若分位数为负，VaR为正；反之则负）

# 3. 绘制直方图，并标出 VaR 线
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='k', alpha=0.7, color='steelblue')
plt.axvline(var_cutoff, color='red', linestyle='--', linewidth=2,
            label=f'VaR {confidence*100:.0f}% = {var_value:,.2f}')
plt.xlabel('Profit & Loss (¥)')
plt.ylabel('Frequency')
plt.title('Historical P&L Distribution with 1-Day VaR')
plt.legend()
plt.grid(alpha=0.3)

# 4. 保存图片并构建结果字典
figure_path = 'var_histogram.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

result = {
    'hist_var_95_1d': var_value,
    'figure_path': os.path.abspath(figure_path)
}

# 5. 报告结果
print("✅ 计算完成，结果字典：")
print(result)
