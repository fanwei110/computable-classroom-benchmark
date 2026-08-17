import numpy as np

def main():
    # 给定数据
    beta = 1.42
    market_monthly_return = -0.058  # 市场上月下跌5.8%
    annual_risk_free_rate = 0.047   # 年化无风险利率4.7%

    # 将年化无风险利率折算为月利率（使用几何平均法以保证内部一致）
    monthly_risk_free_rate = (1 + annual_risk_free_rate) ** (1/12) - 1

    # 根据CAPM计算该股票的期望月度收益
    # 公式: E(R_i) = R_f + beta * (R_m - R_f)
    expected_monthly_return = (
        monthly_risk_free_rate
        + beta * (market_monthly_return - monthly_risk_free_rate)
    )

    # 将结果存入字典
    result = {
        'capm_return_monthly': expected_monthly_return
    }

    # 输出结果（供投屏展示）
    print("CAPM计算结果：")
    print(f"月无风险利率: {monthly_risk_free_rate:.6f} ({monthly_risk_free_rate*100:.4f}%)")
    print(f"市场月收益: {market_monthly_return:.6f} ({market_monthly_return*100:.4f}%)")
    print(f"股票期望月收益 (CAPM): {expected_monthly_return:.6f} ({expected_monthly_return*100:.4f}%)")
    print(f"\nresult = {result}")

    return result

if __name__ == "__main__":
    result = main()
