import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# ============================================================
# 可调参数
# ============================================================
STRIKE = 97.5                # 行权价 K
RISK_FREE_RATE = 0.043       # 无风险利率 (4.3% 每年)
MATURITY = 0.58              # 剩余到期时间 (年)
S_MIN = 70                   # 标的价格下限
S_MAX = 140                  # 标的价格上限
S_TARGET = 110               # 要求报告的标的价
SIGMA_TARGET = 0.276         # 报告时的波动率
# 三条波动率曲线（可在此增减或修改）
VOL_LIST = [0.15, 0.276, 0.40]

# ============================================================
# 函数定义
# ============================================================
def bs_call_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Delta (不分红)
    Delta = N(d1)
    """
    # 处理 sigma <= 0 或 T <= 0 的极端情况（本脚本不会出现）
    if sigma <= 0.0 or T <= 0.0:
        return np.where(S >= K, 1.0, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ============================================================
# 计算 Delta 并绘图
# ============================================================
S_range = np.linspace(S_MIN, S_MAX, 500)

plt.figure(figsize=(8, 5))
for sigma in VOL_LIST:
    delta = bs_call_delta(S_range, STRIKE, MATURITY, RISK_FREE_RATE, sigma)
    plt.plot(S_range, delta, label=f'σ = {sigma*100:.1f}%')

plt.xlabel('标的价格 S')
plt.ylabel('Delta')
plt.title(f'欧式看涨期权 Delta（K={STRIKE}, r={RISK_FREE_RATE*100:.1f}%, T={MATURITY} 年）')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# 保存图片
figure_path = os.path.abspath('delta_curves.png')
plt.savefig(figure_path, dpi=200)
plt.close()  # 释放内存

# ============================================================
# 报告特定点 Delta
# ============================================================
delta_at_s110 = bs_call_delta(S_TARGET, STRIKE, MATURITY, RISK_FREE_RATE, SIGMA_TARGET)
# 转为 Python float，避免 numpy 类型
delta_at_s110 = float(delta_at_s110)

# ============================================================
# 输出契约
# ============================================================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print("输出结果：")
print(f"  delta_at_s110 = {delta_at_s110:.6f}")
print(f"  figure_path   = {figure_path}")

# 如果以脚本方式运行，result 字典可在交互环境中检查
