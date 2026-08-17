import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 参数设定
K = 97.5                # 行权价
r = 0.043               # 无风险利率（连续复利，小数形式）
T = 0.58                # 剩余期限（年）
S_min = 70.0            # 标的资产价格下限
S_max = 140.0           # 标的资产价格上限
num_points = 500        # 标的资产价格网格点数
S_grid = np.linspace(S_min, S_max, num_points)

# 波动率参数（可调节）
volatilities = [0.15, 0.276, 0.40]  # 分别对应 15%, 27.6%, 40%

def black_scholes_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权的Delta（连续复利，不分红）
    公式：Delta = N(d1)
    d1 = [ln(S/K) + (r + 0.5*sigma^2)*T] / (sigma * sqrt(T))
    """
    if sigma <= 0 or T <= 0 or S <= 0:
        return np.nan
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# 创建图形
plt.figure(figsize=(10, 6))

# 对每个波动率计算并绘制Delta曲线
for sigma in volatilities:
    delta_values = black_scholes_delta(S_grid, K, T, r, sigma)
    plt.plot(S_grid, delta_values, linewidth=2, label=f'σ = {sigma*100:.1f}%')

# 特定点计算：标的=110，波动率=27.6%
S_target = 110.0
sigma_target = 0.276
delta_at_s110 = black_scholes_delta(S_target, K, T, r, sigma_target)

# 在图中标注特定点
plt.scatter(S_target, delta_at_s110, color='red', s=80, zorder=5,
            label=f'Spot 110, σ=27.6%\nDelta = {delta_at_s110:.4f}')
plt.axvline(x=S_target, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=delta_at_s110, color='gray', linestyle='--', alpha=0.5)

# 图形美化
plt.xlabel('标的资产价格', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.title('欧式看涨期权 Delta 曲线 (Black-Scholes)\n'
          f'行权价 K={K}, 无风险利率 r={r*100:.1f}%, 剩余期限 T={T} 年',
          fontsize=13)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(S_min, S_max)
plt.ylim(0, 1.05)

# 保存图形
figure_path = 'delta_curves_volatility.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 输出结果存入字典
result = {
    'delta_at_s110': round(delta_at_s110, 6),
    'figure_path': figure_path
}

# 即时输出（供课堂查看）
print("=== 计算结果 ===")
print(f"标的资产价格 110，波动率 27.6% 时的 Delta = {result['delta_at_s110']:.6f}")
print(f"图形已保存至：{result['figure_path']}")
print("\n=== 结果字典 ===")
print(result)

# 显示图形（如果交互式环境）
# plt.show()
