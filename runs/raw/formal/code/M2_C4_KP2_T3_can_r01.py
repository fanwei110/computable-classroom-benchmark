
"""
CAPM 与证券市场线课堂演示代码
计算：给定 beta、市场收益率和无风险利率，按 CAPM 求股票月度期望收益。
课程约定：利率、收益率用小数表示；年利率折算月利率用简单除法（年/12）。
"""

def main():
    # ---------- 给定参数（全部小数） ----------
    beta = 1.42                       # 股票 beta
    market_monthly = -0.058           # 上个月市场收益率 (下跌 5.8%)
    rf_annual = 0.047                 # 年化无风险利率 (4.7%)

    # 1. 年无风险利率折算为月利率（简单除法）
    rf_monthly = rf_annual / 12.0

    # 2. 月度层面套用 CAPM 公式：E(R) = Rf + beta * (Rm - Rf)
    capm_return_monthly = rf_monthly + beta * (market_monthly - rf_monthly)

    # 3. 按输出契约存入字典
    result = {
        'capm_return_monthly': capm_return_monthly
    }

    # 投屏友好输出
    print("=" * 50)
    print("CAPM 月度期望收益计算")
    print("-" * 50)
    print(f"年无风险利率      : {rf_annual:.4f} ({rf_annual*100:.2f}%)")
    print(f"月无风险利率      : {rf_monthly:.6f} ({rf_monthly*100:.4f}%)")
    print(f"市场月收益率      : {market_monthly:.4f} ({market_monthly*100:.2f}%)")
    print(f"股票 Beta         : {beta}")
    print("-" * 50)
    print(f"CAPM 月度期望收益 : {capm_return_monthly:.6f}")
    print(f"                   ({capm_return_monthly*100:.4f}%)")
    print("=" * 50)
    print("结果字典 result =", result)
    return result


# 脚本入口
if __name__ == "__main__":
    result = main()
