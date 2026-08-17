# 计算CAPM月收益
beta = 1.42
market_return_monthly = -0.058
risk_free_annual = 0.047
risk_free_monthly = risk_free_annual / 12

# CAPM预期收益
expected_return = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 存储结果
result = {
    'capm_return_monthly': expected_return
}
