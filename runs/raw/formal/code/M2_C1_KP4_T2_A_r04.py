import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ========== 可调参数区 ==========
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
S_min, S_max = 70, 140   # 标的价格范围
sigmas = [0.15, 0.276, 0.40]  # 波动率列表（可修改）
S_target = 110    # 需要单独计算 delta 的标的价格
sigma_target = 0.276  # 对应波动率
# ===============================

# 生成标的价序列
S = np.linspace(S_min, S_max, 500)

# 绘图
plt.figure(figsize=(10, 6))
for sigma in sigmas:
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    plt.plot(S, delta, label=f'σ = {sigma*100:.1f}%')

plt.axvline(K, color='gray', linestyle='--', alpha=0.6, label=f'Strike = {K}')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.title('Call Option Delta vs Underlying Price (BSM)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 保存图片
figure_path = 'delta_plot.png'
plt.savefig(figure_path)
plt.close()

# 计算指定点的 delta
d1_target = (np.log(S_target / K) + (r + 0.5 * sigma_target**2) * T) / (sigma_target * np.sqrt(T))
delta_at_s110 = norm.cdf(d1_target)

# 按要求存入字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print(result)
