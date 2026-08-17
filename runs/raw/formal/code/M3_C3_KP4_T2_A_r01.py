import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ================= 可调参数 =================
# 波动率参数列表，可根据需要在此处调整（小数表示）
SIGMA_LIST = [0.15, 0.276, 0.40]  
# ==========================================

# 固定参数
K = 97.5         # 行权价
r = 0.043        # 连续复利无风险利率
T = 0.58         # 剩余期限（年）
S_range = np.linspace(70, 140, 700)  # 标的价格范围

# 计算Call Option Delta的函数
def calculate_call_delta(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 1. 计算标的等于110、波动率27.6%时的delta
S_target = 110
sigma_target = 0.276
delta_at_s110 = calculate_call_delta(S_target, K, r, T, sigma_target)

# 2. 画delta随标的价格变化的图
plt.figure(figsize=(10, 6))
for sigma in SIGMA_LIST:
    deltas = calculate_call_delta(S_range, K, r, T, sigma)
    plt.plot(S_range, deltas, label=f'σ = {sigma*100:.1f}%')

# 图表修饰
plt.title('Call Option Delta vs Underlying Price')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.axvline(x=110, color='gray', linestyle='--', alpha=0.5, label='S = 110 (Target)')
plt.legend()
plt.grid(True)

# 保存图表到文件
figure_path = 'delta_vs_underlying_price.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 3. 将所有要求的输出存入名为 `result` 的字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)  # 存入文件的绝对路径
}

# 打印结果以供验证
print(result)
