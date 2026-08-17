import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# 1. 参数设置
K = 97.5          # 行权价
r = 0.043         # 无风险利率 4.3%
T = 0.58          # 到期时间 0.58年
S_range = np.linspace(70, 140, 500) # 标的资产价格范围 70-140
vol_list = [0.15, 0.276, 0.40]      # 波动率列表(可在此处调整vol)

# 2. 定义Black-Scholes看涨期权Delta计算函数
def call_delta(S, K, r, T, vol):
    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    return norm.cdf(d1)

# 3. 绘制Delta曲线
plt.figure(figsize=(10, 6))
for vol in vol_list:
    deltas = call_delta(S_range, K, r, T, vol)
    plt.plot(S_range, deltas, label=f'Vol = {vol*100:.1f}%')

plt.title('Call Option Delta Curve (K=97.5, r=4.3%, T=0.58)')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.axvline(x=K, color='gray', linestyle='--', alpha=0.5, label='Strike Price (97.5)')
plt.legend()
plt.grid(True)

# 4. 保存图像
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 5. 计算特定点的Delta值：标的110，vol 27.6%
delta_at_s110 = call_delta(110, K, r, T, 0.276)

# 6. 按照输出契约构造结果字典
result = {
    'delta_at_s110': float(delta_at_s110),
    'figure_path': figure_path
}

# 打印结果以供验证
print(result)
