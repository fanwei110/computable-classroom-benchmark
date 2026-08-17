import numpy as np
import pandas as pd

# 假设你的课程数据已加载为名为 df 的 DataFrame
# 若 df['fund'] 为日收益率序列，则直接使用：
daily_returns = df['fund']

# （补充说明：若 df['fund'] 是单位净值/累计净值，则需要先计算日收益率，取消下面这行的注释）
# daily_returns = df['fund'].pct_change().dropna()

# 给定无风险利率
rf_annual = 0.021

# 计算年化收益率 (假设一年252个交易日)
annual_return = daily_returns.mean() * 252

# 计算年化波动率
annual_volatility = daily_returns.std() * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = (annual_return - rf_annual) / annual_volatility

# 按照输出契约存入字典
result = {
    'sharpe_annual': sharpe_annual
}
