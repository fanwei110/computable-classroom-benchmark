import numpy as np
import matplotlib.pyplot as plt

# ============================
# 参数设定 (可根据需要调整)
# ============================
FACE = 100.0             # 面值
COUPON_RATE = 0.046      # 票面利率（年化）
MATURITY = 7             # 剩余期限（年）
YTM0 = 0.053             # 当前到期收益率
SHIFT_BP = 100           # 收益率变动幅度（基点），可调

# 内部假设：每年付息一次，现金流发生在年末
C = FACE * COUPON_RATE   # 每期票息 = 4.6

# ============================
# 定价与风险指标函数
# ============================
def price(ytm):
    """精确债券价格（年付息）"""
    t = np.arange(1, MATURITY + 1)
    pv_coupons = np.sum(C / (1 + ytm) ** t)
    pv_face = FACE / (1 + ytm) ** MATURITY
    return pv_coupons + pv_face

def macaulay_duration(ytm):
    """麦考利久期"""
    p = price(ytm)
    t = np.arange(1, MATURITY + 1)
    pv_coupons = C / (1 + ytm) ** t
    pv_face = FACE / (1 + ytm) ** MATURITY
    weighted_sum = np.sum(t * pv_coupons) + MATURITY * pv_face
    return weighted_sum / p

def modified_duration(ytm):
    """修正久期"""
    return macaulay_duration(ytm) / (1 + ytm)

# ============================
# 计算当前价格、修正久期
# ============================
P0 = price(YTM0)
MD = modified_duration(YTM0)

# ============================
# 1. 精确价格曲线 (2% ~ 9% 收益率网格)
# ============================
y_grid = np.linspace(0.02, 0.09, 200)
prices_exact = np.array([price(y) for y in y_grid])

# ============================
# 2. 久期近似曲线
# ============================
# 近似价格： P_approx = P0 * (1 - MD * (y - YTM0))
prices_approx = P0 * (1 - MD * (y_grid - YTM0))

# ============================
# 3. 收益率上升100bp 的精确价格与久期估计的相对变化
# ============================
delta_y = SHIFT_BP / 10000.0             # 100bp = 0.01
price_up100bp = price(YTM0 + delta_y)     # 精确价格
dur_approx_change = -MD * delta_y         # 久期估计的相对价格变化 (ΔP/P)

# ============================
# 4. 绘图并保存
# ============================
plt.figure(figsize=(8, 5))
plt.plot(y_grid * 100, prices_exact, label="精确价格 (精确定价)")
plt.plot(y_grid * 100, prices_approx, '--', label="久期近似 (久期线性近似)")
plt.axvline(YTM0 * 100, color='gray', linestyle=':', alpha=0.7, label=f"当前收益率 {YTM0*100:.2f}%")
plt.xlabel("收益率 (%)")
plt.ylabel("价格")
plt.title("债券价格-收益率曲线 (精确 vs 久期近似)")
plt.legend()
plt.grid(True, alpha=0.3)

figure_path = "price_yield_curve.png"
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ============================
# 结果汇总
# ============================
result = {
    "price_at_up100bp": round(price_up100bp, 6),
    "dur_approx_change_up100bp": round(dur_approx_change, 6),
    "figure_path": figure_path
}

print("====== 计算结果 ======")
print(f"当前收益率 (YTM0): {YTM0*100:.2f}%")
print(f"当前价格 (P0): {P0:.6f}")
print(f"修正久期 (MD): {MD:.6f}")
print(f"收益率上升 {SHIFT_BP} bp 后:")
print(f"  精确价格: {result['price_at_up100bp']:.6f}")
print(f"  久期估计的相对变化: {result['dur_approx_change_up100bp']:.6f} ({result['dur_approx_change_up100bp']*100:.4f}%)")
print(f"图形已保存至: {result['figure_path']}")
print("=======================")

# result 字典可供教师后续调用
