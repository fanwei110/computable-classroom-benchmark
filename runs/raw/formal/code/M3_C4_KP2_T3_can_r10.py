# ==========================================
# 《证券投资学》课堂实时计算：CAPM 与证券市场线
# ==========================================

# 1. 定义已知参数 (所有利率、收益率均用小数表示)
beta = 1.42                      # 股票的 Beta 系数
market_return_monthly = -0.058   # 上个月市场收益率 (跌了 5.8%)
risk_free_annual = 0.047         # 年化无风险利率 (4.7%)

# 2. 把年无风险利率按简单除法折算为月利率 (课程约定：年利率 / 12)
risk_free_monthly = risk_free_annual / 12

# 3. 在月度层面套用 CAPM 公式: E(Ri) = Rf + Beta * (Rm - Rf)
# 其中 Rf 和 Rm 均为月度数据
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 4. 填充 result 字典，键名严格为 'capm_return_monthly'
result = {
    'capm_return_monthly': capm_return_monthly
}

# 5. 课堂投屏输出展示
print("="*40)
print("CAPM 月度期望收益率计算过程演示")
print("="*40)
print(f"股票 Beta: {beta}")
print(f"市场月度收益率: {market_return_monthly:.4f} (即 {market_return_monthly*100:.1f}%)")
print(f"年化无风险利率: {risk_free_annual:.4f} (即 {risk_free_annual*100:.1f}%)")
print("-" * 40)
print(f"折算后的月度无风险利率: {risk_free_monthly:.6f} (即 {risk_free_monthly*100:.4f}%)")
print(f"市场风险溢价 (Rm - Rf): {(market_return_monthly - risk_free_monthly):.6f}")
print(f"CAPM 月度期望收益率: {capm_return_monthly:.6f} (即 {capm_return_monthly*100:.4f}%)")
print("="*40)
print(f"最终输出字典: {result}")
