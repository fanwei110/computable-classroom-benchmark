import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# 计算d1
def calculate_d1(S, K, r, sigma, T):
    return (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))

# 计算看涨期权delta
def call_delta(S, K, r, sigma, T):
    d1 = calculate_d1(S, K, r, sigma, T)
    return norm.cdf(d1)

# 参数设置
K = 97.5  # 行权价
r = 0.043  # 无风险利率
T = 0.58  # 到期时间
S_range = np.linspace(70, 140, 500)  # 标的价格范围

# 波动率列表
vol_list = [0.15, 0.276, 0.40]
vol_labels = ['15%', '27.6%', '40%']

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制三条delta曲线
for vol, label in zip(vol_list, vol_labels):
    delta_values = call_delta(S_range, K, r, vol, T)
    plt.plot(S_range, delta_values, linewidth=2, label=f'Vol = {label}')

# 标出S=110, vol=27.6%的点
delta_at_s110 = call_delta(110, K, r, 0.276, T)
plt.scatter(110, delta_at_s110, color='red', s=100, zorder=5, 
            label=f'S=110, Vol=27.6%, Δ={delta_at_s110:.4f}')
plt.plot([70, 110], [delta_at_s110, delta_at_s110], 'r--', linewidth=0.8, alpha=0.6)
plt.plot([110, 110], [0, delta_at_s110], 'r--', linewidth=0.8, alpha=0.6)

# 添加图例和标签
plt.xlabel('标的价格 (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.title('看涨期权Delta曲线 (K=97.5, r=4.3%, T=0.58)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(loc='lower right', fontsize=10)
plt.xlim(70, 140)
plt.ylim(0, 1)

# 保存图形
figure_path = os.path.join(os.getcwd(), 'delta_curve.png')
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 存入结果字典
result = {
    'delta_at_s110': round(delta_at_s110, 6),
    'figure_path': figure_path
}

print(f"Delta at S=110, Vol=27.6%: {result['delta_at_s110']:.6f}")
print(f"Figure saved to: {result['figure_path']}")
