import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场组合上月收益率（-5.8%）
annual_risk_free = 0.047        # 年无风险利率（4.7%）

# 1. 将年无风险利率折算为月利率
# 假设为简单利率（单利），即月利率 = 年利率 / 12
# 这是CAPM计算中最常见的处理方式，与单期期望收益模型保持一致
risk_free_monthly = annual_risk_free / 12.0

# 2. 在月度层面套用CAPM：E(R) = R_f + beta * (R_m - R_f)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 3. 填充结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印以供课堂查看
print(result)
