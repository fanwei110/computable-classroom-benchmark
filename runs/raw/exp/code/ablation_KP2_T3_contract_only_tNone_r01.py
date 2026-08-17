import numpy as np

# 给定参数
beta = 1.42
market_monthly_return = -5.8 / 100  # 市场月收益率（-5.8%）
annual_risk_free_rate = 4.7 / 100  # 年化无风险利率 4.7%

# 将年化无风险利率转换为月化无风险利率 (单利近似：月利率 = 年利率/12)
monthly_risk_free_rate = annual_risk_free_rate / 12

# CAPM公式：预期月收益 = 无风险月利率 + beta * (市场月收益 - 无风险月利率)
# 注意：通常CAPM用超额收益形式，这里完整写出：
# E(R_i) = R_f + beta * (R_m - R_f)
capm_return_monthly = monthly_risk_free_rate + beta * (market_monthly_return - monthly_risk_free_rate)

# 按照输出契约，存入字典 result，键名严格为 'capm_return_monthly'
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果（便于查看，非必须）
print(f"Beta: {beta}")
print(f"市场月收益率: {market_monthly_return*100:.2f}%")
print(f"月无风险利率: {monthly_risk_free_rate*100:.4f}%")
print(f"CAPM月度预期收益: {result['capm_return_monthly']*100:.4f}%")
