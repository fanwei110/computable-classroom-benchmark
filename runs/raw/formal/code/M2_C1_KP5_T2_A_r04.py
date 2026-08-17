import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- 参数 ----------
confidence_level = 0.95
position = 1_000_000  # 头寸 100 万元
file_path = 'data/market_snapshot_v1.csv'
fig_path = 'var_hist.png'

# ---------- 读取数据 ----------
df = pd.read_csv(file_path)
returns = df['fund']  # 日收益率（假设为小数形式，如 0.01 代表 1%）

# ---------- 计算日损益 ----------
pnl = position * returns

# ---------- 历史法 VaR ----------
var_percentile = (1 - confidence_level) * 100
var_value = -np.percentile(pnl, var_percentile)  # VaR 取正数表示损失

# ---------- 作图 ----------
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7)
plt.axvline(x=-var_value, color='red', linestyle='--', linewidth=2,
            label=f'{int(confidence_level*100)}% Historical VaR: {var_value:,.2f}')
plt.xlabel('Daily P&L')
plt.ylabel('Frequency')
plt.title('Daily P&L Distribution with Historical VaR')
plt.legend()
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ---------- 结果 ----------
result = {
    'hist_var_95_1d': round(var_value, 2),
    'figure_path': fig_path
}

print(result)
