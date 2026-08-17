import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
ANNUAL_TRADING_DAYS = 252    # 每年交易日
RF_ANNUAL = 0.021           # 年化无风险利率 2.1%
WINDOW = 60                 # 可调滚动窗口长度
FIGURE_PATH = 'rolling_sharpe.png'

# ==================== 1. 读取快照与无风险利率折算 ====================
df = pd.read_csv('data/market_snapshot_v1.csv')
daily_returns = df['fund']

# 日无风险利率 = 年利率 / 252
rf_daily = RF_ANNUAL / ANNUAL_TRADING_DAYS

# ==================== 2. 计算 60 日滚动夏普（ddof=1），按 sqrt(252) 年化 ====================
# 计算指定窗口的滚动均值和滚动标准差（ddof=1 为样本标准差）
rolling_mean = daily_returns.rolling(window=WINDOW).mean()
rolling_std = daily_returns.rolling(window=WINDOW).std(ddof=1)

# 计算滚动年化夏普比率：(滚动日均值 - 日无风险) / 滚动日标准差 * sqrt(252)
# 注：由于日无风险利率在每日为常数，超额收益的标准差与原收益率标准差一致
rolling_sharpe = (rolling_mean - rf_daily) / rolling_std * np.sqrt(ANNUAL_TRADING_DAYS)

# ==================== 3. 报告最后一个窗口的值（小数） ====================
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# ==================== 4. 画出时间序列并保存图形 ====================
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe, label=f'{WINDOW}-Day Rolling Sharpe', color='tab:blue')
plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio', fontsize=14)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Annualized Sharpe Ratio', fontsize=12)
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# 保存图形
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 输出契约：填充 result ====================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}

# 打印结果以便课堂展示验证
print(f"最后{WINDOW}日窗口的年化夏普比率: {rolling_sharpe_last:.4f}")
print(f"图形已保存至: {FIGURE_PATH}")
