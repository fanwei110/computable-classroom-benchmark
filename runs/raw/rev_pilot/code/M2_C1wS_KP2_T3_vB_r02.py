import numpy as np
import pandas as pd

# ============================================================
# 给定数据
# ============================================================
beta = 1.42                     # 该股票的 beta
market_return_monthly = -0.058  # 上个月大盘收益率 (-5.8%)
rf_annual = 0.047               # 年化无风险利率 (4.7%)

# ============================================================
# 1. 年无风险利率折算为月利率
# ============================================================
# 采用几何平均折算： (1 + r_f_annual)^(1/12) - 1
rf_monthly = (1 + rf_annual) ** (1/12) - 1

# ============================================================
# 2. 月度层面套用 CAPM 公式
# ============================================================
# CAPM: E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# ============================================================
# 3. 填充 result 字典（严格键名）
# ============================================================
result = {
    'capm_return_monthly': capm_return_monthly
}

# ============================================================
# 输出结果（投屏展示用）
# ============================================================
print("=" * 60)
print("          CAPM 期望收益计算")
print("=" * 60)
print(f"  年化无风险利率 (Rf annual)     : {rf_annual:.4f} ({rf_annual*100:.2f}%)")
print(f"  折算月无风险利率 (Rf monthly)   : {rf_monthly:.6f} ({rf_monthly*100:.4f}%)")
print(f"  股票 Beta                      : {beta}")
print(f"  市场月收益率 (Rm monthly)       : {market_return_monthly:.4f} ({market_return_monthly*100:.2f}%)")
print("-" * 60)
print(f"  市场风险溢价 (Rm - Rf) monthly  : {market_return_monthly - rf_monthly:.6f} ({(market_return_monthly - rf_monthly)*100:.4f}%)")
print(f"  按CAPM股票月期望收益率          : {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print("=" * 60)

print("\n>>> result 字典内容:")
print(result)
