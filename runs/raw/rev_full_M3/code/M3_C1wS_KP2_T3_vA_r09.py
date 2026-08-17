import numpy as np

# ==================== 题目参数 ====================
beta = 1.42                     # 股票的 Beta 值
market_return_monthly = -0.058  # 上个月市场收益率 (-5.8%)
risk_free_rate_annual = 0.047   # 年化无风险利率 (4.7%)

# ==================== 步骤 1：年无风险利率折算为月利率 ====================
# 采用复利折算方式，确保在时间维度上的严谨性
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1 / 12) - 1

# ==================== 步骤 2：套用 CAPM 模型 ====================
# CAPM 公式: E(R_i) = R_f + Beta * (E(R_m) - R_f)
# 在此场景中，用上个月的实际市场收益替代期望市场收益，计算该股票在CAPM框架下的本应收益
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# ==================== 步骤 3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果以便课堂投屏展示
print(f"年无风险利率折算月利率: {risk_free_rate_monthly:.6%}")
print(f"按CAPM计算的股票上月本该收益: {capm_return_monthly:.6%}")
print(f"result字典: {result}")
