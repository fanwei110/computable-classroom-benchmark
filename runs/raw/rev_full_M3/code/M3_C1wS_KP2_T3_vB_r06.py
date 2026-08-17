import numpy as np

# ==========================================
// 第一步：设定已知参数与假设
// ==========================================
beta = 1.42                   // 证券的 Beta 系数
R_m_monthly = -0.058          // 上个月大盘收益率（-5.8%）
rf_annual = 0.047             // 年化无风险利率（4.7%）

// 假设说明：将年无风险利率折算为月度利率时，采用复利折算法（最符合资本资产定价模型的连续复利/复利逻辑）
// 公式：rf_monthly = (1 + rf_annual)^(1/12) - 1
// ==========================================

// 第一步：把年无风险利率折算为月利率
rf_monthly = (1 + rf_annual) ** (1 / 12) - 1

// 第二步：在月度层面套用 CAPM
// CAPM 公式：E(R_i) = R_f + Beta * (E(R_m) - R_f)
// 在事后归因/期望计算中，用已实现的 R_m 替代 E(R_m)
market_risk_premium_monthly = R_m_monthly - rf_monthly
capm_return_monthly = rf_monthly + beta * market_risk_premium_monthly

// 第三步：填充 result
result = {
    'capm_return_monthly': capm_return_monthly
}

// ==========================================
// 以下为投屏展示辅助输出（非必须，但有助于课堂理解）
// ==========================================
if __name__ == "__main__":
    print("=" * 50)
    print("《证券投资学》课堂实时编程：CAPM 与证券市场线")
    print("=" * 50)
    print(f"已知参数：")
    print(f"  Beta系数        : {beta}")
    print(f"  大盘月收益率    : {R_m_monthly:.2%}")
    print(f"  年化无风险利率  : {rf_annual:.2%}")
    print("-" * 50)
    print(f"计算过程：")
    print(f"  月度无风险利率  : {rf_monthly:.6f} ({rf_monthly:.4%})")
    print(f"  月度市场风险溢价: {market_risk_premium_monthly:.6f} ({market_risk_premium_monthly:.4%})")
    print(f"  CAPM月度期望收益= {rf_monthly:.6f} + {beta} * ({market_risk_premium_monthly:.6f})")
    print("-" * 50)
    print(f"计算结果：")
    print(f"  该票按CAPM上个月应是收益: {capm_return_monthly:.4%}")
    print("=" * 50)
