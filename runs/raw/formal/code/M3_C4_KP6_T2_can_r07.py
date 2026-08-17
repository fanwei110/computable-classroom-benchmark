import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 防止弹窗，适配投屏环境
import matplotlib.pyplot as plt

# ==========================================
# 课程计算约定与参数设置
# ==========================================
TRADING_DAYS_PER_YEAR = 252
RF_ANNUAL = 0.021  # 年无风险利率 2.1%
RF_DAILY = RF_ANNUAL / TRADING_DAYS_PER_YEAR  # 日无风险利率，简单除法

WINDOW = 60  # 滚动窗口长度，设为变量可调
FIGURE_PATH = 'rolling_sharpe_ratio.png'

# ==========================================
# 步骤 1：读取快照 CSV，提取日收益
# ==========================================
df = pd.read_csv('data/market_snapshot_v1.csv')
daily_returns = df['fund']

# ==========================================
# 步骤 2：计算 60 日滚动年化夏普比率
# ==========================================
# 计算超额日收益
excess_daily_returns = daily_returns - RF_DAILY

# 计算滚动均值和滚动标准差（严格使用 ddof=1 样本估计量）
rolling_mean = excess_daily_returns.rolling(window=WINDOW).mean()
rolling_std = excess_daily_returns.rolling(window=WINDOW).std(ddof=1)

# 计算日夏普比率并年化（波动率按 sqrt(252) 缩放，收益按 252 累乘，综合乘子为 sqrt(252)）
rolling_sharpe_daily = rolling_mean / rolling_std
rolling_sharpe_annualized = rolling_sharpe_daily * np.sqrt(TRADING_DAYS_PER_YEAR)

# ==========================================
# 步骤 3：报告最后一个窗口的值并绘图
# ==========================================
# 提取最后一个窗口（最近一天）的夏普值
rolling_sharpe_last = rolling_sharpe_annualized.iloc[-1]

# 绘制时间序列图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rolling_sharpe_annualized.index, rolling_sharpe_annualized.values, 
        label=f'{WINDOW}-Day Rolling Annualized Sharpe', color='royalblue', linewidth=1.2)

ax.set_title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (Fund)', fontsize=14)
ax.set_xlabel('Time Index', fontsize=12)
ax.set_ylabel('Sharpe Ratio', fontsize=12)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')  # 零轴参考线
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=11)

# ==========================================
# 步骤 4：保存图形并填充 result 字典
# ==========================================
fig.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close(fig)

result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}
