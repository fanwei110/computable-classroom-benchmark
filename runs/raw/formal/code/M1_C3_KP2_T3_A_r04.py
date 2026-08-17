import math

# 已知条件
beta = 1.42
market_return_monthly = -0.058
risk_free_rate_annual = 0.047

# 计算月度无风险利率
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

# 计算市场风险溢价
market_risk_premium = market_return_monthly - risk_free_rate_monthly

# 计算CAPM预期收益率
capm_return_monthly = risk_free_rate_monthly + beta * market_risk_premium

# 存入结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

print(result)
