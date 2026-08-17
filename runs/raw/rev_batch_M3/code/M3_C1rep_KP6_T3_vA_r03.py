import numpy as np

# 假设课程数据已加载为 pandas DataFrame，变量名为 df
# df['fund'] 为基金的净值序列

# 1. 计算基金的日收益率
daily_returns = df['fund'].pct_change().dropna()

# 2. 设定年化无风险利率
rf_annual = 0.021

# 3. 设定一年的交易日天数（国内金融市场通常按252天计算）
trading_days = 252

# 4. 计算年化收益率
annual_return = daily_returns.mean() * trading_days

# 5. 计算年化波动率（使用样本标准差，pandas默认ddof=1）
annual_volatility = daily_returns.std() * np.sqrt(trading_days)

# 6. 计算年化夏普比率
sharpe_annual = (annual_return - rf_annual) / annual_volatility

# 7. 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}
