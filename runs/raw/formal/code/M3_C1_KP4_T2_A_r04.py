import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ================= 可调参数 =================
K = 97.5                          # 行权价
r = 0.043                         # 利率
T = 0.58                          # 剩余期限（年）
S_min, S_max = 70, 140            # 标的价格范围
# 波动率参数（修改此列表即可调整绘制的波动率线条及数量）
volatilities = [0.15, 0.276, 0.40] 
# ============================================

def call_delta(S, K, T, r, sigma):
    """计算欧式看涨期权的Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 1. 计算标的等于110、波动率27.6%时的delta
S_target = 110
sigma_target = 0.276
delta_at_s110 = float(call_delta(S_target, K, T, r, sigma_target))

# 2. 生成标的价序列并绘图
S_range = np.linspace(S_min, S_max, 500)

plt.figure(figsize=(10, 6))

for sigma in volatilities:
    deltas = call_delta(S_range, K, T, r, sigma)
    plt.plot(S_range, deltas, label=f'Vol = {sigma*100:.1f}%')

plt.title('Call Option Delta vs. Underlying Price')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 3. 保存图片
figure_path = 'delta_vs_underlying_price.png'
plt.savefig(figure_path)
plt.close()

# 4. 构造结果字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print(result)
