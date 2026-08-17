import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# -------------------- 参数定义 --------------------
K = 97.5           # 行权价
r = 0.043          # 无风险利率（年化）
T = 0.58           # 剩余期限（年）
S_min = 70.0       # 标的价格下限
S_max = 140.0      # 标的价格上限
n_points = 500     # 曲线平滑度（描点数）

# 波动率参数（可调）
sigmas = [0.15, 0.276, 0.40]

# 指定要报告的参数
S_report = 110.0
sigma_report = 0.276

# -------------------- Delta 计算 --------------------
def delta_call(S, K, r, T, sigma):
    """计算欧式看涨期权的 Delta 值"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# -------------------- 绘图数据 --------------------
S = np.linspace(S_min, S_max, n_points)

# 分别计算不同波动率下的 Delta
delta_curves = {}
for sigma in sigmas:
    delta_curves[sigma] = delta_call(S, K, r, T, sigma)

# -------------------- 报告点计算 --------------------
delta_at_s110 = delta_call(S_report, K, r, T, sigma_report)

# -------------------- 画图与保存 --------------------
plt.figure(figsize=(10, 6))
for sigma in sigmas:
    plt.plot(S, delta_curves[sigma], label=f'σ = {sigma*100:.1f}%')

plt.axvline(x=K, color='grey', linestyle='--', alpha=0.6, label=f'Strike K={K}')
plt.axhline(y=0.5, color='grey', linestyle=':', alpha=0.4)

plt.xlabel('Spot Price S')
plt.ylabel('Delta')
plt.title('Delta of European Call Option (K=97.5, r=4.3%, T=0.58Y)')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# -------------------- 输出契约 --------------------
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 可选打印，便于直接查看
if __name__ == "__main__":
    print(f"Delta at S=110, σ=27.6%: {result['delta_at_s110']:.6f}")
    print(f"Figure saved to: {result['figure_path']}")
