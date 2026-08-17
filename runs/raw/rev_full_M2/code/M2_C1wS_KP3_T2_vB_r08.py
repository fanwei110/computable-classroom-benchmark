import numpy as np
import matplotlib.pyplot as plt
import os

# ============================
# 债券参数与假设
# ============================
FACE = 100.0          # 面值
COUPON_RATE = 0.046   # 票息率 4.6%
T = 7                 # 期限（年）
YTM0 = 0.053          # 初始到期收益率 5.3%
SHIFT_BP = 100        # 收益率变动幅度（基点），可调
DELTA_Y = SHIFT_BP / 10_000  # 转换为小数

# 付息频率假设：每年一次
FREQ = 1
PERIODS = T * FREQ
coupon = FACE * COUPON_RATE / FREQ

# ============================
# 定价函数与风险指标
# ============================
def bond_price(ytm):
    """计算债券的精确价格（全价）"""
    disc = (1 + ytm / FREQ) ** np.arange(1, PERIODS + 1)
    pv_coupons = coupon / disc
    pv_face = FACE / (1 + ytm / FREQ) ** PERIODS
    return np.sum(pv_coupons) + pv_face

def bond_duration_convexity(ytm):
    """计算麦考利久期、修正久期和凸性"""
    disc = (1 + ytm / FREQ) ** np.arange(1, PERIODS + 1)
    pv_c = coupon / disc
    pv_face = FACE / (1 + ytm / FREQ) ** PERIODS
    price = np.sum(pv_c) + pv_face

    # 权重：各现金流现值占总价格的比例
    w_c = pv_c / price
    w_face = pv_face / price

    # 时间点（年）
    t = np.arange(1, PERIODS + 1) / FREQ

    # 麦考利久期
    mac_dur = np.sum(t * w_c) + T * w_face
    # 修正久期
    mod_dur = mac_dur / (1 + ytm / FREQ)
    # 凸性
    convex = np.sum(t * (t + 1/FREQ) * w_c) + T * (T + 1/FREQ) * w_face
    convex /= (1 + ytm / FREQ)**2

    return mac_dur, mod_dur, convex

# ============================
# 当前债券（YTM0=5.3%）的指标
# ============================
price0 = bond_price(YTM0)
mac_dur0, mod_dur0, convex0 = bond_duration_convexity(YTM0)

# ============================
# 收益率曲线：2% 到 9%
# ============================
yields = np.linspace(0.02, 0.09, 200)  # 200个点保证平滑
prices_exact = np.array([bond_price(y) for y in yields])

# 切线近似：P(y) ≈ P0 + dP/dy * (y - YTM0)
# dP/dy = -修正久期 * P0
dPdy = -mod_dur0 * price0
prices_tangent = price0 + dPdy * (yields - YTM0)

# ============================
# +100bp 时的精确价格与久期法估计
# ============================
ytm_up = YTM0 + DELTA_Y
price_up_exact = bond_price(ytm_up)
# 久期近似相对变化 ΔP/P ≈ -修正久期 * Δy
delta_p_ratio_dur = -mod_dur0 * DELTA_Y
# 近似价格
price_up_dur = price0 * (1 + delta_p_ratio_dur)

# 相对变化率输出为小数（例如 -0.05 表示 -5%）
dur_approx_change = delta_p_ratio_dur

# ============================
# 绘图
# ============================
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yields * 100, prices_exact, 'b-', linewidth=2, label='精确价格 (全价)')
ax.plot(yields * 100, prices_tangent, 'r--', linewidth=1.5, label='久期近似 (切线)')

# 标记初始点
ax.plot(YTM0 * 100, price0, 'ko', markersize=6, label=f'当前 YTM={YTM0*100:.2f}%')
# 标记 +100bp 的点
ax.plot(ytm_up * 100, price_up_exact, 'bs', markersize=8, label=f'+{SHIFT_BP}bp 精确价格')
ax.plot(ytm_up * 100, price_up_dur, 'r^', markersize=8, label=f'+{SHIFT_BP}bp 久期近似')

ax.set_xlabel('到期收益率 (%)', fontsize=12)
ax.set_ylabel('债券价格', fontsize=12)
ax.set_title('债券价格-收益率曲线 (面值100, 票息4.6%, 7年)', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# 添加说明文本
textstr = f'当前 YTM={YTM0*100:.2f}%\n修正久期={mod_dur0:.4f}\n凸性={convex0:.4f}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

# 保存图形
output_dir = os.getcwd()
figure_filename = 'bond_price_curve.png'
figure_path = os.path.join(output_dir, figure_filename)
fig.tight_layout()
fig.savefig(figure_path, dpi=150)
plt.close(fig)  # 避免在非交互环境中显示

# ============================
# 填充结果字典
# ============================
result = {
    'price_at_up100bp': round(price_up_exact, 4),
    'dur_approx_change_up100bp': round(dur_approx_change, 6),
    'figure_path': figure_path
}

# 输出以验证
if __name__ == '__main__':
    print("债券定价与久期分析结果：")
    print(f"初始价格 (YTM={YTM0*100:.2f}%): {price0:.4f}")
    print(f"修正久期: {mod_dur0:.4f}")
    print(f"凸性: {convex0:.4f}")
    print(f"收益率+{SHIFT_BP}bp后精确价格: {price_up_exact:.4f}")
    print(f"久期法估计相对变化: {dur_approx_change*100:.4f}%")
    print(f"图形保存至: {figure_path}")
    print("结果字典:", result)
