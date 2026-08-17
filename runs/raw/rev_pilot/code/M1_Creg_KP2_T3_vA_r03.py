import numpy as np

# 输入参数
beta = 1.42
market_return_monthly = -0.058  # 市场上个月跌了 5.8%
risk_free_rate_annual = 0.047   # 年化无风险利率 4.7%

# 将年化无风险利率转换为月度无风险利率
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

# 根据 CAPM 计算预期月度收益率
# CAPM 公式: E(R_i) = R_f + beta_i * (E(R_m) - R_f)
expected_market_return_monthly = market_return_monthly  # 题目中市场实际收益即为 E(R_m)
capm_return_monthly = risk_free_rate_monthly + beta * (expected_market_return_monthly - risk_free_rate_monthly)

# 将结果存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（可选，用于验证）
print(result)
