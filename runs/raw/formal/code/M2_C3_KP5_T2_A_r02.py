import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------- 参数设置 --------------------
DATA_PATH = 'data/market_snapshot_v1.csv'   # 数据路径
POSITION = 1_000_000                         # 头寸（元）
CONF_LEVEL = 0.95                            # 置信水平（可调）
DAYS_PER_YEAR = 252                          # 年交易日数
OUTPUT_FIG = 'hist_var_figure.png'           # 图片保存路径

# -------------------- 1. 读取数据 --------------------
df = pd.read_csv(DATA_PATH)
# 假设 fund 列已经是小数日收益率（如 0.005 代表 0.5%）
daily_returns = df['fund'].dropna()

# -------------------- 2. 计算日损益 --------------------
pnl = POSITION * daily_returns   # 损益序列（正为盈利，负为损失）

# -------------------- 3. 历史法 VaR --------------------
# 左尾分位数（例如 5% 分位数）
var_cutoff = np.percentile(pnl, 100 * (1 - CONF_LEVEL))
# VaR 报告为正的损失金额
hist_var = -var_cutoff

# -------------------- 4. 绘图 --------------------
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7, label='Daily P&L')
plt.axvline(var_cutoff, color='red', linestyle='--', linewidth=2,
            label=f'{CONF_LEVEL*100:.0f}% 1-Day Historical VaR = {hist_var:,.2f} CNY')
plt.title('Daily P&L Distribution (Historical Simulation)')
plt.xlabel('P&L (CNY)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_FIG)
plt.close()

# -------------------- 5. 保存结果 --------------------
result = {
    'hist_var_95_1d': round(hist_var, 2),
    'figure_path': OUTPUT_FIG
}

print(result)
