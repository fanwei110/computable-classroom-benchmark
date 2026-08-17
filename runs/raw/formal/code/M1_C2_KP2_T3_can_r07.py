import numpy as np

# 输入参数
beta = 1.42
market_return_monthly = -0.058  # 市场上个月跌了5.8%
risk_free_rate_annual = 0.047   # 年无风险利率4.7%

# 1. 将年无风险利率折算为月利率（连续复利方式）
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

# 2. 在月度层面套用CAPM公式：E(R_i) = R_f + beta_i * (E(R_m) - R_f)
# 这里使用实际市场收益代替期望市场收益（题目未给出期望值，采用实际值）
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 3. 存储结果
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（可选，用于验证）
print(result)
