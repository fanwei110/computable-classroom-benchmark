import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd  # 按题目要求导入，备用

# ========================
# 参数设置
# ========================
K = 97.5             # 行权价
r = 0.043            # 无风险利率（4.3%）
T = 0.58             # 剩余到期时间（年）
q = 0.0              # 股息率（不分红）

# 波动率参数 —— 可调参数区域
sigmas = [0.15, 0.276, 0.40]   # 对应 15%, 27.6%, 40%

# 标的价格网格
S_min, S_max = 70.0, 140.0
S = np.linspace(S_min, S_max, 500)

# ========================
# Delta 计算函数（Black-Scholes 欧式看涨）
# ========================
def delta_call(S, K, r, q, T, sigma):
    """
    计算欧式看涨期权的 Delta
    Δ = N(d1)
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ========================
# 1. & 2. 绘图
# ========================
plt.figure(figsize=(10, 6))

for sigma in sigmas:
    delta = delta_call(S, K, r, q, T, sigma)
    plt.plot(S, delta, linewidth=2, label=f'$\sigma$ = {sigma*100:.1f}%')

plt.xlabel('标的价格 S')
plt.ylabel('Delta $\Delta$')
plt.title('欧式看涨期权 Delta 曲线 (Black-Scholes)\n'
          f'K = {K},  r = {r*100:.1f}%,  T = {T} 年,  无分红')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# 保存图片到当前目录
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ========================
# 3. 报告特定点的 Delta
# ========================
S_specific = 110.0
sigma_specific = 0.276
delta_at_s110 = delta_call(S_specific, K, r, q, T, sigma_specific)

# ========================
# 输出契约
# ========================
result = {
    'delta_at_s110': delta_at_s110,   # float
    'figure_path': figure_path        # str
}

if __name__ == '__main__':
    print("结果字典：")
    print(result)
    print(f"\n标的=110、波动率=27.6% 时的 Delta = {delta_at_s110:.6f}")
