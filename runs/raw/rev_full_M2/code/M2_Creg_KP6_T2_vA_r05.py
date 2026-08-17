import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 0. 可复现的模拟数据（若存在真实数据文件可替换此部分）
# ----------------------------------------------------------------------
np.random.seed(42)
n_days = 1000                # 模拟交易日数量
dates = pd.bdate_range(start='2020-01-01', periods=n_days, freq='C')
fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)
df = pd.DataFrame({'fund': fund_returns}, index=dates)

# ----------------------------------------------------------------------
# 1. 参数设定
# ----------------------------------------------------------------------
RISK_FREE_RATE = 0.021       # 年化无风险利率
TRADING_DAYS = 252           # 年交易日数
WINDOW = 60                  # 滚动窗口长度（可调）

# ----------------------------------------------------------------------
# 2. 计算滚动年化夏普比率
# ----------------------------------------------------------------------
daily_rf = RISK_FREE_RATE / TRADING_DAYS

rolling_mean = df['fund'].rolling(window=WINDOW).mean()
rolling_std = df['fund'].rolling(window=WINDOW).std()
rolling_sharpe = (rolling_mean - daily_rf) / rolling_std * np.sqrt(TRADING_DAYS)
rolling_sharpe = rolling_sharpe.dropna()

# 最后一个窗口的夏普值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# ----------------------------------------------------------------------
# 3. 画图并保存
# ----------------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe.index, rolling_sharpe.values, label='60-Day Rolling Sharpe', color='steelblue')
plt.title('60-Day Rolling Annualized Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()

figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ----------------------------------------------------------------------
# 4. 输出结果
# ----------------------------------------------------------------------
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 打印结果以便检查
print(result)
