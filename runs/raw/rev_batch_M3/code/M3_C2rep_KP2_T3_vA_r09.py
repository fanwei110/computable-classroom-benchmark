import numpy as np

# ====================
// 输入参数
// ====================
beta = 1.42                     # 股票的 Beta 系数
market_return_monthly = -0.058  # 上个月市场收益率（跌 5.8%）
risk_free_rate_annual = 0.047   # 年化无风险利率（4.7%）

# ====================
// 步骤 1：把年无风险利率折算为月利率
// ====================
// 在标准的金融学折算中，采用复利折算方式更为严谨：R_monthly = (1 + R_annual)^(1/12) - 1
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1 / 12) - 1

# ====================
// 步骤 2：在月度层面套用 CAPM
// ====================
// CAPM 公式: E(R_i) = R_f + β * (E(R_m) - R_f)
// 此处将上个月市场的实际收益率作为 E(R_m) 代入，计算该股票按 CAPM 本该实现的收益率
market_risk_premium_monthly = market_return_monthly - risk_free_rate_monthly
capm_return_monthly = risk_free_rate_monthly + beta * market_risk_premium_monthly

# ====================
// 步骤 3：填充 result
// ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# --------------------
// 课堂投屏展示辅助打印 (仅供参考，不影响 result 字典输出)
// --------------------
print(f"年化无风险利率: {risk_free_rate_annual:.4f}")
print(f"折算后月无风险利率: {risk_free_rate_monthly:.6f} (即 {risk_free_rate_monthly*100:.4f}%)")
print(f"市场月收益率: {market_return_monthly:.4f}")
print(f"按 CAPM 计算的月度期望收益率: {capm_return_monthly:.6f} (即 {capm_return_monthly*100:.4f}%)")
print("-" * 50)
print("最终输出字典 result:", result)
