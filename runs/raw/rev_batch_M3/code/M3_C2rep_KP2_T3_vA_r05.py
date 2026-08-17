import numpy as np

# ==================== 已知参数 ====================
beta = 1.42                     # 股票的 Beta 系数
market_return_monthly = -0.058  # 上个月市场收益率 (-5.8%)
rf_annual = 0.047               # 年化无风险利率 (4.7%)

# ==================== 步骤1：折算无风险利率 ====================
# 假设：采用复利折算方式将年化无风险利率转化为月度无风险利率
# 公式：rf_monthly = (1 + rf_annual)^(1/12) - 1
rf_monthly = (1 + rf_annual) ** (1 / 12) - 1

# ==================== 步骤2：套用 CAPM ====================
# CAPM 公式：E(R_i) = R_f + β * (E(R_m) - R_f)
# 在月度层面，所有变量均使用月度数据
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# ==================== 步骤3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==================== 课堂展示打印 ====================
print(f"【计算过程】")
print(f"1. 年化无风险利率折算为月利率: (1 + {rf_annual})^(1/12) - 1 = {rf_monthly:.6f} ({rf_monthly*100:.4f}%)")
print(f"2. 月度市场风险溢价: {market_return_monthly:.4f} - {rf_monthly:.6f} = {market_return_monthly - rf_monthly:.6f}")
print(f"3. CAPM 月度期望收益: {rf_monthly:.6f} + {beta} * ({market_return_monthly - rf_monthly:.6f}) = {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print("-" * 50)
print(f"result = {result}")
