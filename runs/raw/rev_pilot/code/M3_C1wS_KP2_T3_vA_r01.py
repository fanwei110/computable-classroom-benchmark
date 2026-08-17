import numpy as np

# =====================
// 已知参数
# =====================
beta = 1.42                     // 股票的 Beta 值
market_return_monthly = -0.058  // 上个月市场收益率 (-5.8%)
risk_free_annual = 0.047        // 年化无风险利率 (4.7%)

# =====================
// 1. 把年无风险利率折算为月利率
# =====================
// 假设处理：由于给定的市场月度收益率为离散百分比，为保持一致性，
// 采用单利折算（简单除以12），这也是投资学实务与教学中处理短期离散收益的常用且合理的假设。
risk_free_monthly = risk_free_annual / 12

# =====================
// 2. 在月度层面套用 CAPM
# =====================
// CAPM 公式: E(R_i) = R_f + β * (E(R_m) - R_f)
// 题目将已发生的市场收益代入，求该股票按CAPM本该有的月度期望收益
market_risk_premium_monthly = market_return_monthly - risk_free_monthly
capm_return_monthly = risk_free_monthly + beta * market_risk_premium_monthly

# =====================
// 3. 填充 result
# =====================
result = {
    'capm_return_monthly': capm_return_monthly
}

// （投屏辅助打印，方便课堂展示计算过程与结果）
print(f"年化无风险利率: {risk_free_annual:.4f}")
print(f"折算后月度无风险利率: {risk_free_monthly:.6f}")
print(f"月度市场风险溢价: {market_risk_premium_monthly:.6f}")
print(f"按CAPM计算的上月本该有收益: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print(f"\n最终输出结果字典: {result}")
