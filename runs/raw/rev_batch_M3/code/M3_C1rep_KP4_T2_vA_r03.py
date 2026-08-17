import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ================= 基础参数设置 =================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 4.3%
T = 0.58          # 剩余期限 0.58年
S_min = 70        # 标的价格范围下限
S_max = 140       # 标的价格范围上限

# 可调的波动率参数列表（在此修改即可调整图中的线条）
sigmas = [0.15, 0.276, 0.40]

# ================= Black-Scholes 计算 =================
def calc_d1(S, K, r, sigma, T):
    """计算BSM模型中的d1"""
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def calc_call_delta(S, K, r, sigma, T):
    """计算看涨期权的Delta"""
    d1 = calc_d1(S, K, r, sigma, T)
    return norm.cdf(d1)

# 1. 计算标的等于110、波动率27.6%时的delta
target_S = 110
target_sigma = 0.276
delta_at_s110 = calc_call_delta(target_S, K, r, target_sigma, T)

# 2. 绘制Delta随标的价格变化图
S_range = np.linspace(S_min, S_max, 500)

plt.figure(figsize=(10, 6))
for sigma in sigmas:
    deltas = calc_call_delta(S_range, K, r, sigma, T)
    plt.plot(S_range, deltas, label=f'Vol = {sigma*100:.1f}%')

# 图表格式设置
plt.title('Call Option Delta vs. Underlying Price', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axvline(x=K, color='grey', linestyle='--', linewidth=1, label=f'Strike = {K}')
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图表
figure_path = 'delta_vs_price.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 构建输出契约 =================
result = {
    'delta_at_s110': float(delta_at_s110),
    'figure_path': figure_path
}

# 打印结果（供查阅）
print(f"当标的=110、波动率=27.6%时的Delta值为: {result['delta_at_s110']:.4f}")
print(f"图表已保存至: {result['figure_path']}")
print(f"\nresult字典内容:\n{result}")
