import numpy as np

# ==================== 已知参数 ====================
beta = 1.42                    # 股票的 Beta 值
market_return_monthly = -0.058 # 上个月市场收益率（小数表示，-5.8%）
risk_free_rate_annual = 0.047  # 年化无风险利率（小数表示，4.7%）

# ==================== 步骤 1：折算月度无风险利率 ====================
# 按课程约定：年利率折算到更短期限用简单除法（月 = 年 / 12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# ==================== 步骤 2：套用 CAPM 公式 ====================
# CAPM 公式: E(R_i) = R_f + beta * (E(R_m) - R_f)
# 在月度层面计算：
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# ==================== 步骤 3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==================== 输出验证（供投屏展示） ====================
print(f"年化无风险利率: {risk_free_rate_annual:.4f}")
print(f"月度无风险利率: {risk_free_rate_monthly:.6f}")
print(f"市场月度收益率: {market_return_monthly:.4f}")
print(f"Beta: {beta:.2f}")
print(f"按 CAPM 计算的月度期望收益率: {capm_return_monthly:.6f} (即 {capm_return_monthly*100:.4f}%)")
print(f"\nresult = {result}")
