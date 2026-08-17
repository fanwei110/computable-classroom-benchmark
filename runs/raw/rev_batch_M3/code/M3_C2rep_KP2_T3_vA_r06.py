import numpy as np

# ==================== 已知参数 ====================
beta = 1.42              # 股票的 Beta 值
rm_monthly = -0.058      # 上个月市场收益率（跌 5.8%）
rf_annual = 0.047        # 年化无风险利率（4.7%）

# ==================== 步骤 1：折算年无风险利率为月利率 ====================
# 假设年利率 4.7% 为名义年利率(APR)，在单期 CAPM 模型中，
# 月度无风险利率通常采用简单算术折算（即直接除以 12），这符合传统投资学教材的默认处理。
rf_monthly = rf_annual / 12

# ==================== 步骤 2：在月度层面套用 CAPM ====================
# CAPM 公式: E(R_i) = R_f + Beta_i * (E(R_m) - R_f)
# 在此情景下，市场已实现的月度收益率为 -5.8%，计算该股票按 CAPM 本该有的月度收益
capm_return_monthly = rf_monthly + beta * (rm_monthly - rf_monthly)

# ==================== 步骤 3：填充 result ====================
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==================== 课堂输出展示 ====================
# 为方便教师投屏展示，打印关键计算步骤与结果
print("=" * 50)
print("《证券投资学》课堂实时计算：CAPM 与证券市场线")
print("=" * 50)
print(f"1. 参数设定：")
print(f"   - Beta = {beta}")
print(f"   - 市场月收益率 (Rm) = {rm_monthly:.2%}")
print(f"   - 无风险年利率 (Rf_annual) = {rf_annual:.2%}")
print(f"2. 利率折算：")
print(f"   - 无风险月利率 (Rf_monthly) = {rf_annual:.2%} / 12 = {rf_monthly:.4%}")
print(f"3. CAPM 计算：")
print(f"   - E(Ri) = Rf + Beta * (Rm - Rf)")
print(f"   - E(Ri) = {rf_monthly:.4%} + {beta} * ({rm_monthly:.2%} - {rf_monthly:.4%})")
print(f"   - E(Ri) = {capm_return_monthly:.4%}")
print("=" * 50)
print(f"最终结果字典: {result}")

