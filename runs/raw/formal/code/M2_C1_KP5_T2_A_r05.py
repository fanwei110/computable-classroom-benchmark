import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 1. 读取数据并计算日收益率
# ------------------------------
df = pd.read_csv('data/market_snapshot_v1.csv')
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

# 假设 fund 列为基金净值，计算简单日收益率；若已是日收益率，则直接使用
# 检查是否像收益率（绝对值普遍小于1且平均值接近0）
if df['fund'].abs().mean() < 0.1:  # 经验阈值，判断是否已是收益率
    returns = df['fund'].dropna()
else:
    returns = df['fund'].pct_change().dropna()

# ------------------------------
# 2. 参数设置（置信水平可调）
# ------------------------------
position = 1_000_000                # 头寸 100 万元
confidence_level = 0.95             # 可调置信水平
alpha = 1 - confidence_level

# ------------------------------
# 3. 计算历史法 VaR
# ------------------------------
var_return = np.percentile(returns, alpha * 100)   # 收益率的分位数（通常为负值）
hist_var = -position * var_return                 # VaR 以正数表示损失

# ------------------------------
# 4. 日损益与直方图
# ------------------------------
pnl = position * returns

plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='k', alpha=0.7, label='Daily PnL')
plt.axvline(x=-hist_var, color='r', linestyle='--', linewidth=2,
            label=f'{confidence_level*100:.0f}% 1-Day Historical VaR: ¥{hist_var:,.2f}')
plt.xlabel('Daily Profit & Loss (¥)')
plt.ylabel('Frequency')
plt.title('Historical VaR - Daily PnL Distribution')
plt.legend()
figure_path = 'hist_var_plot.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ------------------------------
# 5. 输出结果字典
# ------------------------------
result = {
    'hist_var_95_1d': round(hist_var, 2),
    'figure_path': figure_path
}

print(result)
