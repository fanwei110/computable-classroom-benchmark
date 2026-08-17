import numpy as np

# 已知参数
beta = 1.42                    # 股票的 Beta 值
market_return_monthly = -0.058 # 上个月市场收益率 (-5.8%)
risk_free_rate_annual = 0.047  # 无风险利率 (每年 4.7%)

# 将年化无风险利率转换为月度复利利率，以匹配市场收益率的月度周期
# 公式: R_f_monthly = (1 + R_f_annual)^(1/12) - 1
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1 / 12) - 1

# 按 CAPM 模型计算该股票上个月的预期收益率
# CAPM 公式: E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 按照输出契约存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果以供验证
print(f"月度无风险利率: {risk_free_rate_monthly:.6f}")
print(f"按 CAPM 计算的该股票上个月本该收益率: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print(f"Result dictionary: {result}")
