import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 债券基本参数设定
# ==========================================
F = 100          # 面值
c_rate = 0.046   # 票息率 4.6%
n = 7            # 期限 7年
y0 = 0.053       # 当前收益率 5.3%

# ==========================================
# 2. 核心计算函数定义
# ==========================================
def calc_bond_price(y):
    """
    计算债券精确价格（向量化兼容）
    P = C * [1 - (1+y)^(-n)] / y + F * (1+y)^(-n)
    """
    C = F * c_rate
    pv_coupons = C * (1 - (1 + y) ** (-n)) / y
    pv_face = F * (1 + y) ** (-n)
    return pv_coupons + pv_face

def calc_mod_duration(y):
    """
    计算修正久期 (Modified Duration)
    """
    C = F * c_rate
    P = calc_bond_price(y)
    t = np.arange(1, n + 1)
    
    # 构造各期现金流
    cf = np.full(n, C)
    cf[-1] += F
    
    # 麦考利久期 MacD = Sum[t * CF_t / (1+y)^t] / P
    mac_d = np.sum(t * cf / (1 + y) ** t) / P
    
    # 修正久期 ModD = MacD / (1+y)
    mod_d = mac_d / (1 + y)
    return mod_d

# 计算当前收益率下的精确价格与修正久期
P0 = calc_bond_price(y0)
ModD = calc_mod_duration(y0)

# ==========================================
# 3. 绘图数据准备
# ==========================================
# 任务1：在 2% 到 9% 的收益率网格上为精确曲线定价
y_grid = np.linspace(0.02, 0.09, 1000)
P_exact_grid = calc_bond_price(y_grid)

# 任务2：在 5.3% 附近叠加基于久期的近似，收益率变动幅度做成可调
delta_y_range = 0.03  # 可调参数：当前收益率上下变动幅度（此处设为300个基点）
y_approx_grid = np.linspace(y0 - delta_y_range, y0 + delta_y_range, 200)

# 久期近似公式：P_approx = P0 * (1 - ModD * Δy)
P_approx_grid = P0 * (1 - ModD * (y_approx_grid - y0))

# ==========================================
# 4. 绘图与保存
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, P_exact_grid, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(y_approx_grid * 100, P_approx_grid, label='Duration-Based Approximation', color='red', linestyle='--', linewidth=2)
plt.scatter([y0 * 100], [P0], color='black', zorder=5, label=f'Current Point (y={y0*100:.1f}%)')

plt.title('Bond Price-Yield Curve and Duration Approximation')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.legend()
plt.grid(True, linestyle=':')

fig_path = 'bond_price_yield_curve.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 5. +100bp 计算任务
# ==========================================
# 收益率上升 100 个基点
y_up = y0 + 0.01
price_at_up100bp = calc_bond_price(y_up)

# 久期法估计的相对价格变化: ΔP/P ≈ -ModD * Δy
dur_approx_change_up100bp = -ModD * 0.01

# ==========================================
# 6. 封装输出结果
# ==========================================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}
