import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场上个月跌了5.8%
annual_risk_free_rate = 0.047   # 年无风险利率4.7%

# 1. 将年无风险利率折算为月利率（复利计算）
monthly_risk_free_rate = (1 + annual_risk_free_rate) ** (1/12) - 1

# 2. 在月度层面套用 CAPM 公式：E(R_i) = R_f + beta_i * (E(R_m) - R_f)
# 这里市场实际收益已知，直接代入 CAPM 计算期望收益
capm_return_monthly = monthly_risk_free_rate + beta * (market_return_monthly - monthly_risk_free_rate)

# 3. 将结果存入 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（供课堂展示）
print("CAPM 预期月收益率:", result['capm_return_monthly'])
