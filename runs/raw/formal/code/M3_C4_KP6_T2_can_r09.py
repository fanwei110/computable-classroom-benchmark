import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== 可调参数 ====================
WINDOW = 60                 # 滚动窗口长度（可按需调整）
RF_ANNUAL = 0.021           # 年化无风险利率（小数表示）
FIGURE_PATH = 'rolling_sharpe_ratio.png'  # 图形保存路径

# ==================== 1. 读取数据与无风险利率折算 ====================
df = pd.read_csv('data/market_snapshot_v1.csv')

# 日无风险利率 = 年无风险利率 / 252
rf_daily = RF_ANNUAL / 252

# 计算日超额收益
df['excess_return'] = df['fund'] - rf_daily

# ==================== 2. 计算滚动年化夏普比率 ====================
# 滚动均值与滚动标准差（样本标准差 ddof=1）
rolling_mean = df['excess_return'].rolling(window=WINDOW).mean()
rolling_std = df['excess_return'].rolling(window=WINDOW).std(ddof=1)

# 日夏普比率 = 平均超额收益 / 波动率
# 年化夏普比率 = 日夏普比率 * sqrt(252)
rolling_sharpe_annual = (rolling_mean / rolling_std) * np.sqrt(252)

# ==================== 3. 报告最后一个窗口的夏普值 ====================
rolling_sharpe_last = float(rolling_sharpe_annual.iloc[-1])

# ==================== 4. 画图并保存 ====================
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rolling_sharpe_annual.index, rolling_sharpe_annual.values, 
        label=f'{WINDOW}-Day Rolling Annualized Sharpe Ratio', color='blue')
ax.set_title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio over Time')
ax.set_xlabel('Time / Index')
ax.set_ylabel('Annualized Sharpe Ratio')
ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
ax.legend()
ax.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
fig.savefig(FIGURE_PATH, dpi=150)
plt.close(fig)

# ==================== 5. 封装输出契约 ====================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}
