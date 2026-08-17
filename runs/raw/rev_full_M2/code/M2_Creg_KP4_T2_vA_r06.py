import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

def call_delta(S, K, T, r, sigma):
    """计算无分红欧式看涨期权的 Delta (Black-Scholes)."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

def main():
    # ---------- 合约参数 ----------
    K = 97.5          # 行权价
    r = 0.043         # 无风险利率 (4.3%)
    T = 0.58          # 剩余期限 (年)

    # ---------- 波动率 (可调参数) ----------
    sigmas = [0.15, 0.276, 0.40]   # 15%, 27.6%, 40%

    # ---------- 标的价格范围 ----------
    S_range = np.linspace(70, 140, 500)

    # ---------- 画 Delta 曲线 ----------
    plt.figure(figsize=(10, 6))
    for sigma in sigmas:
        delta_vals = call_delta(S_range, K, T, r, sigma)
        plt.plot(S_range, delta_vals, linewidth=2, label=f'σ = {sigma*100:.1f}%')

    plt.xlabel('Spot Price')
    plt.ylabel('Delta')
    plt.title('Call Option Delta (K=97.5, T=0.58yr, r=4.3%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # 保存图像，使用绝对路径确保可访问
    figure_filename = 'call_delta_curve.png'
    figure_path = os.path.abspath(figure_filename)
    plt.savefig(figure_path, dpi=150)
    plt.close()

    # ---------- 计算指定点的 Delta ----------
    S_target = 110.0
    sigma_target = 0.276   # 27.6%
    delta_at_s110 = call_delta(S_target, K, T, r, sigma_target)

    # ---------- 结果字典 ----------
    result = {
        'delta_at_s110': delta_at_s110,
        'figure_path': figure_path
    }

    # 控制台简要输出
    print(f"Delta at S=110, σ=27.6%: {delta_at_s110:.6f}")
    print(f"Figure saved to: {figure_path}")

    return result

if __name__ == "__main__":
    result = main()
