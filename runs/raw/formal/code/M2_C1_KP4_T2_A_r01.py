import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def calculate_delta(S, K, T, r, sigma, option_type='call'):
    """计算期权的delta值"""
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    if option_type == 'call':
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1

# 参数设置
K = 97.5  # 行权价
r = 0.043  # 利率4.3%
T = 0.58  # 剩余0.58年
S_range = np.linspace(70, 140, 1000)  # 标的价从70到140

# 波动率参数（可调整）
volatilities = [0.15, 0.276, 0.40]  # 15%, 27.6%, 40%
volatility_labels = ['15%', '27.6%', '40%']

# 创建图表
plt.figure(figsize=(10, 6))

# 计算并绘制不同波动率下的delta曲线
for sigma, label in zip(volatilities, volatility_labels):
    deltas = [calculate_delta(S, K, T, r, sigma) for S in S_range]
    plt.plot(S_range, deltas, label=f'σ = {label}', linewidth=2)

# 添加图表元素
plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
plt.axvline(x=K, color='red', linestyle='--', alpha=0.3, label=f'行权价 {K}')
plt.xlabel('标的价格', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.title('看涨期权Delta随标的价格变化', fontsize=14)
plt.legend(loc='lower right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(70, 140)
plt.ylim(0, 1)

# 保存图表
figure_path = 'delta_vs_spot_price.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
print(f"图表已保存为: {figure_path}")

# 计算特定条件下的delta值
S_specific = 110
sigma_specific = 0.276
delta_at_s110 = calculate_delta(S_specific, K, T, r, sigma_specific)

print(f"\n标的=110, 波动率=27.6%时的delta: {delta_at_specific:.6f}")

# 按要求构建结果字典
result = {
    'delta_at_s110': delta_at_specific,
    'figure_path': os.path.abspath(figure_path)
}

print(f"\n结果字典已创建:")
print(f"delta_at_s110: {result['delta_at_s110']}")
print(f"figure_path: {result['figure_path']}")

plt.show()
