import numpy as np
import matplotlib.pyplot as plt

# ---------- 债券参数 ----------
face_value = 100
coupon_rate = 0.046       # 4.6%
years = 7
ytm_initial = 0.053       # 5.3%

# ---------- 收益率变动幅度（可调参数） ----------
delta_y = 0.01            # 100个基点

# ---------- 工具函数：精确价格 ----------
def bond_price(face, coupon, maturity, y):
    """计算年付息债券的精确价格"""
    t = np.arange(1, maturity + 1)
    cash_flows = np.full(maturity, coupon * face)
    cash_flows[-1] += face
    pv = np.sum(cash_flows / (1 + y) ** t)
    return pv

# ---------- 工具函数：麦考利久期 & 修正久期 ----------
def macaulay_duration(face, coupon, maturity, y):
    price = bond_price(face, coupon, maturity, y)
    t = np.arange(1, maturity + 1)
    cash_flows = np.full(maturity, coupon * face)
    cash_flows[-1] += face
    pv_cf = cash_flows / (1 + y) ** t
    mac_dur = np.sum(t * pv_cf) / price
    return mac_dur

def modified_duration(face, coupon, maturity, y):
    mac_dur = macaulay_duration(face, coupon, maturity, y)
    return mac_dur / (1 + y)

# ---------- 计算 ----------
P0 = bond_price(face_value, coupon_rate, years, ytm_initial)
mod_dur = modified_duration(face_value, coupon_rate, years, ytm_initial)

# 收益率上升100个基点后的精确价格
y_up = ytm_initial + delta_y
P_up_exact = bond_price(face_value, coupon_rate, years, y_up)

# 用久期估算的相对价格变化（ΔP/P ≈ -ModDur * Δy）
dur_approx_change = -mod_dur * delta_y

# ---------- 准备画图数据 ----------
y_grid = np.linspace(0.02, 0.09, 500)   # 2% 到 9%
price_exact = bond_price(face_value, coupon_rate, years, y_grid)

# 久期近似切线： P_approx(y) = P0 - P0 * ModDur * (y - y0)
price_approx = P0 * (1 - mod_dur * (y_grid - ytm_initial))

# ---------- 画图 ----------
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, price_exact, label='精确价格 (Exact)', linewidth=2)
plt.plot(y_grid * 100, price_approx, '--', label='久期近似 (Duration Approx.)', linewidth=2)
plt.axvline(ytm_initial * 100, color='gray', linestyle=':', alpha=0.7)
plt.axhline(P0, color='gray', linestyle=':', alpha=0.7)
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.title('债券价格随收益率变化曲线 (精确 vs 久期近似)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
figure_path = 'bond_price_duration.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ---------- 存入结果字典 ----------
result = {
    'price_at_up100bp': P_up_exact,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': figure_path
}

# 输出结果
print(result)
