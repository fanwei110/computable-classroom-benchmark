import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数与假设 ====================
# 假设：每年付息一次（年付息债券）
FACE = 100.0               # 面值
COUPON_RATE = 0.046        # 票息率
COUPON = FACE * COUPON_RATE # 年票息 = 4.6
MATURITY = 7               # 期限（年）
Y0 = 0.053                 # 当前收益率
DY = 0.01                  # 收益率变动幅度（可调，此处为 100 bp）

# ==================== 函数定义 ====================
def bond_price(y):
    """计算给定收益率 y 下的债券价格"""
    t = np.arange(1, MATURITY + 1)
    cf = np.full(MATURITY, COUPON)
    cf[-1] += FACE                 # 最后一年还本
    return np.sum(cf / (1 + y) ** t)

# ==================== 当前价格与久期 ====================
P0 = bond_price(Y0)

# 现金流时间
t = np.arange(1, MATURITY + 1)
cf = np.full(MATURITY, COUPON)
cf[-1] += FACE

# 修正久期： D_mod = - (1/P) * dP/dy
dP_dy = -np.sum(t * cf / (1 + Y0) ** (t + 1))
D_mod = -dP_dy / P0

print(f"当前收益率: {Y0:.2%}")
print(f"当前价格: {P0:.4f}")
print(f"修正久期: {D_mod:.4f}")

# ==================== 价格-收益率曲线 ====================
y_grid = np.linspace(0.02, 0.09, 500)          # 2% 到 9%
prices_exact = np.array([bond_price(y) for y in y_grid])
prices_dur_approx = P0 * (1 - D_mod * (y_grid - Y0))  # 基于久期的切线近似

# ==================== +100 bp 情景 ====================
y_up = Y0 + DY
price_up_exact = bond_price(y_up)              # 精确价格
dur_rel_change = -D_mod * DY                   # 久期法估计的相对价格变化

print(f"\n收益率上升 {DY*100:.0f} bp 后:")
print(f"  精确价格: {price_up_exact:.4f}")
print(f"  久期法估计的相对价格变化: {dur_rel_change:.4%}")

# ==================== 绘图 ====================
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, prices_exact, label="精确价格", linewidth=2)
plt.plot(y_grid * 100, prices_dur_approx, "--", label="久期近似 (切线)", linewidth=1.5)
plt.axvline(Y0 * 100, color="gray", linestyle=":", alpha=0.7,
            label=f"当前收益率 {Y0*100:.1f}%")
plt.xlabel("收益率 (%)")
plt.ylabel("债券价格")
plt.title("债券价格–收益率曲线及久期近似")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
figure_path = "bond_price_yield.png"
plt.savefig(figure_path)
plt.show()

# ==================== 结果字典 ====================
result = {
    "price_at_up100bp": price_up_exact,
    "dur_approx_change_up100bp": dur_rel_change,
    "figure_path": figure_path
}

print("\n===== 最终结果 =====")
print(result)
