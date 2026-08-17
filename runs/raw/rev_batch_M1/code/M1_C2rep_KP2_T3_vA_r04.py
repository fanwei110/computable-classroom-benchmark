import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场上个月跌了5.8%
annual_risk_free_rate = 0.047   # 年无风险利率4.7%

# 1. 将年无风险利率折算为月利率（连续复利）
monthly_risk_free_rate = annual_risk_free_rate / 12

# 2. 在月度层面套用 CAPM 公式：
#    E(R_i) = R_f + beta_i * (E(R_m) - R_f)
# 这里 E(R_m) 是市场实际收益率（已知），因此直接计算期望收益
capm_return_monthly = monthly_risk_free_rate + beta * (market_return_monthly - monthly_risk_free_rate)

# 3. 填充 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（供课堂展示）
print(result)
