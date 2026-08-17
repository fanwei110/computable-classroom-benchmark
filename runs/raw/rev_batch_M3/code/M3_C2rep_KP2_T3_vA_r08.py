import numpy as np

# ==================== 输入参数 ====================
beta = 1.42                     # 股票的 Beta 系数
market_return_monthly = -0.058  # 上个月市场收益率（跌 5.8% 记为 -0.058）
risk_free_rate_annual = 0.047   # 年化无风险利率（4.7% 记为 0.047）

# ==================== 步骤 1：折算年无风险利率为月利率 ====================
# 假设：采用复利折算方式，将年利率折算为月利率。
# 这种方式在理论上最为严谨，确保 (1 + r_monthly)^12 = 1 + r_annual。
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1 / 12) - 1

# ==================== 步骤 2：在月度层面套用 CAPM ====================
# CAPM 公式: E(R_i) = R_f + β * (E(R_m) - R_f)
# 此处由于是计算历史某月的应得收益，市场收益 R_m 直接取实际发生的市场收益率。
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# ==================== 步骤 3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==================== 课堂展示输出 ====================
# 为方便教师投屏讲解，打印关键中间过程与最终结果
print(f"假设处理：年转月采用复利折算 (1+r_annual)^(1/12)-1")
print(f"1. 月度无风险利率: {risk_free_rate_monthly:.6f} ({risk_free_rate_monthly*100:.4f}%)")
print(f"2. CAPM 预期月收益: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print(f"3. 结果字典: {result}")
