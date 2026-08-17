import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058   # 上月市场跌了5.8%
annual_risk_free_rate = 0.047    # 年无风险利率4.7%

# 1. 把年无风险利率按简单除法折算为月利率
monthly_risk_free_rate = annual_risk_free_rate / 12

# 2. 在月度层面套用 CAPM
# CAPM: E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = monthly_risk_free_rate + beta * (market_return_monthly - monthly_risk_free_rate)

# 3. 填充 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（教师投屏可见）
print("月无风险利率:", round(monthly_risk_free_rate, 6))
print("CAPM 月度期望收益:", round(capm_return_monthly, 6))
print("result:", result)
