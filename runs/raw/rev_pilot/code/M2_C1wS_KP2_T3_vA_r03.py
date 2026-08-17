import numpy as np

# ============================================================
# CAPM 月度期望收益计算
# 题目条件：
#   股票 beta = 1.42
#   上个月市场收益率 = -5.8% (即 -0.058)
#   年无风险利率 = 4.7% (即 0.047)
# ============================================================

# 给定参数
beta = 1.42
market_return_monthly = -0.058
rf_annual = 0.047

# ---------- 1. 将年无风险利率折算为月利率 ----------
# 采用有效月利率 (复利折算)，内部一致且符合金融学常见处理方式
rf_monthly = (1 + rf_annual) ** (1 / 12) - 1

# ---------- 2. 套用 CAPM 计算月度期望收益 ----------
# CAPM 公式：E(R) = Rf + beta * (Rm - Rf)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# ---------- 3. 填充结果字典 ----------
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（方便教师投屏查看）
print("=== CAPM 计算结果 ===")
print(f"年无风险利率: {rf_annual:.4%}")
print(f"折算月无风险利率: {rf_monthly:.6%}")
print(f"市场月度收益率: {market_return_monthly:.4%}")
print(f"股票 beta: {beta}")
print(f"CAPM 预期月度收益率: {capm_return_monthly:.6%}")
print("\nresult 字典:", result)
