import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 给定的参数
    rf = 0.023          # 无风险利率
    rm = 0.094          # 市场期望收益
    beta_x = 0.62
    beta_y = 1.18
    beta_z = 1.51
    actual_y = 0.131    # 股票Y实际年收益

    # 1. 计算CAPM期望收益
    market_premium = rm - rf
    er_x = rf + beta_x * market_premium
    er_y = rf + beta_y * market_premium
    er_z = rf + beta_z * market_premium

    # 2. 计算股票Y的alpha
    alpha_y = actual_y - er_y

    # 3. 填入结果字典
    result = {
        'er_x': er_x,
        'er_y': er_y,
        'er_z': er_z,
        'alpha_y': alpha_y
    }

    # （可选）打印结果，便于课堂投屏展示
    for key, value in result.items():
        print(f"{key}: {value:.6f} ({value*100:.4f}%)")

    # 可视化：证券市场线 (SML)
    betas = np.array([0.0, beta_x, beta_y, beta_z, 1.0, 1.5])
    sml_returns = rf + betas * market_premium

    plt.figure(figsize=(8, 5))
    plt.plot(betas, sml_returns, 'b-', linewidth=2, label='SML')
    plt.scatter([beta_x, beta_y, beta_z], [er_x, er_y, er_z], color='red', zorder=5)
    plt.scatter([beta_y], [actual_y], color='green', marker='^', s=100, zorder=5, label='Y actual')
    plt.axhline(y=rf, linestyle='--', color='gray', alpha=0.5)
    plt.xlabel('Beta')
    plt.ylabel('Expected Return')
    plt.title('Security Market Line (SML)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    return result

if __name__ == "__main__":
    result = main()
