import numpy as np
import matplotlib
matplotlib.use('Agg')  # 无GUI后台保存图片
import matplotlib.pyplot as plt

# ---- 债券与市场参数 ----
face = 100.0
coupon_rate = 0.046   # 票息率4.6%
maturity = 7          # 期限7年
ytm0 = 0.053          # 当前YTM 5.3%
dy_bp = 100           # 变动幅度（可调）：基点
dy = dy_bp / 10000    # 转为小数，100bp = 0.01
y_range = np.linspace(0.02, 0.09, 200)  # 收益率范围2%至9%

# ---- 函数定义 ----
def bond_price(ytm):
    """计算年付息债券的精确价格"""
    pv = 0.0
    for t in range(1, maturity + 1):
        cf = coupon_rate * face if t < maturity else coupon_rate * face + face
        pv += cf / (1 + ytm) ** t
    return pv

def macaulay_duration(ytm):
    """麦考利久期"""
    P = bond_price(ytm)
    weighted_sum = 0.0
    for t in range(1, maturity + 1):
        cf = coupon_rate * face if t < maturity else coupon_rate * face + face
        weighted_sum += t * cf / (1 + ytm) ** t
    return weighted_sum / P

def modified_duration(ytm):
    """修正久期"""
    mac_dur = macaulay_duration(ytm)
    return mac_dur / (1 + ytm)

# ---- 计算核心数值 ----
P0 = bond_price(ytm0)                  # 当前精确价格
D_mod = modified_duration(ytm0)        # 修正久期

# 收益率+100bp精确价格
ytm_up = ytm0 + dy
P_up_exact = bond_price(ytm_up)

# 久期法估计的相对变化（ΔP/P）
approx_relative_change = -D_mod * dy

# ---- 画图 ----
prices_exact = np.array([bond_price(y) for y in y_range])
prices_dur_line = P0 - P0 * D_mod * (y_range - ytm0)  # 切线近似

plt.figure(figsize=(8, 5))
plt.plot(y_range * 100, prices_exact, label='Exact Price', linewidth=2)
plt.plot(y_range * 100, prices_dur_line, '--', label='Duration Approximation', linewidth=2)
plt.axvline(ytm0 * 100, color='gray', linestyle=':', alpha=0.7)
plt.axhline(P0, color='gray', linestyle=':', alpha=0.7)
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.title('Price-Yield Curve & Duration Approximation')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

fig_path = 'price_yield_curve.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# ---- 结果汇总 ----
result = {
    'price_at_up100bp': round(P_up_exact, 6),
    'dur_approx_change_up100bp': round(approx_relative_change, 6),
    'figure_path': fig_path
}

print(result)
