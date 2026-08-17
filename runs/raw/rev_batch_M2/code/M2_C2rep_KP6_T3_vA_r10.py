import pandas as pd
import numpy as np

# 读取课程数据
data = pd.read_csv('data/market_snapshot_v1.csv')

# 设置无风险利率
risk_free_rate = 0.021  # 2.1%

# 提取fund列数据
fund_returns = data['fund']

# 计算fund列的日收益率（假设数据是每日净值）
# 如果数据本身就是收益率，直接使用；如果是价格，需要计算收益率
# 根据常见情况，假设数据是每日收益率
daily_returns = fund_returns

# 计算年化收益率
# 假设一年有252个交易日
annual_return = daily_returns.mean() * 252

# 计算年化波动率
annual_volatility = daily_returns.std() * np.sqrt(252)

# 计算年化超额收益率
annual_excess_return = annual_return - risk_free_rate

# 计算年化夏普比率
sharpe_annual = annual_excess_return / annual_volatility

# 将结果存入字典
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果
print(f"年化夏普比率: {sharpe_annual:.4f}")
print(f"结果字典: {result}")
