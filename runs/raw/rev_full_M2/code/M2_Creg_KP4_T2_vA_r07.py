import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 可调参数 ====================
# 波动率列表（可在此处增减或修改）
SIGMAS = [0.15, 0.276, 0.40]
# ================================================

def delta_call(S, K, T, r, sigma):
    """计算欧式看涨期权的 Delta（Black-Scholes，无分红）"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

def main():
    # 合约参数
    K = 97.5          # 行权价
    r = 0.043         # 无风险利率
    T = 0.58          # 剩余期限（年）
    S_range = np.linspace(70, 140, 500)

    # 画图
    fig, ax = plt.subplots(figsize=(8, 5))
    for sigma in SIGMAS:
        delta_vals = delta_call(S_range, K, T, r, sigma)
        ax.plot(S_range, delta_vals, label=f'σ = {sigma*100:.1f}%')

    ax.set_xlabel('标的资产价格')
    ax.set_ylabel('Delta')
    ax.set_title('欧式看涨期权 Delta 曲线')
    ax.legend()
    ax.grid(True)

    figure_path = 'delta_curve.png'
    fig.savefig(figure_path, dpi=120, bbox_inches='tight')
    plt.close(fig)

    # 计算特定点：标的=110, 波动率=27.6%
    S_target = 110.0
    sigma_target = 0.276
    delta_at_s110 = float(delta_call(S_target, K, T, r, sigma_target))

    # 按要求存入字典
    result = {
        'delta_at_s110': delta_at_s110,
        'figure_path': figure_path
    }
    print(result)

if __name__ == '__main__':
    main()
