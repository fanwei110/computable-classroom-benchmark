import numpy as np

# 输入参数
beta = 1.42
market_return_monthly = -0.058  # 市场月收益率 -5.8%
risk_free_rate_annual = 0.047   # 年化无风险利率 4.7%

# 将年化无风险利率转为月利率（复利方式）
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

# CAPM 计算月期望收益
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 按照输出契约存入 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印以便验证
print("月度无风险利率:", risk_free_rate_monthly)
print("CAPM 月度预期收益率:", capm_return_monthly)
