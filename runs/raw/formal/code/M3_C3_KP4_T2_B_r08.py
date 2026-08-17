import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ========== 参数设置 ==========
K = 97.5             # 行权价
r = 0.043            # 无风险利率（连续复利）
T = 0.58             # 剩余期限（年）
S_min = 70           # 标的价格下界
S_max = 140          # 标的价格上界
vols = [0.15, 0.276, 0.40]  # 波动率列表（可在此处调整）

# ========== Black-Scholes 欧式看涨期权 Delta 计算函数 ==========
def call_delta(S, K, r, T, sigma):
    """计算欧式看涨期权的 Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ========== 计算标的110，波动率27.6%的Delta ==========
S_target = 110
vol_target = 0.276
delta_at_s110 = call_delta(S_target, K, r, T, vol_target)

# ========== 绘制 Delta 曲线 ==========
S_range = np.linspace(S_min, S_max, 700)

plt.figure(figsize=(10, 6))
for vol in vols:
    delta_vals = call_delta(S_range, K, r, T, vol)
    plt.plot(S_range, delta_vals, label=f'Vol = {vol*100:.1f}%')

plt.title('Call Option Delta Curve (K=97.5, r=4.3%, T=0.58)')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend(title='Volatility')
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ========== 封装输出结果 ==========
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果供查看
print(result)
