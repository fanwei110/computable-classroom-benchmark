import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

def black_scholes_delta(S, K, r, T, sigma, option_type='call'):
    """
    计算欧式期权的 Delta (闭式解)
    S: 标的资产价格 (标量或数组)
    K: 行权价
    r: 无风险利率 (年化, 连续复利)
    T: 剩余期限 (年)
    sigma: 波动率 (年化)
    option_type: 'call' 或 'put'
    """
    if T <= 0:
        # 到期时 delta 为 1 或 0 (call), -1 或 0 (put)
        if option_type == 'call':
            return np.where(S > K, 1.0, 0.0)
        else:
            return np.where(S < K, -1.0, 0.0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1.0

def main():
    # 给定参数
    K = 97.5
    r = 4.3 / 100          # 4.3%
    T = 0.58               # 0.58 年
    S_min, S_max = 70, 140
    S_grid = np.linspace(S_min, S_max, 500)   # 标的网格

    # 三个波动率
    vol_list = [0.15, 0.276, 0.40]
    vol_labels = [f'{v*100:.1f}%' for v in vol_list]  # 用于图例

    # 计算并绘图
    plt.figure(figsize=(10, 6))
    for vol in vol_list:
        delta = black_scholes_delta(S_grid, K, r, T, vol, option_type='call')
        plt.plot(S_grid, delta, lw=2, label=f'$\sigma$ = {vol*100:.1f}%')

    # 标注特定点: S=110, vol=27.6%
    vol_target = 0.276
    S_target = 110.0
    delta_target = black_scholes_delta(S_target, K, r, T, vol_target, option_type='call')
    plt.plot(S_target, delta_target, 'ro', markersize=8)
    plt.annotate(f'({S_target}, {delta_target:.4f})',
                 xy=(S_target, delta_target),
                 xytext=(S_target+5, delta_target-0.05),
                 arrowprops=dict(arrowstyle='->', color='red'),
                 fontsize=10, color='red')

    plt.title(f'Call Option Delta vs Spot Price (K={K}, r={r*100}%, T={T}yr)')
    plt.xlabel('Spot Price S')
    plt.ylabel('Delta')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # 保存图像
    figure_path = 'delta_curves.png'
    plt.savefig(figure_path, dpi=150, bbox_inches='tight')
    plt.close()  # 避免在某些环境中弹出窗口

    # 构造结果字典
    result = {
        'delta_at_s110': delta_target,
        'figure_path': figure_path
    }
    
    # 输出结果
    print("=== 结果 ===")
    print(f"标的=110, 波动率=27.6% 时, 看涨期权 Delta = {delta_target:.6f}")
    print(f"图片已保存至: {os.path.abspath(figure_path)}")
    print("result 字典:", result)
    
    return result

if __name__ == '__main__':
    main()
