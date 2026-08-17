import numpy as np

# ==================== 参数设定 ====================
beta = 1.42                      # 股票的 Beta 系数
market_return_monthly = -0.058   # 上个月市场收益率 (跌 5.8%)
risk_free_rate_annual = 0.047    # 年化无风险利率 (4.7%)

# ==================== 步骤 1：折算年无风险利率为月利率 ====================
# 假设处理：在月度层面的 CAPM 实证与计算中，通常采用简单算术折算（即年利率 / 12），
# 这与月度超额收益率的计算逻辑保持内部一致，避免复利折算带来的期限错配。
risk_free_rate_monthly = risk_free_rate_annual / 12

# ==================== 步骤 2：在月度层面套用 CAPM ====================
# CAPM 核心公式: E(R_i) = R_f + β * (E(R_m) - R_f)
# 其中 (E(R_m) - R_f) 为市场风险溢价
market_risk_premium = market_return_monthly - risk_free_rate_monthly
capm_return_monthly = risk_free_rate_monthly + beta * market_risk_premium

# ==================== 步骤 3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==================== 课堂投屏展示 ====================
print("=" * 50)
print("《证券投资学》- CAPM 与证券市场线计算演示")
print("=" * 50)
print(f"1. 股票 Beta           : {beta}")
print(f"2. 市场月度收益率      : {market_return_monthly:.2%}")
print(f"3. 年化无风险利率      : {risk_free_rate_annual:.2%}")
print(f"4. 月度无风险利率(折算): {risk_free_rate_monthly:.4%}")
print("-" * 50)
print(f"市场风险溢价 (月度)   : {market_risk_premium:.4%}")
print(f"按 CAPM 预期月度收益率 : {capm_return_monthly:.4%}")
print("=" * 50)
print(f"输出字典结果: {result}")

