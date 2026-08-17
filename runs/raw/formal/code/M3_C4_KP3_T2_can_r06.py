import numpy as np
import matplotlib.pyplot as plt

# =========================================
# 1. 债券参数与现金流设置
# =========================================
F = 100           # 面值
c = 0.046         # 票息率（小数表示）
n = 7             # 期限（年）
y0 = 0.053        # 当前收益率（小数表示）
dy_target = 0.01  # 收益率变动幅度：+100个基点

# 生成现金流序列：前 n-1 期为票息，第 n 期为票息+面值
t = np.arange(1, n + 1)
cf = np.full(n, c * F)
cf[-1] += F

# =========================================
# 2. 计算当前收益率下的指标（精确价格、久期、凸性）
# =========================================
# 精确价格 P0
P0 = np.sum(cf / (1 + y0)**t)

# 麦考利久期 Dmac
Dmac = np.sum(t * cf / (1 + y0)**t) / P0

# 修正久期 Dmod
Dmod = Dmac / (1 + y0)

# 凸性 Conv (按课程约定公式)
Conv = np.sum(t * (t + 1) * cf / (1 + y0)**(t + 2)) / P0

# =========================================
# 3. 任务3：计算 +100bp 后的精确价格与一阶相对变化
# =========================================
y_up = y0 + dy_target
price_at_up100bp = np.sum(cf / (1 + y_up)**t)

# 久期法估计的相对价格变化（一阶近似）
dur_approx_change_up100bp = -Dmod * dy_target

# =========================================
# 4. 任务1 & 2：计算收益率网格上的精确与近似价格
# =========================================
y_grid = np.linspace(0.02, 0.09, 500)

# 精确价格曲线（利用NumPy广播机制）
P_exact_grid = np.sum(cf / (1 + y_grid[:, None])**t, axis=1)

# 近似计算基准
dy_grid = y_grid - y0

# 一阶久期近似：dP/P = -Dmod * dy  =>  P = P0 * (1 - Dmod * dy)
P_dur_grid = P0 * (1 - Dmod * dy_grid)

# 久期+凸性近似：dP/P = -Dmod * dy + 0.5 * Conv * dy^2  =>  P = P0 * (1 - Dmod * dy + 0.5 * Conv * dy^2)
P_dur_conv_grid = P0 * (1 - Dmod * dy_grid + 0.5 * Conv * dy_grid**2)

# =========================================
# 5. 绘图与保存
# =========================================
# 设置中文字体支持与负号显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制曲线
ax.plot(y_grid * 100, P_exact_grid, label='精确价格曲线', color='blue', linewidth=2)
ax.plot(y_grid * 100, P_dur_grid, label='一阶久期近似 (线性)', color='red', linestyle='--', linewidth=1.5)
ax.plot(y_grid * 100, P_dur_conv_grid, label='久期+凸性近似 (二次)', color='green', linestyle=':', linewidth=1.5)

# 标注当前收益率参考线
ax.axvline(x=y0 * 100, color='gray', linestyle='-.', alpha=0.6, label=f'当前收益率 {y0*100:.1f}%')

ax.set_xlabel('收益率 (%)')
ax.set_ylabel('债券价格')
ax.set_title(f'债券价格-收益率关系及久期/凸性近似 (面值{F}, 票息{c*100}%, 期限{n}年)')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# =========================================
# 6. 输出契约要求的结果字典
# =========================================
result = {
    'price_at_up100bp': float(price_at_up100bp),
    'dur_approx_change_up100bp': float(dur_approx_change_up100bp),
    'figure_path': figure_path
}

# 控制台打印以供现场演示核对
print("--- 计算结果报告 ---")
print(f"当前收益率下精确价格 P0: {P0:.4f}")
print(f"麦考利久期 Dmac: {Dmac:.4f}")
print(f"修正久期 Dmod: {Dmod:.4f}")
print(f"凸性 Conv: {Conv:.4f}")
print(f"+100bp后精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计相对变化: {result['dur_approx_change_up100bp']:.6f} (即 {result['dur_approx_change_up100bp']*100:.4f}%)")
print(f"图形已保存至: {result['figure_path']}")
