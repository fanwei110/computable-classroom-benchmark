import numpy as np

# 给定参数
beta = 1.42
rm_monthly = -0.058  # 大盘上月收益
rf_annual = 0.047    # 年化无风险利率（年复利）

# 年复利转换为月复利：按每年12个月等分
rf_monthly = (1 + rf_annual) ** (1/12) - 1

# CAPM 公式：E(R) = Rf + beta * (Rm - Rf)
capm_return_monthly = rf_monthly + beta * (rm_monthly - rf_monthly)

result = {'capm_return_monthly': capm_return_monthly}
print(result)
