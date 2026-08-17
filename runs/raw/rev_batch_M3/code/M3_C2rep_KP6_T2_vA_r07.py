import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 参数设置 (可调参数)
# ==========================================
FILE_PATH = 'data/market_snapshot_v1.csv'
RF_ANNUAL = 0.021              # 年化无风险利率 2.1%
WINDOW = 60                    # 滚动窗口长度（可调）
TRADING_DAYS = 252             # 一年的交易日数

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
# 尝试将第一列作为索引（通常为日期）以方便绘制时间序列
df = pd.read_csv(FILE_PATH, index_col=0)

# 如果索引可以被解析为日期，则转换为 datetime 格式以保证绘图美观
try:
    df.index = pd.to_datetime(df.index)
except Exception:
    pass

# 提取 fund 列的日收益率
daily_returns = df['fund']

# 计算日无风险利率（简单算术平均，常用于日度超额收益计算）
rf_daily = RF_ANNUAL / TRADING_DAYS

# 计算日超额收益
excess_returns = daily_returns - rf_daily

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
# 滚动计算日超额收益的均值与标准差
rolling_mean_excess = excess_returns.rolling(window=WINDOW).mean()
rolling_std_excess = excess_returns.rolling(window=WINDOW).std(ddof=1)

# 计算滚动日夏普比率
rolling_sharpe_daily = rolling_mean_excess / rolling_std_excess

# 年化夏普比率 = 日夏普比率 * sqrt(一年交易日)
rolling_sharpe_annualized = rolling_sharpe_daily * np.sqrt(TRADING_DAYS)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 获取最后一个有效窗口的夏普值
rolling_sharpe_last = rolling_sharpe_annualized.dropna().iloc[-1]

# 绘制时间序列图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rolling_sharpe_annualized.index, rolling_sharpe_annualized.values, 
        color='royalblue', linewidth=1.2, label=f'{WINDOW}-Day Rolling Annualized Sharpe')

# 添加零线以便观察正负
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)

# 标注最近一个窗口的值
ax.scatter(rolling_sharpe_annualized.dropna().index[-1], rolling_sharpe_last, 
           color='red', zorder=5)
ax.annotate(f'Last: {rolling_sharpe_last:.4f}', 
            xy=(rolling_sharpe_annualized.dropna().index[-1], rolling_sharpe_last), 
            xytext=(-60, 20), textcoords='offset points',
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

ax.set_title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (Rf = {RF_ANNUAL*100}%)', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, linestyle=':', alpha=0.6)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
FIGURE_PATH = 'rolling_sharpe_ratio.png'
fig.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close(fig)

# 封装结果
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}

# 打印供课堂投屏检验
print(f"最后一个 {WINDOW} 日窗口的年化夏普比率: {rolling_sharpe_last:.4f}")
print(f"图形已保存至: {FIGURE_PATH}")
