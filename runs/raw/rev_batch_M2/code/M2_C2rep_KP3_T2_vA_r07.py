import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 可调参数：收益率变动幅度（基点）
# ============================================================
yield_change_bps = 100          # 基点，可改为其他值
delta_y = yield_change_bps / 10000  # 转换为小数 (例如 100bp -> 0.01)

# ============================================================
# 债券基本参数
# ============================================================
face_value = 100.0             # 面值
coupon_rate = 0.046            # 票息率（年化）
maturity = 7                   # 剩余期限（年）
current_yield = 0.053          # 当前到期收益率

# 现金流：每年付息一次，最后一期还本
coupon = face_value * coupon_rate
t = np.arange(1, maturity + 1)          # 现金流发生时间（年）
cash_flows = np.full(maturity, coupon)
cash_flows[-1] += face_value            # 最后一期加上本金

def bond_price(ytm):
    """计算精确价格"""
    discount = (1 + ytm) ** t
    pv = cash_flows / discount
    return np.sum(pv)

def macaulay_duration(ytm):
    """计算麦考利久期"""
    pv = cash_flows / (1 + ytm) ** t
    price = np.sum(pv)
    weighted_times = t * pv
    return np.sum(weighted_times) / price

def modified_duration(ytm):
    """计算修正久期（年复利）"""
    mac_dur = macaulay_duration(ytm)
    return mac_dur / (1 + ytm)

# ============================================================
# 在当前收益率 5.3% 处计算价格和修正久期
# ============================================================
P0 = bond_price(current_yield)
mod_dur = modified_duration(current_yield)

# ============================================================
# 生成收益率网格（2% 至 9%）
# ============================================================
yield_grid = np.linspace(0.02, 0.09, 200)   # 200个点使曲线平滑
exact_prices = np.array([bond_price(y) for y in yield_grid])

# 基于久期的近似：P_approx(y) = P0 * (1 - mod_dur * (y - y0))
approx_prices = P0 * (1 - mod_dur * (yield_grid - current_yield))

# ============================================================
# 计算 +100bp 情形（可调）
# ============================================================
y_up = current_yield + delta_y
price_up_exact = bond_price(y_up)

# 久期法估计的相对价格变化
# (P_approx - P0) / P0 = -mod_dur * delta_y
dur_approx_rel_change = -mod_dur * delta_y

# ============================================================
# 画图
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(yield_grid * 100, exact_prices, label='Exact Price', linewidth=2)
ax.plot(yield_grid * 100, approx_prices, '--', label='Duration Approximation', linewidth=2)
ax.axvline(current_yield * 100, color='gray', linestyle=':', alpha=0.7)
ax.set_xlabel('Yield to Maturity (%)')
ax.set_ylabel('Bond Price')
ax.set_title('Price–Yield Curve (7-Year 4.6% Coupon Bond)')
ax.legend()
ax.grid(True, alpha=0.3)

# 保存图片
figure_filename = 'price_yield_curve.png'
fig.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close(fig)

# ============================================================
# 汇总结果
# ============================================================
result = {
    'price_at_up100bp': round(price_up_exact, 6),
    'dur_approx_change_up100bp': round(dur_approx_rel_change, 6),
    'figure_path': figure_filename
}

# 可选：打印输出，方便教师查看
print("Result dictionary:")
for k, v in result.items():
    print(f"  {k}: {v}")
