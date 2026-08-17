import numpy as np

# ==========================================
# 《证券投资学》课堂实时演示代码
# 概念：CAPM 与证券市场线 (SML)
# ==========================================

# --- 输入参数 ---
beta = 1.42                     # 股票的 Beta 系数
market_return_monthly = -0.058   # 上个月市场收益率 (-5.8%)
risk_free_rate_annual = 0.047    # 年无风险利率 (4.7%)

# --- 步骤 1：把年无风险利率折算为月利率 ---
# 假设处理：采用复利折算方式将年利率转换为月利率，这在金融学中比简单除法更严谨。
# 公式: R_f_monthly = (1 + R_f_annual)^(1/12) - 1
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1 / 12) - 1

# --- 步骤 2：在月度层面套用 CAPM ---
# CAPM 公式: E(R_i) = R_f + Beta * (E(R_m) - R_f)
# 题目要求计算“上个月本该收益多少”，因此将上个月的实际市场收益率作为 E(R_m) 代入。
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# --- 步骤 3：填充 result ---
result = {
    'capm_return_monthly': capm_return_monthly
}

# --- 课堂投屏展示辅助信息 ---
print("="*45)
print(" CAPM 与证券市场线 - 月度期望收益计算")
print("="*45)
print(f" 股票 Beta:                {beta}")
print(f" 市场月度收益率 (R_m):     {market_return_monthly:.4f} ({market_return_monthly*100:.2f}%)")
print(f" 年无风险利率 (R_f_annual):{risk_free_rate_annual:.4f} ({risk_free_rate_annual*100:.1f}%)")
print(f" 月无风险利率 (R_f_monthly):{risk_free_rate_monthly:.6f} ({risk_free_rate_monthly*100:.4f}%)")
print("-"*45)
print(f" 👉 CAPM 预期月度收益率:   {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print("="*45)
print(f"\n要求的输出字典 result:\n{result}")
