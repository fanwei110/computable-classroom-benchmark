import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取数据（如果实际文件存在，直接使用下面注释的pd.read_csv）
# df = pd.read_csv('data/market_snapshot_v1.csv')
# returns = df['fund']

# ---- 模拟数据演示（实际使用时删除此段） ----
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=500, freq='B')
returns = pd.Series(np.random.normal(0.001, 0.02, size=500), index=dates)
# ------------------------------------------

position = 1_000_000  # 头寸100万元
pnl = position * returns

# 2. 可调置信水平
conf_level = 0.95  # 95%

# 3. 计算历史VaR（损失正数）
var_cut = np.percentile(pnl, 100 * (1 - conf_level))
hist_var = -var_cut

# 4. 画图
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='k', alpha=0.7, label='Daily P&L')
plt.axvline(var_cut, color='red', linestyle='dashed', linewidth=2,
            label=f'Hist VaR ({conf_level*100:.0f}%): {hist_var:,.2f}')
plt.title('Daily P&L Distribution and Historical VaR')
plt.xlabel('P&L (CNY)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(alpha=0.3)

figure_path = 'hist_pnl_histogram.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 5. 输出结果字典
result = {
    'hist_var_95_1d': round(hist_var, 2),   # 以95%为例，数值根据实际数据定
    'figure_path': figure_path
}

print(result)
