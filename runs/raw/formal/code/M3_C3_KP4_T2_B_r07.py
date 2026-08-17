import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ==================== 参数设置 ====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (连续复利)
T = 0.58          # 到期时间 (年)
S_min = 70        # 标的资产价格范围下限
S_max = 140       # 标的资产价格范围上限
vols = [0.15, 0.276, 0.40]  # 三条曲线的波动率

# 计算 S=110, vol=27.6% 时的特定 Delta
S_target = 110
vol_target = 0.276

# ==================== Black-Scholes Delta 计算公式 ====================
# 默认计算看涨期权 Delta
def calc_call_delta(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ==================== 绘制 Delta 曲线 ====================
S_range = np.linspace(S_min, S_max, 700)

plt.figure(figsize=(10, 6))
for vol in vols:
    delta_vals = calc_call_delta(S_range, K, r, T, vol)
    # 图例标好vol，vol作为参数可调
    plt.plot(S_range, delta_vals, label=f'Vol = {vol*100:.1f}%')

plt.title('Call Option Delta vs Underlying Price')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 计算特定点 Delta 并组装结果 ====================
delta_at_s110 = calc_call_delta(S_target, K, r, T, vol_target)

result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以供查看
print(f"标的价格110，波动率27.6%时的Delta为: {delta_at_s110:.6f}")
print(f"图片已保存至: {figure_path}")
print("Result字典内容:", result)
