import numpy as np
import pandas as pd

# --- 假设您已通过 pd.read_csv() 或其他方式加载数据为 df ---
# daily_returns = df['fund']  # 确保 fund 列的日收益是小数表示（如 0.05 表示 5%）

# 1. 无风险利率参数（小数表示）
rf_annual = 0.021

# 2. 债券收益率按年复利报价，折算为日无风险利率
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# 3. 计算日超额收益
daily_ex_returns = daily_returns - rf_daily

# 4. 计算日均超额收益与日超额收益样本标准差（ddof=1）
mean_ex_daily = np.mean(daily_ex_returns)
std_ex_daily = np.std(daily_ex_returns, ddof=1)

# 5. 计算年化夏普比率 (Sharpe = (均值/标准差) * sqrt(252))
sharpe_annual = (mean_ex_daily / std_ex_daily) * np.sqrt(252)

# 6. 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
