import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================================================
# 1. 参数设定（波动率列表为可调参数）
# ==================================================
K = 97.5                 # 行权价
r = 0.043                # 无风险利率（年化）
T = 0.58                 # 剩余时间（年）
S_min, S_max = 70, 140   # 标的价格范围
S_grid = np.linspace(S_min, S_max, 200)  # 标的网格

# 可调参数：波动率列表
sigma_list = [0.15, 0.276, 0.40]

# ==================================================
# 2. 定义 delta 计算函数（欧式看涨）
# ==================================================
def bs_call_delta(S, K, r, T, sigma):
    """
    返回欧式看涨期权的 Black-Scholes delta。
    S 可为标量或数组。
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ==================================================
# 3. 对每个波动率计算 delta，并绘图
# ==================================================
fig, ax = plt.subplots(figsize=(8, 5))

for sigma in sigma_list:
    delta = bs_call_delta(S_grid, K, r, T, sigma)
    ax.plot(S_grid, delta, label=f'σ = {sigma*100:.1f}%')

ax.axvline(x=K, color='gray', linestyle='--', linewidth=0.7, label=f'Strike = {K}')
ax.set_xlabel('Spot Price')
ax.set_ylabel('Delta')
ax.set_title('Delta of European Call Option (Black-Scholes)')
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)

# 保存图片
figure_path = './delta_curve.png'
fig.savefig(figure_path, dpi=200, bbox_inches='tight')
plt.close(fig)  # 避免在课堂上弹窗（如需显示可注释此行）

# ==================================================
# 4. 计算指定点的 delta（标的 110，波动率 27.6%）
# ==================================================
S_target = 110.0
sigma_target = 0.276
delta_target = bs_call_delta(S_target, K, r, T, sigma_target)

# ==================================================
# 5. 构建结果字典并输出
# ==================================================
result = {
    'delta_at_s110': delta_target,
    'figure_path': figure_path
}

# 课堂运行时可见（投屏显示）
print("=== Black-Scholes Delta 计算结果 ===")
print(f"标的={S_target}, 行权价={K}, 波动率={sigma_target*100}%, T={T}年")
print(f"Delta = {delta_target:.6f}")
print(f"图片路径 = {figure_path}")
print("\nresult 字典内容：")
print(result)
