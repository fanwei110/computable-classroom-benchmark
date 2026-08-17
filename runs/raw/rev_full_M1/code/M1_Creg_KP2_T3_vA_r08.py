import numpy as np

# 输入参数
beta = 1.42
market_return_monthly = -0.058  # 市场上个月跌了5.8%
risk_free_rate_annual = 0.047   # 年化无风险利率4.7%

# 将年化无风险利率转换为月度无风险利率
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

# CAPM 公式计算月度预期收益率
# E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 结果存储
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（可选，用于验证）
print(result)
