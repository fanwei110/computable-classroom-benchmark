import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ============================================================
# Black-Scholes 公式与希腊字母
# ===========================================================-==============================
def bs_price(S, K, T, r, sigma, option_type='call'):
    """计算欧式看涨期权的BS价格"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price, d1, d2

def bs_delta(S, K, T, r, sigma, option_type='call'):
    """计算欧式期权的Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1

# ============================================================
# 参数设置
# =================================-=======================-
K = 97.5           # 行权价
r = 0.043          # 无风险利率
T = 0.58           # 剩余期限（年）
S0 = 110.0        # 标的当前价
sigmas = [0.15, 0.276, 0.40]  # 波动率（15%, 27.6%, 40%）

# 标的网格：从70到140
S_grid = np.linspace(70, 140, 200)

# ===========================================================-======================
# 1. 计算每个波动率下的 delta
# =================================-=======================-
plt.figure(figsize=(8, 5))

# 存储各波动率下的delta数据
delta_data = {}

for sigma in sigmas:
    deltas = bs_delta(S_grid, K, T, r, sigma)
    delta_data[sigma] = deltas
    plt.plot(S_grid, deltas, label=f'σ = {sigma*100:.1f}%')

# ============================================================
# 2. 画图与标注
# ===============================-=========================
plt.xlabel('标的价格 (S)')
plt.ylabel('Delta')
plt.title('欧式看涨期权 Delta 曲线 (参数化波动率)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图形
figure_path = 'delta_curves.png'
plt.savefig(figure_path, dpi=120)
plt.close()

# =======================================================-=====
# 3. 计算特定点：标的价格110，波动率27.6%
# ============================================================
sigma_target = 0.276
S_target = 110.0
delta_at_s110 = bs_delta(S_target, K, T, r, sigma_target)

# ============================================================
# 输出结果字典
# =========================-===============================
result = {
    'delta_at_s110': float(delta_at_s110),
    'figure_path': figure_path
}

print("=== 期权Delta计算结果 ===")
print(f"标的价格 = {S_target}，波动率 = {sigma_target*100}%")
print(f"Delta = {result['delta_at_s110']:.6f}")
print(f"图形已保存至：{result['figure_path']}")

# 打印验证信息
print("\n=== 所有波动率下的Delta曲线极值 ===")
for sigma, deltas in delta_data.items():
    print(f"σ={sigma*100:.1f}%: min delta={min(deltas):.4f}, max delta={max(deltas):.4f}")
