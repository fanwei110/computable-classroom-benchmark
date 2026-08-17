import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# 1. 参数设置
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 到期时间(年)
S_min = 70        # 标的资产价格范围下限
S_max = 140       # 标的资产价格范围上限
vols = [0.15, 0.276, 0.40]  # 三条曲线的波动率

# 2. Black-Scholes 欧式看涨期权 Delta 计算函数
def bs_call_delta(S, K, r, T, vol):
    """
    S: 标的资产价格 (可以是数组)
    K: 行权价
    r: 无风险利率
    T: 到期时间
    vol: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    return norm.cdf(d1)

# 3. 生成标的价格序列及计算对应的 Delta
S = np.linspace(S_min, S_max, 500)

# 4. 绘图
plt.figure(figsize=(10, 6), dpi=120)
for vol in vols:
    delta = bs_call_delta(S, K, r, T, vol)
    plt.plot(S, delta, label=f'Vol = {vol*100}%')

plt.title('Delta Curve (Call Option)', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图表
fig_path = os.path.join(os.getcwd(), 'delta_curve.png')
plt.savefig(fig_path)
plt.close()

# 5. 计算特定点的 Delta: 标的110, vol 27.6%
target_S = 110
target_vol = 0.276
delta_at_s110 = bs_call_delta(target_S, K, r, T, target_vol)

# 6. 按照输出契约存入字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': fig_path
}

# 打印结果以供查看
print(f"标的110, Vol 27.6% 的 Delta 值为: {result['delta_at_s110']:.6f}")
print(f"图表已保存至: {result['figure_path']}")
print(f"Result Dictionary: {result}")
