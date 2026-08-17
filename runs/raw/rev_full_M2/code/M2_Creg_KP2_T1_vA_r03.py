import numpy as np

def calculate_capm_and_alpha():
    """
    根据 CAPM 模型计算股票期望收益和 alpha 值
    
    参数:
    无风险利率 = 2.3% (0.023)
    市场期望收益 = 9.4% (0.094)
    股票 X beta = 0.62
    股票 Y beta = 1.18
    股票 Z beta = 1.51
    股票 Y 实际收益 = 13.1% (0.131)
    """
    
    # 输入参数
    risk_free_rate = 0.023  # 无风险利率
    market_return = 0.094   # 市场期望收益
    
    # 各股票的 beta 值
    beta_x = 0.62
    beta_y = 1.18
    beta_z = 1.51
    
    # 股票 Y 的实际年收益
    actual_return_y = 0.131
    
    # 计算市场风险溢价
    market_risk_premium = market_return - risk_free_rate
    
    # 根据 CAPM 计算期望收益: E(Ri) = Rf + βi * (E(Rm) - Rf)
    expected_return_x = risk_free_rate + beta_x * market_risk_premium
    expected_return_y = risk_free_rate + beta_y * market_risk_premium
    expected_return_z = risk_free_rate + beta_z * market_risk_premium
    
    # 计算 alpha: α = 实际收益 - CAPM 期望收益
    alpha_y = actual_return_y - expected_return_y
    
    # 构建结果字典
    result = {
        'er_x': expected_return_x,
        'er_y': expected_return_y,
        'er_z': expected_return_z,
        'alpha_y': alpha_y
    }
    
    return result

def main():
    # 执行计算
    result = calculate_capm_and_alpha()
    
    # 打印结果
    print("CAPM 期望收益和 Alpha 计算结果:")
    print(f"股票 X 的 CAPM 期望收益 (er_x): {result['er_x']:.6f} ({result['er_x']*100:.4f}%)")
    print(f"股票 Y 的 CAPM 期望收益 (er_y): {result['er_y']:.6f} ({result['er_y']*100:.4f}%)")
    print(f"股票 Z 的 CAPM 期望收益 (er_z): {result['er_z']:.6f} ({result['er_z']*100:.4f}%)")
    print(f"股票 Y 的 Alpha (alpha_y): {result['alpha_y']:.6f} ({result['alpha_y']*100:.4f}%)")
    
    # 验证 CAPM 公式
    rf = 0.023
    rm = 0.094
    print(f"\n验证计算:")
    print(f"市场风险溢价 = {rm - rf:.6f} ({(rm - rf)*100:.4f}%)")
    print(f"股票 X 期望收益 = {rf} + {0.62} * {rm - rf:.6f} = {result['er_x']:.6f}")
    print(f"股票 Y 期望收益 = {rf} + {1.18} * {rm - rf:.6f} = {result['er_y']:.6f}")
    print(f"股票 Z 期望收益 = {rf} + {1.51} * {rm - rf:.6f} = {result['er_z']:.6f}")
    actual_y = 0.131
    print(f"股票 Y Alpha = {actual_y} - {result['er_y']:.6f} = {result['alpha_y']:.6f}")
    
    return result

if __name__ == "__main__":
    main()
