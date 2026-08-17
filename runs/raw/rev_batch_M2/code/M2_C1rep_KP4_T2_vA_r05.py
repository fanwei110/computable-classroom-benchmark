import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# ========== 可调参数 ==========
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余年限
S_min, S_max = 70, 140   # 标的价格范围
volatility_list = [0.15, 0.276, 0.40]   # 波动率参数（可任意调整）
S_target = 110    # 需要报告 delta 的标的价格
sigma_target = 0.276  # 对应的波动率
# =============================

# 生成标的价格序列
S = np.linspace(S_min, S_max, 300)

# 绘图
plt.figure(figsize=(10, 6))
for sigma in volatility_list:
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta_call = norm.cdf(d1)
    plt.plot(S, delta_call, label=f'σ = {sigma*100:.1f}%')

plt.xlabel('Spot Price')
plt.ylabel('Delta (Call)')
plt.title('Call Option Delta vs Spot Price')
plt.grid(True)
plt.legend()
plt.tight_layout()

# 保存图片
figure_path = os.path.abspath('delta_vs_spot.png')
plt.savefig(figure_path, dpi=150)
plt.close()

# 计算指定点的delta
d1_target = (np.log(S_target / K) + (r + 0.5 * sigma_target**2) * T) / (sigma_target * np.sqrt(T))
delta_at_target = norm.cdf(d1_target)

# 构建结果字典
result = {
    'delta_at_s110': delta_at_target,
    'figure_path': figure_path
}

# 输出结果（供查看）
print(result)
