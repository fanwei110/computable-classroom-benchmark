import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 模拟数据：生成500个交易日的日收益率（均值为0.0005，标准差0.02）
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=500, freq='B')
fund = np.random.normal(0.0005, 0.02, len(dates))

# 参数设置
window = 60          # 滚动窗口（可调）
rf_annual = 0.021    # 年化无风险利率
rf_daily = rf_annual / 252

# 计算滚动年化夏普比率
returns = pd.Series(fund, index=dates)
rolling_excess = returns.rolling(window).mean() - rf_daily
rolling_std = returns.rolling(window).std()
rolling_sharpe_annualized = (rolling_excess / rolling_std) * np.sqrt(252)

# 最后一个窗口的年化夏普值
rolling_sharpe_last = rolling_sharpe_annualized.iloc[-1]
print(f"最后一个窗口（{window}日）的滚动年化夏普比率: {rolling_sharpe_last:.4f}")

# 绘制曲线并保存
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe_annualized, label=f'{window}-Day Rolling Annualized Sharpe')
plt.axhline(y=0, color='gray', linestyle='--')
plt.title('Rolling Annualized Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Annualized Sharpe')
plt.legend()
plt.tight_layout()
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}
print(result)
