import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058   # 上个月市场收益 -5.8%
risk_free_rate_annual = 0.047    # 年无风险利率 4.7%

# 1. 年无风险利率折算为月利率（简单除法）
risk_free_rate_monthly = risk_free_rate_annual / 12

# 2. 按 CAPM 计算该股票月度期望收益
#   E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 3. 存入 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出供教师投屏
print(f"月度无风险利率: {risk_free_rate_monthly:.6f}")
print(f"CAPM 月度期望收益: {capm_return_monthly:.6f}")
print(f"result = {result}")
