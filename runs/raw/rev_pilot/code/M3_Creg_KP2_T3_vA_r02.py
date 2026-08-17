import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 上个月市场跌幅 5.8%
risk_free_rate_annual = 0.047   # 无风险利率年化 4.7%

# 将年化无风险利率转换为月度无风险利率（采用标准单利折算，即除以12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# 根据 CAPM 公式计算股票上个月的预期收益率：
# E(R_i) = R_f + β * (E(R_m) - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 按照输出契约存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

print(result)
