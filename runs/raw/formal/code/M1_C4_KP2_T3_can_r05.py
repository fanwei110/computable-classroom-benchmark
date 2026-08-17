import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场上个月跌了5.8%
annual_risk_free_rate = 0.047   # 年无风险利率4.7%

# 步骤1：将年无风险利率折算为月利率（简单除法）
monthly_risk_free_rate = annual_risk_free_rate / 12

# 步骤2：在月度层面套用CAPM公式：E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = monthly_risk_free_rate + beta * (market_return_monthly - monthly_risk_free_rate)

# 存储结果
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（供课堂展示）
print(result)
