import numpy as np

def main():
    # 给定数据
    beta = 1.42
    market_return_monthly = -0.058  # 市场月收益 -5.8%
    risk_free_annual = 0.047        # 年无风险利率 4.7%

    # 1. 将年无风险利率折算为月利率（简单利息折算，内部一致）
    risk_free_monthly = risk_free_annual / 12.0

    # 2. 应用CAPM公式：E(Ri) = Rf + beta * (Rm - Rf)
    capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

    # 3. 将结果存入字典
    result = {
        'capm_return_monthly': capm_return_monthly
    }

    # 输出结果以供课堂投屏
    print("=== CAPM 计算结果 ===")
    print(f"年无风险利率: {risk_free_annual*100:.2f}%")
    print(f"折算月无风险利率: {risk_free_monthly*100:.4f}%")
    print(f"市场月收益: {market_return_monthly*100:.2f}%")
    print(f"股票 beta: {beta}")
    print(f"按CAPM计算的股票月期望收益: {capm_return_monthly*100:.4f}%")
    print("\n结果字典:")
    print(result)

    return result

if __name__ == "__main__":
    result = main()
