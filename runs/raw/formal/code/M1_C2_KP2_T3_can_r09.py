import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场上个月跌了5.8%
risk_free_rate_annual = 0.047   # 年无风险利率4.7%

# 步骤1：将年无风险利率折算为月利率（复利计算）
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

# 步骤2：在月度层面套用CAPM公式
# CAPM公式：E(R_i) = R_f + beta_i * (E(R_m) - R_f)
# 这里E(R_m)为市场实际收益率（题目中已给出），因此直接计算期望收益
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 步骤3：填充result字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（可选，便于调试）
print(result)
