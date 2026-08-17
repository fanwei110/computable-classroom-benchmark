import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= 1. 模拟数据 (实际使用时请替换为您的数据) =================
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=300, freq='B')
# 模拟一个基金净值序列
nav = [1.0]
for r in np.random.normal(loc=0.0004, scale=0.015, size=len(dates)-1):
    nav.append(nav[-1] * (1 + r))
df = pd.DataFrame({'fund': nav}, index=dates)

# ================= 2. 参数与计算约定设定 =================
rf_annual = 0.021       # 无风险利率 2.1%，小数表示
window = 60             # 可调窗口大小

# 债券收益率按年复利报价，转换为日化无风险利率
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# ================= 3. 计算滚动夏普 =================
# 计算日收益率
daily_returns = df['fund'].pct_change().dropna()

# 计算日超额收益
excess_returns = daily_returns - rf_daily

# 计算滚动均值和滚动标准差 (样本估计量 ddof=1)
rolling_mean = excess_returns.rolling(window=window).mean()
rolling_std = excess_returns.rolling(window=window).std(ddof=1)

# 计算年化滚动夏普比率 (每年252个交易日)
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

# 提取最后一个窗口的值
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# ================= 4. 绘图与保存 =================
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.dropna(), label=f'{window}-Day Rolling Sharpe', color='blue')
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf_annual*100}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
plt.legend()
plt.grid(True, alpha=0.3)

figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ================= 5. 输出契约 =================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

print(result)
