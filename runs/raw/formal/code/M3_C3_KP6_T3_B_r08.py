import numpy as np
import pandas as pd

# 假设 df 为包含基金日收益率数据的 DataFrame，列名为 'fund'
# df = pd.read_csv("your_data.csv") 

rf_annual = 0.021  # 2.1% 转换为小数表示

# 1. 根据债券收益率年复利报价约定，计算日度无风险利率
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# 2. 计算日度超额收益率
excess_daily = df['fund'] - rf_daily

# 3. 计算日度超额收益率的均值和样本标准差（ddof=1）
mu_daily = excess_daily.mean()
sigma_daily = excess_daily.std(ddof=1)

# 4. 计算年化夏普比率（按 252 个交易日年化）
sharpe_annual = (mu_daily / sigma_daily) * np.sqrt(252)

# 5. 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
