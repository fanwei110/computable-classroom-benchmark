import numpy as np

# ==================== 输入参数 ====================
beta = 1.42                      # 股票的 Beta 值
market_return_monthly = -0.058   # 上个月市场收益率 (跌了 5.8%，即 -5.8%)
risk_free_rate_annual = 0.047    # 年化无风险利率 (4.7%)

# ==================== 步骤 1：把年无风险利率折算为月利率 ====================
# 假设处理：采用单利折算（即直接除以12），这是《证券投资学》中处理短期CAPM计算
# 最常见且与月度市场收益率口径最一致的惯例（若用复利折算，差异极小，此处取教材最常见做法）。
risk_free_rate_monthly = risk_free_rate_annual / 12

# ==================== 步骤 2：在月度层面套用 CAPM ====================
# CAPM 公式: E(R_i) = R_f + beta * (E(R_m) - R_f)
# 其中：
# E(R_i) 为股票预期收益率
# R_f 为月度无风险利率
# E(R_m) 为市场收益率
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# ==================== 步骤 3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# 课堂展示辅助打印（非必须，但有助于投屏观察）
print(f"年化无风险利率折算月利率: {risk_free_rate_monthly:.6%}")
print(f"CAPM 月度预期收益率: {capm_return_monthly:.6%}")
print(f"结果字典 result: {result}")
