import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ------------------------------ 参数设置（可调）-------------------------------
K = 97.5          # 行权价
r = 0.043         # 无风险利率（年化）
T = 0.58          # 剩余期限（年）
S_range = (70, 140)    # 标的价格绘图范围
S_specific = 110.0     # 需要单独报告的标的价格
sigma_specific = 0.276 # 需要单独报告的波动率
sigma_list = [0.15, 0.276, 0.40]  # 三条波动率曲线（可调）
figure_filename = "delta_curve.png"
# -------------------------------------------------------------------------

def black_scholes_call_delta(S, K, r, T, sigma):
    """计算欧式看涨期权的 Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

def main() -> dict:
    # 1. 生成标的价格网格并计算每条曲线的 Delta
    S_grid = np.linspace(S_range[0], S_range[1], 200)

    # 2. 绘图
    plt.figure(figsize=(10, 6))
    for sigma in sigma_list:
        delta = black_scholes_call_delta(S_grid, K, r, T, sigma)
        plt.plot(S_grid, delta, label=f"σ = {sigma*100:.1f}%")

    plt.xlabel("标的价格 S")
    plt.ylabel("Delta")
    plt.title("Black-Scholes 欧式看涨期权 Delta")
    plt.legend()
    plt.grid(True)
    plt.savefig(figure_filename, dpi=150)
    plt.close()

    # 3. 计算指定点的 Delta
    delta_at_s110 = black_scholes_call_delta(S_specific, K, r, T, sigma_specific)

    result = {
        "delta_at_s110": delta_at_s110,
        "figure_path": figure_filename,
    }
    return result

if __name__ == "__main__":
    result = main()
    print("delta_at_s110 =", result["delta_at_s110"])
    print("figure saved at:", result["figure_path"])
