import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058          # 上个月市场下跌 5.8%
risk_free_annual = 0.047               # 年化无风险利率 4.7%

# 步骤1：将年无风险利率折算为月利率
# 采用简单比例折算（许多教材及实务中的常见做法）
risk_free_monthly = risk_free_annual / 12.0

# 步骤2：在月度层面应用 CAPM
# 公式：E(R_i) = R_f + β * (E(R_m) - R_f)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 步骤3：按要求输出
result = {
    'capm_return_monthly': capm_return_monthly
}

print(result)
