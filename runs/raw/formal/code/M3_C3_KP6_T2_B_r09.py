import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 模拟数据 (若已有真实数据，请替换此部分)
# ==========================================
np.random.seed(42)
dates = pd.date_range(start='2022-01-01', periods=500, freq='B')
# 模拟一个基金净值序列
fund_nav = (1 + np.random.normal(0.0005, 0.01, len(dates))).cumprod() * 1.0
df = pd.DataFrame({'fund': fund_nav}, index=dates)

# ==========================================
# 2. 参数与计算约定
# ==========================================
rf = 0.021          # 无风险利率 2.1%，小数表示
window = 60         # 滚动窗口大小，可按需调整
annual_factor = 252 # 每年252个交易日

# ==========================================
# 3. 核心计算逻辑
# ==========================================
# 计算日度简单收益率
df['daily_ret'] = df['fund'].pct_change()

# 计算滚动均值与滚动标准差 (严格遵循 ddof=1 样本估计量)
rolling_mean = df['daily_ret'].rolling(window=window).mean()
rolling_std = df['daily_ret'].rolling(window=window).std(ddof=1)

# 计算滚动夏普比率
# 年化收益率 = 日均值 * 252
# 年化波动率 = 日标准差 * sqrt(252)
# 滚动夏普 = (年化收益率 - rf) / 年化波动率
rolling_sharpe = (rolling_mean * annual_factor - rf) / (rolling_std * np.sqrt(annual_factor))

# 获取最后一个窗口的值
last_sharpe_value = rolling_sharpe.iloc[-1]

# ==========================================
# 4. 绘图与保存
# ==========================================
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe, label=f'{window}-Day Rolling Sharpe', color='tab:blue')
plt.axhline(y=0, color='tab:red', linestyle='--', linewidth=1)
plt.title(f'{window}-Day Rolling Sharpe Ratio (rf={rf*100}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(alpha=0.3)

# 保存图表
fig_path = 'rolling_sharpe_plot.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 输出契约
# ==========================================
result = {
    'rolling_sharpe_last': last_sharpe_value,
    'figure_path': fig_path
}

# 打印结果查看
print(result)
