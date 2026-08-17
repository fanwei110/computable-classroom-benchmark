import numpy as np

# 给定数据
beta = 1.42
market_return_monthly = -0.058  # 大盘跌了5.8%
rf_annual = 0.047  # 年化无风险利率4.7%

# 年化无风险利率转换为月利率（复利年化，按每年252个交易日，近似12个月）
rf_monthly = (1 + rf_annual) ** (1/12) - 1

# CAPM公式计算预期月度收益
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 构建结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果
print(result)
