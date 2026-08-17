import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ----- 参数设置 -----
K = 97.5            # 行权价
r = 0.043           # 无风险利率
T = 0.58            # 剩余期限（年）
S = np.linspace(70, 140, 300)   # 标的价格范围
vols = [0.15, 0.276, 0.40]      # 三条波动率曲线

# ----- 计算看涨期权 Delta -----
def delta_call(S, K, r, sigma, T):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ----- 画图 -----
plt.figure(figsize=(10, 6))
for sigma in vols:
    plt.plot(S, delta_call(S, K, r, sigma, T),
             label=f'$\sigma$ = {sigma*100:.1f}%')
plt.xlabel('标的资产价格')
plt.ylabel('Delta')
plt.title('欧式看涨期权 Delta 曲线')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ----- 计算特定点 Delta（标的=110，波动率=27.6%）-----
S_target = 110
sigma_target = 0.276
delta_value = delta_call(S_target, K, r, sigma_target, T)

# ----- 输出契约 -----
result = {
    'delta_at_s110': delta_value,
    'figure_path': figure_path
}

print(result)
