import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 定义债券计算核心函数 ====================
def bond_metrics(face_value, coupon_rate, T, y):
    """
    计算债券的精确价格、修正久期和凸性
    :param face_value: 面值
    :param coupon_rate: 票息率 (小数表示)
    :param T: 期限 (年)
    :param y: 收益率 (小数表示, 年复利)
    :return: (价格, 修正久期, 凸性)
    """
    C = face_value * coupon_rate
    F = face_value
    
    # 现金流时间点与金额
    t_array = np.arange(1, T + 1)
    cf_array = np.full(T, C)
    cf_array[-1] += F  # 最后一期加入本金
    
    # 贴现因子
    discount_factors = (1 + y) ** t_array
    
    # 现值
    pv_array = cf_array / discount_factors
    P = np.sum(pv_array)
    
    # 麦考利久期 D_mac = Σ[t * CF_t / (1+y)^t] / P
    D_mac = np.sum(t_array * pv_array) / P
    
    # 修正久期 D_mod = D_mac / (1+y)
    D_mod = D_mac / (1 + y)
    
    # 凸性 Conv = Σ[t(t+1)CF_t / (1+y)^(t+2)] / P
    conv = np.sum(t_array * (t_array + 1) * cf_array / (1 + y) ** (t_array + 2)) / P
    
    return P, D_mod, conv


# ==================== 2. 基本参数设定 ====================
face_value = 100
coupon_rate = 0.046
T = 7
y0 = 0.053  # 当前收益率

# 获取当前收益率下的价格、久期与凸性
P0, D_mod0, Conv0 = bond_metrics(face_value, coupon_rate, T, y0)


# ==================== 3. 收益率网格与定价 ====================
# 精确曲线的收益率网格：2% 到 9%
y_grid_full = np.linspace(0.02, 0.09, 700)
P_exact_grid = np.array([bond_metrics(face_value, coupon_rate, T, y)[0] for y in y_grid_full])

# 近似曲线的收益率网格（在当前收益率附近，幅度可调）
# 可调参数：approx_dy_range 控制了在 y0 附近多大的收益率区间内叠加近似曲线
approx_dy_range = 0.035  # 可调：上下浮动 3.5% (350bp)
y_grid_approx = np.linspace(y0 - approx_dy_range, y0 + approx_dy_range, 400)
dy_approx = y_grid_approx - y0

# 一阶久期近似: dP/P = -D_mod * dy  =>  P_approx = P0 * (1 - D_mod * dy)
P_dur_approx = P0 * (1 - D_mod0 * dy_approx)

# 二阶久期+凸性近似: dP/P ≈ -D_mod * dy + 0.5 * Conv * dy^2
P_dur_conv_approx = P0 * (1 - D_mod0 * dy_approx + 0.5 * Conv0 * dy_approx**2)


# ==================== 4. 计算+100bp的指标 ====================
y_up100bp = y0 + 0.01
price_at_up100bp, _, _ = bond_metrics(face_value, coupon_rate, T, y_up100bp)

# 久期法估计的相对价格变化 (一阶近似，下跌为负)
dur_approx_change_up100bp = -D_mod0 * 0.01


# ==================== 5. 绘图 ====================
plt.figure(figsize=(10, 6), dpi=120)

# 绘制精确价格-收益率曲线
plt.plot(y_grid_full * 100, P_exact_grid, 
         label='Exact Price-Yield Curve', color='blue', linewidth=2)

# 在当前收益率附近叠加一阶久期直线
plt.plot(y_grid_approx * 100, P_dur_approx, 
         label='First-order (Duration) Approx', color='red', linestyle='--', linewidth=1.5)

# 在当前收益率附近叠加久期+凸性曲线
plt.plot(y_grid_approx * 100, P_dur_conv_approx, 
         label='Second-order (Duration + Convexity) Approx', color='green', linestyle='-.', linewidth=1.5)

# 标记当前点 (y0, P0)
plt.scatter([y0 * 100], [P0], color='black', s=60, zorder=5)
plt.annotate(f'Current Point\ny = {y0*100:.1f}%, P = {P0:.2f}', 
             xy=(y0 * 100, P0), 
             xytext=(y0 * 100 + 1.0, P0 + 3),
             arrowprops=dict(facecolor='black', width=1, shrink=0.05),
             fontsize=10, 
             bbox=dict(boxstyle="round,pad=0.3", fc="aliceblue", ec="gray"))

# 图表修饰
plt.title('Bond Price-Yield Relationship and Approximations', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, linestyle=':', alpha=0.6)

# 保存图形
figure_path = 'bond_price_yield_approx.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.close()


# ==================== 6. 输出结果字典 ====================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 为方便教师投屏演示，在控制台打印核对信息
print("--- 计算结果 ---")
print(f"当前收益率下债券价格 P0: {P0:.4f}")
print(f"修正久期 D_mod: {D_mod0:.4f}")
print(f"凸性 Conv: {Conv0:.4f}")
print(f"收益率上升100bp后的精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.6f}")
print(f"图形已保存至: {result['figure_path']}")
