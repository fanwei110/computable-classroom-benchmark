import numpy as np
import matplotlib.pyplot as plt

# ==================== 债券参数设置 ====================
F = 100            # 面值
c = 0.046          # 票息率 4.6%
T = 7              # 期限 7年
y0 = 0.053         # 当前收益率 5.3%
dy_shock = 0.01    # 收益率变动幅度（100个基点），可调参数

# 现金流序列
t_arr = np.arange(1, T + 1)
cf_arr = np.full(T, c * F)
cf_arr[-1] += F    # 最后一期加上面值

# ==================== 精确定价与指标计算 ====================
# 当前收益率下的贴现因子与精确价格
disc_y0 = (1 + y0) ** t_arr
P0 = np.sum(cf_arr / disc_y0)

# 麦考利久期
D_mac = np.sum(t_arr * cf_arr / disc_y0) / P0

# 修正久期
D_mod = D_mac / (1 + y0)

# 凸性 (按课程约定：Σ[t(t+1)CF_t/(1+y)^(t+2)]/P)
conv = np.sum(t_arr * (t_arr + 1) * cf_arr / ((1 + y0) ** (t_arr + 2))) / P0

# ==================== 收益率网格与曲线计算 ====================
# 收益率变动范围做成可调
y_min, y_max = 0.02, 0.09
y_grid = np.linspace(y_min, y_max, 500)

# 1. 精确价格-收益率曲线（利用numpy广播机制向量化计算）
P_exact = np.sum(cf_arr / (1 + y_grid[:, np.newaxis]) ** t_arr, axis=1)

# 2. 久期一阶近似与久期+凸性二阶近似
dy_grid = y_grid - y0
P_dur_approx = P0 * (1 - D_mod * dy_grid)
P_dur_conv_approx = P0 * (1 - D_mod * dy_grid + 0.5 * conv * dy_grid**2)

# ==================== 特定情景计算 (+100bp) ====================
y_up = y0 + dy_shock
# 精确价格
P_up_exact = np.sum(cf_arr / ((1 + y_up) ** t_arr))
# 久期法估计的相对价格变化 (一阶近似，下跌为负)
dur_approx_rel_change = -D_mod * dy_shock

# ==================== 绘图 ====================
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, P_exact, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(y_grid * 100, P_dur_approx, label='Duration Approximation (1st Order)', color='red', linestyle='--')
plt.plot(y_grid * 100, P_dur_conv_approx, label='Duration + Convexity Approximation (2nd Order)', color='green', linestyle=':')
plt.axvline(y0 * 100, color='gray', linestyle=':', alpha=0.7, label=f'Current Yield ({y0*100:.1f}%)')
plt.title('Bond Price-Yield Curve and Approximations', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 结果输出 ====================
result = {
    'price_at_up100bp': P_up_exact,
    'dur_approx_change_up100bp': dur_approx_rel_change,
    'figure_path': figure_path
}

# 为方便课堂投屏展示，打印核心结果
print("--- 计算结果 ---")
print(f"当前价格 P0: {P0:.4f}")
print(f"修正久期 D_mod: {D_mod:.4f}")
print(f"凸性 Conv: {conv:.4f}")
print(f"收益率上升100bp后精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.6f} ({result['dur_approx_change_up100bp']*100:.4f}%)")
print(f"图形已保存至: {result['figure_path']}")
