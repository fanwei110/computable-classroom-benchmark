import numpy as np

# ==================== 输入参数 ====================
beta = 1.42                    # 股票的 Beta 值
market_return_monthly = -0.058 # 上个月市场收益率（跌5.8%记为负数）
risk_free_annual = 0.047       # 年化无风险利率（4.7%）

# ==================== 步骤1：年无风险利率折算为月利率 ====================
# 假设：采用复利折算方式，将年化利率转换为等价月利率，这在学术计算中更为严谨。
# 公式：r_f_monthly = (1 + r_f_annual)^(1/12) - 1
risk_free_monthly = (1 + risk_free_annual) ** (1 / 12) - 1

# ==================== 步骤2：在月度层面套用 CAPM ====================
# CAPM 公式：E(R_i) = R_f + β * (E(R_m) - R_f)
# 此处将给定的上月市场收益率作为 E(R_m) 代入
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# ==================== 步骤3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==================== 课堂演示输出 ====================
# 便于投屏时向学生展示计算过程与结果
print(f"假设处理：年转月利率采用复利折算 (1+r_f)^(1/12)-1")
print(f"年化无风险利率: {risk_free_annual:.4%}")
print(f"折算后月无风险利率: {risk_free_monthly:.6%}")
print(f"上月市场收益率: {market_return_monthly:.4%}")
print(f"股票 Beta: {beta}")
print("-" * 30)
print(f"CAPM 月度期望收益: {risk_free_monthly:.6%} + {beta} * ({market_return_monthly:.4%} - {risk_free_monthly:.6%})")
print(f"CAPM 月度期望收益: {capm_return_monthly:.6%}")
print("-" * 30)
print(f"result字典内容: {result}")
