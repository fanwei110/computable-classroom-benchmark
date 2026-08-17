import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ============ 参数设置 ============
K = 97.5                      # 行权价
r = 0.043                     # 连续复利无风险利率（按年）
T = 0.58                      # 剩余期限（年）
S_min, S_max = 70, 140        # 标的价格范围
S_target = 110                # 需要报告的标的价格
sigma_target = 0.276          # 需要报告的波动率
vols = [0.15, 0.276, 0.40]    # 三条波动率曲线

# ============ 计算 Delta（欧式看涨期权）============
def delta_call(S, K, r, T, sigma):
    """欧式看涨期权 Delta = N(d1)"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 生成标的价格序列
S_array = np.linspace(S_min, S_max, 500)

# ============ 画图 ============
plt.figure(figsize=(10, 6))
for vol in vols:
    delta_vals = delta_call(S_array, K, r, T, vol)
    plt.plot(S_array, delta_vals, label=f'σ = {vol*100:.1f}%')

plt.axvline(x=K, color='gray', linestyle='--', linewidth=0.8, label=f'Strike={K}')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.title('Call Option Delta Curve')
plt.legend()
plt.grid(alpha=0.3)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ============ 计算指定点的 Delta ============
delta_at_s110 = delta_call(S_target, K, r, T, sigma_target)

# ============ 结果存入字典 ============
result = {
    'delta_at_s110': round(delta_at_s110, 6),
    'figure_path': os.path.abspath(figure_path)
}

# 打印结果（方便查看）
print(result)
