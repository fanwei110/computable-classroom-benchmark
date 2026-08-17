# 模拟数据 + 计算过程
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 生成日度模拟收益数据（2020-01-01 至 2024-12-31）
np.random.seed(42)
dates = pd.date_range('2020-01-01', '2024-12-31', freq='B')
fund_return = np.random.normal(0.0005, 0.015, len(dates))
df = pd.DataFrame({'fund': fund_return}, index=dates)

# 参数设置
window = 60
rf_annual = 0.021
rf_daily = rf_annual / 252

# 超额收益
excess = df['fund'] - rf_daily

# 滚动夏普 (年化)
rolling_sharpe = (excess.rolling(window).mean() / excess.rolling(window).std()) * np.sqrt(252)

# 最后一个窗口值
rolling_sharpe_last = round(rolling_sharpe.iloc[-1], 4)

# 绘图并保存
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe, label='60-Day Rolling Sharpe', color='steelblue')
plt.axhline(0, color='gray', linestyle='--')
plt.title('Rolling Sharpe Ratio (rf=2.1%)')
plt.xlabel('Date')
plt.ylabel('Annualized Sharpe')
plt.legend()
plt.tight_layout()
fig_path = './rolling_sharpe.png'
plt.savefig(fig_path)
plt.close()

# 结果字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': fig_path
}
