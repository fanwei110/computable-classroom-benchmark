import pandas as pd
import numpy as np

# 读取数据文件（请根据实际路径/格式修改）
df = pd.read_csv('data.csv')          # 若为 Excel 可用 pd.read_excel
daily_returns = df['fund']

# 若收益率是百分比形式（如 1.0 代表 1%），转换为小数
# daily_returns = daily_returns / 100

# 参数设定
rf_annual = 0.021                     # 年化无风险利率
trading_days = 252                    # 年度交易日数
rf_daily = rf_annual / trading_days   # 日无风险利率

# 计算日超额收益
excess_returns = daily_returns - rf_daily

# 年化夏普比率
mean_excess = excess_returns.mean()
std_excess = excess_returns.std()
sharpe_annual = np.sqrt(trading_days) * (mean_excess / std_excess)

# 按要求存入字典
result = {'sharpe_annual': sharpe_annual}
