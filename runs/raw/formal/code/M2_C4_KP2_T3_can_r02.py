import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场月收益：-5.8%
risk_free_annual = 0.047         # 年无风险利率：4.7%

# 1. 年无风险利率简单折算为月利率
risk_free_monthly = risk_free_annual / 12

# 2. 在月度层面套用 CAPM
# CAPM: E[R_i] = R_f + beta * (E[R_m] - R_f)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 3. 按要求存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果，便于课堂投屏
print(f"年无风险利率: {risk_free_annual}")
print(f"月无风险利率: {risk_free_monthly:.6f} ({risk_free_monthly*100:.4f}%)")
print(f"市场月收益: {market_return_monthly} ({market_return_monthly*100:.2f}%)")
print(f"CAPM 预期月收益: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print(f"\nresult = {result}")
