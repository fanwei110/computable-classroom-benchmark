import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 债券参数与假设设定
# ==========================================
# 假设：采用每年付息一次的离散复利计算方式，这在《证券投资学》基础教学中最为标准。
Face_Value = 100.0          # 面值
Coupon_Rate = 0.046         # 票息率 4.6%
Maturity = 7                # 期限 7年
YTM_0 = 0.053              # 初始到期收益率 5.3%
Delta_Y = 0.01             # 可调变动幅度：100bp (0.01)

# 现金流构造
times = np.arange(1, Maturity + 1)
cash_flows = np.full(Maturity, Face_Value * Coupon_Rate)
cash_flows[-1] += Face_Value # 最后一期加入本金

# ==========================================
# 核心计算函数：精确价格、久期
# ==========================================
def bond_price(ytm, cfs, ts):
    """计算债券精确价格"""
    return np.sum(cfs / (1 + ytm)**ts)

def macaulay_duration(ytm, cfs, ts):
    """计算麦考利久期"""
    price = bond_price(ytm, cfs, ts)
    weighted_times = ts * cfs / (1 + ytm)**ts
    return np.sum(weighted_times) / price

def modified_duration(ytm, cfs, ts):
    """计算修正久期"""
    return macaulay_duration(ytm, cfs, ts) / (1 + ytm)

# ==========================================
# 1. 在 2% 到 9% 的收益率网格上为精确曲线定价
# ==========================================
y_grid = np.linspace(0.02, 0.09, 700)
P_grid = np.array([bond_price(y, cash_flows, times) for y in y_grid])

# ==========================================
# 2. 在 5.3% 附近叠加基于久期的近似
# ==========================================
# 计算初始点的精确价格与修正久期
P0 = bond_price(YTM_0, cash_flows, times)
Mod_Dur0 = modified_duration(YTM_0, cash_flows, times)

# 久期近似公式: P_approx(y) = P0 * [1 - Mod_Dur0 * (y - YTM_0)]
P_approx_grid = P0 * (1 - Mod_Dur0 * (y_grid - YTM_0))

# ==========================================
# 3. 报告 +100bp 的精确价格与久期法估计的相对变化
# ==========================================
y_up = YTM_0 + Delta_Y
price_at_up100bp = bond_price(y_up, cash_flows, times)
# 久期法估计的相对变化: ΔP/P ≈ -Mod_Dur * Δy
dur_approx_change_up100bp = -Mod_Dur0 * Delta_Y

# ==========================================
# 4. 绘图与保存
# ==========================================
plt.figure(figsize=(10, 6), dpi=120)

# 绘制精确价格-收益率曲线
plt.plot(y_grid * 100, P_grid, label='Exact Price-Yield Curve', color='blue', linewidth=2.5)

# 绘制久期近似直线（切线）
plt.plot(y_grid * 100, P_approx_grid, label='Duration Approximation (Tangent at 5.3%)', 
         color='red', linestyle='--', linewidth=2)

# 标记初始点 (5.3%)
plt.scatter(YTM_0 * 100, P0, color='black', zorder=5)
plt.annotate(f'Initial Point\nYTM={YTM_0*100:.1f}%, P={P0:.2f}', 
             xy=(YTM_0 * 100, P0), xytext=(YTM_0*100 + 0.8, P0 + 5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# 标记 +100bp 点
plt.scatter(y_up * 100, price_at_up100bp, color='green', zorder=5)
plt.annotate(f'+100bp Exact\nYTM={y_up*100:.1f}%, P={price_at_up100bp:.2f}', 
             xy=(y_up * 100, price_at_up100bp), xytext=(y_up*100 + 0.8, price_at_up100bp + 5),
             arrowprops=dict(facecolor='green', shrink=0.05, width=1.5, headwidth=8),
             fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# 图表美化
plt.title('Bond Price-Yield Curve and Duration Approximation', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(loc='upper right', fontsize=11, framealpha=0.9)
plt.grid(True, linestyle=':', alpha=0.6)
plt.xlim(2, 9)
plt.xticks(np.arange(2, 10, 1))

# 保存图形
fig_path = 'bond_price_yield_duration.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 输出契约：填充 result 字典
# ==========================================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}

# 课堂投屏辅助打印（方便教师展示结果）
print(f"--- 债券定价与久期计算结果 ---")
print(f"初始 YTM = {YTM_0*100:.1f}% 时的精确价格: {P0:.4f}")
print(f"修正久期: {Mod_Dur0:.4f}")
print(f"+100bp 后的精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对变化: {result['dur_approx_change_up100bp']:.4%}")
print(f"图形已保存至: {result['figure_path']}")
