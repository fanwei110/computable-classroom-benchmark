import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算欧式期权的 Black-Scholes delta
    S: 标的资产价格
    K: 行权价
    T: 剩余期限（年）
    r: 无风险利率
    sigma: 波动率
    option_type: 'call' 或 'put'
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    return delta

# 参数设置
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
S_range = np.linspace(70, 140, 100)  # 标的价格范围
volatilities = [0.15, 0.276, 0.40]  # 波动率列表

# 1. 计算不同波动率下的delta
deltas = {}
for sigma in volatilities:
    deltas[sigma] = [black_scholes_delta(S, K, T, r, sigma) for S in S_range]

# 2. 绘制图形
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    plt.plot(S_range, deltas[sigma], label=f'Volatility = {sigma*100:.1f}%')

plt.title('Delta vs Underlying Price for Different Volatilities')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_vs_underlying.png'
plt.savefig(figure_path)
plt.close()

# 3. 计算特定条件下的delta
S_target = 110
sigma_target = 0.276
delta_at_s110 = black_scholes_delta(S_target, K, T, r, sigma_target)

# 4. 填充result字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果以供验证
print(f"Delta at S=110, σ=27.6%: {delta_at_s110:.4f}")
print(f"Figure saved to: {result['figure_path']}")
