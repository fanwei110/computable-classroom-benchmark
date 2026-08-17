import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ========== 可调参数 ==========
K = 97.5               # 行权价
r = 0.043              # 无风险利率（连续复利，小数形式）
T = 0.58               # 剩余到期时间（年）
S_min, S_max = 70, 140 # 标的价范围
S_target = 110         # 需要报告 delta 的标的价格
sigma_target = 0.276   # 对应报告 delta 的波动率
# 三条曲线的波动率（可在此处增减/修改）
volatility_list = [0.15, 0.276, 0.40]
# =============================

def bs_call_delta(S, K, r, T, sigma):
    """计算欧式看涨期权的 Delta (Black-Scholes)"""
    if sigma <= 0 or T <= 0:
        return np.where(S > K, 1.0, 0.0)  # 处理极端情况
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 生成标的价格序列
S_array = np.linspace(S_min, S_max, 500)

# 绘图
plt.figure(figsize=(10, 6))
for sigma in volatility_list:
    delta = bs_call_delta(S_array, K, r, T, sigma)
    plt.plot(S_array, delta, label=f'σ = {sigma:.1%}')

# 计算并标记特定点
delta_target = bs_call_delta(S_target, K, r, T, sigma_target)
plt.scatter(S_target, delta_target, color='red', zorder=5)
plt.annotate(f'S=110, σ={sigma_target:.1%}\nΔ = {delta_target:.4f}',
             xy=(S_target, delta_target), xytext=(S_target+5, delta_target-0.05),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10, color='red')

plt.xlabel('Spot Price (S)')
plt.ylabel('Delta (Δ)')
plt.title('Delta vs Spot Price (European Call Option)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
fig_path = 'delta_vs_spot.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# ========== 输出契约 ==========
result = {
    'delta_at_s110': delta_target,
    'figure_path': os.path.abspath(fig_path)
}

print("计算结果：")
print(f"标的 S=110, 波动率 σ={sigma_target:.1%} 时的 Delta = {delta_target:.6f}")
print(f"图片已保存至：{result['figure_path']}")
print("\nresult 字典内容：")
print(result)
