import numpy as np

# ==================== 输入参数 ====================
beta = 1.42                     # 股票的 Beta 值
market_return_monthly = -0.058  # 上个月市场收益率 (-5.8%)
risk_free_rate_annual = 0.047   # 年化无风险利率 (4.7%)

# ==================== 步骤 1：折算年无风险利率为月利率 ====================
# 采用复利折算（Compound rate），将年化利率转换为等价月度利率。
# 假设：(1 + R_annual) = (1 + R_monthly)^12
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1 / 12) - 1

# ==================== 步骤 2：在月度层面套用 CAPM ====================
# CAPM 公式: E(R_i) = R_f + beta * (E(R_m) - R_f)
# 其中 R_f 和 E(R_m) 均为月度数值
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# ==================== 步骤 3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果以便课堂展示
print(f"年无风险利率折算为月利率: {risk_free_rate_monthly:.6f} ({risk_free_rate_monthly*100:.4f}%)")
print(f"按 CAPM 计算的该股票上月预期收益率: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print(f"\nresult 字典内容: {result}")
