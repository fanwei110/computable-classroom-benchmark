import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= 1. 准备数据 =================
# 这里使用模拟数据，如果您有真实数据，请替换这部分读取逻辑
# 例如: df = pd.read_csv('your_data.csv', parse_dates=['date'], index_col='date')
np.random.seed(42)
dates = pd.date_range(start='2022-01-01', periods=500, freq='D')
fund_values = np.cumprod(1 + np.random.normal(0.0005, 0.015, 500)) # 模拟基金净值
df = pd.DataFrame({'fund': fund_values}, index=dates)

# ================= 2. 参数设置与计算 =================
rf = 0.021           # 无风险利率 2.1%
window = 60          # 滚动窗口大小（可在此调整）
trading_days = 252   # 一年交易日

# 计算日收益率
returns = df['fund'].pct_change().dropna()

# 计算滚动均值和标准差
rolling_mean = returns.rolling(window=window).mean()
rolling_std = returns.rolling(window=window).std()

# 计算60日滚动年化夏普比率
rolling_sharpe = (rolling_mean * trading_days - rf) / (rolling_std * np.sqrt(trading_days))

# 获取最后一个窗口的数值
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# ================= 3. 画图与保存 =================
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.dropna(), label=f'{window}-Day Rolling Annualized Sharpe (rf={rf*100}%)', color='blue')
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
plt.legend()
plt.grid(True, alpha=0.3)

figure_path = 'rolling_sharpe_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ================= 4. 输出契约 =================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

print(result)
