import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ========== 参数设置 ==========
DATA_PATH = 'data/market_snapshot_v1.csv'
POSITION = 1_000_000          # 头寸 100 万元
ALPHA = 0.95                  # 置信水平（可调）
FIG_PATH = 'var_histogram.png' # 图片保存路径

# ========== 1. 读取数据 ==========
df = pd.read_csv(DATA_PATH)

# 判断 fund 列是价格还是收益率：如果数值普遍在 1 附近波动，视为价格，计算日收益率
sample_vals = df['fund'].dropna().head(20)
if sample_vals.median() > 0.1:  # 价格型数据（>0.1 大概率是价格，非小数收益率）
    # 计算简单日收益率
    returns = df['fund'].pct_change().dropna()
else:
    # 已经是日收益率
    returns = df['fund'].dropna()

# 确保收益率是小数形式（如果百分比形式，则除以100）
if returns.abs().max() > 1:
    returns = returns / 100.0

# 计算日损益（单位：元）
pnl = POSITION * returns

# ========== 2. 历史法 VaR ==========
# 95% 置信水平对应 5% 分位数（左尾）
var_percentile = (1 - ALPHA) * 100
var_cutoff = np.percentile(pnl, var_percentile)  # 这是一个负值（损失）或小正值
hist_var_95_1d = -var_cutoff  # VaR 通常用正数表示损失大小

# ========== 3. 绘图 ==========
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, alpha=0.7, color='steelblue', edgecolor='white')
plt.axvline(var_cutoff, color='red', linestyle='dashed', linewidth=2,
            label=f'Hist VaR ({ALPHA*100:.0f}% 1d) = {hist_var_95_1d:,.2f} 元')
plt.xlabel('日损益 (元)')
plt.ylabel('频数')
plt.title('日损益直方图与历史法 VaR')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_PATH, dpi=150)
plt.close()

# ========== 4. 结果存入字典 ==========
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': os.path.abspath(FIG_PATH)
}

print(result)
