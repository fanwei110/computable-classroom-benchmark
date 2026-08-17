import numpy as np
import matplotlib.pyplot as plt

# 债券参数
face_value = 100
coupon_rate = 0.046
maturity = 7
y0 = 0.053  # 初始收益率

# 现金流时间
t = np.arange(1, maturity + 1)
cash_flows = np.full(maturity, face_value * coupon_rate)
cash_flows[-1] += face_value

# ----- 计算需要输出的指标 -----
def bond_price(y):
    return np.sum(cash_flows / (1 + y) ** t)

P0 = bond_price(y0)
dy = 0.01  # 收益率变动幅度（100bp），这里做成可调变量
y_up = y0 + dy
P_up = bond_price(y_up)  # 精确价格

# 修正久期
macaulay_dur = np.sum(t * cash_flows / (1 + y0) ** t) / P0
modified_dur = macaulay_dur / (1 + y0)
dur_approx_change = -modified_dur * dy

# ----- 画图 -----
y_range = np.linspace(0.02, 0.09, 200)
P_exact = bond_price(y_range)
P_approx = P0 * (1 - modified_dur * (y_range - y0))  # 久期近似（切线）

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(y_range, P_exact, label='精确价格 (PV)', color='steelblue')
ax.plot(y_range, P_approx, label='久期近似 (切线)', color='darkorange', linestyle='--')
ax.axvline(y0, color='gray', linestyle=':', alpha=0.7)
ax.axvline(y_up, color='gray', linestyle=':', alpha=0.7)

# 标注收益率变动
ax.annotate(f'初始收益率 {y0*100:.2f}%', xy=(y0, P0),
            xytext=(y0-0.015, P0+2), arrowprops=dict(arrowstyle='->'))
ax.annotate(f'上调 {dy*100:.0f}bp 后 {y_up*100:.2f}%', xy=(y_up, P_up),
            xytext=(y_up+0.005, P_up+2), arrowprops=dict(arrowstyle='->'))

ax.set_xlabel('收益率')
ax.set_ylabel('价格')
ax.set_title('债券价格-收益率曲线（精确 vs. 久期近似）')
ax.legend()
ax.grid(True, alpha=0.3)

fig_path = './bond_price_curve.png'
fig.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ----- 最终输出字典 -----
result = {
    'price_at_up100bp': round(P_up, 6),
    'dur_approx_change_up100bp': round(dur_approx_change, 6),
    'figure_path': fig_path
}

result
