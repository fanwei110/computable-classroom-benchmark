import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ========== 参数 ==========
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 到期时间（年）
vols = [0.15, 0.276, 0.40]   # 三条波动率曲线
S_low, S_high = 70, 140      # 标的价格范围

# ========== 计算看涨期权 Delta ==========
def call_delta(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ========== 生成数据并绘图 ==========
S_vals = np.linspace(S_low, S_high, 300)
plt.figure(figsize=(8, 5))

for sigma in vols:
    delta_vals = call_delta(S_vals, K, r, T, sigma)
    plt.plot(S_vals, delta_vals, label=f'vol = {sigma*100:.1f}%')

plt.xlabel('Underlying Price')
plt.ylabel('Call Delta')
plt.title('Call Delta Curve (K=97.5, r=4.3%, T=0.58)')
plt.legend()
plt.grid(True)

# 保存图像
fig_path = 'delta_curve.png'
plt.savefig(fig_path, dpi=150)
# plt.show()

# ========== 计算指定点 Delta ==========
S_target = 110
sigma_target = 0.276
delta_at_s110 = call_delta(S_target, K, r, T, sigma_target)

# ========== 按要求输出结果 ==========
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': fig_path
}

print(result)
