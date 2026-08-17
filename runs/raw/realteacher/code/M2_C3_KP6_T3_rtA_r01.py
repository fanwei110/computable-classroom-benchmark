import pandas as pd
import numpy as np

# ---------- 读取数据 ----------
# 假设数据文件为 csv/excel，包含 'fund' 列，代表日收益（小数形式）
# df = pd.read_csv('your_file.csv')   # 或 pd.read_excel(...)
# daily_returns = df['fund']

# ---------- 参数 ----------
rf_annual = 0.021          # 无风险利率 2.1%（年复利）
trading_days = 252

# ---------- 计算 ----------
# 日收益均值与标准差（ddof=1 即样本标准差）
mu_daily = daily_returns.mean()
sigma_daily = daily_returns.std(ddof=1)

# 年化
mu_annual = mu_daily * trading_days
sigma_annual = sigma_daily * np.sqrt(trading_days)

# 年化夏普比率
sharpe_annual = (mu_annual - rf_annual) / sigma_annual

# ---------- 输出 ----------
result = {'sharpe_annual': sharpe_annual}
print(result)
