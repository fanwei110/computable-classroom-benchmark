import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算欧式期权的Black-Scholes Delta
    S: 标的资产价格
    K: 行权价
    T: 到期时间（年）
    r: 无风险利率
    sigma: 波动率
    option_type: 'call'或'put'
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
T = 0.58          # 到期时间（年）
S_range = np.linspace(70, 140, 100)  # 标的价格范围
volatilities = [0.15, 0.276, 0.40]  # 波动率列表

# 1. 计算不同波动率下的delta值
delta_results = {}
for vol in volatilities:
    delta_values = [black_scholes_delta(S, K, T, r, vol) for S in S_range]
    delta_results[vol] = delta_values

# 2. 绘制delta曲线
plt.figure(figsize=(10, 6))
for vol in volatilities:
    plt.plot(S_range, delta_results[vol], label=f'Vol = {vol*100:.1f}%')

plt.axvline(x=K, color='gray', linestyle='--', alpha=0.5)
plt.title('Black-Scholes Delta for European Call Option')
plt.xlabel('Underlying Asset Price')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 3. 计算标的110、波动率27.6%的delta
S_target = 110
vol_target = 0.276
delta_at_s110 = black_scholes_delta(S_target, K, T, r, vol_target)

# 4. 填充result字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)
