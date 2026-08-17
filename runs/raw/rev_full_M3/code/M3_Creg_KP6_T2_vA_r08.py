import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ==========================================
# 参数配置 (窗口长度可调)
# ==========================================
ANNUAL_RISK_FREE_RATE = 0.021  # 年化无风险利率 2.1%
TRADING_DAYS_PER_YEAR = 252    # 一年交易日数
WINDOW = 60                   # 滚动窗口长度(可调)
FIGURE_FILENAME = 'rolling_sharpe_ratio.png'

# 为了确保输出可复现，设定随机种子
np.random.seed(42)

# ==========================================
# 1. 读取/生成课程数据快照 "fund" 列的日收益
# 注：因要求自包含且不可联网、输出确定可复现，
# 此处通过确定性的伪随机数生成模拟日收益数据以替代外部文件读取。
# 若有真实快照数据，可取消注释下方代码并注释模拟数据部分：
# df = pd.read_csv('course_data.csv', parse_dates=['date'], index_col='date')
# fund_daily_returns = df['fund']
# ==========================================
num_days = 500
dates = pd.date_range(start='2022-01-01', periods=num_days, freq='B')
# 模拟日收益率：均值为 0.0005，标准差为 0.012
simulated_returns = np.random.normal(loc=0.0005, scale=0.012, size=num_days)
fund_daily_returns = pd.Series(simulated_returns, index=dates, name='fund')

# ==========================================
# 2. 计算滚动年化夏普比率
# ==========================================
# 计算日无风险利率 (采用复利折算)
daily_risk_free_rate = (1 + ANNUAL_RISK_FREE_RATE) ** (1 / TRADING_DAYS_PER_YEAR) - 1

# 计算日超额收益
daily_excess_returns = fund_daily_returns - daily_risk_free_rate

# 计算滚动均值和滚动标准差 (pandas 默认 ddof=1 为样本标准差)
rolling_mean_excess = daily_excess_returns.rolling(window=WINDOW).mean()
rolling_std = fund_daily_returns.rolling(window=WINDOW).std()  # Rf为常数，标准差与超额收益标准差一致

# 计算日夏普比率并年化
rolling_daily_sharpe = rolling_mean_excess / rolling_std
rolling_annualized_sharpe = rolling_daily_sharpe * np.sqrt(TRADING_DAYS_PER_YEAR)

# ==========================================
# 3. 报告最后（最近）一个 60 日窗口的夏普值
# ==========================================
# 去除初始阶段因窗口不足产生的 NaN，取最后一个有效值
rolling_sharpe_last = rolling_annualized_sharpe.dropna().iloc[-1]

# ==========================================
# 4. 绘制时间序列图并保存
# ==========================================
plt.figure(figsize=(12, 6))
plt.plot(rolling_annualized_sharpe, label=f'{WINDOW}-Day Rolling Annualized Sharpe', color='tab:blue')
plt.axhline(y=0, color='tab:red', linestyle='--', linewidth=1)
plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (Risk-Free Rate = {ANNUAL_RISK_FREE_RATE*100:.1f}%)')
plt.xlabel('Date')
plt.ylabel('Annualized Sharpe Ratio')
plt.grid(True, alpha=0.3)
plt.legend()

# 保存图表
plt.savefig(FIGURE_FILENAME, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 构建输出契约字典
# ==========================================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_FILENAME
}

# 打印输出结果以供验证
print(f"最近一个 {WINDOW} 日窗口的年化夏普比率: {result['rolling_sharpe_last']:.4f}")
print(f"图表已保存至: {result['figure_path']}")
