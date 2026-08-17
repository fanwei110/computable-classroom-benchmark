import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# =========================================================
# 可调参数区域
# =========================================================
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
S_min, S_max = 70, 140   # 标的价格范围
S_target = 110.0  # 需要报告的标的价格

# 波动率参数（可调）
sigma_list = [0.15, 0.276, 0.40]

# 绘图点数
num_points = 200

# =========================================================
# Black-Scholes 欧式看涨期权 Delta 函数
# 注意：题目未指定看涨/看跌，此处默认欧式看涨期权
#       Delta_call = N(d1)
# =========================================================
def delta_call(S, K, r, sigma, T):
    """返回欧式看涨期权的 Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# =========================================================
# 1. 对标的价格网格计算每条波动率对应的 Delta
# =========================================================
S_grid = np.linspace(S_min, S_max, num_points)

curves = {}
for sigma in sigma_list:
    curves[sigma] = delta_call(S_grid, K, r, sigma, T)

# =========================================================
# 2. 绘制三条曲线，图例标注波动率
# =========================================================
plt.figure(figsize=(8, 5))
for sigma in sigma_list:
    plt.plot(S_grid, curves[sigma], label=f'σ = {sigma*100:.1f}%')

plt.axvline(x=K, color='gray', linestyle='--', alpha=0.5, label=f'K = {K}')
plt.xlabel('标的价格')
plt.ylabel('Delta')
plt.title('欧式看涨期权 Delta vs 标的价格')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# 保存图形
fig_path = 'delta_vs_spot.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# =========================================================
# 3. 报告 S=110, σ=27.6% 时的 Delta
# =========================================================
sigma_report = 0.276
delta_value = delta_call(S_target, K, r, sigma_report, T)

# =========================================================
# 4. 组装 result 字典
# =========================================================
result = {
    'delta_at_s110': delta_value,
    'figure_path': fig_path
}

# 输出到控制台以供查看（仅用于演示，不会影响变量赋值）
if __name__ == '__main__':
    print(f"Delta at S={S_target}, σ={sigma_report*100:.1f}%: {delta_value:.6f}")
    print(f"Figure saved to: {fig_path}")
