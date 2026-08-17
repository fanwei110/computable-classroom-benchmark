import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ================= 1. 参数与配置 =================
FILE_PATH = 'data/market_snapshot_v1.csv'
RF_ANNUAL = 0.021           # 年化无风险利率 2.1%
TRADING_DAYS = 252          # 一年交易日假设（业内通用）
WINDOW = 60                 # 滚动窗口长度（可调）
FIGURE_PATH = 'rolling_sharpe_ratio.png'

# ================= 2. 读取与处理数据 =================
# 读取快照 CSV
df = pd.read_csv(FILE_PATH)

# 尝试将可能的日期列设为索引，便于绘图时 X 轴自动格式化显示时间
date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
if date_cols:
    df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])
    df.set_index(date_cols[0], inplace=True)

# 提取 fund 列的日收益率，并去除可能存在的缺失值
fund_returns = df['fund'].dropna()

# ================= 3. 计算滚动年化夏普比率 =================
# 假设：日无风险利率采用简单算术平均折算（业内标准简化做法）
rf_daily = RF_ANNUAL / TRADING_DAYS

# 计算日超额收益
excess_returns = fund_returns - rf_daily

# 计算滚动均值与滚动标准差 (pandas 默认 ddof=1 为样本标准差，符合统计规范)
rolling_mean = excess_returns.rolling(window=WINDOW).mean()
rolling_std = excess_returns.rolling(window=WINDOW).std()

# 年化滚动夏普比率 = (日均超额收益 / 日收益标准差) * sqrt(252)
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)

# 报告最后一个窗口的夏普值（转为原生 float 避免序列化问题）
rolling_sharpe_last = float(rolling_sharpe.iloc[-1])

# ================= 4. 绘图与保存 =================
fig, ax = plt.subplots(figsize=(12, 6))

rolling_sharpe.plot(
    ax=ax, 
    color='tab:blue', 
    linewidth=1.5, 
    label=f'{WINDOW}-Day Rolling Annualized Sharpe Ratio'
)

ax.axhline(0, color='tab:red', linestyle='--', linewidth=1, label='Zero Line')
ax.set_title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio of the Fund', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Sharpe Ratio', fontsize=12)
ax.legend()
ax.grid(True, linestyle=':', alpha=0.7)

# 保存图形
fig.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close(fig)

# ================= 5. 输出契约 =================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}
