import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# ========== 债券参数定义 ==========
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity = 7.0              # 期限 7年
initial_ytm = 0.053         # 初始YTM 5.3%
coupon = face_value * coupon_rate  # 每期票息

# ========== 现金流时间 ==========
# 假设每年付息一次
cash_flow_times = np.arange(1, maturity + 1)  # 1, 2, ..., 7年
cash_flows = np.full(int(maturity), coupon)
cash_flows[-1] += face_value  # 最后一期加上本金

# ========== 1. 计算精确价格函数 ==========
def bond_price_exact(ytm):
    """计算债券的精确价格（现金流贴现）"""
    pv = np.sum(cash_flows / (1 + ytm) ** cash_flow_times)
    return pv

# ========== 2. 计算久期和凸性 ==========
def bond_duration_convexity(ytm):
    """计算麦考利久期、修正久期和凸性"""
    pv = cash_flows / (1 + ytm) ** cash_flow_times
    price = np.sum(pv)
    
    # 麦考利久期
    mac_duration = np.sum(cash_flow_times * pv) / price
    
    # 修正久期
    mod_duration = mac_duration / (1 + ytm)
    
    # 凸性
    convexity = np.sum(cash_flow_times * (cash_flow_times + 1) * pv) / (price * (1 + ytm)**2)
    
    return mod_duration, convexity

# ========== 3. 计算初始点的价格和久期 ==========
price_at_initial = bond_price_exact(initial_ytm)
mod_duration, convexity = bond_duration_convexity(initial_ytm)

print(f"初始YTM: {initial_ytm*100:.2f}%")
print(f"精确价格: {price_at_initial:.4f}")
print(f"修正久期: {mod_duration:.4f}")
print(f"凸性: {convexity:.4f}")

# ========== 4. 收益率网格 2%到9% ==========
ytm_grid = np.linspace(0.02, 0.09, 200)
exact_prices = np.array([bond_price_exact(y) for y in ytm_grid])

# 久期近似：P(y) ≈ P(y0) * [1 - D_mod * (y - y0)]
dur_approx_prices = price_at_initial * (1 - mod_duration * (ytm_grid - initial_ytm))

# 久期+凸性近似：P(y) ≈ P(y0) * [1 - D_mod*(y-y0) + 0.5*C*(y-y0)^2]
dur_conv_approx_prices = price_at_initial * (1 - mod_duration * (ytm_grid - initial_ytm) 
                                              + 0.5 * convexity * (ytm_grid - initial_ytm)**2)

# ========== 5. +100bp 冲击分析 ==========
ytm_up100bp = initial_ytm + 0.01  # +100个基点

# 精确价格
price_up100bp_exact = bond_price_exact(ytm_up100bp)

# 久期法估计的价格变化
price_change_duration = -mod_duration * price_at_initial * 0.01
price_up100bp_duration = price_at_initial + price_change_duration

# 相对变化（百分比）
exact_relative_change = (price_up100bp_exact - price_at_initial) / price_at_initial * 100
duration_relative_change = price_change_duration / price_at_initial * 100

print(f"\n===== +100bp 冲击分析 =====")
print(f"新YTM: {ytm_up100bp*100:.2f}%")
print(f"精确价格: {price_up100bp_exact:.4f}")
print(f"久期法估计价格: {price_up100bp_duration:.4f}")
print(f"精确相对变化: {exact_relative_change:.4f}%")
print(f"久期法估计相对变化: {duration_relative_change:.4f}%")

# ========== 6. 绘制图形 ==========
fig, ax = plt.subplots(figsize=(12, 8))

# 精确价格曲线
ax.plot(ytm_grid * 100, exact_prices, 'b-', linewidth=2.5, label='精确价格（现金流贴现）', alpha=0.9)

# 久期近似曲线（仅久期）
ax.plot(ytm_grid * 100, dur_approx_prices, 'r--', linewidth=2, label='久期近似（切线）', alpha=0.8)

# 久期+凸性近似曲线
ax.plot(ytm_grid * 100, dur_conv_approx_prices, 'g-.', linewidth=2, label='久期+凸性近似', alpha=0.8)

# 标记初始YTM点
ax.axvline(x=initial_ytm*100, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax.plot(initial_ytm*100, price_at_initial, 'ko', markersize=8, label=f'初始点 (YTM={initial_ytm*100:.1f}%)')

# 标记+100bp点
ax.axvline(x=ytm_up100bp*100, color='orange', linestyle=':', alpha=0.5, linewidth=1)
ax.plot(ytm_up100bp*100, price_up100bp_exact, 'rs', markersize=8, label=f'+100bp精确价格')
ax.plot(ytm_up100bp*100, price_up100bp_duration, 'bd', markersize=8, label=f'+100bp久期估计')

# 添加箭头和标注（可调整变动幅度）
shift_amount = 0.01  # 可调整的变动幅度（100bp）
ax.annotate(f'Δy = +{shift_amount*100:.0f}bp',
            xy=(ytm_up100bp*100, price_up100bp_exact),
            xytext=(ytm_up100bp*100 + 0.5, price_up100bp_exact + 2),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5),
            fontsize=11, color='darkred')

ax.set_xlabel('到期收益率 (%)', fontsize=14)
ax.set_ylabel('债券价格', fontsize=14)
ax.set_title('债券价格-收益率曲线：精确定价 vs 久期近似\n'
             rf'(面值={face_value}, 票息={coupon_rate*100}%, 期限={maturity}年, 初始YTM={initial_ytm*100}%)',
             fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim([1.5, 9.5])

# 添加文本信息框
textstr = f'修正久期: {mod_duration:.4f}\n凸性: {convexity:.4f}\n初始价格: {price_at_initial:.2f}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
print(f"\n图形已保存至: {figure_path}")

# ========== 7. 填充结果字典 ==========
result = {
    'price_at_up100bp': round(price_up100bp_exact, 6),
    'dur_approx_change_up100bp': round(duration_relative_change, 6),
    'figure_path': os.path.abspath(figure_path)
}

print("\n===== 结果字典 =====")
print(result)

plt.show()
