import numpy as np

# ==========================================
# 《证券投资学》课堂实时编程：CAPM 与证券市场线
# ==========================================

# 1. 已知参数
beta = 1.42                   # 股票的 Beta 系数
r_m_market = -0.058           # 上个月市场收益率 (-5.8%)
r_f_annual = 0.047            # 年化无风险利率 (4.7%)

# 2. 假设处理与利率折算
# 假设：年化无风险利率为有效年化收益率(EAR)，采用几何折算法将其转换为月度复利利率。
# 折算公式: r_f_monthly = (1 + r_f_annual)^(1/12) - 1
r_f_monthly = (1 + r_f_annual) ** (1 / 12) - 1

# 3. 在月度层面套用 CAPM
# 假设：在事后计算（如计算詹森阿尔法）时，CAPM 中的期望市场收益率 E(R_m) 
# 用上个月已实现的市场收益率 R_m 来替代。
# CAPM 公式: E(R_i) = R_f + Beta * (E(R_m) - R_f)
capm_return_monthly = r_f_monthly + beta * (r_m_market - r_f_monthly)

# 4. 填充 result
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==========================================
# 课堂投屏输出展示
# ==========================================
print("="*50)
print(" CAPM 月度期望收益率计算")
print("="*50)
print(f"股票 Beta          : {beta}")
print(f"市场月度收益率     : {r_m_market:.2%}")
print(f"年化无风险利率     : {r_f_annual:.2%}")
print(f"折算月度无风险利率 : {r_f_monthly:.4%}")
print("-" * 50)
print(f"按 CAPM 本应收益   : {capm_return_monthly:.4%}")
print("="*50)
print(f"result字典内容     : {result}")
