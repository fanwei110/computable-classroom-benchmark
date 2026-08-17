import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. 生成示例数据（日期范围 + 随机日收益率）
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=500, freq='B')
returns = np.random.normal(0.0005, 0.02, len(dates))  # 日均收益约0.05%，标准差2%
fund = pd.Series(returns, index=dates, name='fund')

# 2. 参数设置（窗口可调，这里使用60日）
window = 60
rf = 0.021  # 无风险利率 2.1%

# 3. 计算滚动年化夏普比率
# 年化系数：假设一年252个交易日
annual_factor = 252
rolling_avg_return = fund.rolling(window).mean() * annual_factor
rolling_std = fund.rolling(window).std() * np.sqrt(annual_factor)
rolling_sharpe = (rolling_avg_return - rf) / rolling_std

# 4. 获取最后一个窗口的数值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# 5. 绘制曲线并保存
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe.index, rolling_sharpe, label=f'{window}-Day Rolling Annualized Sharpe')
plt.axhline(y=0, color='gray', linestyle='--')
plt.title(f'Rolling Annualized Sharpe Ratio (rf={rf:.1%})')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path)
plt.close()

# 6. 结果字典
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 4),
    'figure_path': figure_path
}
print(result)
