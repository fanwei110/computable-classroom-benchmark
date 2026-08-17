import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 可调参数：收益率变动幅度（单位：基点）
# ============================================================
YIELD_CHANGE_BP = 100             # 收益率上升 100 个基点
DELTA_Y = YIELD_CHANGE_BP / 10_000  # 转换成小数

# ============================================================
# 债券参数（假设：每年付息一次，面值 100，年票息率 4.6%）
# ============================================================
FACE = 100.0
COUPON_RATE = 0.046
MATURITY = 7                # 年
Y0 = 0.053                  # 当前到期收益率

C = FACE * COUPON_RATE      # 每年票息 = 4.6
T = np.arange(1, MATURITY + 1)  # 现金流发生时间（年）

# ============================================================
# 1. 定义精确价格函数（年复利）
# ============================================================
def exact_price(ytm):
    """计算给定到期收益率 ytm 下的债券全价"""
    pv_coupons = np.sum(C / (1 + ytm) ** T)
    pv_face = FACE / (1 + ytm) ** MATURITY
    return pv_coupons + pv_face

P0 = exact_price(Y0)         # 当前价格

# ============================================================
# 2. 计算麦考利久期与修正久期（在当前收益率处）
# ============================================================
# 各期现金流现值
pv_cf = C / (1 + Y0) ** T
pv_cf[-1] += FACE / (1 + Y0) ** MATURITY   # 最后一期加上本金

weights = pv_cf / P0                       # 权重
macaulay_duration = np.sum(T * weights)    # 麦考利久期
modified_duration = macaulay_duration / (1 + Y0)  # 修正久期

# ============================================================
# 3. 精确价格（收益率 +100 bp）与久期法估计的相对变化
# ============================================================
Y_UP = Y0 + DELTA_Y
P_up = exact_price(Y_UP)                              # 精确价格
dur_approx_rel_change = -modified_duration * DELTA_Y  # 久期法估计的相对价格变化（小数）

print(f"当前收益率 {Y0*100:.2f}% 下的债券价格：{P0:.6f}")
print(f"麦考利久期：{macaulay_duration:.4f} 年")
print(f"修正久期：{modified_duration:.4f}")
print(f"收益率上升 {YIELD_CHANGE_BP} bp 后的精确价格：{P_up:.6f}")
print(f"久期法估计的相对价格变化：{dur_approx_rel_change*100:.4f}%")

# ============================================================
# 4. 画图：精确价格-收益率曲线 + 当前收益率处的久期近似
# ============================================================
y_grid = np.linspace(0.02, 0.09, 200)          # 收益率从 2% 到 9%
p_exact = np.array([exact_price(y) for y in y_grid])

# 久期近似（一阶泰勒展开/切线）
p_approx = P0 * (1 - modified_duration * (y_grid - Y0))

plt.figure(figsize=(8, 5))
plt.plot(y_grid * 100, p_exact, label='精确价格', linewidth=2)
plt.plot(y_grid * 100, p_approx, '--', label='久期近似 (切线)', linewidth=2)
plt.axvline(Y0 * 100, color='gray', linestyle=':', label=f'当前收益率 {Y0*100:.1f}%')
plt.axvline(Y_UP * 100, color='red', linestyle=':', alpha=0.7,
            label=f'上升 {YIELD_CHANGE_BP} bp 后收益率 {Y_UP*100:.2f}%')
plt.xlabel('到期收益率 (%)')
plt.ylabel('债券价格')
plt.title('债券价格-收益率曲线与久期近似')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# 保存图像
fig_path = 'bond_price_duration.png'
plt.savefig(fig_path, dpi=150)
plt.close()
print(f"图形已保存至：{fig_path}")

# ============================================================
# 5. 输出字典
# ============================================================
result = {
    'price_at_up100bp': P_up,
    'dur_approx_change_up100bp': dur_approx_rel_change,
    'figure_path': fig_path
}

# 如果需要查看结果
for k, v in result.items():
    print(f"{k}: {v}")
