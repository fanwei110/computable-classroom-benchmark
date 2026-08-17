import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 参数设置
K = 97.5
r = 0.043
T = 0.58
S_range = np.linspace(70, 140, 500)
vols = [0.15, 0.276, 0.40]

# 计算看涨期权 Delta 的函数
def delta_call(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 绘制 Delta 曲线
plt.figure(figsize=(10, 6))
for vol in vols:
    delta = delta_call(S_range, K, r, T, vol)
    plt.plot(S_range, delta, label=f'σ = {vol*100:.1f}%')

plt.xlabel('标的价格')
plt.ylabel('Delta')
plt.title('看涨期权 Delta 曲线')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path)
plt.close()

# 计算指定点的 Delta
S_target = 110
vol_target = 0.276
delta_target = delta_call(S_target, K, r, T, vol_target)

# 存入结果字典
result = {
    'delta_at_s110': delta_target,
    'figure_path': figure_path
}

result
