import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------- 可调参数 ----------
CONFIDENCE = 0.95            # 置信度（可调）
INVESTMENT = 1_000_000       # 头寸 100 万
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'var_histogram.png'  # 图片保存路径
# ----------------------------

# 1. 读取数据
df = pd.read_csv(DATA_PATH)
returns = df['fund']  # 日收益率（假设为小数，例如 0.01 表示 1%）

# 2. 计算损益
pnl = returns * INVESTMENT

# 3. 历史 VaR（5% 分位数，取负值表示损失额）
var_cutoff = np.percentile(pnl, (1 - CONFIDENCE) * 100)  # 损益的分位数
hist_var_95_1d = -var_cutoff  # VaR 为正的损失金额

# 4. 绘制直方图并标注 VaR 线
plt.figure(figsize=(8, 5))
plt.hist(pnl, bins=50, color='skyblue', edgecolor='black', alpha=0.7, label='Daily P&L')
plt.axvline(var_cutoff, color='red', linestyle='dashed', linewidth=2,
            label=f'95% 1-day VaR: {hist_var_95_1d:,.2f}')
plt.xlabel('Profit & Loss')
plt.ylabel('Frequency')
plt.title('Historical VaR - 95% Confidence')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURE_PATH)
plt.close()

# 5. 构造结果字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': os.path.abspath(FIGURE_PATH)
}

print("Result Dictionary:")
print(result)
