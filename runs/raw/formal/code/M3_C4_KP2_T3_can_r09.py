import numpy as np

# ==================== 输入参数 ====================
# 课程约定：所有利率、收益率均用小数表示
beta = 1.42
market_return_monthly = -0.058      # 上个月市场跌幅 5.8%
risk_free_rate_annual = 0.047       # 年化无风险利率 4.7%

# ==================== 步骤 1 ====================
# 把年无风险利率按简单除法折算为月利率（年利率/12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# ==================== 步骤 2 ====================
# 在月度层面套用 CAPM: E(R_i) = R_f + β * (E(R_m) - R_f)
# 此时 R_f 和 E(R_m) 均为月度数据
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# ==================== 步骤 3 ====================
# 填充 result 字典，键名严格为 'capm_return_monthly'
result = {
    'capm_return_monthly': capm_return_monthly
}

# ==================== 课堂投屏展示 ====================
print("=" * 50)
print("《证券投资学》- CAPM 与证券市场线计算")
print("=" * 50)
print(f"输入参数:")
print(f"  Beta (β)             : {beta}")
print(f"  市场月收益率 (R_m)    : {market_return_monthly:.4f} ({market_return_monthly*100:.1f}%)")
print(f"   年化无风险利率 (R_f) : {risk_free_rate_annual:.4f} ({risk_free_rate_annual*100:.1f}%)")
print("-" * 50)
print(f"步骤1 - 月度无风险利率 : {risk_free_rate_monthly:.6f} ({risk_free_rate_monthly*100:.4f}%)")
print(f"步骤2 - CAPM月度期望收益: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print("=" * 50)
print(f"最终结果字典:\n{result}")
