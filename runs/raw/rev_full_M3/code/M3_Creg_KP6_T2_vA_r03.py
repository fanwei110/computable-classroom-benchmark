import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 参数配置
# ==========================================
WINDOW_LENGTH = 60             # 滚动窗口长度（可调）
RF_ANNUAL = 0.021              # 年化无风险利率 2.1%
TRADING_DAYS_PER_YEAR = 252    # 一年的交易日数（用于年化）
FIGURE_FILENAME = 'rolling_sharpe_ratio.png'

# ==========================================
# 数据读取与生成
# ==========================================
# 尝试读取课程数据快照。如果文件不存在，则生成确定性模拟数据以保证脚本自包含与可复现
try:
    # 假设快照为csv格式，且包含日期索引与'fund'列
    df = pd.read_csv('snapshot.csv', index_col=0, parse_dates=True)
    daily_returns = df['fund']
except FileNotFoundError:
    # 生成模拟数据：约 10% 年化收益，15% 年化波动率
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=500, freq='B') 
    mu_daily = 0.10 / TRADING_DAYS_PER_YEAR
    sigma_daily = 0.15 / np.sqrt(TRADING_DAYS_PER_YEAR)
    mock_returns = np.random.normal(mu_daily, sigma_daily, len(dates))
    daily_returns = pd.Series(mock_returns, index=dates, name='fund')

# ==========================================
# 核心计算：滚动年化夏普比率
# ==========================================
# 日度无风险利率
rf_daily = RF_ANNUAL / TRADING_DAYS_PER_YEAR

# 计算指定窗口的滚动均值与标准差
rolling_mean = daily_returns.rolling(window=WINDOW_LENGTH).mean()
rolling_std = daily_returns.rolling(window=WINDOW_LENGTH).std()

# 滚动日夏普 = (日收益均值 - 日无风险利率) / 日收益标准差
# 年化夏普 = 滚动日夏普 * sqrt(一年的交易日数)
rolling_sharpe_annualized = (rolling_mean - rf_daily) / rolling_std * np.sqrt(TRADING_DAYS_PER_YEAR)

# 提取最后一个（最近的）60日窗口的夏普值
rolling_sharpe_last = rolling_sharpe_annualized.iloc[-1]

# ==========================================
# 绘图与保存
# ==========================================
fig, ax = plt.subplots(figsize=(12, 6))
rolling_sharpe_annualized.plot(ax=ax, color='steelblue', linewidth=1.5)

ax.set_title(f'{WINDOW_LENGTH}-Day Rolling Annualized Sharpe Ratio (Rf = {RF_ANNUAL*100:.1f}%)', fontsize=14)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.set_xlabel('Date', fontsize=12)
ax.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.7)
ax.grid(True, linestyle='--', alpha=0.4)
fig.tight_layout()

# 保存图表
fig.savefig(FIGURE_FILENAME, dpi=150)
plt.close(fig)

# ==========================================
# 输出契约
# ==========================================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': os.path.abspath(FIGURE_FILENAME)
}

# 打印结果以供检验
print(f"Last {WINDOW_LENGTH}-day rolling Sharpe ratio: {result['rolling_sharpe_last']:.4f}")
print(f"Figure saved at: {result['figure_path']}")
