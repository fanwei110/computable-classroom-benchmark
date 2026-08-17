import numpy as np
import matplotlib.pyplot as plt

# ==================== 债券参数与现金流 ====================
face_value = 100.0           # 面值
coupon_rate = 0.046          # 票息率（年）
maturity = 7                 # 年限（年）
y0 = 0.053                   # 当前收益率（年复利）

# 现金流时间点 1..7 年
t = np.arange(1, maturity + 1, dtype=float)

# 票息现金流，最后一年加上面值
coupon = coupon_rate * face_value
cf = np.full(maturity, coupon)
cf[-1] += face_value  # 最后一年：票息 + 面值

# ==================== 债券定价函数 ====================
def bond_price(y):
    """返回给定收益率 y (小数) 下的债券价格"""
    return np.sum(cf / (1 + y) ** t)

# 当前价格
P0 = bond_price(y0)

# ==================== 久期与凸性 ====================
# 麦考利久期
mac_dur = np.sum(t * cf / (1 + y0) ** t) / P0
# 修正久期
mod_dur = mac_dur / (1 + y0)
# 凸性（年的平方）
conv = np.sum(t * (t + 1) * cf / (1 + y0) ** (t + 2)) / P0

# ==================== 精确价格-收益率曲线 ====================
y_grid = np.linspace(0.02, 0.09, 500)           # 收益率 2% 到 9%
price_exact = np.array([bond_price(y) for y in y_grid])

# 一阶近似（切线）: P ≈ P0 - D_mod * P0 * (y - y0)
price_approx1 = P0 - mod_dur * P0 * (y_grid - y0)

# 二阶近似（久期+凸性）: P ≈ P0 - D_mod * P0 * Δy + 0.5 * Conv * P0 * (Δy)^2
price_approx2 = (P0 - mod_dur * P0 * (y_grid - y0)
                 + 0.5 * conv * P0 * (y_grid - y0) ** 2)

# ==================== 情景分析：收益率上升 100 个基点 ====================
dy = 0.01                    # +100 bp
y_up = y0 + dy
price_up100bp = bond_price(y_up)                 # 精确价格
dur_approx_change = -mod_dur * dy                # 一阶相对价格变化（负数表示下跌）

# ==================== 绘图 ====================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(y_grid * 100, price_exact, label='精确价格曲线', color='black', linewidth=1.5)
ax.plot(y_grid * 100, price_approx1, '--', label='一阶久期近似（切线）', color='red', linewidth=1.2)
ax.plot(y_grid * 100, price_approx2, '-.', label='久期+凸性近似', color='blue', linewidth=1.2)

# 标记当前收益率点
ax.scatter([y0 * 100], [P0], color='green', zorder=5)
ax.annotate(f'当前 ({y0*100:.1f}%, {P0:.2f})', (y0 * 100, P0),
            textcoords="offset points", xytext=(10, -10), fontsize=9)

ax.set_xlabel('收益率 (%)')
ax.set_ylabel('价格')
ax.set_title('债券价格-收益率曲线及久期近似')
ax.legend()
ax.grid(True, linestyle=':', alpha=0.7)

# 保存图像
figure_path = 'bond_price_curve.png'
fig.tight_layout()
fig.savefig(figure_path, dpi=150)

# ==================== 输出结果字典 ====================
result = {
    'price_at_up100bp': round(price_up100bp, 6),
    'dur_approx_change_up100bp': round(dur_approx_change, 6),
    'figure_path': figure_path
}

# 可选：在控制台输出，方便课堂验证
if __name__ == "__main__":
    print("=== 债券定价与久期分析结果 ===")
    for k, v in result.items():
        print(f"{k}: {v}")
