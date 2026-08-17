import numpy as np

# ==================== 已知参数 ====================
beta = 1.42                     # 股票的 Beta 值
market_return_monthly = -0.058  # 上个月市场收益率（跌了 5.8%）
risk_free_annual = 0.047        # 年化无风险利率（4.7%）

# ==================== 步骤 1：折算年无风险利率为月利率 ====================
# 在标准的《证券投资学》CAPM月度计算中，通常采用算术平均法将年利率除以12来折算月利率
risk_free_monthly = risk_free_annual / 12

# ==================== 步骤 2：在月度层面套用 CAPM ====================
# CAPM 公式: E(R_i) = R_f + β * [E(R_m) - R_f]
# 其中：
# E(R_i) 为股票预期收益率
# R_f 为月度无风险利率
# E(R_m) 为市场收益率
# [E(R_m) - R_f] 为市场风险溢价
market_risk_premium = market_return_monthly - risk_free_monthly
capm_return_monthly = risk_free_monthly + beta * market_risk_premium

# ==================== 步骤 3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# (以下为控制台输出验证，便于课堂投屏展示)
print(f"年化无风险利率: {risk_free_annual:.4f}")
print(f"月度无风险利率: {risk_free_monthly:.6f}")
print(f"市场风险溢价(月度): {market_risk_premium:.6f}")
print(f"CAPM 预期月度收益率: {capm_return_monthly:.6f} (即 {capm_return_monthly*100:.4f}%)")
print(f"\n最终结果字典: {result}")
