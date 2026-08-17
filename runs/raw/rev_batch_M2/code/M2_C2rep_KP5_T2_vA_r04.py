import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------
# 参数设置
# ------------------------------
POSITION_VALUE = 1_000_000       # 头寸价值（人民币）
CONFIDENCE = 0.95                # 置信水平（可调参数）
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'var_histogram.png'

# ------------------------------
# 1. 读取数据并构造日损益
# ------------------------------
df = pd.read_csv(DATA_PATH)
returns = df['fund'].dropna().values.astype(float)

# 如果数据是百分比形式（例如 2.5 表示 2.5%），则转换为小数
if np.max(np.abs(returns)) > 1.0:
    returns = returns / 100.0

# 计算日损益（人民币）
pnl = POSITION_VALUE * returns

# ------------------------------
# 2. 计算历史模拟 VaR
# ------------------------------
var_percentile = 100 * (1 - CONFIDENCE)
var_loss = -np.percentile(pnl, var_percentile)  # 损失为正数

# ------------------------------
# 3. 绘制直方图并标注 VaR
# ------------------------------
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='skyblue', edgecolor='white', alpha=0.7, density=True)
plt.axvline(-var_loss, color='red', linestyle='dashed', linewidth=2,
            label=f'VaR {CONFIDENCE*100:.0f}% = ¥{var_loss:,.2f}')
plt.xlabel('日损益（人民币）')
plt.ylabel('频率密度')
plt.title(f'日损益分布与历史 VaR（置信水平 {CONFIDENCE*100:.0f}%）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=150)
plt.close()

# ------------------------------
# 4. 填充输出结果
# ------------------------------
result = {
    'hist_var_95_1d': round(var_loss, 2),
    'figure_path': os.path.abspath(FIGURE_PATH)
}

# 打印结果以供教师查看
print(result)
