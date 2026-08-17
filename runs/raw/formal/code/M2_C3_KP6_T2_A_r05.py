import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 生成模拟 fund 数据（净值序列，252天×2年）
np.random.seed(42)
dates = pd.bdate_range(start='2022-01-01', periods=504, freq='D')
returns = np.random.normal(0.0005, 0.012, len(dates))  # 日均收益0.05%，日波动1.2%
nav = 100 * np.cumprod(1 + returns)
fund = pd.Series(nav, index=dates)

# 参数
rf_annual = 0.021  # 2.1%
window = 60
annual_factor = 252

# 计算日收益率
daily_returns = fund.pct_change().dropna()

# 滚动窗口：年化夏普比率
# 日平均收益 → 年化收益 = 日均收益 * 252
# 年化波动 = 日标准差 * sqrt(252)
rolling_mean = daily_returns.rolling(window).mean() * annual_factor
rolling_std = daily_returns.rolling(window).std(ddof=1) * np.sqrt(annual_factor)
rolling_sharpe = (rolling_mean - rf_annual) / rolling_std

# 最后一个窗口的数值
rolling_sharpe_last = round(rolling_sharpe.iloc[-1], 6)

# 绘制曲线
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=1.5, color='darkblue')
plt.axhline(y=0, color='gray', linestyle='--')
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf=2.1%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.grid(alpha=0.3)
plt.tight_layout()

# 保存图像
figure_path = './rolling_sharpe.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# 封装结果
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}
