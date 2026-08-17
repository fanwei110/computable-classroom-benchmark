import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def calculate_call_delta(S, K, T, r, sigma, q=0.0):
    """
    计算欧式看涨期权的 Delta 值
    S: 标的价格 (可以是标量或数组)
    K: 行权价
    T: 剩余期限 (年)
    r: 无风险利率
    sigma: 波动率 (可调参数)
    q: 连续股息率，默认为0 (即不分红)
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ==================== 基础参数设定 ====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 4.3%
T = 0.58          # 剩余期限 0.58年
q = 0.0           # 标的不分红
sigma_list = [0.15, 0.276, 0.40] # 波动率参数列表 (15%, 27.6%, 40%)

# ==================== 计算指定条件下的 Delta ====================
S_target = 110
sigma_target = 0.276
delta_at_s110 = calculate_call_delta(S_target, K, T, r, sigma_target, q)

# ==================== 绘制 Delta 曲线 ====================
S_range = np.linspace(70, 140, 500) # 标的价格从 70 到 140

plt.figure(figsize=(10, 6))

for sigma in sigma_list:
    # 将波动率作为参数传入计算函数
    deltas = calculate_call_delta(S_range, K, T, r, sigma, q)
    plt.plot(S_range, deltas, label=f'Volatility = {sigma*100:.1f}%')

plt.title('European Call Option Delta vs Underlying Price')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图表
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 输出结果契约 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以供验证
print(result)
