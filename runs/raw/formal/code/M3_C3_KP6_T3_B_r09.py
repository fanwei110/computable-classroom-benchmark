import numpy as np
import pandas as pd

# 假设数据已加载为 DataFrame 变量 df，且包含基金净值列 'fund'
# rf = 2.1% = 0.021

rf_annual = 0.021

# 1. 计算日度无风险利率
# 约定：债券收益率按年复利报价，因此日度化需使用复利折算
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# 2. 计算基金日度收益率
# 假设 'fund' 列为净值序列，计算简单收益率；若 'fund' 本身已是日收益率，则去掉 .pct_change() 
daily_returns = df['fund'].pct_change().dropna()

# 3. 计算日度超额收益率
excess_returns = daily_returns - rf_daily

# 4. 计算超额收益率的样本均值与样本标准差
# 约定：标准差用样本估计量（ddof=1）
mean_excess = excess_returns.mean()
std_excess = excess_returns.std(ddof=1)

# 5. 计算年化夏普比率
# 约定：年化按每年 252 个交易日
sharpe_annual = (mean_excess / std_excess) * np.sqrt(252)

# 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}
