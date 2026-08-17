import numpy as np

# ==========================================
# 1. 参数设定
# ==========================================
beta = 1.42                     # 股票的 Beta 值
market_return_monthly = -0.058  # 大盘上月收益率 -5.8%
risk_free_rate_annual = 0.047   # 年化无风险利率 4.7%

# ==========================================
# 2. 把年无风险利率折算为月利率
# ==========================================
# 假设：采用复利折算法（Compound Interest），这更符合资金时间价值的金融学严谨定义
# 公式: r_monthly = (1 + r_annual)^(1/12) - 1
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

# ==========================================
# 3. 在月度层面套用 CAPM
# ==========================================
# CAPM 核心公式: E(R_i) = R_f + β * (E(R_m) - R_f)
# 注：由于我们计算的是该股票“上个月”应有的收益，大盘已实现的月度收益在此作为市场期望收益 E(R_m) 的代理变量
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# ==========================================
# 4. 填充 result 字典
# ==========================================
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==========================================
# 课堂投屏展示辅助输出
# ==========================================
print("="*40)
print("CAPM 与证券市场线 —— 月度期望收益计算")
print("="*40)
print(f"输入参数:")
print(f"  年化无风险利率 (Rf_annual) : {risk_free_rate_annual:.2%}")
print(f"  折算月无风险利率 (Rf_monthly): {risk_free_rate_monthly:.4%}")
print(f"  大盘月度收益率 (Rm_monthly) : {market_return_monthly:.2%}")
print(f"  股票 Beta (β)              : {beta}")
print("-"*40)
print(f"CAPM 计算过程:")
print(f"  E(Ri) = {risk_free_rate_monthly:.4%} + {beta} * ({market_return_monthly:.2%} - {risk_free_rate_monthly:.4%})")
print(f"  E(Ri) = {capm_return_monthly:.4%}")
print("="*40)
print(f"最终结果字典: {result}")
