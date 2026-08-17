import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 1. 读取数据
# ------------------------------
df = pd.read_csv('data/market_snapshot_v1.csv')

# ------------------------------
# 2. 提取 fund 列的日收益（假设为收益率）
# ------------------------------
fund_returns = df['fund'].astype(float)

# 头寸
position = 1_000_000   # 100万元

# 日损益序列
pnl = position * fund_returns

# ------------------------------
# 3. VaR 计算（置信水平可调）
# ------------------------------
confidence = 0.95               # 可调整的置信水平
alpha = 1 - confidence

# 历史模拟法 VaR：损益分布左尾分位数的绝对值
var_threshold = np.percentile(pnl, 100 * alpha)   # 损益在 alpha 分位点的值
var_value = -var_threshold                        # 损失表示为正数

# ------------------------------
# 4. 绘图
# ------------------------------
plt.figure(figsize=(8, 5))
plt.hist(pnl, bins=50, edgecolor='k', alpha=0.7)
plt.axvline(var_threshold, color='r', linestyle='--', linewidth=2,
            label=f'{confidence*100:.0f}% 1‑Day Hist VaR = {var_value:,.2f}')
plt.title(f'Daily P&L Distribution (Position = {position:,})')
plt.xlabel('Profit / Loss')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()

# 保存图像
figure_path = 'hist_var_plot.png'
plt.savefig(figure_path)
plt.close()

# ------------------------------
# 5. 结果存入字典
# ------------------------------
result = {
    'hist_var_95_1d': var_value,
    'figure_path': figure_path
}

# 输出查看
print(f"95% 1‑Day Historical VaR = {var_value:,.2f}")
print(f"Figure saved to: {figure_path}")
