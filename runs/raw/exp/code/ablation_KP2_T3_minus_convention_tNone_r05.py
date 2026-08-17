import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场月收益率（-5.8%）
annual_risk_free_rate = 0.047   # 年无风险利率 4.7%

# 1. 年无风险利率转换为月利率（简单除法）
monthly_risk_free_rate = annual_risk_free_rate / 12

# 2. 套用月度 CAPM： E(R_i) = R_f + beta * (R_m - R_f)
capm_return_monthly = monthly_risk_free_rate + beta * (market_return_monthly - monthly_risk_free_rate)

# 3. 存入 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果（方便投屏展示）
print("月度无风险利率:", monthly_risk_free_rate)
print("按CAPM计算的该股票上个月应得收益率:", capm_return_monthly)
print("result字典:", result)
