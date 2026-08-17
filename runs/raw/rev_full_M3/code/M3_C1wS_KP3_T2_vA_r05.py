import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 可调参数：收益率变动幅度 (用于绘制久期近似曲线的区间)
# 修改此值可调整近似曲线在初始收益率 5.3% 两侧的延伸范围
# ==========================================
DELTA_Y_MAX = 0.035  # +/- 350个基点 (3.5%)

# ==========================================
# 债券基本参数
# 假设：每年付息一次，按年复利贴现
# ==========================================
FV = 100             # 面值
coupon_rate = 0.046  # 票息率
n_years = 7          # 期限
y0 = 0.053           # 初始收益率

C = FV * coupon_rate # 每年票息现金流

# ==========================================
# 1. 精确定价函数 (向量化计算)
# ==========================================
def bond_prices(y_arr, C, FV, n):
    """
    计算债券在不同收益率下的精确价格
    y_arr: 收益率数组
    C: 票息
    FV: 面值
    n: 期限
    """
    y_arr = np.asarray(y_arr).reshape(-1, 1)
    times = np.arange(1, n + 1).reshape(1, -1)
    cf = np.full(n, C)
    cf[-1] += FV  # 最后一期加上面值
    pv_cf = cf.reshape(1, -1) / (1 + y_arr)**times
    return np.sum(pv_cf, axis=1)

# 在 2% 到 9% 的收益率网格上计算精确价格
y_grid = np.linspace(0.02, 0.09, 300)
prices_exact_grid = bond_prices(y_grid, C, FV, n_years)

# ==========================================
# 2. 计算初始价格、麦考利久期与修正久期
# ==========================================
P0 = bond_prices([y0], C, FV, n_years)[0]

times = np.arange(1, n_years + 1)
cf = np.full(n_years, C)
cf[-1] += FV

pv_cf_at_y0 = cf / (1 + y0)**times
# 麦考利久期
mac_duration = np.sum(times * pv_cf_at_y0) / P0
# 修正久期
mod_duration = mac_duration / (1 + y0)

# 在 5.3% 附近叠加基于久期的近似曲线
# 限定在 [y0 - DELTA_Y_MAX, y0 + DELTA_Y_MAX] 范围内，并确保在 2%~9% 画布内
y_approx_grid = np.linspace(y0 - DELTA_Y_MAX, y0 + DELTA_Y_MAX, 300)
y_approx_grid = np.clip(y_approx_grid, 0.02, 0.09)
# 久期近似公式：ΔP/P ≈ -ModD * Δy  =>  P_approx = P0 * (1 - ModD * (y - y0))
prices_approx_grid = P0 * (1 - mod_duration * (y_approx_grid - y0))

# ==========================================
# 3. 报告 +100bp 的精确价格与久期法估计的相对变化
# ==========================================
y_up100bp = y0 + 0.01
price_at_up100bp = bond_prices([y_up100bp], C, FV, n_years)[0]
dur_approx_change_up100bp = -mod_duration * 0.01  # 久期法估计的相对变化

# ==========================================
# 4. 绘图与保存
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制精确价格曲线
ax.plot(y_grid * 100, prices_exact_grid, 
        label='Exact Price', color='blue', linewidth=2.5)

# 绘制久期近似价格曲线
ax.plot(y_approx_grid * 100, prices_approx_grid, 
        label='Duration Approximation (Linear)', color='red', linestyle='--', linewidth=2.5)

# 标出初始收益率位置
ax.axvline(y0 * 100, color='gray', linestyle=':', label=f'Initial Yield ({y0*100:.1f}%)')

ax.set_xlabel('Yield to Maturity (%)', fontsize=12)
ax.set_ylabel('Bond Price', fontsize=12)
ax.set_title('Bond Price vs. Yield: Exact vs. Duration Approximation', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.7)

fig_path = 'bond_price_duration.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 填充 result 字典
# ==========================================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}

# 在控制台输出结果供课堂投屏参考
print(f"初始收益率 {y0*100:.1f}% 下的债券精确价格: {P0:.4f}")
print(f"修正久期: {mod_duration:.4f}")
print(f"收益率上升100bp后的精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
