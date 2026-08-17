import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (年化)
T = 0.58          # 剩余期限 (年)
S_min = 70        # 标的价格范围下限
S_max = 140       # 标的价格范围上限

# 波动率参数（可调列表，满足“做成可调参数”要求）
volatilities = [0.15, 0.276, 0.40]

# 特定计算要求
S_target = 110
sigma_target = 0.276

# ==================== 核心计算函数 ====================
def calculate_call_delta(S, K, T, r, sigma):
    """
    计算无分红欧式看涨期权的 Delta
    S: 标的价格 (可以是 numpy 数组)
    K: 行权价
    T: 剩余期限
    r: 无风险利率
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ==================== 计算特定点的 Delta ====================
delta_at_s110 = calculate_call_delta(S=S_target, K=K, T=T, r=r, sigma=sigma_target)

# ==================== 绘制 Delta 曲线 ====================
# 生成标的价格序列
S_range = np.linspace(S_min, S_max, 500)

plt.figure(figsize=(10, 6))

# 遍历波动率参数绘图
for sigma in volatilities:
    delta_curve = calculate_call_delta(S=S_range, K=K, T=T, r=r, sigma=sigma)
    # 图例格式化为百分比，保留一位小数（27.6% 则精确显示）
    label_str = f"Vol = {sigma*100:.1f}%" if sigma != 0.276 else f"Vol = {sigma*100:.1f}%"
    plt.plot(S_range, delta_curve, label=label_str)

# 图表装饰
plt.title('European Call Option Delta vs Underlying Price', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axhline(0, color='grey', linestyle='--', linewidth=0.8)
plt.axhline(1, color='grey', linestyle='--', linewidth=0.8)
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图表
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 输出契约 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以供验证
if __name__ == '__main__':
    print(f"标的110、波动率27.6%时的Delta: {result['delta_at_s110']:.6f}")
    print(f"图表已保存至: {result['figure_path']}")
