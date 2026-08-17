import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058   # 上个月市场下跌 5.8%
rf_annual = 0.047                # 年化无风险利率 4.7%

# 将年化无风险利率折算为月利率
# 假设采用简单利率折算（年利率 / 12），这是课堂中常见的处理方式
rf_monthly = np.divide(rf_annual, 12.0)

# 按 CAPM 计算该股票上个月的预期收益
# 公式：E(R_i) = R_f + β_i * (R_m - R_f)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 输出契约要求的字典
result = {
    'capm_return_monthly': capm_return_monthly
}

print(result)
