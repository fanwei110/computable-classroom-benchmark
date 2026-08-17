import pandas as pd
import numpy as np

# 1. 读取数据（请根据实际文件路径和格式修改）
df = pd.read_csv('your_data.csv')          # 也可能是 Excel: pd.read_excel()
daily_returns = df['fund']                 # 日收益序列（例如小数形式，0.01 代表 1%）

# 2. 设定无风险利率与年化交易日数
rf_annual = 0.021           # 2.1%
trading_days = 252          # 一般假设252个交易日
rf_daily = rf_annual / trading_days

# 3. 计算日超额收益
excess_daily = daily_returns - rf_daily

# 4. 年化夏普比率
#    使用样本标准差（ddof=1），更符合金融实务
sharpe_daily = excess_daily.mean() / excess_daily.std(ddof=1)
sharpe_annual = np.sqrt(trading_days) * sharpe_daily

# 5. 按要求存入字典
result = {'sharpe_annual': sharpe_annual}
print(result)
