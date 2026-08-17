import numpy as np

# 题目给定参数（按约定用小数表示）
beta = 1.42
market_return_monthly = -0.058  # 上个月市场跌了 5.8%
risk_free_rate_annual = 0.047   # 年无风险利率 4.7%

# 步骤1：把年无风险利率按简单除法折算为月利率（年利率/12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# 步骤2：在月度层面套用 CAPM
# CAPM 公式: E(R_i) = R_f + β * (R_m - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 步骤3：填充 result
result = {
    'capm_return_monthly': capm_return_monthly
}

# 课堂投屏展示辅助信息
print(f"年无风险利率: {risk_free_rate_annual:.4f}")
print(f"月无风险利率: {risk_free_rate_monthly:.6f}")
print(f"市场月收益率: {market_return_monthly:.4f}")
print(f"股票 Beta: {beta}")
print(f"按CAPM计算的该股票上月期望收益: {capm_return_monthly:.6f} (即 {capm_return_monthly*100:.4f}%)")
print(f"\n结果字典 result: {result}")
