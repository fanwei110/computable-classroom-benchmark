import numpy as np

def calculate_capm_and_alpha():
    """
    计算股票 X、Y、Z 的 CAPM 期望年收益，以及股票 Y 的 alpha。
    """
    # 给定参数
    risk_free_rate = 0.023  # 无风险利率
    market_return = 0.094   # 市场期望收益
    beta_x = 0.62
    beta_y = 1.18
    beta_z = 1.51
    actual_return_y = 0.131  # 股票 Y 当年实际收益

    # 计算市场风险溢价
    market_premium = market_return - risk_free_rate

    # 根据 CAPM 公式计算期望收益: E(R) = Rf + beta * (E(Rm) - Rf)
    er_x = risk_free_rate + beta_x * market_premium
    er_y = risk_free_rate + beta_y * market_premium
    er_z = risk_free_rate + beta_z * market_premium

    # 计算股票 Y 的 alpha: alpha = 实际收益 - 期望收益
    alpha_y = actual_return_y - er_y

    # 将所有结果存入字典
    result = {
        'er_x': er_x,
        'er_y': er_y,
        'er_z': er_z,
        'alpha_y': alpha_y
    }

    return result

if __name__ == "__main__":
    result = calculate_capm_and_alpha()
    
    # 输出结果
    print("CAPM 期望收益和 Alpha 计算结果：")
    print(f"股票 X 的期望年收益 (er_x): {result['er_x']:.4f} ({result['er_x']*100:.2f}%)")
    print(f"股票 Y 的期望年收益 (er_y): {result['er_y']:.4f} ({result['er_y']*100:.2f}%)")
    print(f"股票 Z 的期望年收益 (er_z): {result['er_z']:.4f} ({result['er_z']*100:.2f}%)")
    print(f"股票 Y 的 Alpha (alpha_y): {result['alpha_y']:.4f} ({result['alpha_y']*100:.2f}%)")
