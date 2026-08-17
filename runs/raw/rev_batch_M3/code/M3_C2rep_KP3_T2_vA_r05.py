import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 债券参数与假设设定
# ==========================================
Face_Value = 100          # 面值
Coupon_Rate = 0.046       # 票息率 4.6%
Maturity = 7              # 期限 7年
Yield_Current = 0.053     # 当前收益率 5.3%

# 假设：每年付息1次，按整年计息（符合一般教材未指明付息频率时的标准假设）
# 收益率变动幅度（用于绘制基于久期的近似切线范围），此处设为上下200个基点
Delta_Yield_Range = 0.02  

# ==========================================
# 2. 核心计算函数定义
# ==========================================
def bond_prices(y_arr, F, c, T):
    """计算不同收益率下的债券精确价格"""
    C = F * c
    t = np.arange(1, T + 1)
    cf = np.full(T, C)
    cf[-1] += F  # 最后一期加上面值
    
    # 广播计算折现因子
    df = (1 + y_arr[:, np.newaxis]) ** t
    prices = np.sum(cf / df, axis=1)
    return prices

def modified_duration(y, F, c, T):
    """计算修正久期"""
    y_arr = np.array([y])
    P = bond_prices(y_arr, F, c, T)[0]
    C = F * c
    t = np.arange(1, T + 1)
    cf = np.full(T, C)
    cf[-1] += F
    
    df = (1 + y) ** t
    mac_dur = np.sum(t * cf / df) / P
    mod_dur = mac_dur / (1 + y)
    return mod_dur, P

# ==========================================
# 3. 精确曲线与久期近似计算
# ==========================================
# 生成2%到9%的收益率网格
y_grid = np.linspace(0.02, 0.09, 1000)
P_grid = bond_prices(y_grid, Face_Value, Coupon_Rate, Maturity)

# 当前收益率处的修正久期与精确价格
Mod_Dur_0, P_0 = modified_duration(Yield_Current, Face_Value, Coupon_Rate, Maturity)

# 在当前收益率附近生成久期近似（一阶泰勒展开切线）
y_approx_grid = np.linspace(Yield_Current - Delta_Yield_Range, 
                            Yield_Current + Delta_Yield_Range, 
                            100)
# 久期近似公式: P(y) ≈ P0 - P0 * Mod_Dur * (y - y0)
P_approx_grid = P_0 * (1 - Mod_Dur_0 * (y_approx_grid - Yield_Current))

# ==========================================
# 4. +100bp 情景计算
# ==========================================
Delta_Yield_100bp = 0.01
Yield_Up100bp = Yield_Current + Delta_Yield_100bp

# +100bp的精确价格
Price_Up100bp = bond_prices(np.array([Yield_Up100bp]), Face_Value, Coupon_Rate, Maturity)[0]

# 久期法估计的相对价格变化 (%ΔP ≈ -Mod_Dur * Δy)
Dur_Rel_Change_Up100bp = -Mod_Dur_0 * Delta_Yield_100bp

# ==========================================
# 5. 绘图与保存
# ==========================================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制精确曲线
ax.plot(y_grid * 100, P_grid, 'b-', linewidth=2, label='精确价格-收益率曲线')

# 绘制久期近似曲线
ax.plot(y_approx_grid * 100, P_approx_grid, 'r--', linewidth=2, 
        label=f'基于久期的近似 (±{Delta_Yield_Range*10000:.0f}bps范围)')

# 标记当前收益率点
ax.scatter([Yield_Current * 100], [P_0], color='black', s=80, zorder=5, 
           label=f'当前收益率点 (y={Yield_Current*100}%)')

# 图形修饰
ax.set_xlabel('收益率 (%)', fontsize=12)
ax.set_ylabel('债券价格', fontsize=12)
ax.set_title('债券价格-收益率关系及久期近似', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle=':', alpha=0.7)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
fig.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close(fig)

# ==========================================
# 6. 填充结果字典
# ==========================================
result = {
    'price_at_up100bp': Price_Up100bp,
    'dur_approx_change_up100bp': Dur_Rel_Change_Up100bp,
    'figure_path': figure_path
}

# 可选：打印结果以便课堂展示验证
print(f"+100bp 精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
print(f"图形已保存至: {result['figure_path']}")
