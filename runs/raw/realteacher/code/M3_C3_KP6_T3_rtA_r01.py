import pandas as pd
import numpy as np

# 假设数据已经加载到名为 df 的 DataFrame 中，且包含 'fund' 列
# df = pd.read_csv('your_data_file.csv') 

# 1. 提取日收益率
r_daily = df['fund']

# 2. 无风险利率处理 (按年复利报价转化为日复利)
rf_annual = 0.021
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# 3. 计算日超额收益的均值
mean_excess_daily = r_daily.mean() - rf_daily

# 4. 计算日收益率的标准差 (样本估计量，ddof=1)
std_daily = r_daily.std(ddof=1)

# 5. 计算年化夏普比率
sharpe_annual = (mean_excess_daily / std_daily) * np.sqrt(252)

# 6. 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

# 输出结果
print(result)
