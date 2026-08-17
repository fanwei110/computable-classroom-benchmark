import numpy as np

# 输入参数（小数表示）
beta = 1.42
market_return_monthly = -0.058
risk_free_rate_annual = 0.047

# 步骤 1：把年无风险利率按简单除法折算为月利率（年利率/12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# 步骤 2：在月度层面套用 CAPM
# CAPM 公式: E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 步骤 3：填充 result
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果供教师投屏展示
print(f"年化无风险利率: {risk_free_rate_annual:.4f}")
print(f"月度无风险利率: {risk_free_rate_monthly:.6f}")
print(f"市场月度收益率: {market_return_monthly:.4f}")
print(f"股票 Beta: {beta:.2f}")
print(f"按CAPM计算的月度期望收益率: {capm_return_monthly:.6f} (即 {capm_return_monthly*100:.4f}%)")
print(f"\nresult字典: {result}")
