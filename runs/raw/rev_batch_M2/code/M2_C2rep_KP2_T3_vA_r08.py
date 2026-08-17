import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058   # 市场跌了5.8%
annual_risk_free = 0.047         # 年无风险利率4.7%

# 1. 将年无风险利率折算为月利率（简单计息，符合CAPM单期习惯）
monthly_risk_free = annual_risk_free / 12.0

# 2. 在月度层面套用CAPM公式：E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = monthly_risk_free + beta * (market_return_monthly - monthly_risk_free)

# 3. 输出结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 仅用于课堂屏幕展示
print(result)
