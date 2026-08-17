import numpy as np

# ==================== 已知参数 ====================
beta = 1.42                     # 股票的 Beta 值
market_return_monthly = -0.058  # 上个月市场收益率 (-5.8%)
risk_free_annual = 0.047        # 年化无风险利率 (4.7%)

# ==================== 步骤 1: 折算年无风险利率为月利率 ====================
# 假设：采用复利折算方式，这在金融学理论上更为严谨
# 公式: R_f_monthly = (1 + R_f_annual)^(1/12) - 1
risk_free_monthly = (1 + risk_free_annual) ** (1 / 12) - 1

# ==================== 步骤 2: 在月度层面套用 CAPM ====================
# CAPM 公式: E(R_i) = R_f + β * (E(R_m) - R_f)
# 此处计算的是按 CAPM 预测的该股票上个月本该有的期望收益率
market_excess_return_monthly = market_return_monthly - risk_free_monthly
capm_return_monthly = risk_free_monthly + beta * market_excess_return_monthly

# ==================== 步骤 3: 填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果供课堂投屏查看
print(f"年化无风险利率: {risk_free_annual:.4f}")
print(f"月度无风险利率(复利折算): {risk_free_monthly:.6f}")
print(f"市场月度收益率: {market_return_monthly:.4f}")
print(f"按CAPM计算的上个月期望收益率: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
